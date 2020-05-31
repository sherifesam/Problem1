from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from mainwindow import Ui_MainWindow
import sys
import plotly.express as px
import pandas as pd
import numpy as np
import os
import plotly as py

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Reading the excel sheet
        self.df = pd.read_excel('covid_data.xlsx')
        self.filePath=""
        # Push Buttons Handlers
        self.ui.map_button.clicked.connect(self.Map)
        self.ui.bar_button.clicked.connect(self.Bar)
        self.ui.bubble_button.clicked.connect(self.Bubble)
        # Creating an html file in case it doesnt exist
        f=open("url.html", "w") 
        f.close()

    # The Bubble Graph
    def Bubble(self):  
        fig= px.scatter(self.df, x="deaths", y="recovered", animation_frame="date", animation_group="country",size_max=55, log_x=True, log_y=True,
        size="cases", hover_name="country", range_x=[1,2500], range_y=[1,6500])
        py.io.write_html(fig, 'url.html')
        self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "url.html"))
        self.ui.widget.load(QUrl.fromLocalFile(self.filePath))

    # The Map Graph
    def Map(self):
        if(self.ui.comboBox_map.currentIndex()==0):
            fig = px.choropleth(self.df, locations="appreviation", animation_frame="date",
            color="deaths", range_color=[0,1500], 
            hover_name="country",color_continuous_scale='Inferno', projection="natural earth", width=1400, height= 720)
            py.io.write_html(fig, 'url.html')
            self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "url.html"))
            self.ui.widget.load(QUrl.fromLocalFile(self.filePath))

        elif(self.ui.comboBox_map.currentIndex()==1):
            fig = px.choropleth(self.df, locations="appreviation", animation_frame="date",
            color="cases", range_color=[0,35000], 
            hover_name="country",color_continuous_scale='Inferno', projection="natural earth", width=1400, height= 720)
            py.io.write_html(fig, 'url.html')
            self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "url.html"))
            self.ui.widget.load(QUrl.fromLocalFile(self.filePath))

    # The Sorted Bar Graph  
    def Bar(self):
        if(self.ui.comboBox_bar.currentIndex()==0):
            fig = px.bar(self.df, x="appreviation", y="deaths",
            animation_frame="date", animation_group="country", range_y=[1,2500], log_y=True )
            fig.update_layout(xaxis={'categoryorder' : 'total descending'})
            py.io.write_html(fig, 'url.html')
            self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "url.html"))
            self.ui.widget.load(QUrl.fromLocalFile(self.filePath))

        elif(self.ui.comboBox_bar.currentIndex()==1):
            fig = px.bar(self.df, x="appreviation", y="cases",
            animation_frame="date", animation_group="country", range_y=[1,35000], log_y=True )
            fig.update_layout(xaxis={'categoryorder' : 'total descending'})
            py.io.write_html(fig, 'url.html')
            self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "url.html"))
            self.ui.widget.load(QUrl.fromLocalFile(self.filePath))

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()