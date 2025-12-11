"""TypedDict と dataclass のデモ。

ty は TypedDict と dataclass を完全にサポートしており、
キーや属性の補完、型チェック、ドキュメント表示などが利用できます。
"""

from dataclasses import dataclass, field
from typing import NotRequired, Required, TypedDict

# ========================================
# TypedDict のデモ
# ========================================


class UserDict(TypedDict):
    """ユーザー情報を表す TypedDict。

    辞書のキーと値の型を定義できる。
    user["name"] のように . でなく [] でアクセスする場合に便利。
    """

    id: int
    name: str
    email: str


class UserDictWithOptional(TypedDict, total=False):
    """オプショナルなキーを持つ TypedDict。

    total=False にすると全てのキーがオプショナルになる。
    """

    id: int
    name: str
    nickname: str  # オプショナル


class MixedUserDict(TypedDict):
    """必須とオプショナルを混在させた TypedDict。

    Required/NotRequired を使って個別に指定できる。
    """

    id: Required[int]  # 必須
    name: Required[str]  # 必須
    email: NotRequired[str]  # オプショナル
    age: NotRequired[int]  # オプショナル


def create_user(name: str, email: str) -> UserDict:
    """TypedDict を返す関数。"""
    return {
        "id": 1,
        "name": name,
        "email": email,
    }


def use_typed_dict() -> tuple[str, int]:
    """TypedDict の使用例。"""
    user = create_user("Alice", "alice@example.com")

    # キーへのアクセスは型安全
    name = user["name"]  # str と推論される
    user_id = user["id"]  # int と推論される

    # 存在しないキーへのアクセスはエラー！（補完にも出ない）
    # user["invalid_key"]  # ty error!

    # キーの補完が効く！
    # user["  <- ここで補完候補が表示される

    return name, user_id


class APIResponse(TypedDict):
    """API レスポンスを表す TypedDict。ネストも可能。"""

    status: int
    data: UserDict  # ネストした TypedDict
    message: str


def process_response(response: APIResponse) -> str:
    """ネストした TypedDict を処理する。"""
    # ネストしたアクセスも型安全
    user_name = response["data"]["name"]  # str
    return f"User: {user_name}, Status: {response['status']}"


# ========================================
# dataclass のデモ
# ========================================


@dataclass
class User:
    """ユーザーを表す dataclass。

    dataclass は自動的に __init__, __repr__, __eq__ などを生成する。
    ty は生成されたメソッドも認識して補完してくれる。
    """

    id: int
    name: str
    email: str


@dataclass
class UserWithDefaults:
    """デフォルト値を持つ dataclass。"""

    id: int
    name: str
    email: str = "unknown@example.com"
    is_active: bool = True


@dataclass
class Post:
    """投稿を表す dataclass。"""

    id: int
    title: str
    content: str
    author: User  # 別の dataclass を含められる


@dataclass
class UserWithFactory:
    """factory を使った dataclass。"""

    id: int
    name: str
    tags: list[str] = field(default_factory=list)  # ミュータブルなデフォルト値


def use_dataclass() -> tuple[str, str, str]:
    """Dataclass の使用例。"""
    # コンストラクタの引数が補完される
    user = User(id=1, name="Alice", email="alice@example.com")

    # 属性アクセスは型安全
    name = user.name  # str と推論される

    # デフォルト値を持つ dataclass
    user2 = UserWithDefaults(id=2, name="Bob")  # email と is_active は省略可能

    # ネストした dataclass
    post = Post(id=1, title="Hello", content="World", author=user)
    author_name = post.author.name  # str と推論される

    return name, user2.email, author_name


# ========================================
# frozen dataclass（イミュータブル）
# ========================================


@dataclass(frozen=True)
class Point:
    """イミュータブルな座標。"""

    x: float
    y: float


def use_frozen_dataclass() -> tuple[Point, Point]:
    """Frozen dataclass の使用例。"""
    p = Point(1.0, 2.0)

    # frozen なので代入はエラー！
    # p.x = 3.0  # ty error: Cannot assign to attribute "x"

    # 新しいインスタンスを作る必要がある
    p2 = Point(3.0, p.y)

    return p, p2


# ========================================
# kw_only dataclass（Python 3.10+）
# ========================================


@dataclass(kw_only=True)
class Config:
    """キーワード引数のみを受け付ける dataclass。"""

    host: str
    port: int
    debug: bool = False


def use_kw_only_dataclass() -> Config:
    """kw_only dataclass の使用例。"""
    # 位置引数は使えない
    # config = Config("localhost", 8080)  # ty error!

    # キーワード引数のみ
    return Config(host="localhost", port=8080)


# ========================================
# slots dataclass（Python 3.10+）
# ========================================


@dataclass(slots=True)
class EfficientUser:
    """slots を使ったメモリ効率の良い dataclass。"""

    id: int
    name: str


def use_slots_dataclass() -> EfficientUser:
    """Slots dataclass の使用例。"""
    # 定義されていない属性は追加できない
    # user.extra = "value"  # ty error!

    return EfficientUser(id=1, name="Alice")


# ========================================
# 継承を使った dataclass
# ========================================


@dataclass
class Person:
    """基底クラス。"""

    name: str
    age: int


@dataclass
class Employee(Person):
    """Person を継承した dataclass。"""

    employee_id: str
    department: str


def use_inherited_dataclass() -> tuple[str, str]:
    """継承した dataclass の使用例。"""
    emp = Employee(
        name="Alice",
        age=30,
        employee_id="E001",
        department="Engineering",
    )

    # 親クラスの属性も補完される
    name = emp.name  # str
    dept = emp.department  # str

    return name, dept


if __name__ == "__main__":
    use_typed_dict()
    use_dataclass()
    use_frozen_dataclass()
    use_kw_only_dataclass()
    use_slots_dataclass()
    use_inherited_dataclass()
