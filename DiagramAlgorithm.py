# -*- coding: utf-8 -*-

__author__ = 'Adrian Weber'
__date__ = 'June 2015'
__copyright__ = '(C) 2015, Adrian Weber'

import os
from ConfigParser import ConfigParser
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.outputs import OutputDirectory
from processing.core.parameters import ParameterVector
from processing.tools import dataobjects

class DiagramAlgorithm(GeoAlgorithm):

    availableColorSchemas = []
    configParser = None

    def __init__(self):
        self.configParser = ConfigParser()
        self.configParser.read(os.path.dirname(__file__) + "/COLOR_SCHEMA.ini")
        self.availableColorSchemas = self.configParser.sections()
        GeoAlgorithm.__init__(self)

    def parseColorDefinition(self, section, nbr):
 
        # Parse values from ini file
        cs = self.configParser.get(section, nbr)
        # Initalize a list for colors
        colors = []
        # Divide the colors by 255.0
        # Colors as [r,g,b] whereas 0.0 <= r,g,b <= 1.0
        # see also http://matplotlib.org/api/colors_api.html
        rgb = []
        index = 1
        for c in cs.split(','):
            clc = c.lstrip('[').rstrip(']').lstrip(' "rgb(').rstrip(' )"')
            if index % 3 == 0:
                rgb.append((float(clc)/255.0))
                colors.append(rgb)
                rgb = []
            else:
                rgb.append((float(clc)/255.0))
                    
            index += 1

        return colors
