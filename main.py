import sys
import numpy as np
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
mpl.use('Qt5Agg')
mpl.rcParams.update({'font.size': 12})

class MPLGraph(QWidget):
    def __init__(self, parent=None):
        super(MPLGraph, self).__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the 'figure'
        self.canvas = FigureCanvas(self.figure)
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.lyt = QVBoxLayout()
        self.lyt.addWidget(self.toolbar)
        self.lyt.addWidget(self.canvas)
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.axes.set_title('3-D Graph')
        self.axes.set_xlabel('Energy')
        self.axes.set_ylabel('Alpha')
        #self.axes.set_zlabel('Security')
# Subclass MainWindow to customize application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Variables
        self.RawSensorData = 100000
        self.ReDuctionFactor = 10
        self.BlockSize = 10
        self.Transmission_Scalar = 2000
        self.C_Sensor = self.Transmission_Scalar/4
        self.C_Hash = self.C_Sensor/2
        self.D_HashRaw = 15

        ## Window Settings
        self.setWindowTitle("ECE 548 Project")
        self.setFixedSize(QSize(1600,1150))
        self.frame = QFrame(self)
        self.frame.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.setCentralWidget(self.frame)
        ### Defining the Layouts ###
        self.layout = QHBoxLayout()
        self.Params_layout = QFormLayout()
        self.Graph_layout = QWidget()
        self.frame.setLayout(self.layout)
        self.layout.addLayout(self.Params_layout)
        self.layout.addWidget(self.Graph_layout)
        ### Params ###
        self.RSD_Layout = QHBoxLayout()
        self.RSDslider = QSlider(Qt.Horizontal, self)
        self.RSDslider.setGeometry(30, 40, 100, 30)
        self.RSDslider.setTickPosition(QSlider.TicksBelow)
        self.RSDslider.setTickInterval(100000)
        self.RSDslider.setMaximum(1000000)
        self.RSDslider.setMinimum(0)
        self.RSDslider.valueChanged[int].connect(self.RSDchangeValue)
        self.RSDtext = QLabel(self)
        self.RSDtext.move(20, 20)
        self.RSDtext.resize(280, 40)
        self.RSDtext.setText("Raw Sensor Data:")
        self.RSDtext.setFont(QFont('Times font', 10))
        self.RSDspinbox = QSpinBox()
        self.RSDspinbox.setMaximum(1000000)
        self.RSDspinbox.setMinimum(0)
        self.RSDspinbox.valueChanged.connect(self.RSDchangeValue)
        self.RSDspinbox.setFont(QFont('Times font', 10))

        self.RDF_Layout = QHBoxLayout()
        self.RDFslider = QSlider(Qt.Horizontal, self)
        self.RDFslider.setGeometry(30, 40, 100, 30)
        self.RDFslider.setTickPosition(QSlider.TicksBelow)
        self.RDFslider.setTickInterval(10)
        self.RDFslider.setMaximum(50)
        self.RDFslider.setMinimum(1)
        self.RDFslider.valueChanged[int].connect(self.RDFchangeValue)
        self.RDFtext = QLabel(self)
        self.RDFtext.move(20, 20)
        self.RDFtext.resize(280, 40)
        self.RDFtext.setText("Reduction Factor:")
        self.RDFtext.setFont(QFont('Times font', 10))
        self.RDFspinbox = QSpinBox()
        self.RDFspinbox.setMaximum(50)
        self.RDFspinbox.setMinimum(1)
        self.RDFspinbox.valueChanged.connect(self.RDFchangeValue)
        self.RDFspinbox.setFont(QFont('Times font', 10))


        self.BS_Layout = QHBoxLayout()
        self.BSslider = QSlider(Qt.Horizontal, self)
        self.BSslider.setGeometry(30, 40, 100, 30)
        self.BSslider.setTickPosition(QSlider.TicksBelow)
        self.BSslider.setTickInterval(10)
        self.BSslider.setMaximum(50)
        self.BSslider.setMinimum(2)
        self.BSslider.valueChanged[int].connect(self.BSchangeValue)
        self.BStext = QLabel(self)
        self.BStext.move(20, 20)
        self.BStext.resize(280, 40)
        self.BStext.setText("Block Size:")
        self.BStext.setFont(QFont('Times font', 10))
        self.BSspinbox = QSpinBox()
        self.BSspinbox.setMaximum(50)
        self.BSspinbox.setMinimum(2)
        self.BSspinbox.valueChanged.connect(self.BSchangeValue)
        self.BSspinbox.setFont(QFont('Times font', 10))

        self.combobox_lyt = QHBoxLayout()
        self.RHD_combo_box_Text = QLabel(self)
        self.RHD_combo_box_Text.resize(280, 40)
        self.RHD_combo_box_Text.setText("Select A Hash")
        self.RHD_combo_box_Text.setFont(QFont('Times font', 10))
        self.RHD_combo_box = QComboBox(self)
        self.RHD_combo_box.clear()
        self.RHD_combo_box.addItem("--Select One--")
        self.RHD_combo_box.addItem("MD5")
        self.RHD_combo_box.addItem("SHA")
        self.RHD_combo_box.currentIndexChanged.connect(self.comboboxChanged)

        self.TS_Layout = QHBoxLayout()
        self.TSslider = QSlider(Qt.Horizontal, self)
        self.TSslider.setGeometry(30, 40, 100, 30)
        self.TSslider.setTickPosition(QSlider.TicksBelow)
        self.TSslider.setTickInterval(1000)
        self.TSslider.setMaximum(10000)
        self.TSslider.setMinimum(100)
        self.TSslider.valueChanged[int].connect(self.TSchangeValue)
        self.TStext = QLabel(self)
        self.TStext.move(20, 20)
        self.TStext.resize(280, 40)
        self.TStext.setText("Transmission Scalar:")
        self.TStext.setFont(QFont('Times font', 10))
        self.TSspinbox = QSpinBox()
        self.TSspinbox.setMaximum(10000)
        self.TSspinbox.setMinimum(100)
        self.TSspinbox.valueChanged.connect(self.TSchangeValue)
        self.TSspinbox.setFont(QFont('Times font', 10))

        self.Displayed_labels_lyt = QVBoxLayout()
        self.C_Sensor_Text = QLabel(self)
        self.C_Sensor_Text.move(20, 20)
        self.C_Sensor_Text.resize(280, 40)
        self.C_Sensor_Text.setText("Energy Scaler for Computation for Sensor: " + str(self.C_Sensor))
        self.C_Sensor_Text.setFont(QFont('Times font', 10))
        self.C_Hash_Text = QLabel(self)
        self.C_Hash_Text.move(20, 20)
        self.C_Hash_Text.resize(280, 40)
        self.C_Hash_Text.setText("Energy Scaler for Computation for Hash: " + str(self.C_Hash))
        self.C_Hash_Text.setFont(QFont('Times font', 10))


        # adding all elements
        self.RSD_Layout.addWidget(self.RSDslider)
        self.RSD_Layout.addWidget(self.RSDspinbox)
        self.Params_layout.addRow(self.RSDtext, self.RSD_Layout)

        self.RDF_Layout.addWidget(self.RDFslider)
        self.RDF_Layout.addWidget(self.RDFspinbox)
        self.Params_layout.addRow(self.RDFtext, self.RDF_Layout)

        self.BS_Layout.addWidget(self.BSslider)
        self.BS_Layout.addWidget(self.BSspinbox)
        self.Params_layout.addRow(self.BStext, self.BS_Layout)

        self.combobox_lyt.addWidget(self.RHD_combo_box)
        self.Params_layout.addRow(self.RHD_combo_box_Text,self.combobox_lyt)

        self.TS_Layout.addWidget(self.TSslider)
        self.TS_Layout.addWidget(self.TSspinbox)
        self.Params_layout.addRow(self.TStext, self.TS_Layout)

        self.Displayed_labels_lyt.addWidget(self.C_Sensor_Text)
        self.Displayed_labels_lyt.addWidget(self.C_Hash_Text)
        self.Params_layout.addRow(self.Displayed_labels_lyt)

        self.RunButton = QPushButton("Run")
        self.RunButton.setFont(QFont('Times font', 15))
        self.RunButton.setStyleSheet("background-color: Black;"
                                    "color: white;"
                                    "Margin-top: 20%")
        self.RunButton.clicked.connect(self.RunButtonClicked)
        self.Params_layout.addRow(self.RunButton)

        self.setDefault()


        self.sc1 = MPLGraph()
        self.Graph_layout.setLayout(self.sc1.lyt)


    def setDefault(self):
        self.RSDspinbox.setValue(self.RawSensorData)
        self.RDFspinbox.setValue(self.ReDuctionFactor)
        self.BSspinbox.setValue(self.BlockSize)
        self.TSspinbox.setValue(self.Transmission_Scalar)
    def RSDchangeValue(self,value):
        self.RawSensorData = value
        self.RSDspinbox.setValue(value)
        self.RSDslider.setValue(value)

    def RDFchangeValue(self,value):
        self.ReDuctionFactor = value
        self.RDFspinbox.setValue(value)
        self.RDFslider.setValue(value)

    def BSchangeValue(self,value):
        self.BlockSize = value
        self.BSspinbox.setValue(value)
        self.BSslider.setValue(value)

    def comboboxChanged(self):
        self.RHD_combo = self.RHD_combo_box.currentText()
        if self.RHD_combo == "MD5":
            self.D_HashRaw = 15
        else:
            self.D_HashRaw = 32

    def TSchangeValue(self,value):
        self.Transmission_Scalar = value
        self.C_Sensor = self.Transmission_Scalar / 4
        self.C_Sensor_Text.setText("Energy Scaler for Computation for Sensor: " + str(self.C_Sensor))
        self.C_Hash = self.C_Sensor / 2
        self.C_Hash_Text.setText("Energy Scaler for Computation for Hash: " + str(self.C_Hash))
        self.TSspinbox.setValue(value)
        self.TSslider.setValue(value)

    def RunButtonClicked(self):
        # Percent of Sensor Data Processed
        alpha_list = []
        # Total Energy
        E_list = []
        # Security
        S_list = []
        for i in np.linspace(0, 1, 100):
            # Calculating Sensor Data
            alpha = i
            alpha_list.append(alpha)
            D_SensorTransmit = alpha * (self.RawSensorData / self.ReDuctionFactor) + (1 - alpha) * self.RawSensorData
            B = int(math.ceil(D_SensorTransmit / self.BlockSize))
            # Calculating Data from Hash
            D_HashTransmit = B * self.D_HashRaw
            # Total Data
            D_TotalTransmit = D_SensorTransmit + D_HashTransmit
            # Transmission Energy Scaler
            E_Transmission = D_TotalTransmit * self.Transmission_Scalar
            # Energy For Sensor Computations
            E_SensorProcess = (alpha * self.RawSensorData) * self.C_Sensor
            # Energy for Hash Computations
            E_HashProcess = B * self.C_Hash
            # Total Energy
            E = E_HashProcess + E_SensorProcess + E_Transmission
            E_list.append(E)
            # Total Security
            # Secuirty factors for MD5 and SHA
            if self.D_HashRaw == 16:
                S_f = 2 ^ 128
            else:
                S_f = 2 ^ 256
            S = B * S_f
            S_list.append(S)
        self.sc1.axes.scatter(E_list,alpha_list,S_list,label=self.RHD_combo_box.currentText())
        self.sc1.axes.legend()
        '''
        if  self.RHD_combo_box.currentText() == "MD5":
            plt.figure()
        else:
            pass
        plt.scatter(E_list, alpha_list, c=S_list, marker = 'o', edgecolors='k',linewidth=.4)
        cbar = plt.colorbar()
        cbar.set_label("Security")
        plt.gray()
        plt.xlabel("Energy")
        plt.ylabel("Alpha")
        plt.title("SHA & MD5")
        plt.show()
        '''
def run():
    app = QApplication(sys.argv)
    # Create a Qt widget, which will be our window.
    window = MainWindow()
    window.setWindowIcon(QIcon('logo.png'))
    window.show()  # Important  Windows are hidden by default.

    # Start the event loop.
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()