# bp_setupQtSettings.py
#
# Setup the settings .ini
#
# version: 1.0
# date: 05/7/2013
# authors: cVoellmann


from PySide import QtCore


# -------------------------------------------------------------------------
def bpm_setupQtSettings(windowName):
   """
   Sets up the settings .ini
   
   Returns a QSettings instance
   
   """

   settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "BpQtUiSettings", windowName)

   return settings