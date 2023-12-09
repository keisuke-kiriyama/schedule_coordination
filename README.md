# schedule_coordination

スケジュール連携のスクリプト。SpreadSheetからGoogleカレンダーへの連携を行う。

## Dockerコンテナの起動

```sh
docker compose up
```

## コンテナへの接続

```sh
docker compose exec app bash
```

ローカルでバッチを実行する際は上記コマンドによりDockerコンテナに接続し、`/bin`配下のファイルを実行する。

## コンテナの停止

```sh
docker compose down
```
