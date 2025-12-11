# tomoki-python-setup

[GitHub Repository](https://github.com/Tomoki-Saito/tomoki-python-setup)

## How to use

環境のセットアップ

```sh
uv sync
```

コードの実行

```sh
uv run python -m src.hello
```

パッケージのインストール

```sh
uv add requests
# 開発環境にのみインストール
uv add --dev types-requests
```

パッケージのアップグレード

```sh
uv add --upgrade requests
uv add --upgrade --dev types-requests
```

Ruff のフォーマット

```sh
uv run ruff format
```

Ruff のチェック

```sh
uv run ruff check
```

ty のチェック

```sh
uv run ty check
```
