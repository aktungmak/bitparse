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
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_3), self, self.logout.ledit.setFocus)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_4), self, self.editSt.ledit.setFocus)

        ## DEBUG #####
        self.dataIn.ledit.appendPlainText('FF FF 00 22 00 00 03 00 00 00 02 10 28 14 0A 01 01 01 00 0E 01 00 00 00 03 00 01 1F 40 0B B8 00 00 01')
        self.editSt.ledit.appendPlainText('''
timestamp {
    time_type 8 uimsbf
    if( time_type == 1 ) {
        UTC_seconds      32 uimsbf
        UTC_microseconds 16 uimsbf
    }
    if( time_type == 2 ) {
        hours   8 uimsbf
        minutes 8 uimsbf
        seconds 8 uimsbf
        frames  8 uimsbf
    }
    if( time_type == 3 ) {
        GPI_number 8 uimsbf
        GPI_edge   8 uimsbf
    }
}

multiple_operation_message {
    Reserved                16 uimsbf
    messageSize             16 uimsbf
    protocol_version        8  uimsbf
    AS_index                8  uimsbf
    message_number          8  uimsbf
    DPI_PID_index           16 uimsbf
    SCTE35_protocol_version 8  uimsbf
    timestamp()
    num_ops                 8  uimsbf
    for ( num_ops ) {
        opID                16 uimsbf
        data_length         16 uimsbf
        data       data_length stuff
    }
}

splice_null {}

splice_descriptor {
    splice_descriptor_tag   8  uimsbf
    descriptor_length       8  uimsbf
    identifier              32 uimsbf
    for( 8 ) {
        private_byte 8 uimsbf
    }
}

splice_info_section {
    table_id                 4*2 uimsbf
    section_syntax_indicator 1   bslbf
    private_indicator        1   bslbf
    reserved                 2   bslbf
    section_length           12  uimsbf
    protocol_version         8   uimsbf
    encrypted_packet         1   bslbf
    encryption_algorithm     6   uimsbf
    pts_adjustment           33  uimsbf
    cw_index                 8   uimsbf
    reserved                 12  bslbf
    splice_command_length    12  uimsbf
    splice_command_type      8   uimsbf
    if (splice_command_type == 0x00) {
        splice_null()
    }
    descriptor_loop_length   16  uimsbf
    for ( descriptor_loop_length ) {
        splice_descriptor()
    }
    if(encrypted_packet != 0) {
        E_CRC_32 32 rpchof
    }
    CRC_32 32 rpchof
}

main {
    multiple_operation_message()
}
        ''')
        ##############

    def initUI(self):

        self.dataIn = SubFrame('Data In')
        self.output = SubFrame('Output')
        self.logout = SubFrame('Log')
        self.editSt = SubFrame('Edit')

        self.frames = [self.dataIn, self.output, self.logout, self.editSt]
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
        self.resize(1000, 800)
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
                               self.editSt.ledit.toPlainText())

            self.output.ledit.setPlainText('')
            self.output.ledit.appendPlainText(output)
            if error:
                self.logout.ledit.appendPlainText(error)


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
