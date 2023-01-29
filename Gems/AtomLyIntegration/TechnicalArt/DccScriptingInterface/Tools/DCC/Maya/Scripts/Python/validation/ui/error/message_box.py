#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------
"""! breif: a generic message box"""

# standard imports
import sys
from PySide2 import QtWidgets

# const
DCCSI_TAG = 'DCCsi'

# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
def message_box(message_text,
                message_type='warning',
                info_text=None,
                detail_text=None,
                parent=None,
                wait=None,
                stand_alone=None):
    """creates a custom Qt messageBox.
    Message types: warning, error, info, question, and message
    """

    if parent is not None:
        parent = parent

    elif parent == None or stand_alone:
        stand_alone = True
        sa_app = QtWidgets.QApplication([])
        sa_app.setStyle('Plastique')
        #parent = sa_app

    # create the message box
    message_box = QtWidgets.QMessageBox(parent=parent)

    # Message type
    if message_type == 'warning':
        message_box.setWindowTitle(f'{DCCSI_TAG}: Warning')
        #messageBox.setIcon(2)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)

    elif message_type == 'error':
        message_box.setWindowTitle(f'{DCCSI_TAG}:Error')
        #messageBox.setIcon(3)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)

    elif message_type == 'info':
        message_box.setWindowTitle(f'{DCCSI_TAG}: Information')
        #messageBox.setIcon(1)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)

    elif message_type == 'question':
        message_box.setWindowTitle(f'{DCCSI_TAG}: Question')
        #messageBox.setIcon(4)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Question)

    else:
        message_box.setWindowTitle(f'{DCCSI_TAG}: Message')
        #messageBox.setIcon(0)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.NoIcon)

    # set the main message text
    message_box.setText(message_text)

    # set the info text
    if info_text != None:
        message_box.setInformativeText(info_text)

    # set the detail text
    if detail_text != None:
        message_box.setDetailedText(detail_text)

    # show the window
    message_box.show()

    if wait is True:
        ret = message_box.exec_()

    if stand_alone:
        sys.exit(sa_app.exec_())

    return
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
if __name__ == "__main__":

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

    message = 'Get down with some GobbleDeGook'

    if _maya_mainwindow:
        mb = message_box(message_text=message, parent=_maya_mainwindow)
    else:
        mb = message_box(message_text=message, wait=True, stand_alone=True)

    # if wait = True, this should not print until the dialog ok is pressed
    print('Finished...')
