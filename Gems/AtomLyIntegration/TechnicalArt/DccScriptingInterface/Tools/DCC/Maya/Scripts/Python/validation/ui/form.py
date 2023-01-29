#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------
# standard imports
import sys
from pathlib import Path

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit
from PySide2.QtCore import QFile, QObject


class Form(QObject):

    def __init__(self, ui_file, parent=None):

        super(Form, self).__init__(parent)

        self.ui_file = QFile(ui_file)
        self.ui_file.open(QFile.ReadOnly)

        self.ui = QUiLoader().load(ui_file)
        self.ui_file.close()

        #self.line = self.window.findChild(QLineEdit, 'lineEdit')
        #btn = self.window.findChild(QPushButton, 'pushButton')
        #btn.clicked.connect(self.ok_handler)

        self.window.show()

    def ok_handler(self):

        #language = 'None' if not self.line.text() else self.line.text()

        language = 'Python'

        print(f'Favorite language: {language}')


if __name__ == '__main__':

    import DccScriptingInterface.azpy.test.entry_test
    DccScriptingInterface.azpy.test.entry_test.connect_wing()

    app = QApplication(sys.argv)

    form = Form('validator.ui')

    sys.exit(app.exec_())
