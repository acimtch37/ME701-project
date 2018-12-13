# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:09:02 2018

@author: Alec Mitchell
"""
#Project
import sys
import platform

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import savgol_filter

from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QAction, QMessageBox,QFileDialog,
                             QSizePolicy, QPushButton, QComboBox)
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

"""
To do:
    - Build function to get outputs from indent start and end
    - Get text from input boxes wen button pressed
    - output 3rd graph
    - save as
    - help
    - do more?
    - clean up and comment
    - writeup
"""

my_data = np.loadtxt('WM_1.csv', delimiter=',', skiprows=6)

#Create image of raw data
#plt.figure(1)
#plt.pcolormesh(my_data,vmin=-5.5, vmax=-5)
#plt.grid()

#user inputs y values where a row of indends start and end
#y3 is the location of the center of an indent row
#user inputs y1 and y2
y1=300
y2=440
why = int(.5*(y1+y2))
xprof = np.linspace(0,16, len(my_data[why]))
def getycorrected(y1,y2):
    y3=int(.5*(y1+y2))
    
    xprof = np.linspace(0,16, len(my_data[y3]))
    yraw = my_data[y3]
    
    #replace outliers with local average
    stdev = np.std(yraw)
    mean = np.mean(yraw)
    yprof = np.copy(yraw)
    for i in range(0,len(yraw)):
        if abs(yraw[i]-mean) >= 2*stdev:
            yprof[i] = .5*(yraw[i+15]+yraw[i-15])
    
    #built in scipy funcion to smooth dat
    ysmooth = savgol_filter(yprof, 21, 1)
    
    
    #use plynomial trendline to correct bow in data
    coeff = np.polyfit(xprof, ysmooth, 2)
    trendl = coeff[0]*xprof**2 + coeff[1]*xprof + coeff[2]

    ycorrected = ysmooth-trendl+trendl[0]
    return ycorrected
ycorrected = getycorrected(y1,y2)
#plt.figure(2)
#plt.ylim(-5.6, -5.25)
#plt.grid()
#plt.plot(xprof, ycorrected)

def getapprox(ycorrected):
    R = np.gradient(ycorrected)
    wallleft = np.where((R < -.0019)) #all left sides of indents
    wallright = np.where(R > .0019) #all  right sides of indents
    wall_1=[] #location of left side of indent to be analyzed
    wall_2=[] #location of right side of indent to be analyzed
    diff = np.diff(wallleft)
    for i in range(np.size(wallleft)):
        wall_1.append(wallleft[0][i])
        if diff[0][i]> 1:
            break
    wallnext = wallright[0][np.where(wallright > wall_1[-1])[1][0]:] #look only to the right of wall 1
    #filter wall 2 section from wall right
    for i in range(np.size(wallright)):
        wall_2.append(wallnext[i])
        if wallnext[i+1] > wallnext[i]+1:
            break
    #output of function is ycorrected
    
    #graph indent profile
  
    
    
    #user defines bounds to focus on one indent 
    x_l = wall_1[0]-40
    x_r = wall_2[-1]+55
    
    #edge_a=3.82
    edge_a=xprof[wall_1[0]]
    #edge_b=4.07
    edge_b=xprof[wall_1[-1]]
    #edge_c=7.6
    edge_c=xprof[wall_2[0]]
    #edge_d=8.14
    edge_d=xprof[wall_2[-1]]
    
    D_o_left = np.average(ycorrected[x_l:wall_1[0]])
    D_i =  np.average(ycorrected[wall_1[-1]:wall_2[0]])
    D_o_right = np.average(ycorrected[wall_2[-1]:x_r])
    x_approx = [xprof[x_l],edge_a, edge_b, edge_c, edge_d, xprof[x_r]]
    y_approx = [D_o_left, D_o_left, D_i, D_i, D_o_right, D_o_right]
    
    return (x_approx, y_approx)
approx = getapprox(ycorrected)
#plt.figure(3)
#plt.xlim(approx[0][0],approx[0][-1])
#plt.ylim(-5.6, -5.25)
#plt.grid()
#plt.plot(xprof, ycorrected, approx[0],approx[1])

#%%
class MainWindow(QMainWindow) :
    
    def __init__(self, parent=None) :
        super(MainWindow, self).__init__(parent)

        ########################################################################
        # ADD MENU ITEMS
        ########################################################################
        
        # Create the File menu

        
        # Create the Help menu
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.actionAbout = QAction("&About",self)
        self.actionAbout.triggered.connect(self.about)
        self.menuHelp.addActions([self.actionAbout])
        
        ########################################################################
        # CREATE CENTRAL WIDGET
        ########################################################################

        self.widget = QDialog()
        self.plot1 = MatplotlibColormesh()
        self.plot2 = MatplotlibCanvas()
        self.plot3 = MatplotlibCanvas()
        self.edit1 = QLineEdit("lower edge")
        self.edit2 = QLineEdit("upper edge")
        self.edit3 = QLineEdit("name data entry")
        self.button1 = QPushButton('Show Profile', self)
        self.button2 = QPushButton('Show Output', self)
        
        # signals + slots ()
#        self.edit1.returnPressed.connect(self.update)
        self.button1.clicked.connect(self.update_graph) 
        self.button2.clicked.connect(self.get_outputs)
        #Save function needs to save the outputs
        
        layout = QVBoxLayout()
        layout.addWidget(self.plot1)
        sub_layout1 = QHBoxLayout()
        sub_layout1.addWidget(self.edit1)
        sub_layout1.addWidget(self.edit2)
        sub_layout1.addWidget(self.button1)
        sub_layout2 = QHBoxLayout()
        sub_layout2.addWidget(self.edit3)
        sub_layout2.addWidget(self.button2)
        layout.addLayout(sub_layout1)
        layout.addWidget(self.plot2)
        layout.addLayout(sub_layout2)
        layout.addWidget(self.plot3)
        self.widget.setLayout(layout)        
        self.setCentralWidget(self.widget)
        
       
    def about(self):
        QMessageBox.about(self, 
            "About Program",
            """<b>Preliminary rebar analysis</b>
               <p>Copyright &copy; 2018 Alec Mitchell, All Rights Reserved.
               <p>Python %s -- Qt %s -- PyQt %s on %s""" %
            (platform.python_version(),
             QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

#    def update(self):
#        """Update the figure title.
#        
#        Of course, this is trivial(ish), but it serves as a guid for how
#        to update other parts of the figure (see the reference for more).
#        """
#        title = str(self.edit1.text())
#        self.plot.axes.set_title(title)
#        x = np.linspace(0,10)
#        y = x**2
#        self.plt.draw()

    def update_graph(self):
        """Update the figure graph.
        
        
        """
        self.ybot = eval(self.edit1.text())
        self.ytop = eval(self.edit2.text())
        ymid = (self.ybot+self.ytop)/2
        self.x = np.linspace(0,16, len(my_data[why]))
        self.y = getycorrected(self.ybot,self.ytop)
        self.plot2.redraw(self.x,self.y)
        
    def get_outputs(self):
        """Update the figure graph.
        
        
        """
        approx = getapprox(self.y)
        self.leftslope = (approx[1][1]-approx[1][2])/(approx[0][2]-approx[0][1])
        self.rightslope = (approx[1][4]-approx[1][3])/(approx[0][4]-approx[0][3])
        self.area = .5*(approx[0][1]*approx[1][2] - approx[1][1]*approx[0][2] + approx[0][2]*approx[1][3] - approx[1][2]*approx[0][3] + approx[0][3]*approx[1][4] - approx[1][3]*approx[0][4] + approx[0][4]*approx[1][1] - approx[1][4]*approx[0][1])
        self.depth = .5*(approx[1][1]+approx[1][4]-approx[1][2]-approx[1][3])
        self.plot3.overlay(self.x,self.y, approx[0], approx[1])
        name = self.edit3.text()
        row = [name, self.leftslope, self.rightslope, self.area, self.depth]
        with open('output.csv', mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
        

                
class MatplotlibColormesh(FigureCanvas) :
    """ This is borrowed heavily from the matplotlib documentation;
        specifically, see:
        http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """
    def __init__(self):
        
        # Initialize the figure and axes
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        
        # Give it some default plot (if desired).  
       
        self.axes.pcolormesh(my_data,vmin=-5.5, vmax=-5)
        self.axes.grid()
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y(x)')   
        
        # Now do the initialization of the super class
        FigureCanvas.__init__(self, self.fig)
        #self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
         
class MatplotlibCanvas(FigureCanvas) :
    """ This is borrowed heavily from the matplotlib documentation;
        specifically, see:
        http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """
    def __init__(self):
        
        # Initialize the figure and axes
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        
        # Give it some default plot (if desired).  
       
        self.axes.plot(xprof, getycorrected(y1,y2))
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y(x)')   
        
        # Now do the initialization of the super class
        FigureCanvas.__init__(self, self.fig)
        #self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
         
        
    def redraw(self, x, y) :
        """ Redraw the figure with new x and y values.
        """
        # clear the old image (axes.hold is deprecated)
        self.axes.clear()
        self.axes.plot(x, y)
        self.draw()  

    def overlay(self, x, y, x2, y2) :
        """ Redraw the figure with new x and y values.
        """
        # clear the old image (axes.hold is deprecated)
        self.axes.clear()
        self.axes.plot(x, y, x2, y2)
        self.draw()      
       
app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()