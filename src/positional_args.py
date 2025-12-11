"""位置引数が多い関数のデモ。

ty の Language Server は、関数呼び出し時にインレイヒントで
引数名を表示してくれます。これにより、位置引数が多い関数でも
どの引数が何を意味するのかが一目でわかります。

VSCode で関数呼び出しを見ると、各引数の前に引数名が表示されます。
"""

# ruff: noqa: PLR0913, FBT001, FBT003, DTZ001
# PLR0913: Too many arguments (デモ用に意図的)
# FBT001/FBT003: Boolean positional argument (デモ用に意図的)
# DTZ001: datetime without tzinfo (デモ用に簡略化)

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date


# ========================================
# 位置引数が多い関数の例
# ========================================


def create_user(
    name: str,
    email: str,
    age: int,
    is_active: bool,
    role: str,
    department: str,
) -> dict[str, str | int | bool]:
    """ユーザーを作成する。

    引数が多いが、呼び出し側でインレイヒントが表示される。
    """
    return {
        "name": name,
        "email": email,
        "age": age,
        "is_active": is_active,
        "role": role,
        "department": department,
    }


def schedule_meeting(
    title: str,
    organizer: str,
    start_time: datetime,
    end_time: datetime,
    room: str,
    attendees: list[str],
    is_recurring: bool,
    reminder_minutes: int,
) -> dict[str, object]:
    """ミーティングをスケジュールする。

    8個の引数があるが、インレイヒントで意味がわかる。
    """
    return {
        "title": title,
        "organizer": organizer,
        "start_time": start_time,
        "end_time": end_time,
        "room": room,
        "attendees": attendees,
        "is_recurring": is_recurring,
        "reminder_minutes": reminder_minutes,
    }


def send_email(
    to: str,
    subject: str,
    body: str,
    cc: list[str],
    bcc: list[str],
    attachments: list[str],
    is_html: bool,
    priority: int,
) -> bool:
    """メールを送信する。

    引数が多くても、インレイヒントで各引数の意味が明確。
    """
    _ = to, subject, body, cc, bcc, attachments, is_html, priority
    return True


def create_order(
    customer_id: int,
    product_ids: list[int],
    quantities: list[int],
    shipping_address: str,
    billing_address: str,
    payment_method: str,
    discount_code: str | None,
    gift_wrap: bool,
    delivery_notes: str,
) -> dict[str, object]:
    """注文を作成する。

    9個の引数！でもインレイヒントがあれば大丈夫。
    """
    return {
        "customer_id": customer_id,
        "product_ids": product_ids,
        "quantities": quantities,
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "payment_method": payment_method,
        "discount_code": discount_code,
        "gift_wrap": gift_wrap,
        "delivery_notes": delivery_notes,
    }


# ========================================
# 使用例（インレイヒントが表示される）
# ========================================


def demo_inlay_hints() -> None:
    """インレイヒントのデモ。

    以下の関数呼び出しを VSCode で見ると、
    各引数の前に引数名がグレーで表示される。

    例: create_user(name: "Alice", email: "alice@example.com", ...)
    """
    # 位置引数で呼び出し → インレイヒントで引数名が表示される
    user = create_user(
        "Alice",
        "alice@example.com",
        30,
        True,
        "engineer",
        "development",
    )

    # 同様に、他の関数も引数名が表示される
    meeting = schedule_meeting(
        "Weekly Standup",
        "Bob",
        datetime(2024, 1, 15, 10, 0),
        datetime(2024, 1, 15, 10, 30),
        "Room A",
        ["Alice", "Charlie", "David"],
        True,
        15,
    )

    # メール送信
    send_email(
        "user@example.com",
        "Hello",
        "This is a test email",
        ["cc@example.com"],
        [],
        [],
        False,
        1,
    )

    # 注文作成
    order = create_order(
        12345,
        [1, 2, 3],
        [1, 2, 1],
        "123 Main St",
        "456 Billing Ave",
        "credit_card",
        None,
        False,
        "Leave at door",
    )

    print(user, meeting, order)


# ========================================
# 座標系の例（数値の引数が多い）
# ========================================


def draw_rectangle(
    x: float,
    y: float,
    width: float,
    height: float,
    rotation: float,
    fill_color: str,
    stroke_color: str,
    stroke_width: float,
) -> None:
    """矩形を描画する。

    数値の引数が多いと、インレイヒントが特に役立つ。
    x, y, width, height の順番を間違えやすいが、
    インレイヒントがあれば安心。
    """
    _ = x, y, width, height, rotation, fill_color, stroke_color, stroke_width


def create_3d_point(x: float, y: float, z: float) -> tuple[float, float, float]:
    """3D座標を作成する。"""
    return (x, y, z)


def transform_point(
    x: float,
    y: float,
    z: float,
    scale_x: float,
    scale_y: float,
    scale_z: float,
    rotate_x: float,
    rotate_y: float,
    rotate_z: float,
    translate_x: float,
    translate_y: float,
    translate_z: float,
) -> tuple[float, float, float]:
    """3D点を変換する。

    12個の引数！インレイヒントなしでは読めない。
    """
    _ = scale_x, scale_y, scale_z, rotate_x, rotate_y, rotate_z
    return (x + translate_x, y + translate_y, z + translate_z)


def demo_numeric_args() -> None:
    """数値引数のデモ。"""
    # 矩形を描画
    draw_rectangle(
        10.0,
        20.0,
        100.0,
        50.0,
        45.0,
        "#FF0000",
        "#000000",
        2.0,
    )

    # 3D点を作成
    point = create_3d_point(1.0, 2.0, 3.0)

    # 点を変換（12個の引数！）
    transformed = transform_point(
        1.0,
        2.0,
        3.0,
        1.5,
        1.5,
        1.5,
        0.0,
        45.0,
        0.0,
        10.0,
        20.0,
        30.0,
    )

    print(point, transformed)


# ========================================
# 日付関連の関数（似た型の引数が多い）
# ========================================


def create_event(
    name: str,
    description: str,
    start_date: date,
    end_date: date,
    registration_start: date,
    registration_end: date,
    early_bird_deadline: date,
) -> dict[str, object]:
    """イベントを作成する。

    date 型の引数が5つもある！
    インレイヒントがないと、どれがどれかわからない。
    """
    return {
        "name": name,
        "description": description,
        "start_date": start_date,
        "end_date": end_date,
        "registration_start": registration_start,
        "registration_end": registration_end,
        "early_bird_deadline": early_bird_deadline,
    }


# ========================================
# dataclass との組み合わせ
# ========================================


@dataclass
class Rectangle:
    """矩形を表す dataclass。"""

    x: float
    y: float
    width: float
    height: float
    rotation: float = 0.0
    fill_color: str = "#FFFFFF"
    stroke_color: str = "#000000"
    stroke_width: float = 1.0


def demo_dataclass_args() -> None:
    """Dataclass のコンストラクタでもインレイヒントが表示される。"""
    # dataclass のコンストラクタも同様にインレイヒントが表示される
    rect = Rectangle(
        10.0,
        20.0,
        100.0,
        50.0,
        45.0,
        "#FF0000",
        "#000000",
        2.0,
    )

    # 名前付き引数と混在しても OK
    rect2 = Rectangle(
        10.0,
        20.0,
        100.0,
        50.0,
        fill_color="#00FF00",
    )

    print(rect, rect2)


if __name__ == "__main__":
    demo_inlay_hints()
    demo_numeric_args()
    demo_dataclass_args()
