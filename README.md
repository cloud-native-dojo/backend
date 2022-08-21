# backend

## 動かし方

仮想環境を適宜つくる．

```
python -m venv .venv
. .venv/bin/activate
```

パッケージを入れる．

```
pip install fastapi uvicorn
```

helmのインストール

https://helm.sh/ja/docs/intro/install/

bitnamiのレポジトリを追加

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

起動する．

```
uvicorn main:app --host 0.0.0.0
```
