# Copyright 2020 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from PySide2 import QtCore, QtGui, QtWidgets
import ctypes
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySide2 High DPI example')
        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)   
        self._layout = QtWidgets.QVBoxLayout(self._central_widget)
        r = QtWidgets.QApplication.desktop().devicePixelRatio()
        self._label1 = QtWidgets.QLabel(f'devicePixelRatio = {r}', self._central_widget)
        self._layout.addWidget(self._label1)
        self._buttons = [
            self._add_buttons(size=None),
            self._add_buttons(size=(32, 32)),
            self._add_buttons(size=(64, 64)),
        ]
            
    def _add_buttons(self, size=None):
        w = QtWidgets.QWidget(self._central_widget)
        layout = QtWidgets.QHBoxLayout(w)
        label = QtWidgets.QLabel(str(size), w)
        layout.addWidget(label)
        w1 = self._add_button_using_addfile(w, size)
        w2 = self._add_button_using_pixmap(w, size)
        spacer = QtWidgets.QSpacerItem(40, 20,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Minimum)
        layout.addItem(spacer)
        self._layout.addWidget(w)
        return [w, label, spacer] + w1 + w2
    
    def _add_button_using_addfile(self, parent, size=None):
        # Use separate images and Icon.addFile
        button = QtWidgets.QPushButton(parent)
        icon = QtGui.QIcon()
        icon.addFile('./resources/zoom_in_32x32.png')
        icon.addFile('./resources/zoom_in_32x32@2x.png')
        icon.addFile('./resources/zoom_in_64x64.png')
        icon.addFile('./resources/zoom_in_64x64@2x.png')
        button.setIcon(icon)
        if size is not None:
            button.setIconSize(QtCore.QSize(*size))
        parent.layout().addWidget(button)
        return [button, icon]
        
    def _add_button_using_pixmap(self, parent, size=None):
        # Use a single high-res image, Pixmap and scaling
        button = QtWidgets.QPushButton(self._central_widget)
        icon = QtGui.QIcon()
        pixmap = QtGui.QPixmap('./resources/zoom_in_64x64@2x.png')
        icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        if size is not None:
            button.setIconSize(QtCore.QSize(*size))
        parent.layout().addWidget(button)
        return [button, icon, pixmap]


if __name__ == '__main__':
    # http://doc.qt.io/qt-5/highdpi.html
    # https://vicrucann.github.io/tutorials/osg-qt-high-dpi/
    if sys.platform.startswith('win'):
       ctypes.windll.user32.SetProcessDPIAware()
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    app.exec_()
