from typing import List, Optional

from pydantic import BaseModel


class Alert(BaseModel):
    line: str
    status: str  # "delay" / "suspended" / "normal"
    info: str  # 詳細テキスト


class TransitState(BaseModel):
    location: str  # ユーザー入力の地名
    nearest_station: Optional[str]  # 例: "大阪駅"
    alerts: List[Alert] = []  # 運行情報リスト
