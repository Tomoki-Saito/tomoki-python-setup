"""ジェネリクスと Protocol のデモ。

ty は高度なジェネリクス機能と Protocol（構造的部分型）をサポートしています。
Language Server が補完候補や型エラーを適切に表示してくれます。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

# ========================================
# ジェネリクス（型パラメータ）のデモ
# ========================================


def first[T](items: list[T]) -> T | None:
    """リストの最初の要素を返す。

    T は型パラメータ。呼び出し時に具体的な型に置き換えられる。
    """
    return items[0] if items else None


def pair[T, U](a: T, b: U) -> tuple[T, U]:
    """2つの値をタプルにする。"""
    return (a, b)


class Stack[T]:
    """ジェネリックなスタック。

    T はスタックに格納する要素の型。
    """

    def __init__(self) -> None:
        """スタックを初期化する。"""
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """要素をスタックに追加する。"""
        self._items.append(item)

    def pop(self) -> T:
        """スタックから要素を取り出す。"""
        return self._items.pop()

    def peek(self) -> T | None:
        """スタックの先頭要素を返す。"""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """スタックが空かどうかを返す。"""
        return len(self._items) == 0


def use_generics_demo() -> tuple[int | None, str | None, int, tuple[int, str]]:
    """ジェネリクスの使用例。"""
    # first() の戻り値の型が自動的に推論される
    nums = [1, 2, 3]
    first_num = first(nums)  # int | None と推論される

    strs = ["a", "b", "c"]
    first_str = first(strs)  # str | None と推論される

    # Stack も型パラメータが推論される
    int_stack = Stack[int]()
    int_stack.push(1)
    int_stack.push(2)
    value = int_stack.pop()  # int と推論される

    # pair の戻り値も正確に推論される
    p = pair(42, "hello")  # tuple[int, str]

    return first_num, first_str, value, p


# ========================================
# Protocol（構造的部分型）のデモ
# ========================================


class Printable(Protocol):
    """print可能なものを表す Protocol。

    __str__ メソッドを持つ任意のクラスが Printable になる。
    継承は不要！（ダックタイピングの型安全版）
    """

    def __str__(self) -> str:
        """文字列表現を返す。"""
        ...


class Comparable[T](Protocol):
    """比較可能なものを表す Protocol。"""

    def __lt__(self, other: T) -> bool:
        """小なり比較。"""
        ...

    def __le__(self, other: T) -> bool:
        """以下比較。"""
        ...


class HasLength(Protocol):
    """len() が使えるものを表す Protocol。"""

    def __len__(self) -> int:
        """長さを返す。"""
        ...


def print_item(item: Printable) -> None:
    """Printable な任意のオブジェクトを印刷する。"""
    print(str(item))


def get_length(item: HasLength) -> int:
    """HasLength な任意のオブジェクトの長さを取得する。"""
    return len(item)


def find_min(items: Iterable[Point]) -> Point | None:
    """Point のリストから原点に最も近い点を見つける。"""
    result: Point | None = None
    for item in items:
        if result is None or item < result:
            result = item
    return result


# Protocol を満たすカスタムクラス（継承不要！）
class Point:
    """2D座標。Printable と Comparable を暗黙的に満たす。"""

    def __init__(self, x: float, y: float) -> None:
        """座標を初期化する。"""
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """文字列表現を返す。"""
        return f"Point({self.x}, {self.y})"

    def __lt__(self, other: Self) -> bool:
        """原点からの距離で比較する。"""
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

    def __le__(self, other: Self) -> bool:
        """原点からの距離で比較する。"""
        return (self.x**2 + self.y**2) <= (other.x**2 + other.y**2)


def use_protocol_demo() -> tuple[int, int, Point | None]:
    """Protocol の使用例。"""
    # Point は Printable Protocol を満たす
    p = Point(3, 4)
    print_item(p)  # OK! Point には __str__ がある

    # int も Printable を満たす
    print_item(42)  # OK! int には __str__ がある

    # str, list は HasLength を満たす
    length1 = get_length("hello")  # OK!
    length2 = get_length([1, 2, 3])  # OK!

    # Point は Comparable を満たすので find_min で使える
    points = [Point(1, 1), Point(0, 0), Point(2, 3)]
    closest = find_min(points)  # Point | None

    return length1, length2, closest


# ========================================
# Callable Protocol のデモ
# ========================================


def apply_twice[T](f: Callable[[T], T], x: T) -> T:
    """関数を2回適用する。"""
    return f(f(x))


def transform_all[T, U](items: list[T], func: Callable[[T], U]) -> list[U]:
    """リストの全要素に関数を適用する。"""
    return [func(item) for item in items]


def callable_demo() -> tuple[int, list[str]]:
    """Callable の使用例。"""
    # apply_twice は関数と値を受け取る
    result1 = apply_twice(lambda x: x * 2, 3)  # 12 (3 -> 6 -> 12)

    # transform_all は型を変換できる
    nums = [1, 2, 3]
    strs = transform_all(nums, str)  # list[str] と推論される

    return result1, strs


# ========================================
# イテレータ Protocol のデモ
# ========================================


class Counter:
    """カウントアップするイテレータ。Iterator Protocol を満たす。"""

    def __init__(self, start: int, end: int) -> None:
        """カウンタを初期化する。"""
        self.current = start
        self.end = end

    def __iter__(self) -> Self:
        """イテレータを返す。"""
        return self

    def __next__(self) -> int:
        """次の値を返す。"""
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def iterate_demo() -> list[int]:
    """イテレータの使用例。"""
    counter = Counter(0, 5)
    return list(counter)  # [0, 1, 2, 3, 4]


if __name__ == "__main__":
    use_generics_demo()
    use_protocol_demo()
    callable_demo()
    iterate_demo()
