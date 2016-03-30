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

from PyQt4.QtGui import *

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from processing.tools import system
#from diagram.SwissStyleAlgorithm import SwissStyleAlgorithm
from diagram.PiechartDiagramAlgorithm import PiechartDiagramAlgorithm
from diagram.DividedWingchartDiagramAlgorithm import DividedWingchartDiagramAlgorithm
from diagram.BarchartDiagramAlgorithm import BarchartDiagramAlgorithm
from diagram.DivergentBarchartDiagramAlgorithm import DivergentBarchartDiagramAlgorithm
from diagram.DividedBarchartDiagramAlgorithm import DividedBarchartDiagramAlgorithm

class DiagramAlgorithmProvider(AlgorithmProvider):

    alglist = []

    def __init__(self):
        AlgorithmProvider.__init__(self)

        # Activate provider by default
        self.activate = False

        # Load algorithms
        self.alglist = [
            PiechartDiagramAlgorithm(),
            DividedWingchartDiagramAlgorithm(),
            BarchartDiagramAlgorithm(),
            DivergentBarchartDiagramAlgorithm(),
            DividedBarchartDiagramAlgorithm(),
        ]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        """In this method we add settings needed to configure our
        provider.

        Do not forget to call the parent method, since it takes care
        or automatically adding a setting for activating or
        deactivating the algorithms in the provider.
        """
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        """Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded.
        """
        AlgorithmProvider.unload(self)

    def getName(self):
        """This is the name that will appear on the toolbox group.

        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'diagram'

    def getDescription(self):
        """This is the provired full name.
        """
        return 'Diagrams creation algorithms'

    def getIcon(self):
        """We return the default icon.
        """
        filepath = os.path.dirname(__file__) + "/logo.png"
        return QIcon(filepath)

    def _loadAlgorithms(self):
        """Here we fill the list of algorithms in self.algs.

        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here.

        In this case, since the list is always the same, we assign from
        the pre-made list. This assignment has to be done in this method
        even if the list does not change, since the self.algs list is
        cleared before calling this method.
        """
        self.algs = self.alglist
