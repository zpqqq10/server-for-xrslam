# HTTP Server for XRSlam 

1. Installation

```bash
conda create -n vis python=3.10
conda activate vis
pip install -i https://mirrors.aliyun.com/pypi/simple pyqtgraph
pip install -i https://mirrors.aliyun.com/pypi/simple PyQt5
pip install -i https://pypi.douban.com/simple pyOpenGL
pip install seaborn, numpy
```



2. Start the server

```bash
python server.py 2>http.log
```

Ctrl+C退出

iPhone上需要输入的ip和port可以在server.log中查看



3. Visualize

```bash
conda activate vis
python gui.py
```

- 左键改变视角
- 滑轮平移



# Notice

由于网络问题，有时xrslam发过来的包会延迟很大甚至没有被接收到。这个时候需要对照包的时间对iPhone上的多余照片进行删除，为此代码中json的命名是来自于请求中附带的时间信息（上一版代码是电脑接收到请求时的本机时间）。
