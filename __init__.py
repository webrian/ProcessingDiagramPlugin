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

def classFactory(iface):
    from diagram.ProcessingDiagramPlugin import ProcessingDiagramPlugin
    return ProcessingDiagramPlugin()
