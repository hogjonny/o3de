#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------
"""! TThis init allows us to treat Maya as a DCCsi tools python package

:file: DccScriptingInterface\\Tools\\DCC\\Maya\\Scripts\Python\Validation\ui\error\__init__.py
:Status: Prototype
:Version: 0.0.1
"""

# standard imports
import logging as _logging

from DccScriptingInterface.Tools.DCC.Maya.Scripts.Python.validation.ui import _PACKAGENAME
_PACKAGENAME = f'{_PACKAGENAME}.error'
_LOGGER = _logging.getLogger(_PACKAGENAME)

__all__ = ['message_box',
           'ok_cancel_dialog']
