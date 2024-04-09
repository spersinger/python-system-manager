import os
import sys
import psutil
from PyQt5 import QtChart
from PyQt5.QtChart import QChart, QPieSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from taskman_ui import Ui_MainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.ram_pie_chart_series = QPieSeries()
        self.ram_pie_chart = QChart()
        self.cpu_pie_chart_series = QPieSeries()
        self.cpu_pie_chart = QChart()
        self.gpu_pie_chart_series = QPieSeries()
        self.gpu_pie_chart = QChart()

        self.setWindowTitle("System Manager")
        self.init_ui()

    def init_ui(self):
        self.CPU_Graph.setRange(0, 100)
        self.RAM_graph.setRange(0, 100)
        self.GPU_graph.setRange(0, 100)
        self.GPU_graph.setValue(0)
        self.CPU_Graph.hide()
        self.RAM_graph.hide()
        self.GPU_graph.hide()

        self.ram_pie_chart.addSeries(self.ram_pie_chart_series)
        self.cpu_pie_chart.addSeries(self.cpu_pie_chart_series)
        self.gpu_pie_chart.addSeries(self.gpu_pie_chart_series)

        self.ramPieChart.setChart(self.ram_pie_chart)
        self.cpuPieGraph.setChart(self.cpu_pie_chart)
        self.gpuPieChart.setChart(self.gpu_pie_chart)
        self.viewTypeDropdown.view().pressed.connect(self.handle_view_type_dropdown_clicked)
        self.ram_pie_chart.setTitle("RAM Usage")
        self.cpu_pie_chart.setTitle("CPU Usage")
        self.gpu_pie_chart.setTitle("GPU Usage")

        self.ramPieChart.setRenderHint(QPainter.Antialiasing)
        self.cpuPieGraph.setRenderHint(QPainter.Antialiasing)
        self.gpuPieChart.setRenderHint(QPainter.Antialiasing)

        self.cpu_pie_chart_series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
        self.ram_pie_chart_series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
        self.gpu_pie_chart_series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)

        self.ram_pie_chart_series.append("Used", int(0))
        self.ram_pie_chart_series.append("Unused", 100-int(0))

        self.cpu_pie_chart_series.append("Used", int(0))
        self.cpu_pie_chart_series.append("Unused", 100-int(0))

        self.gpu_pie_chart_series.append("Used", int(0))
        self.gpu_pie_chart_series.append("Unused", 100-int(0))

        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget_3.setCurrentIndex(1)

        self.timer.timeout.connect(self.update_ui)  # Connect the timeout signal to your update_ui function

        # Start the timer with a 500 ms interval
        self.timer.start(1000)

        self.show()
        self.update_ui()

    def update_ui(self):
        QApplication.processEvents()
        mem = psutil.virtual_memory()
        cpu_usage = psutil.cpu_percent(interval=None)

        if self.viewTypeDropdown.currentText() == "Pie Graph":
            self.update_graph(mem, cpu_usage)
        elif self.viewTypeDropdown.currentText() == "Percent Line":
            self.RAM_graph.setValue(int(mem.percent))
            self.CPU_Graph.setValue(int(cpu_usage))
        else:
            print("Nothign")

    def handle_view_type_dropdown_clicked(self, index):
        item = self.viewTypeDropdown.model().itemFromIndex(index)
        if item.text() == "Pie Graph":
            self.CPU_Graph.hide()
            self.RAM_graph.hide()
            self.GPU_graph.hide()
            self.ramPieChart.show()
            self.cpuPieGraph.show()
            self.gpuPieChart.show()
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_2.setCurrentIndex(1)
            self.stackedWidget_3.setCurrentIndex(1)
        elif item.text() == "Percent Line":
            self.ramPieChart.hide()
            self.cpuPieGraph.hide()
            self.gpuPieChart.hide()
            self.CPU_Graph.show()
            self.RAM_graph.show()
            self.GPU_graph.show()
            self.stackedWidget.setCurrentIndex(0)
            self.stackedWidget_2.setCurrentIndex(0)
            self.stackedWidget_3.setCurrentIndex(0)
        elif item.text() == "Line Graph":
            print("Line Graph")
        else:
            print("Invalid View Type")
        self.update_ui()

    def update_graph(self, mem, cpu_usage):
        self.ram_pie_chart_series.slices()[0].setValue(int(mem.percent))
        self.ram_pie_chart_series.slices()[1].setValue(100-int(mem.percent))

        self.cpu_pie_chart_series.slices()[0].setValue(int(cpu_usage))
        self.cpu_pie_chart_series.slices()[1].setValue(100-int(cpu_usage))

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
