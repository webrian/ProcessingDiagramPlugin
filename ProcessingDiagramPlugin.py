# -*- coding: utf-8 -*-

"""
***************************************************************************
    __init__.py
    ---------------------
    Date                 : March 2016
    Copyright            : (C) 2016 by Adrian Weber
    Email                : webrian at gmx dot net
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Adrian Weber'
__date__ = 'March 2016'
__copyright__ = '(C) 2016, Adrian Weber'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from qgis.core import *

from processing.core.Processing import Processing
from diagram.DiagramAlgorithmProvider import DiagramAlgorithmProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class ProcessingDiagramPlugin:

    def __init__(self):
        self.provider = DiagramAlgorithmProvider()

    def initGui(self):
        Processing.addProvider(self.provider)

    def unload(self):
        Processing.removeProvider(self.provider)
