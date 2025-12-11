"""Pandas の型アノテーションのデモ。

pandas-stubs が組み込まれているため、DataFrame や Series に対して
適切な型チェックと補完が効く。
"""

from __future__ import annotations

import pandas as pd

# 定数
MIN_ADULT_AGE = 30
MIN_YOUNG_AGE = 25


# ========================================
# 基本的な DataFrame の型アノテーション
# ========================================


def create_dataframe() -> pd.DataFrame:
    """DataFrame を作成して返す。

    戻り値の型として pd.DataFrame を指定できる。
    """
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "city": ["Tokyo", "Osaka", "Nagoya"],
        }
    )


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """DataFrame を受け取って加工する。

    Args:
        df: 入力の DataFrame。

    Returns:
        フィルタリングされた DataFrame。
    """
    return df[df["age"] >= MIN_ADULT_AGE]


def use_dataframe_demo() -> None:
    """DataFrame の基本的な型アノテーションの使用例。"""
    df = create_dataframe()
    filtered = process_dataframe(df)
    print("Filtered DataFrame:")
    print(filtered)


# ========================================
# Series の型アノテーション
# ========================================


def get_column(df: pd.DataFrame, column: str) -> pd.Series[object]:
    """DataFrame から列を取得する。

    pd.Series[T] で Series の要素の型を指定できる。
    """
    return df[column]


def sum_numeric_series(series: pd.Series[int]) -> int:
    """数値の Series を合計する。"""
    result = series.sum()
    # pandas の sum() は numpy スカラーを返すことがあるので int に変換
    return int(result)


def use_series_demo() -> None:
    """Series の型アノテーションの使用例。"""
    df = create_dataframe()
    ages = df["age"]
    total_age = sum_numeric_series(ages)
    print(f"Total age: {total_age}")


# ========================================
# 集計・グループ化の型
# ========================================


def group_and_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """グループ化して集計する。

    groupby().agg() の結果も DataFrame として型付けできる。
    """
    return df.groupby("city").agg({"age": "mean"}).reset_index()


def pivot_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """ピボットテーブルを作成する。"""
    df_with_value = df.copy()
    df_with_value["value"] = [100, 200, 300]
    return df_with_value.pivot_table(
        index="city",
        values="value",
        aggfunc="sum",
    )


def use_aggregation_demo() -> None:
    """集計の型アノテーションの使用例。"""
    df = create_dataframe()
    grouped = group_and_aggregate(df)
    print("Grouped DataFrame:")
    print(grouped)


# ========================================
# Index の型アノテーション
# ========================================


def get_index(df: pd.DataFrame) -> pd.Index[object]:
    """DataFrame のインデックスを取得する。"""
    return df.index


def set_custom_index(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """指定した列をインデックスに設定する。"""
    return df.set_index(column)


def use_index_demo() -> None:
    """Index の型アノテーションの使用例。"""
    df = create_dataframe()
    indexed = set_custom_index(df, "name")
    print("Indexed DataFrame:")
    print(indexed)


# ========================================
# 読み書きの型
# ========================================


def read_csv_data(path: str) -> pd.DataFrame:
    """CSV ファイルを読み込む。

    pd.read_csv() は DataFrame を返すため、戻り値は pd.DataFrame。
    """
    return pd.read_csv(path)


def save_to_csv(df: pd.DataFrame, path: str) -> None:
    """DataFrame を CSV に保存する。"""
    df.to_csv(path, index=False)


def dataframe_to_dict(df: pd.DataFrame) -> dict[str, list[object]]:
    """DataFrame を辞書に変換する。

    to_dict("list") は {列名: [値...]} の形式の辞書を返す。
    """
    return df.to_dict("list")


# ========================================
# 条件フィルタリングとマスク
# ========================================


def filter_by_condition(df: pd.DataFrame, min_age: int) -> pd.DataFrame:
    """条件でフィルタリングする。

    ブールマスクを使ったフィルタリングも型が通る。
    """
    mask: pd.Series[bool] = df["age"] >= min_age
    return df[mask]


def filter_multiple_conditions(df: pd.DataFrame) -> pd.DataFrame:
    """複数条件でフィルタリングする。"""
    return df[(df["age"] >= MIN_YOUNG_AGE) & (df["city"] == "Tokyo")]


def use_filter_demo() -> None:
    """フィルタリングの型アノテーションの使用例。"""
    df = create_dataframe()
    filtered = filter_by_condition(df, 30)
    print("Filtered by condition:")
    print(filtered)


# ========================================
# 実践的な例: データ変換パイプライン
# ========================================


def normalize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """列を正規化（0-1スケール）する。"""
    df = df.copy()
    col = df[column]
    df[column] = (col - col.min()) / (col.max() - col.min())
    return df


def add_derived_column(df: pd.DataFrame) -> pd.DataFrame:
    """派生列を追加する。"""
    df = df.copy()
    df["age_group"] = df["age"].apply(lambda x: "young" if x < MIN_ADULT_AGE else "adult")
    return df


def transform_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """変換パイプラインを実行する。

    複数の変換を連鎖させる。
    """
    return df.pipe(normalize_column, "age").pipe(add_derived_column)


def use_pipeline_demo() -> None:
    """パイプラインの使用例。"""
    df = create_dataframe()
    transformed = transform_pipeline(df)
    print("Transformed DataFrame:")
    print(transformed)


# ========================================
# merge と concat の型
# ========================================


def merge_dataframes(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: str,
) -> pd.DataFrame:
    """2つの DataFrame をマージする。"""
    return left.merge(right, on=on)


def concat_dataframes(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """複数の DataFrame を縦に結合する。"""
    return pd.concat(dfs, ignore_index=True)


def use_merge_demo() -> None:
    """merge と concat の使用例。"""
    df1 = create_dataframe()
    df2 = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "salary": [50000, 60000],
        }
    )
    merged = merge_dataframes(df1, df2, on="name")
    print("Merged DataFrame:")
    print(merged)


if __name__ == "__main__":
    use_dataframe_demo()
    print()
    use_series_demo()
    print()
    use_aggregation_demo()
    print()
    use_index_demo()
    print()
    use_filter_demo()
    print()
    use_pipeline_demo()
    print()
    use_merge_demo()
