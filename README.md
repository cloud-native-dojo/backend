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

起動する．

```
uvicorn main:app --host 0.0.0.0
```
