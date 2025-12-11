"""オーバーロードと Literal 型のデモ。

ty は @overload デコレータと Literal 型を完全にサポートしており、
引数の型に応じた正確な戻り値の型を推論してくれます。
"""

from dataclasses import dataclass
from typing import Final, Literal, LiteralString, overload

# ========================================
# @overload による関数オーバーロード
# ========================================


@overload
def process(value: int) -> str: ...


@overload
def process(value: str) -> int: ...


@overload
def process(value: list[int]) -> int: ...


def process(value: int | str | list[int]) -> str | int:
    """引数の型に応じて異なる処理を行う。

    ty は呼び出し時の引数の型を見て、
    正確な戻り値の型を推論してくれる。
    """
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return len(value)
    return sum(value)


def use_overload() -> tuple[str, int, int]:
    """オーバーロードの使用例。"""
    # 引数が int なら戻り値は str
    result1 = process(42)  # str と推論される！

    # 引数が str なら戻り値は int
    result2 = process("hello")  # int と推論される！

    # 引数が list[int] なら戻り値は int
    result3 = process([1, 2, 3])  # int と推論される！

    return result1, result2, result3


# ========================================
# オプション引数を含むオーバーロード
# ========================================


@overload
def fetch(url: str) -> str: ...


@overload
def fetch(url: str, *, as_bytes: Literal[False]) -> str: ...


@overload
def fetch(url: str, *, as_bytes: Literal[True]) -> bytes: ...


def fetch(url: str, *, as_bytes: bool = False) -> str | bytes:
    """URL からデータを取得する。

    Args:
        url: 取得先の URL。
        as_bytes: True なら bytes を、False なら str を返す。

    Returns:
        取得したデータ。
    """
    _ = url  # デモ用のため未使用
    data = b"example data"
    if as_bytes:
        return data
    return data.decode()


def use_fetch_overload() -> tuple[str, str, bytes]:
    """Fetch のオーバーロード使用例。"""
    # as_bytes 未指定 -> str
    text = fetch("https://example.com")  # str

    # as_bytes=False -> str
    text2 = fetch("https://example.com", as_bytes=False)  # str

    # as_bytes=True -> bytes
    binary = fetch("https://example.com", as_bytes=True)  # bytes

    return text, text2, binary


# ========================================
# Literal 型のデモ
# ========================================


def set_log_level(level: Literal["debug", "info", "warning", "error"]) -> None:
    """ログレベルを設定する。

    Literal 型を使うと、特定の文字列リテラルのみを受け付ける。
    補完も Literal の値が候補として表示される！
    """
    print(f"Log level set to: {level}")


def use_literal() -> None:
    """Literal 型の使用例。"""
    set_log_level("debug")  # OK
    set_log_level("info")  # OK

    # typo があるとエラー！
    # set_log_level("debg")  # ty error!

    # 補完で候補が表示される
    # set_log_level("  <- ここで "debug", "info", ... が候補に出る


# ========================================
# Literal と条件分岐の組み合わせ
# ========================================


def get_status_message(status: Literal["ok", "error", "pending"]) -> str:
    """ステータスに応じたメッセージを返す。"""
    match status:
        case "ok":
            return "Operation successful"
        case "error":
            return "Operation failed"
        case "pending":
            return "Operation in progress"


# ========================================
# Literal を使った判別共用体
# ========================================


@dataclass
class SuccessResult:
    """成功結果。"""

    status: Literal["success"]
    value: str


@dataclass
class ErrorResult:
    """エラー結果。"""

    status: Literal["error"]
    message: str


Result = SuccessResult | ErrorResult


def handle_result(result: Result) -> str:
    """Literal 型を使った判別共用体（Discriminated Union）。

    isinstance で型を判別できる。
    """
    if isinstance(result, SuccessResult):
        # result は SuccessResult として扱える
        return result.value
    # result は ErrorResult として扱える
    return result.message


# ========================================
# LiteralString（Python 3.11+）
# ========================================


def execute_query(query: LiteralString) -> list[dict[str, object]]:
    """SQL クエリを実行する。

    LiteralString を使うと、リテラル文字列のみを受け付ける。
    SQL インジェクション対策に有効。

    Args:
        query: 実行する SQL クエリ。

    Returns:
        クエリ結果。
    """
    _ = query  # デモ用のため未使用
    return [{"id": 1, "name": "Alice"}]


def use_literal_string() -> list[dict[str, object]]:
    """LiteralString の使用例。"""
    # リテラル文字列は OK
    # 変数を連結した文字列はエラー！
    # table = "users"
    # execute_query(f"SELECT * FROM {table}")  # ty error!

    return execute_query("SELECT * FROM users")


# ========================================
# 数値 Literal
# ========================================


def set_priority(priority: Literal[1, 2, 3]) -> None:
    """優先度を設定する。1, 2, 3 のみ受け付ける。"""
    print(f"Priority: {priority}")


def use_numeric_literal() -> None:
    """数値 Literal の使用例。"""
    set_priority(1)  # OK
    set_priority(2)  # OK
    # set_priority(4)  # ty error!


# ========================================
# Final と Literal の組み合わせ
# ========================================

MAX_RETRIES: Final = 3  # Literal[3] として推論される


def retry_operation() -> None:
    """Final 変数は Literal 型として扱われる。"""
    for i in range(MAX_RETRIES):
        print(f"Attempt {i + 1}")


if __name__ == "__main__":
    use_overload()
    use_fetch_overload()
    use_literal()
    use_literal_string()
    use_numeric_literal()
