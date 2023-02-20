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

