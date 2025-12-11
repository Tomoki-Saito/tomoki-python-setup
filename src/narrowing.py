"""型の絞り込み（Type Narrowing）のデモ。

ty は条件分岐や型チェック関数を解析して、
ブロック内で変数の型を自動的に絞り込んでくれます。
これにより不要なキャストなしで安全にコードが書けます。
"""

from typing import TypeGuard, TypeIs, assert_never

# ========================================
# 基本的な型の絞り込み
# ========================================


def handle_value(value: int | str | None) -> str:
    """Union 型の値を処理する。

    各ブランチで型が自動的に絞り込まれる。
    """
    if value is None:
        # ここでは value は None
        return "Nothing"

    if isinstance(value, int):
        # ここでは value は int
        # int のメソッドが補完候補に出る！
        return f"Number: {value * 2}"

    # ここでは value は str（残りの型）
    # str のメソッドが補完候補に出る！
    return f"Text: {value.upper()}"


def process_optional(items: list[str] | None) -> int:
    """Optional な値を安全に処理する。"""
    if items is None:
        return 0

    # ここでは items は list[str]（None が除外された）
    return len(items)


# ========================================
# truthiness による絞り込み
# ========================================


def truthy_narrowing(value: str | None) -> str:
    """Truthiness チェックによる絞り込み。"""
    if value:
        # ここでは value は str（None と空文字が除外）
        return value.upper()
    return "default"


def falsy_narrowing(items: list[int]) -> int:
    """空リストチェックによる絞り込み。"""
    if not items:
        return 0

    # ここでは items は空でないことが保証される
    # （型としては list[int] のまま）
    return items[0]


# ========================================
# TypeGuard によるカスタム型ガード
# ========================================


def is_string_list(value: list[object]) -> TypeGuard[list[str]]:
    """リストが文字列のリストかどうかをチェックする型ガード。

    TypeGuard を使うと、カスタムの型チェック関数を定義できる。
    """
    return all(isinstance(item, str) for item in value)


def is_positive_int(value: int) -> TypeGuard[int]:
    """正の整数かどうかをチェックする型ガード。"""
    return value > 0


def use_type_guard(value: int | str) -> str:
    """TypeGuard の使用例。"""
    # TypeGuard を使うと、カスタムの型チェック関数を定義できる
    if isinstance(value, str):
        # isinstance により value は str として扱える
        return value.upper()

    # ここでは value は int
    return str(value * 2)


# ========================================
# TypeIs（Python 3.13+）によるより正確な絞り込み
# ========================================


def is_str(value: object) -> TypeIs[str]:
    """TypeIs は TypeGuard より正確な絞り込みを行う。

    TypeIs は「双方向」の絞り込みを行う。
    True の場合は str に絞り込み、False の場合は str を除外する。
    """
    return isinstance(value, str)


def use_type_is(value: str | int) -> str:
    """TypeIs の使用例。"""
    if is_str(value):
        # value は str
        return value.upper()
    # value は int（str が除外された！）
    return str(value * 2)


# ========================================
# パターンマッチングによる絞り込み
# ========================================


class Dog:
    """犬クラス。"""

    def bark(self) -> str:
        """吠える。"""
        return "Woof!"


class Cat:
    """猫クラス。"""

    def meow(self) -> str:
        """鳴く。"""
        return "Meow!"


class Bird:
    """鳥クラス。"""

    def chirp(self) -> str:
        """さえずる。"""
        return "Tweet!"


Animal = Dog | Cat | Bird


def handle_animal(animal: Animal) -> str:
    """Match 文による型の絞り込み。"""
    match animal:
        case Dog():
            # animal は Dog として扱える
            return animal.bark()
        case Cat():
            # animal は Cat として扱える
            return animal.meow()
        case Bird():
            # animal は Bird として扱える
            return animal.chirp()


# ========================================
# assert_never による網羅性チェック
# ========================================


def exhaustive_check(*, value: int | str | bool) -> str:
    """全ての型を網羅的に処理する。

    assert_never を使うと、処理漏れがあるとエラーになる。
    """
    if isinstance(value, bool):
        return f"bool: {value}"
    if isinstance(value, int):
        return f"int: {value}"
    if isinstance(value, str):
        return f"str: {value}"

    # ここに到達する型がないことを保証
    # 新しい型を Union に追加して処理を忘れると、
    # ty がエラーを出してくれる！
    assert_never(value)


# ========================================
# in による絞り込み
# ========================================


def check_membership(value: str) -> str:
    """In 演算子による絞り込み。"""
    valid_options = {"a", "b", "c"}

    if value in valid_options:
        # value は "a" | "b" | "c" のいずれか
        return f"Valid: {value}"

    return "Invalid"


# ========================================
# isinstance による絞り込み
# ========================================


class Success:
    """成功結果を表す。"""

    def __init__(self, value: str) -> None:
        """成功結果を初期化する。"""
        self.value = value


class Failure:
    """失敗結果を表す。"""

    def __init__(self, error: str) -> None:
        """失敗結果を初期化する。"""
        self.error = error


Result = Success | Failure


def handle_result(result: Result) -> str:
    """Result を処理して文字列を返す。"""
    if isinstance(result, Success):
        # result は Success として扱える
        return result.value
    # result は Failure として扱える
    return result.error


if __name__ == "__main__":
    print(handle_value(42))
    print(handle_value("hello"))
    print(handle_value(None))

    print(handle_animal(Dog()))
    print(handle_animal(Cat()))
