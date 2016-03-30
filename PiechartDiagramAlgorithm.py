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

class PiechartDiagramAlgorithm(DiagramAlgorithm):

    INPUT_VECTOR = 'INPUT_VECTOR'
    ID_FIELD = 'ID_FIELD'
    FIELDS = 'FIELDS'
    COLOR_SCHEMA = 'COLOR_SCHEMA'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'

    def defineCharacteristics(self):
        self.name = "Pie Charts"
        self.group = "Diagrams"
        
        # Add the input parameters to the dialog
        self.addParameter(ParameterVector(self.INPUT_VECTOR, self.tr("Input")))
        self.addParameter(ParameterTableField(self.ID_FIELD, self.tr("Identifier field"), datatype=0))
        self.addParameter(ParameterString(self.FIELDS, self.tr("Fields comma separated"), default="Fishery__1,Fishery__2,Fishery__3"))
        self.addParameter(ParameterSelection(self.COLOR_SCHEMA, self.tr("Color schema"), self.availableColorSchemas))
        self.addOutput(OutputDirectory(self.OUTPUT_DIRECTORY, self.tr("Store to directory")))


    def processAlgorithm(self, progress):
        # Get all input parameters
        layer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.INPUT_VECTOR))
        id_field = self.getParameterValue(self.ID_FIELD)
        # An array with fields
        fields = self.getParameterValue(self.FIELDS).split(',')
        color_schema_index = self.getParameterValue(self.COLOR_SCHEMA)
        color_schema = self.availableColorSchemas[color_schema_index]

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
            # Get all values
            values = np.array([float(attrs[i]) for i in fieldIdxs])
    
            # Get the correct color schema from the module
            cls = self.parseColorDefinition(color_schema, str(values.size)) 

            # Draw the pie chart with above values and colors
            wedges = plt.pie(values, colors=cls, startangle=90)
            # Set a white edge color for all wedges
            for w in wedges[0]:
                w.set_edgecolor('w')
            # Set aspect ratio to be equal so that pie is drawn as a circle.
            plt.axis('equal')

            # Save the plot as figure to the specified directory
            plt.savefig("%s/piecharts_%s.svg" % (outputDir, id_field), format="svg", transparent=True, frameon=False)

            # Close the figure properly
            plt.close()
            # Set the progress in percentage
            progress.setPercentage(float(currentFeatureIdx / nbrFeatures) * 100.0)
            # Increase the index of the current feature
            currentFeatureIdx += 1
        
    def getIcon(self):
        """
        Returns custom icon for pie charts algorithm
        """
        return QIcon(os.path.dirname(__file__) + "/images/piechart.png")
