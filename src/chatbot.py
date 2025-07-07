"""
chatbot.py
----------

簡易 CLI。入力を読み取り、回答を標準出力する。
"""

from __future__ import annotations

import sys

from .graph import bot
from .state import ChatState


def main() -> None:
    """CLI エントリポイント。"""
    if len(sys.argv) < 2:
        print('使い方: python -m src.chatbot "丸ノ内線の遅延は？"')
        sys.exit(1)

    question = sys.argv[1]
    init_state: ChatState = {"query": question, "operator": None, "status": None}
    result = bot.invoke(init_state)
    print(result["answer"])


if __name__ == "__main__":
    main()
