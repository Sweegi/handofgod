# handofgod
daily work in Games

### Docker运行开发环境(无法使用截图功能)
```
# 创建
$ docker build -t python3.8 .

# 执行
$ docker run -it --rm -v "$PWD/src":/app/src -w /app/src python3.8 python main.py
```
