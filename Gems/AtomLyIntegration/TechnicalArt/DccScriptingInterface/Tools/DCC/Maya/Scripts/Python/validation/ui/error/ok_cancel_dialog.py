#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------
"""! breif: a simple ok cancel dialog"""

# standard imports
import sys
from PySide2 import QtWidgets

from DccScriptingInterface.azpy.shared.common.core_utils import synthetic_property

# const
DCCSI_TAG = 'DCCsi'
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
class OkCancelMessageBox(QtWidgets.QMessageBox):

    def __init__(self, title=f'{DCCSI_TAG}: Message',
                 message='Are you sure you want to quit?',
                 init_ask=True,
                 parent=None,
                 stand_alone=None):

        super(OkCancelMessageBox, self).__init__()

        if parent is not None:
            parent = parent

        elif parent == None or stand_alone:
            stand_alone = True
            self.start()

        synthetic_property(self, '_title', title)
        synthetic_property(self, '_message', message)
        synthetic_property(self, '_response', None)

        if init_ask:
            self.prompt()

    def start(self):
        synthetic_property(self, 'app', QtWidgets.QApplication([]))
        self.app.setStyle('Plastique')
        return self.app

    def prompt(self):
        reply = self.question(self, self.get_title(),
                              self.get_message(),
                              self.Yes | self.No,
                              self.No)

        if reply == self.Yes:
            self._response = True
            return True
        else:
            self._response = False
            return False
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
if __name__ == '__main__':

    import DccScriptingInterface.azpy.test.entry_test
    DccScriptingInterface.azpy.test.entry_test.connect_wing()

    from shiboken2 import wrapInstance

    _maya_mainwindow = None
    try:
        from maya import OpenMayaUI as omui
        maya_mainwindow_ptr = omui.MQtUtil.mainWindow()
        _maya_mainwindow = wrapInstance(int(maya_mainwindow_ptr), QtWidgets.QWidget)
    except:
        _maya_mainwindow = None

    if _maya_mainwindow:
        response = OkCancelMessageBox(parent=_maya_mainwindow).get_response()
        print(response)

    else:
        response = OkCancelMessageBox(stand_alone=True).get_response()
        print(response)

    print('Finished...')
