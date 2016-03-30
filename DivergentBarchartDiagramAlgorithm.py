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

class DivergentBarchartDiagramAlgorithm(DiagramAlgorithm):

    INPUT_VECTOR = 'INPUT_VECTOR'
    ID_FIELD = 'ID_FIELD'
    LEFT_FIELDS = 'LEFT_FIELDS'
    RIGHT_FIELDS = 'RIGHT_FIELDS'
    COLOR_SCHEMA = 'COLOR_SCHEMA'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'

    def defineCharacteristics(self):
        self.name = "Divergent Bar Charts"
        self.group = "Diagrams"
        
        self.addParameter(ParameterVector(self.INPUT_VECTOR, self.tr("Input")))
        self.addParameter(ParameterTableField(self.ID_FIELD, self.tr("Identifier field"), datatype=0))
        self.addParameter(ParameterString(self.LEFT_FIELDS, self.tr("Left fields comma separated"), default="Fishery__1,Fishery__2,Fishery__3,Fishery__4"))
        self.addParameter(ParameterString(self.RIGHT_FIELDS, self.tr("Right fields comma separated"), default="Fishery__4,Fishery__5,Fishery__6,Fishery__1"))
        self.addParameter(ParameterSelection(self.COLOR_SCHEMA, self.tr("Color schema"), self.availableColorSchemas))
        self.addOutput(OutputDirectory(self.OUTPUT_DIRECTORY, self.tr("Output directory")))


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
            idx = inputFields.indexFromName(f.strip())
            if idx == -1:
                raise GeoAlgorithmExecutionException('Field not found: %s' % f)
            leftFieldIdxs.append(idx)

        rightFieldIdxs = []
        for f in rightFields:
            idx = inputFields.indexFromName(f.strip())
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
            plt.axis('off')

            # Handle the left bars
            # First get all left values
            lvalues = np.array([float(attrs[i]) for i in leftFieldIdxs])
            # Calc ratios
            lratios = lvalues / lvalues.sum() * 100
            # Draw the left bars
            lbars = plt.barh(np.arange(lratios.size), (-1)*lratios, height=1.0, color='g', edgecolor='w')


            # Handle the right bars
            # First get all right values
            rvalues = np.array([float(attrs[i]) for i in rightFieldIdxs])
            # Calc ratios
            rratios = rvalues / rvalues.sum() * 100
            # Draw the right bars
            rbars = plt.barh(np.arange(rratios.size), rratios, height=1.0, color='r', edgecolor='w')

            # Set the x system from -100 to 100
            plt.xlim(xmax=100.0)
            plt.xlim(xmin=-100.0)

            # Save the plot as figure to the specified directory
            plt.savefig("%s/divergentbarcharts_%s.svg" % (outputDir, id_field), format="svg", transparent=True, frameon=False)

            plt.close()
            # Set the progress in percentage
            progress.setPercentage(float(currentFeatureIdx / nbrFeatures) * 100.0)
            # Increase the index of the current feature
            currentFeatureIdx += 1
