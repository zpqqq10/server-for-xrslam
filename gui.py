
import numpy as np
import pyqtgraph as pg
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets, QtGui
import pyqtgraph.opengl as gl
import os, json
import seaborn as sns

class Gui():
    def __init__(self):
        self.app = pg.mkQApp('gui')
        self.area = DockArea()
        self.d1 = Dock("Dock1")   
        self.w1 = None
    
    def prepareData(self, path = 'frames'):
        positions = []
        c2ws = []
        n = 0
        for root, dirs, files in os.walk(path):
            n = len(files)
            for name in files:
                with open(os.path.join(root, name)) as f:
                    pose = json.load(f)['pose']
                    position = pose['position']
                    positions.append(position)
                    x, y, z, w = pose['quaternion']
                    # JPL, left-handed
                    c2ws.append([[1-2*y*y-2*z*z, 2*x*y+2*w*z, 2*x*z-2*w*y, position[0]], 
                                 [2*x*y-2*w*z, 1-2*x*x-2*z*z, 2*y*z+2*w*x, position[1]], 
                                 [2*x*z+2*w*y, 2*y*z-2*w*x, 1-2*x*x-2*y*y, position[2]]])
                    # Hamilton, right-handed
                    # c2ws.append([[1-2*y*y-2*z*z, 2*x*y-2*w*z, 2*x*z+2*w*y, position[0]], 
                    #              [2*x*y+2*w*z, 1-2*x*x-2*z*z, 2*y*z-2*w*x, position[1]], 
                    #              [2*x*z-2*w*y, 2*y*z+2*w*x, 1-2*x*x-2*y*y, position[2]]])
        c2ws = np.array(c2ws)
        pts = np.hstack((positions, sns.hls_palette(n_colors=n)))
        return c2ws, pts
    
    def vis_trajectory(self, c2ws, pts, scale = 0.2):
        '''visualize camera, point clouds
        cameras are rotated from direction (1, 0, 0)

        Args:
            c2ws (K x 3 x 4 ndarray): camera to world system matrix, K 3x3 rotation matrix and K 3x1 translate matrix
            pts (N x 6 ndarray): point clouds, N x (x, y, z, R, G, B)
            scale (float): scale of camera
        '''
        # configs
        SHOWGRID = False  # whether to draw x-y grid
        SHOWAXIS = True  # whether to draw axis
        POINTSIZE = .1  # size of points in point clouds
        GRID = 25  # size of grid
        CAMERACOLOR = (1, 0, 0, 1)  # color of cameras

        # preparing the widget & grid
        # pg.mkQApp("Visualize cluster")
        w = gl.GLViewWidget()
        # w.show()
        # w.resize(1000, 800)
        # w.setWindowTitle('Visualize cluster')
        w.setCameraPosition(distance=50)
        if SHOWGRID:
            griditem = gl.GLGridItem(size=QtGui.QVector3D(GRID * 2, GRID * 2, 1))
            w.addItem(griditem)
        if SHOWAXIS:
            # x is blue, y is yellow, z is green
            axisitem = gl.GLAxisItem(size=QtGui.QVector3D(GRID, GRID, GRID))
            w.addItem(axisitem)

        # preparing camera
        # vertexes = np.array([[0, 0, 0], [-3, 1, 1], [-3, 1, -1], [-3, -1, -1], [-3, -1, 1]])*scale # facing -x-axis
        # vertexes = np.array([[0, 0, 0], [3, 1, 1], [3, 1, -1], [3, -1, -1], [3, -1, 1]])*scale # facing x-axis
        # vertexes = np.array([[0, 0, 0], [1, -3, 1], [1, -3, -1], [-1, -3, -1], [-1, -3, 1]])*scale # facing -y-axis
        # vertexes = np.array([[0, 0, 0], [1, 3, 1], [1, 3, -1], [-1, 3, -1], [-1, 3, 1]])*scale # facing y-axis
        vertexes = np.array([[0, 0, 0], [1, 1, -3], [1, -1, -3], [-1, -1, -3], [-1, 1, -3]])*scale # facing -z-axis
        # vertexes = np.array([[0, 0, 0], [1, 1, 3], [1, -1, 3], [-1, -1, 3], [-1, 1, 3]])*scale # facing z-axis
        faces = np.array([[1, 0, 2], [2, 0, 3], [3, 0, 4], [4, 0, 1]])
        for mat in c2ws:
            rotation = mat[:, :3]  # rotation matrix
            v = np.array([np.dot(vert, rotation) for vert in vertexes])
            camera = gl.GLMeshItem(vertexes=v,
                                faces=faces,
                                drawFaces=False,
                                drawEdges=True,
                                edgeColor=CAMERACOLOR,
                                smooth=False,
                                shader='balloon',
                                glOptions='additive')
            camera.translate(mat[0][3], mat[1][3], mat[2][3])  # translate matrix
            w.addItem(camera)

        # preparing point clouds
        N = pts.shape[0]
        pos = pts[:, 0:3]
        size = np.full((N), POINTSIZE)
        color = np.hstack((pts[:, 3:], np.ones((N, 1))))
        # If True, spots are always the same size regardless of scaling, and size is given in px.
        # Otherwise, size is in scene coordinates and the spots scale with the view.
        ppts = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        w.addItem(ppts)
        
        # draw line
        plt = gl.GLLinePlotItem(pos=pos, color=pg.mkColor(240, 240, 240), width=1., antialias=True)
        w.addItem(plt)
        

        # dispalay the widget
        # pg.exec()
        return w
        
    def run(self, path = 'frames'): 
        # main window & dock area
        win = QtWidgets.QMainWindow()
        win.setCentralWidget(self.area)
        win.resize(1000,500)
        win.setWindowTitle('gui')
        # docks
        self.d1.hideTitleBar()  
        self.area.addDock(self.d1)
        
        # visualize
        c2ws, pts = self.prepareData(path)
        self.w1 = self.vis_trajectory(c2ws, pts)
        self.w1.setBackgroundColor(1, 1, 0, 1)
        self.d1.addWidget(self.w1)
        # dispalay the widget
        win.show()
        pg.exec()

if __name__ == '__main__':
    g = Gui()
    g.run('frames')