#----------------------------------------------------------------------
#bp_setupHelpMenu.py
#Standard Help menu setup for bpTools GUIs
#Version 1.0
#Created 7/5/2011
#Author: Chris Voellmann, edits: hogjonny
#----------------------------------------------------------------------

# modules
#from PyQt4 import QtGui, QtCore        # deprecated, now using PySide
from PySide import QtGui, QtCore

global gMaya
from bp_config.mayaConfig.mayaConfig import gMaya
if gMaya:
	import maya.cmds as mc

########################################################################
class SetupHelpMenu():
	"""
	This sets up the Standard Help menu for bpTools GUIs.
	
	INPUTS:
	mainWindow = the class instance of the QMainWindow
	toolLabel = the menu label for the tool's help item
	toolHelpPage = the http;// path to the specific bpTool help page
	
	Here's an example which is run from the init of the Animation Exporter GUI:
	#self.helpMenu = bpui.SetupHelpMenu(self, 'Scene Annotation Help...', 'https://sites.google.com/a/bluepointgames.com/maya-tools/home/file/scene-annotation')
	
	"""

	#----------------------------------------------------------------------
	def __init__(self, mainWindow, toolLabel, toolHelpPage):
		"""Constructor"""
		
		self.mainWindow = mainWindow
		self.menubar = self.mainWindow.menuBar()
		self.toolLabel = toolLabel
		self.toolHelpPage = toolHelpPage
		
		self.menuHelp = QtGui.QMenu(self.menubar)
		self.menuHelp.setObjectName("menuHelp")
		self.menuHelp.setTitle("Help")
		
		self.setupSpecificToolHelp()
		self.setupGenericToolHelp()
		self.setupReportToolBug()
		
		
	#----------------------------------------------------------------------
	def setupSpecificToolHelp(self):
		""""""
		self.actionTool_Help = QtGui.QAction(self.mainWindow)
		self.actionTool_Help.setObjectName("actionTool_Help")
		self.menuHelp.addAction(self.actionTool_Help)
		self.menubar.addAction(self.menuHelp.menuAction())
		self.actionTool_Help.setText(self.toolLabel)
		self.mainWindow.connect(self.actionTool_Help,  QtCore.SIGNAL("triggered()"), self.displayToolHelp)
	
	#----------------------------------------------------------------------
	def setupGenericToolHelp(self):
		""""""
		self.actionBpTools_Help = QtGui.QAction(self.mainWindow)
		self.actionBpTools_Help.setObjectName("actionBpTools_Help")
		self.menuHelp.addAction(self.actionBpTools_Help)
		self.menubar.addAction(self.menuHelp.menuAction())
		self.actionBpTools_Help.setText("bpTools Help...")
		self.mainWindow.connect(self.actionBpTools_Help,  QtCore.SIGNAL("triggered()"), self.displayBpToolsHelp)
		
	#----------------------------------------------------------------------
	def setupReportToolBug(self):
		""""""
		self.actionReportTool_Bug = QtGui.QAction(self.mainWindow)
		self.actionReportTool_Bug.setObjectName("actionReportTool_Bug")
		self.menuHelp.addAction(self.actionReportTool_Bug)
		self.menubar.addAction(self.menuHelp.menuAction())
		self.actionReportTool_Bug.setText("Report a Tool Bug...")
		self.mainWindow.connect(self.actionReportTool_Bug,  QtCore.SIGNAL("triggered()"), self.displayBugReport)
		
		
	#----------------------------------------------------------------------
	def displayToolHelp(self):
		""""""
		if gMaya:
			mc.showHelp(self.toolHelpPage, absolute = True)
		else:
			print 'This command, {0}: only works when running in Maya.'.format('displayToolHelp')
		pass
		
	#----------------------------------------------------------------------
	def displayBpToolsHelp(self):
		""""""
		#link to BP docs
		if gMaya:
			mc.showHelp('https://sites.google.com/a/bluepointgames.com/maya-tools/', absolute = True)
		else:
			print 'This command, {0}: only works when running in Maya.'.format('displayBpToolsHelp')
		pass		
		
	#----------------------------------------------------------------------
	def displayBugReport(self):
		""""""
		if gMaya:
			mc.showHelp('http://bp-jiracp6-vm:8080/secure/Dashboard.jspa', absolute = True)
		else:
			print 'This command, {0}: only works when running in Maya.'.format('displayBugReport')
		pass
		
	
		
		
		
		
    
	