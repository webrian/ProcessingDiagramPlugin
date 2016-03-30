# -*- coding: utf-8 -*-

"""
*************
*************
"""

__author__ = 'Adrian Weber'
__date__ = 'June 2015'
__copyright__ = '(C) 2015, Adrian Weber'

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.outputs import OutputDirectory
from processing.core.parameters import ParameterVector
from processing.tools import dataobjects

class DivergentBarchartDiagramAlgorithm(GeoAlgorithm):

    INPUT_VECTOR = 'INPUT_VECTOR'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'

    def defineCharacteristics(self):
        self.name = "Divergent Bar Charts"
        self.group = "Diagrams"
        
        self.addParameter(ParameterVector(self.INPUT_VECTOR, self.tr("Data layer")))

        self.addOutput(OutputDirectory(self.OUTPUT_DIRECTORY, self.tr("Output directory")))


    def processAlgorithm(self, progress):
        layer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.INPUT_VECTOR))

        print layer

        outputDir = self.getOutputValue(self.OUTPUT_DIRECTORY)
        
        f = open("%s/test.txt" % outputDir, 'w')
        f.write("htellsdaldskjf")
        f.close()
