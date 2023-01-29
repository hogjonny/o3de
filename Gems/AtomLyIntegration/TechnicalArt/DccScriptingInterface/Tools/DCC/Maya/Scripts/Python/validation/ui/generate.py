#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------
# standard imports
import os
from pathlib import Path
import logging as _logging
import xml.etree.ElementTree as xml
from io import StringIO

# PySide2
import PySide.QtGui as QtGui

from DccScriptingInterface.Tools.DCC.Maya.Scripts.Python.validation import _PACKAGENAME
_MODULENAME = f'{_PACKAGENAME}.generate'
_LOGGER = _logging.getLogger(_MODULENAME)
_LOGGER.info(f'Initializing: {_MODULENAME}')

try:
    import pysideuic
except ImportError as e:
    _LOGGER.error(f'Import failed: {e}')
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def generate_ui_classes(filepath):
    """! @brief: Parse .ui File and Return PySide2 Classes.

    Usage: from generate import generate_ui_classes
        form_class, base_class = generate_ui_classes(Path('c:\path\to\file'))
    """

    # resolves the full file path, fails if file doesn't exist
    ui_file = Path(filepath).resolve(strict=True)

    parsed = xml.parse(ui_file.as_posix())
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file.as_posix(), 'r') as ui_file:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(ui_file, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec(pyc in frame)

        # based on type in xml, retreive widget class and form
        form_class = frame['Ui_{0}'.format(form_class)]
        base_class = eval('QtGui.{0}'.format(widget_class))

    return form_class, base_class
