#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------

"""! @brief O3DE Maya Scene Validation Tool

This tool will check a scene for validation and help users repair,
to make a clean scene for export.

:file: DccScriptingInterface\\Tools\\DCC\\Maya\\scripts\\python\\validation\\validator.py
:Status: Prototype
:Version: 0.0.1
:Entrypoint: entrypoint, configures logging, includes cli
:Notice:
    Currently windows only (not tested on other platforms)
    Currently only tested with Wing Pro 8 in Windows
"""

# standard imports
import os
from pathlib import Path
from functools import partial

# pyside and Qt imports
from PySide2 import QtWidgets, QtCore, QtGui

# local imports
import DccScriptingInterface.azpy.shared.ui as azpyui
from DccScriptingInterface.azpy.shared.ui.puic_utils import from_ui_generate_form_and_base_class
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
GMAYA = None
try:
    # maya imports
    import maya.cmds as mc
    import maya.OpenMaya as om
    GMAYA = True
except:
    GMAYA = False

_main_window = None
if GMAYA:
    import maya.OpenMayaUI as omui
    _main_window = pm.language.melGlobals['gMainWindow']
# -------------------------------------------------------------------------

# ui file
validator_ui_file = Path(Path(__file__).parent, 'validator.ui')
#Loads the ui files into the form and base classes
form_class, base_class = from_ui_generate_form_and_base_class(validator_ui_file)

type_widget_ui_file = Path(Path(__file__).parent, 'validator_type_widget.ui')

type_widget_form_class, type_widget_base_class = from_ui_generate_form_and_base_class(type_widget_ui_file)
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# lists
FACE_TYPE_LIST = ["N_Sided", "Non_Planar", "Concave", "Holed",
                  "Lamina", "Non_Triangularable", "Un_Mapped",
                  "Zero_Geometry", "Zero_Map_Area"]

EDGE_TYPE_LIST = ["Non_Manifold", "Zero_Length"]

VERT_TYPE_LIST = ["Non_Manifold", ]
# -------------------------------------------------------------------------


###########################################################################
class TypeWidget(type_widget_base_class, type_widget_form_class):

    def __init__(self, parent=None):
        """Constructor"""
        super(TypeWidget, self).__init__(parent)
        #creates all the widgets from the .ui file
        self.setupUi(self)
# -------------------------------------------------------------------------


