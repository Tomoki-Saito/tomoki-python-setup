"""*args と **kwargs のデモ。

ty は *args と **kwargs の型アノテーションを正確に理解し、
呼び出し側でも適切な型チェックを行います。
"""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, ParamSpec, TypedDict, TypeVar, Unpack

if TYPE_CHECKING:
    from collections.abc import Callable

# ========================================
# 基本的な *args
# ========================================


def sum_all(*numbers: int) -> int:
    """全ての引数を合計する。

    *numbers: int は「int 型の可変長引数」を意味する。
    ty は呼び出し側で int 以外が渡されるとエラーを出す。
    """
    return sum(numbers)


def concat_strings(*strings: str, separator: str = "") -> str:
    """全ての文字列を連結する。

    *args の後にキーワード引数を置ける。
    """
    return separator.join(strings)


def use_args_demo() -> None:
    """*args の使用例。"""
    # 任意の数の int を渡せる
    total1 = sum_all(1, 2, 3)
    total2 = sum_all(1, 2, 3, 4, 5)
    total3 = sum_all()  # 0個でも OK

    # 型が合わないとエラー
    # sum_all(1, 2, "3")  # ty error: str は int に合わない

    # separator はキーワード引数として渡す
    text = concat_strings("a", "b", "c", separator="-")  # "a-b-c"

    print(total1, total2, total3, text)


# ========================================
# 基本的な **kwargs
# ========================================


def print_info(**kwargs: str | int) -> None:
    """キーワード引数を全て表示する。

    **kwargs: str | int は「値が str または int のキーワード引数」を意味する。
    """
    for key, value in kwargs.items():
        print(f"{key}: {value}")


def create_dict(**kwargs: object) -> dict[str, object]:
    """キーワード引数から辞書を作成する。"""
    return dict(kwargs)


def use_kwargs_demo() -> None:
    """**kwargs の使用例。"""
    # 任意のキーワード引数を渡せる
    print_info(name="Alice", age=30, city="Tokyo")

    # 辞書を作成
    data = create_dict(id=1, name="Bob", active=True)

    print(data)


# ========================================
# *args と **kwargs の組み合わせ
# ========================================


def flexible_function(
    required: str,
    *args: int,
    option: bool = False,
    **kwargs: str,
) -> dict[str, object]:
    """必須引数、*args、キーワード引数、**kwargs を組み合わせた関数。

    Args:
        required: 必須の引数。
        *args: 可変長の int 引数。
        option: オプションのブール値。
        **kwargs: 追加のキーワード引数（値は str）。

    Returns:
        引数をまとめた辞書。
    """
    return {
        "required": required,
        "args": args,
        "option": option,
        "kwargs": kwargs,
    }


def use_combined_demo() -> None:
    """*args と **kwargs の組み合わせの使用例。"""
    result = flexible_function(
        "hello",  # required
        1,
        2,
        3,  # *args
        option=True,  # キーワード引数
        extra="value",
        another="data",  # **kwargs
    )
    print(result)


# ========================================
# TypedDict と Unpack を使った型付き **kwargs
# ========================================


class UserKwargs(TypedDict, total=False):
    """ユーザー作成時のキーワード引数の型。"""

    name: str
    email: str
    age: int
    is_active: bool


def create_user_typed(**kwargs: Unpack[UserKwargs]) -> dict[str, object]:
    """型付きの **kwargs を受け取る関数。

    Unpack[TypedDict] を使うと、**kwargs の型を詳細に指定できる。
    ty は指定されたキー以外が渡されるとエラーを出す。
    補完も効く！
    """
    return dict(kwargs)


class ConfigKwargs(TypedDict):
    """設定のキーワード引数の型（全て必須）。"""

    host: str
    port: int
    debug: bool


def setup_server(**kwargs: Unpack[ConfigKwargs]) -> None:
    """必須の型付き **kwargs を受け取る関数。

    total=True（デフォルト）の TypedDict を使うと、
    全てのキーが必須になる。
    """
    print(f"Server: {kwargs['host']}:{kwargs['port']}, debug={kwargs['debug']}")


def use_typed_kwargs_demo() -> None:
    """型付き **kwargs の使用例。"""
    # TypedDict で定義されたキーのみ渡せる
    user = create_user_typed(name="Alice", email="alice@example.com", age=30)

    # 補完が効く！ kwargs の中で name=, email=, age=, is_active= が候補に出る

    # 未定義のキーを渡すとエラー
    # create_user_typed(name="Alice", invalid_key="value")  # ty error!

    # 必須キーを持つ TypedDict
    setup_server(host="localhost", port=8080, debug=True)

    # 必須キーが足りないとエラー
    # setup_server(host="localhost")  # ty error: port, debug が必要

    print(user)


# ========================================
# ParamSpec を使った関数のラップ
# ========================================

P = ParamSpec("P")
R = TypeVar("R")


def log_call[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """関数呼び出しをログするデコレータ。

    ParamSpec を使うと、ラップした関数の引数の型を保持できる。
    """
    name = getattr(func, "__name__", "unknown")

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {name}")
        return func(*args, **kwargs)

    return wrapper


@log_call
def greet(name: str, greeting: str = "Hello") -> str:
    """挨拶を返す。"""
    return f"{greeting}, {name}!"


def use_paramspec_demo() -> None:
    """ParamSpec の使用例。"""
    # デコレータでラップしても、元の関数の型情報が保持される
    result = greet("Alice")  # 補完で name: str, greeting: str が見える

    # 型が合わないとエラー
    # greet(123)  # ty error: int は str に合わない

    print(result)


# ========================================
# Callable での *args/**kwargs
# ========================================


def apply_to_all(
    items: list[int],
    func: Callable[[int], int],
) -> list[int]:
    """リストの全要素に関数を適用する。"""
    return [func(item) for item in items]


def apply_with_args(
    func: Callable[..., str],  # ... は任意の引数を意味する
    *args: object,
    **kwargs: object,
) -> str:
    """任意の引数で関数を呼び出す。

    Callable[..., str] は「任意の引数を取り str を返す関数」を意味する。
    """
    return func(*args, **kwargs)


def use_callable_demo() -> None:
    """Callable の使用例。"""
    # 引数の型が明確な Callable
    doubled = apply_to_all([1, 2, 3], lambda x: x * 2)

    # 任意の引数を取る Callable
    result = apply_with_args(str.format, "Hello, {}!", "World")

    print(doubled, result)


# ========================================
# 実践的な例: ロガー関数
# ========================================


def log(
    level: str,
    message: str,
    *args: object,
    **kwargs: object,
) -> None:
    """ログを出力する。

    args と kwargs は message.format() に渡される。
    """
    formatted = message.format(*args, **kwargs)
    print(f"[{level}] {formatted}")


def use_logger_demo() -> None:
    """ロガーの使用例。"""
    log("INFO", "User {} logged in", "Alice")
    log("DEBUG", "Processing {count} items", count=10)
    log("ERROR", "Failed to connect to {host}:{port}", host="localhost", port=5432)


if __name__ == "__main__":
    use_args_demo()
    use_kwargs_demo()
    use_combined_demo()
    use_typed_kwargs_demo()
    use_paramspec_demo()
    use_callable_demo()
    use_logger_demo()
