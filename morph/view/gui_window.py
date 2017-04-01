# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.image as image
import matplotlib.pyplot as plt
import numpy as np
import morph.view.image_label as il
import morph.morpher


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.slider_value = 0.0
        self.image3 = None
        self.f_path = '../../'
        self.timer_id = -1
        self.setup_ui(self)

    def setup_ui(self, form):
        form.setObjectName("Form")
        form.resize(760, 591)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setObjectName("gridLayout")
        self.image_label1 = il.ImageLabel(form)
        self.image_label1.setText("")
        self.image_label1.setObjectName("image_label1")
        self.gridLayout.addWidget(self.image_label1, 0, 0, 1, 1)
        self.image_label2 = il.ImageLabel(form)
        self.image_label2.setText("")
        self.image_label2.setObjectName("image_label2")
        self.gridLayout.addWidget(self.image_label2, 0, 1, 1, 1)

        self.image_label1.set_twin(self.image_label2)
        self.image_label2.set_twin(self.image_label1)
        self.image_label1.release()
        self.image_label2.lock()

        self.image2_load_button = QtWidgets.QPushButton(form)
        self.image2_load_button.setToolTip("Load Image 2")
        self.image2_load_button.clicked.connect(self.on_click_button2)
        self.image2_load_button.setObjectName("image2_load_button")
        self.gridLayout.addWidget(self.image2_load_button, 1, 1, 1, 1)

        self.image1_load_button = QtWidgets.QPushButton(form)
        self.image1_load_button.setToolTip("Load Image 1")
        self.image1_load_button.clicked.connect(self.on_click_button1)
        self.image1_load_button.setObjectName("image1_load_button")
        self.gridLayout.addWidget(self.image1_load_button, 1, 0, 1, 1)

        self.image_label3 = QtWidgets.QLabel(form)
        self.image_label3.setText("")
        self.image_label3.setObjectName("image_label3")
        self.gridLayout.addWidget(self.image_label3, 7, 0, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.delete_button = QtWidgets.QPushButton(form)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setToolTip("Delete Last Entered Point")
        self.delete_button.clicked.connect(self.on_click_delete_button)
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.generate_button = QtWidgets.QPushButton(form)
        self.generate_button.setObjectName("generate_button")
        self.generate_button.setToolTip("Initiate Morph Generation")
        self.generate_button.clicked.connect(self.on_click_generate_button)
        self.horizontalLayout_2.addWidget(self.generate_button)
        self.slider = QtWidgets.QSlider(form)
        self.slider.setMaximum(500)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.slider.valueChanged.connect(self.on_value_changed_slider)
        self.horizontalLayout_2.addWidget(self.slider)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Image Morphing Tool"))
        self.image2_load_button.setText(_translate("Form", "Load Image"))
        self.image1_load_button.setText(_translate("Form", "Load Image"))
        self.delete_button.setText(_translate("Form", "Delete Last Point"))
        self.generate_button.setText(_translate("Form", "Generate"))

    def on_click_button2(self):
        file_name = self.get_filename("Open Image 2")
        if not file_name:
            return
        self.image_label1.delete_all()
        self.image_label2.delete_all()
        self.image_label2.setPixmap(QtGui.QPixmap(file_name))
        self.image2 = image.imread(file_name)
        self.resize_img()

    def on_click_button1(self):
        file_name = self.get_filename("Open Image 1")
        if not file_name:
            return
        self.image_label1.delete_all()
        self.image_label2.delete_all()
        self.image_label1.setPixmap(QtGui.QPixmap(file_name))
        self.image1 = image.imread(file_name)
        self.resize_img()

    def on_click_delete_button(self):
        if self.image_label1.is_locked():
            self.image_label1.delete()
            self.image_label1.release()
            self.image_label2.lock()
        else:
            self.image_label2.delete()
            self.image_label2.release()
            self.image_label1.lock()

    def on_click_generate_button(self):
        if self.image_label1.is_locked():
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Error",
                                  "Both images should have same number of points (more than 4 points)").exec_()
            return
        if len(self.image_label1.get_points()) < 4:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Error",
                                  "There should be more than 4 points selected in both images").exec_()
            return
        morph.morpher.set_data(self.image_label1.get_points(), self.image_label2.get_points(), self.image1, self.image2)
        self.on_value_changed_slider()

    def on_value_changed_slider(self):
        self.slider_value = self.slider.value()/500.0
        if self.timer_id != -1:
            self.killTimer(self.timer_id)
        self.timer_id = self.startTimer(300)

    def show_image3(self, img: np.ndarray):
        h, w, ch = img.shape
        fmt = QtGui.QImage.Format_RGB888
        if ch == 4:
            fmt = QtGui.QImage.Format_RGBA8888
        self.image_label3.setPixmap(QtGui.QPixmap(
            QtGui.QImage(img.data, w, h, w*ch, fmt)))

    def get_filename(self, title) -> str:
        fname = QtWidgets.QFileDialog.getOpenFileName(self, title, self.f_path, "JPEG Files (*.jpg);;PNG Files (*.png)")
        if fname[0]:
            self.f_path = fname[0]
            return fname[0]
        return ""

    def resize_img(self):
        pass

    def timerEvent(self, a0):
        self.killTimer(self.timer_id)
        self.timer_id = -1
        # heavy task
        self.morph_thread = MorphThread(self.slider_value)
        self.morph_thread.finish_signal.connect(self.show_image3)
        self.morph_thread.start()


class MorphThread(QtCore.QThread):

    finish_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, slider_value):
        QtCore.QThread.__init__(self)
        self.slider_value = slider_value

    def __del__(self):
        self.wait()

    def run(self):
        img = morph.morpher.pw_aff(self.slider_value)
        img = (255 * img.clip(0, 1)).round().astype(np.uint8)
        self.finish_signal.emit(img)