###########################################################################
class ValidatorWindow(base_class, form_class):
    """Maya Mesh validation tool, checks polygon components"""

    #----------------------------------------------------------------------
    def __init__(self, parent=ui.bpm_getMayaMainWindow()):
        """Constructor"""

        super(ValidatorWindow, self).__init__(parent)

        # check if window exists
        self.window_name = 'ValidatorWindow'
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name, window=True)

        #creates all the widgets from the .ui file
        self.setupUi(self)

        #Vars for all the check types and data instances
        self.face_types = FACE_TYPE_LIST
        self.face_data = {}

        self.edge_types = EDGE_TYPE_LIST
        self.edge_data = {}

        self.vert_types = VERT_TYPE_LIST
        self.vert_data = {}

        #polygon geometry objects
        self.poly_geom_objects = []

        #init type UI elements
        self.set_check_type_ui_elements()

        self.connect_interface()
        self.helpMenu = ui.SetupHelpMenu(self,
                                         'Validator Help...',
                                         'http://path/to/help')

        # show window in Maya
        mc.showWindow(self.window_name)

    #----------------------------------------------------------------------
    def connect_interface(self):
        """connects UI elements"""

        QtCore.QObject.connect(self.check_model_button,
                               QtCore.SIGNAL("clicked()"),
                               self.validate_poly_models)

    #----------------------------------------------------------------------
    def set_check_type_ui_elements(self):
        """sets up the UI types elements"""

        #per-category storage dictionaries
        self.face_widgets = {}
        self.edge_widgets = {}
        self.vert_widgets = {}

        #create face type widgets
        for this_type in self.face_types:
            self.face_widgets[this_type] = TypeWidget(self)
            self.face_widgets[this_type].componentLabel.setText(this_type)
            self.facesVLayout.addWidget(self.face_widgets[this_type])

            QtCore.QObject.connect(self.face_widgets[this_type].componentSelectButton,
                                   QtCore.SIGNAL("clicked()"),
                                   partial(self.select_validated_faces, this_type))

            QtCore.QObject.connect(self.face_widgets[this_type].objectSelectButton,
                                   QtCore.SIGNAL("clicked()"),
                                   partial(self.select_poly_objects, this_type))

        #create edge type widgets
        for this_type in self.edge_types:
            self.edge_widgets[this_type] = TypeWidget(self)
            self.edge_widgets[this_type].componentLabel.setText(this_type)
            self.edgesVLayout.addWidget(self.edge_widgets[this_type])

            QtCore.QObject.connect(self.edge_widgets[this_type].componentSelectButton,
                                   QtCore.SIGNAL("clicked()"),
                                   partial(self.select_validated_edges, this_type))

            QtCore.QObject.connect(self.edge_widgets[this_type].objectSelectButton,
                                   QtCore.SIGNAL("clicked()"),
                                   partial(self.select_poly_objects, this_type))

        #create vert type widgets
        for this_type in self.vert_types:
            self.vert_widgets[this_type] = TypeWidget(self)
            self.vert_widgets[this_type].componentLabel.setText(this_type)
            self.vertsVLayout.addWidget(self.vert_widgets[this_type])

            QtCore.QObject.connect(self.vert_widgets[this_type].componentSelectButton,
                                   QtCore.SIGNAL("clicked()"),
                                   partial(self.select_validated_verts, this_type))

            QtCore.QObject.connect(self.vert_widgets[this_type].objectSelectButton,
                                   QtCore.SIGNAL("clicked()"),
                                   partial(self.select_poly_objects, this_type))

    #------------------------------------------------------------------
    def validate_poly_models(self):

        #Clears any previous error messages
        print ''

        #Get the Poly Object List to check
        self.poly_geom_objects = self.get_poly_object_list()

        #Check face types
        for each_type in self.face_types:
            self.face_data[each_type] = CheckPolyFaces(self.poly_geom_objects, each_type)
            self.face_widgets[each_type].componentLineEdit.setText(str(self.face_data[each_type].count))

        #Check edge types
        for each_type in self.edge_types:
            self.edge_data[each_type] = CheckPolygonEdges(self.poly_geom_objects, each_type)
            self.edge_widgets[each_type].componentLineEdit.setText(str(self.edge_data[each_type].count))

        #Check vert types
        for each_type in self.vert_types:
            self.vert_data[each_type] = CheckPolygonVerts(self.poly_geom_objects, each_type)
            self.vert_widgets[each_type].componentLineEdit.setText(str(self.vert_data[each_type].count))

        mc.select(self.poly_geom_objects)

    #------------------------------------------------------------------
    def get_poly_object_list(self):
        """Returns list of selected polygon objects, or all"""

        if self.all_radio_button.isChecked() == True:
            #select all of the poly objects in the scene
            all_poly_objects = mc.ls(dag=True, noIntermediate=True, type='mesh')
            return all_poly_objects

        else:
            #List the Selected Poly Objects
            selected_poly_objects = mc.ls(selection=True, dag=True, noIntermediate=True, type='mesh')
            selection_size = len(selected_poly_objects)
            if selection_size == 0:
                azpyui.error.bp_mayaError("Please select a polygon object and run \'Check Model\' again!")
                mc.select(clear=True)
            else:
                return selected_poly_objects

    #------------------------------------------------------------------
    def select_validated_faces(self, face_type):

        try:
            mc.select(self.face_data[face_type].faces)
        except:
            pass

    #------------------------------------------------------------------
    def select_validated_edges(self, edge_type):

        try:
            mc.select(self.edge_data[edge_type].edges)
        except:
            pass

    #------------------------------------------------------------------
    def select_validated_verts(self, vert_type):

        try:
            mc.select(self.vert_data[vert_type].verts)
        except:
            pass

    #----------------------------------------------------------------------
    def select_poly_objects(self, component_type):

        try:
            if component_type in self.face_types:
                object_list = self.component_to_object(self.face_data[component_type].faces)
                mc.select(object_list)

            elif component_type in self.edge_types:
                object_list = self.component_to_object(self.edge_data[component_type].edges)
                mc.select(object_list)

            elif component_type in self.vert_types:
                object_list = self.component_to_object(self.vert_data[component_type].verts)
                mc.select(object_list)

        except:
            pass

    #----------------------------------------------------------------------
    def component_to_object(self, component_list):

        object_list = []

        for component in component_list:
            if "." in component:
                obj = component.split(".")[0]
                if obj not in object_list:
                    object_list.append(obj)

        return object_list
#--------------------------------------------------------------------------


POLY_FLAGS_DICT = {"N_Sided": 'size',
                   "Non_Planar": 'planarity',
                   "Concave": 'convexity',
                   "Holed": 'holes',
                   "Lamina": 'topology',
                   "Non_Triangularable": 'topology',
                   "Un_Mapped": 'textured',
                   "Zero_Geometry": 'geometricarea',
                   "Zero_Map_Area": 'texturedarea'}

VALUE_DICT = {"N_Sided": 3,
              "Non_Planar": 1,
              "Concave": 1,
              "Holed": 1,
              "Lamina": 2,
              "Non_Triangularable": 1,
              "Un_Mapped": 2,
              "Zero_Geometry": 1,
              "Zero_Map_Area": 1}

###########################################################################


