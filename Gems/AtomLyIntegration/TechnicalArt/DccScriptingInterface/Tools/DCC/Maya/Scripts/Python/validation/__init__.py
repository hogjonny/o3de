#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -------------------------------------------------------------------------
"""! An O3DE Maya Scene Validation Util

:file:
    <DCCsi>\\Tools\\DCC\\Maya\\Scripts\Python\Validation\__init__.py
:Status: Prototype
:Version: 0.0.1
"""

# standard imports
import logging as _logging

from DccScriptingInterface.Tools.DCC.Maya.Scripts.Python import _PACKAGENAME
_PACKAGENAME = f'{_PACKAGENAME}.validation'
_LOGGER = _logging.getLogger(_PACKAGENAME)

__all__ = ['validator', 'ui']
