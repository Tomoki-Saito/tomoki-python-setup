# ruff, ty

このコードに対して

以下のコマンド実行し、lint error, warning をできる限り直してください。

```sh
# 環境にあれば
uv run ruff check --fix && uv run ruff format
# 環境になければ
uvx ruff check --fix && uvx ruff format
```

また、 ty を使って、型のエラーを修正していって。

```sh
# 環境にあれば
uv run ty check
# 環境になければ
uvx ty check
```