class CheckPolyFaces(object):
    '''Checks polygon faces for problems using Maya's polySelectConstraints command'''

    def __init__(self, polygon_object_list, check_type):
        self.polygon_object_list = polygon_object_list
        self.check_type = check_type
        self.size = 0
        self.planarity = 0
        self.convexity = 0
        self.holes = 0
        self.topology = 0
        self.textured = 0
        self.geometricarea = 0
        self.texturedarea = 0
        self.poly_flags = POLY_FLAGS_DICT
        self.values = VALUE_DICT

        setattr(self, self.poly_flags[self.check_type], self.values[self.check_type])

    #Get the faces using poly constraints
    def __get_faces(self):
        if self.check_type == "Zero_Map_Area": # Fix for multiple UV sets
            faces = []
            for each_object in self.polygon_object_list:
                mc.select(each_object)
                uv_set_list = mc.polyUVSet(query=True, allUVSets=True)
                current_set = mc.polyUVSet(query=True, currentUVSet=True)[0]
                for uv_set in uv_set_list:
                    mc.polyUVSet(currentUVSet=True, uvSet=uv_set)
                    mc.polySelectConstraint(mode=3,
                                            disable=1,
                                            type=8,
                                            size=self.size,
                                            planarity=self.planarity,
                                            convexity=self.convexity,
                                            holes=self.holes,
                                            topology=self.topology,
                                            textured=self.textured,
                                            geometricarea=self.geometricarea,
                                            geometricareabound=[0, 0.000001],
                                            texturedarea=self.texturedarea,
                                            texturedareabound=[0, 0.0000000000000001])
                    current_faces = (mc.ls(selection=True, flatten=True))
                    for face in current_faces:
                        faces.append(face)
                mc.polyUVSet(currentUVSet=True, uvSet=current_set)
                faces = list(set(faces)) #remove duplicates

        else:
            mc.select(self.polygon_object_list)
            mc.polySelectConstraint(mode=3,
                                    disable=1,
                                    type=8,
                                    size=self.size,
                                    planarity=self.planarity,
                                    convexity=self.convexity,
                                    holes=self.holes,
                                    topology=self.topology,
                                    textured=self.textured,
                                    geometricarea=self.geometricarea,
                                    geometricareabound=[0, 0.000001],
                                    texturedarea=self.texturedarea,
                                    texturedareabound=[0, 0.0000000000000001])
            faces = mc.ls(selection=True, flatten=True)

        mc.select(clear=True)
        mc.polySelectConstraint(mode=0)
        return faces

    face_list = property(__get_faces)

    def __get_face_count(self):
        count = len(self.face_list)
        return count

    count = property(__get_face_count)
#--------------------------------------------------------------------------


###########################################################################
class CheckPolygonEdges(object):
    '''Check Polygon edges using multiple Maya commands'''

    def __init__(self, polygon_object_list, check_type):
        self.polygon_object_list = polygon_object_list
        self.check_type = check_type

    def __check_edges(self):
        if self.check_type == "Non_Manifold":
            mc.select(self.polygon_object_list)
            mc.selectType(polymeshFace=True)
            edges = mc.polyInfo(nonManifoldEdges=True)
            mc.select(edges)
            edges = mc.ls(selection=True, flatten=True)
            mc.select(clear=True)
            return edges

        if self.check_type == "Zero_Length":
            mc.select(self.polygon_object_list)
            mc.polySelectConstraint(mode=3,
                                    disable=1,
                                    type=0x8000,
                                    length=True,
                                    lengthbound=[0, 0.001])
            edges = mc.ls(selection=True, flatten=True)
            mc.polySelectConstraint(mode=0)
            mc.select(clear=True)
            return edges

    edge_list = property(__check_edges)

    def __get_edge_count(self):
        if self.edge_list != None:
            count = len(self.edge_list)
        else:
            count = 0

        return count

    count = property(__get_edge_count)
#--------------------------------------------------------------------------


###########################################################################
class CheckPolygonVerts(object):
    '''Check polygon vertices using multiple Maya commands'''

    def __init__(self, polygon_object_list, check_type):
        self.polygon_object_list = polygon_object_list
        self.check_type = check_type

    def __check_verts(self):
        if self.check_type == "Non_Manifold":
            mc.select(self.polygon_object_list)
            mc.selectType(polymeshVertex=True)
            vertices = mc.polyInfo(nonManifoldVertices=True)
            mc.select(vertices)
            vertices = mc.ls(selection=True, flatten=True)
            mc.select(clear=True)
            return vertices

    verts_list = property(__check_verts)

    def __get_vertex_count(self):
        if self.verts_list != None:
            count = len(self.verts_list)
        else:
            count = 0
        return count

    count = property(__get_vertex_count)
#--------------------------------------------------------------------------


###########################################################################
def main():
    """starts the UI"""
    global polyCheckerWindow
    polyCheckerWindow = ValidatorWindow()
