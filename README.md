# schedule_coordination

スケジュール連携のスクリプト。SpreadSheetからGoogleカレンダーへの連携を行う。

## バッチの実行

```sh
docker compose up
```

## コンテナへの接続

```sh
docker compose exec app bash
```

## コンテナの停止

```sh
docker compose down
```

## 備考

一旦はマスタのシートを参照用シートにコピーしたものからGoogleカレンダーに連携。
追ってマスタのシート参照しつつcronで定期更新されるようにする。
