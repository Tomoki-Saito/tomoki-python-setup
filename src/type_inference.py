"""ty の型推論機能のデモ。

ty は型アノテーションがなくても賢く型を推論してくれます。
変数にカーソルを合わせると、推論された型が表示されます。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def basic_inference() -> tuple[int, str, float, bool, list[int], list[str], dict[str, int]]:
    """基本的な型推論のデモ。"""
    # 変数にホバーすると推論された型が見える
    number = 42  # int と推論
    text = "hello"  # str と推論
    pi = 3.14  # float と推論
    flag = True  # bool と推論 (Literal[True] かも)

    # リストも中身の型まで推論される
    numbers = [1, 2, 3]  # list[int]
    names = ["Alice", "Bob"]  # list[str]

    # 辞書も key/value の型が推論される
    scores = {"math": 90, "english": 85}  # dict[str, int]

    return number, text, pi, flag, numbers, names, scores


def flow_sensitive_inference() -> tuple[int, int]:
    """フロー解析による型推論のデモ。"""
    value: int | str = "hello"

    # この時点で value は str
    length = len(value)  # OK! str には len() がある

    value = 42
    # この時点で value は int
    doubled = value * 2  # OK! int には * 演算子がある

    return length, doubled


def conditional_inference(*, flag: bool) -> int:
    """条件分岐での型推論のデモ。"""
    # 両方のブランチで list[int] なので result は list[int]
    result = [1, 2, 3] if flag else [4, 5]
    return sum(result)


def infer_from_usage() -> tuple[list[int], int, str]:
    """使い方から型を推論するデモ。"""
    # 空のリストでも、後の使い方から型を推論できる場合がある
    items: list[int] = []
    items.append(1)
    items.append(2)

    # タプルも要素ごとに型が推論される
    pair = (42, "hello")  # tuple[int, str]
    num, txt = pair  # num: int, txt: str

    return items, num, txt


def comprehension_inference() -> tuple[list[int], dict[str, int], set[int], Generator[int]]:
    """内包表記の型推論のデモ。"""
    # リスト内包表記
    squares = [x * x for x in range(10)]  # list[int]

    # 辞書内包表記
    char_codes = {c: ord(c) for c in "abc"}  # dict[str, int]

    # 集合内包表記
    unique_lengths = {len(s) for s in ["a", "bb", "ccc"]}  # set[int]

    # ジェネレータ式
    gen = (x * 2 for x in range(5))  # Generator[int, None, None]

    return squares, char_codes, unique_lengths, gen


if __name__ == "__main__":
    basic_inference()
    flow_sensitive_inference()
    conditional_inference(flag=True)
    infer_from_usage()
    comprehension_inference()
