# -*- coding: utf-8 -*-

"""
*************
*************
"""

__author__ = 'Adrian Weber'
__date__ = 'June 2015'
__copyright__ = '(C) 2015, Adrian Weber'

import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt4.QtGui import QIcon
from DiagramAlgorithm import DiagramAlgorithm
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.outputs import OutputDirectory
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.parameters import ParameterSelection
from processing.core.parameters import ParameterString
from processing.tools import dataobjects

class DividedWingchartDiagramAlgorithm(DiagramAlgorithm):

    INPUT_VECTOR = 'INPUT_VECTOR'
    ID_FIELD = 'ID_FIELD'
    LEFT_FIELDS = 'LEFT_FIELDS'
    RIGHT_FIELDS = 'RIGHT_FIELDS'
    COLOR_SCHEMA = 'COLOR_SCHEMA'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'

    def defineCharacteristics(self):
        self.name = "Divided Wing Charts"
        self.group = "Diagrams"
        
        self.addParameter(ParameterVector(self.INPUT_VECTOR, self.tr("Input")))
        self.addParameter(ParameterTableField(self.ID_FIELD, self.tr("Identifier field"), datatype=0))
        self.addParameter(ParameterString(self.LEFT_FIELDS, self.tr("Left fields comma separated"), default="Fishery__1,Fishery__2,Fishery__3"))
        self.addParameter(ParameterString(self.RIGHT_FIELDS, self.tr("Right fields comma separated"), default="Fishery__4,Fishery__5,Fishery__6"))
        self.addParameter(ParameterSelection(self.COLOR_SCHEMA, self.tr("Color schema"), self.availableColorSchemas))
        self.addOutput(OutputDirectory(self.OUTPUT_DIRECTORY, self.tr("Store to directory")))


    def processAlgorithm(self, progress):
        layer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.INPUT_VECTOR))
        id_field = self.getParameterValue(self.ID_FIELD)
        # An array with fields
        leftFields = self.getParameterValue(self.LEFT_FIELDS).split(',')
        rightFields = self.getParameterValue(self.RIGHT_FIELDS).split(',')
        colorSchemaIdx = self.getParameterValue(self.COLOR_SCHEMA)
        color_schema = self.availableColorSchemas[colorSchemaIdx]

        outputDir = self.getOutputValue(self.OUTPUT_DIRECTORY)

        # Get a list of used field indexes
        inputFields = layer.pendingFields()
        leftFieldIdxs = []
        for f in leftFields:
            idx = inputFields.indexFromName(f)
            if idx == -1:
                raise GeoAlgorithmExecutionException('Field not found: %s' % f)
            leftFieldIdxs.append(idx)

        rightFieldIdxs = []
        for f in rightFields:
            idx = inputFields.indexFromName(f)
            if idx == -1:
                raise GeoAlgorithmExecutionException("Field not found: %s" % f)
            rightFieldIdxs.append(idx)

        # The number of the left wings must be the same as the number of the
        # right fields
        if len(leftFieldIdxs) != len(rightFieldIdxs):
            raise GeoAlgorithmExecutionException("Different nbr of fields")
   
        # Get the attribute index of the identifier field
        identifierIdx = inputFields.indexFromName(id_field)

        # Get the total count of features, this is used to set the progress
        nbrFeatures = layer.featureCount()
        # 1-based index of current feature
        currentFeatureIdx = 1
        # Loop all features
        for feature in layer.getFeatures():
            # Get all attributes of the current feature
            attrs = feature.attributes()
            # Get the index as integer
            id_field = int(attrs[identifierIdx])

            # Setup a polar figure without labels
            plt.axes(polar=True)
            plt.axis('off')

            # Handle the left wings
            # First get all left values
            lvalues = np.array([float(attrs[i]) for i in leftFieldIdxs])
            # Get the colors from the INI file
            cls = self.parseColorDefinition(color_schema, str(lvalues.size))

            # Calc the angles per sector
            langles = np.array([(i / lvalues.sum()) * np.pi for i in lvalues])
            # Calc the start angles, start is at +PI/2
            la = np.pi/2
            ltheta = []
            for i in range(len(langles)):
                ltheta.append(la)
                la += langles[i]

            lradii = np.array([1.0 for i in ltheta])
            # Draw the left wings
            plt.bar(ltheta, lradii, width=langles, bottom=0.0, color=cls, edgecolor='w')


            # Handle the right wings
            # First get all right values
            rvalues = np.array([float(attrs[i]) for i in rightFieldIdxs])
            # Calc the right angles per sector
            rangles = np.array([(-1)*(i / rvalues.sum()) * np.pi for i in rvalues])
            # Calc the right start angles, start is at +PI/2
            ra = np.pi/2
            rtheta = []
            for i in range(len(rangles)):
                rtheta.append(ra)
                ra += rangles[i]

            rradii = np.array([0.8 for i in rtheta])
            # Draw the right wings
            plt.bar(rtheta, rradii, width=rangles, bottom=0.0, color=cls, edgecolor='w')

            # Save the plot as figure to the specified directory
            plt.savefig("%s/dividedwingcharts_%s.svg" % (outputDir, id_field), format="svg", transparent=True, frameon=False)

            plt.close()
            # Set the progress in percentage
            progress.setPercentage(float(currentFeatureIdx / nbrFeatures) * 100.0)
            # Increase the index of the current feature
            currentFeatureIdx += 1

    def getIcon(self):
        """
        Returns custom icon for divided wing charts algorithm
        """
        return QIcon(os.path.dirname(__file__) + "/images/dividedwingchart.png")
