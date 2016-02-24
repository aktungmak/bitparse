import sys
from PySide import QtGui, QtCore

class MainView(QtGui.QWidget):

    def __init__(self):
        super(MainView, self).__init__()
        self.initUI()

        self.editCallbacks = []

        self.dataIn.ledit.textChanged.connect(self.processCallbacks)
        self.editSt.ledit.textChanged.connect(self.processCallbacks)

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R), self, self.rotate)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_1), self, self.dataIn.ledit.setFocus)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_2), self, self.output.ledit.setFocus)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_3), self, self.errors.ledit.setFocus)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_4), self, self.editSt.ledit.setFocus)

    def initUI(self):

        self.dataIn = SubFrame('Data In')
        self.output = SubFrame('Output')
        self.errors = SubFrame('Errors')
        self.editSt = SubFrame('Edit')

        self.frames = [self.dataIn, self.output, self.errors, self.editSt]
        self.locs = [(0, 1, 1, 1),
                     (1, 1, 1, 1),
                     (2, 1, 1, 1),
                     (0, 0, 3, 1)]

        self.gridLayout = QtGui.QGridLayout()

        self.gridLayout.setSpacing(0)
        for frame, loc in zip(self.frames, self.locs):
            self.gridLayout.addWidget(frame, *loc)

        self.setLayout(self.gridLayout)

        self.move(300, 150)
        self.setWindowTitle('RE_SPEC')
        self.show()

    def rotate(self):
        while self.gridLayout.count():
            self.gridLayout.takeAt(0)
        self.frames.insert(0 , self.frames.pop())
        for frame, loc in zip(self.frames, self.locs):
            self.gridLayout.addWidget(frame, *loc)

    def registerCallback(self, callback):
        self.editCallbacks.append(callback)

    def processCallbacks(self):
        for cb in self.editCallbacks:
            output, error = cb(self.dataIn.ledit.toPlainText(),
                               self.dataIn.ledit.toPlainText())

            self.output.ledit.appendPlainText(output)
            if error:
                self.errors.ledit.appendPlainText(error)


class SubFrame(QtGui.QWidget):
    def __init__(self, name):
        super(SubFrame, self).__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        layo = QtGui.QVBoxLayout()

        self.label = QtGui.QLabel(self.name)
        self.ledit = QtGui.QPlainTextEdit()

        self.label.setFont(QtGui.QFont("Fixedsys"))
        self.ledit.setFont(QtGui.QFont("Fixedsys"))

        layo.addWidget(self.label)
        layo.addWidget(self.ledit)

        self.setLayout(layo)

        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = MainView()
    sys.exit(app.exec_())
