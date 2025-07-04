from __future__ import annotations

import logging
import os

import requests
from langgraph.graph import StateGraph

from state import Alert, TransitState

MOCK = os.getenv("MOCK_API", "1") == "1"
YAHOO_KEY = os.getenv("YAHOO_API_KEY")  # ← 実運用は取得


# ---------------- ① ジオコーディング & 最寄り駅推定 ----------------
def geocode_and_find_station(state: TransitState) -> TransitState:
    if MOCK or not YAHOO_KEY:
        # とりあえず地名 + "駅" を雑に返す
        state.nearest_station = f"{state.location}駅"
        return state

    # 例: ジオコーダで緯度経度取得→駅検索 API
    # lat, lng = ...
    # station = ...
    state.nearest_station = station
    return state


# ---------------- ② 運行情報取得 ----------------
def fetch_transit_alerts(state: TransitState) -> TransitState:
    station = state.nearest_station or state.location
    if MOCK or not YAHOO_KEY:
        # ダミーデータ: ランダムで遅延/通常を返す
        dummy = [
            Alert(
                line="JR大阪環状線",
                status="delay",
                info="人身事故の影響で15分前後の遅れ",
            ),
            Alert(line="Osaka Metro 御堂筋線", status="normal", info="平常運転"),
        ]
        state.alerts = dummy
        return state

    # 実 API（例: https://transit.yahooapis.jp/traininfo）
    try:
        resp = requests.get(
            "https://transit.yahooapis.jp/traininfo",
            params={"appid": YAHOO_KEY, "name": station},
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()  # ← 実際は XML なので適宜変換
        state.alerts = [
            Alert(line=item["Line"], status=item["Status"], info=item["Description"])
            for item in data["Result"]["Train"]
        ]
    except Exception as e:
        logging.warning("運行情報取得失敗: %s", e)
        state.alerts = [Alert(line="情報取得エラー", status="unknown", info=str(e))]
    return state


# ---------------- ③ レスポンス整形 ----------------
def render_response(state: TransitState) -> TransitState:
    if not state.alerts:
        state.response_text = (
            f"🚉 {state.location} 周辺の路線に遅延情報はありませんでした。"
        )
        return state

    lines = [f"📍 **{state.nearest_station or state.location} 周辺の運行情報**"]
    for a in state.alerts:
        icon = "⚠️" if a.status != "normal" else "✅"
        lines.append(f"{icon} **{a.line}** – {a.info}")
    state.response_text = "\n".join(lines)
    return state
