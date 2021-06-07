# PrajnaBlog

## 数据库迁移
```
alembic revision -m "init"  # --autogenerate 自动生成
```
## 数据库升级
```
alembic upgrade head
```

## 启动命令
```
uvicorn main:app
```
