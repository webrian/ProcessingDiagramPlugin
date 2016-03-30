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

class BarchartDiagramAlgorithm(DiagramAlgorithm):

    INPUT_VECTOR = 'INPUT_VECTOR'
    ID_FIELD = 'ID_FIELD'
    FIELDS = 'FIELDS'
    COLOR_SCHEMA = 'COLOR_SCHEMA'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'

    def defineCharacteristics(self):
        self.name = "Bar Charts"
        self.group = "Diagrams"
        
        self.addParameter(ParameterVector(self.INPUT_VECTOR, self.tr("Input")))
        self.addParameter(ParameterTableField(self.ID_FIELD, self.tr("Identifier field"), datatype=0))
        self.addParameter(ParameterString(self.FIELDS, self.tr("Fields comma separated"), default="Fishery__1,Fishery__2,Fishery__3,Fishery__4,Fishery__5,Fishery__6"))
        self.addParameter(ParameterSelection(self.COLOR_SCHEMA, self.tr("Color schema"), self.availableColorSchemas))
        self.addOutput(OutputDirectory(self.OUTPUT_DIRECTORY, self.tr("Store to directory")))


    def processAlgorithm(self, progress):
        layer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.INPUT_VECTOR))
        id_field = self.getParameterValue(self.ID_FIELD)
        # An array with fields
        fields = self.getParameterValue(self.FIELDS).split(',')
        colorSchemaIdx = self.getParameterValue(self.COLOR_SCHEMA)
        color_schema = self.availableColorSchemas[colorSchemaIdx]
        
        outputDir = self.getOutputValue(self.OUTPUT_DIRECTORY)

        # Get a list of used field indexes
        inputFields = layer.pendingFields()
        fieldIdxs = []
        for f in fields:
            idx = inputFields.indexFromName(f.strip())
            if idx == -1:
                raise GeoAlgorithmExecutionException('Field not found: %s' % f)
            fieldIdxs.append(idx)

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
            # Get all values as absolute numbers
            values = np.array([float(attrs[i]) for i in fieldIdxs])
            # Calc ratios for all values
            ratios = values / values.sum() * 100
            x = np.arange(ratios.size)

            # Get the correct color schema from the module
            cls = self.parseColorDefinition(color_schema, str(values.size)) 

            plt.axis('off')

            # Draw the pie chart with above values and colors
            bars = plt.bar(x, ratios, width=1.0, color=cls, edgecolor='w')

            plt.ylim(ymax=100.0)

            # Save the plot as figure to the specified directory
            plt.savefig("%s/barcharts_%s.svg" % (outputDir, id_field), format="svg", transparent=True, frameon=False)

            # Close the figure properly
            plt.close()
            # Set the progress in percentage
            progress.setPercentage(float(currentFeatureIdx / nbrFeatures) * 100.0)
            # Increase the index of the current feature
            currentFeatureIdx += 1
