from graph import app
from state import TransitState


def run_chat(message: str) -> str:
    init = TransitState(location=message)
    final = app.invoke(init)
    return getattr(final, "response_text", "情報を取得できませんでした。")


if __name__ == "__main__":
    while True:
        user = input("地名を入力してください（例: 大阪）> ").strip()
        if user.lower() in {"exit", "quit"}:
            break
        print(run_chat(user), "\n")
