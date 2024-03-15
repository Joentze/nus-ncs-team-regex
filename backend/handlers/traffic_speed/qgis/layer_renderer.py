'''
NOTE: This script is to be run in the QGIS Python Console for the purposes of exploratory data analysis. This script converts the JSON data pulled from LTA datamall and creates a LineString vector layer in QGIS.

TO BE COMPLETED:
1. Script-based symbology creation
2. Script-based layer save and image creation
3. Batching for all datasets collected
'''
import json
from qgis.PyQt.QtCore import QVariant

# Define the path to your JSON file
json_file_path = #branch_name_here

# Open the JSON file and read the data
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Define an empty list to store polylines
polylines = []

# Setup the QGIS layer with the data types and attributes
layer = QgsVectorLayer('LineString?crs=epsg:4326', 'Roads', 'memory')
provider = layer.dataProvider()
provider.addAttributes([QgsField("RoadName", QVariant.String),
                        QgsField("LineID",  QVariant.Int),
                       QgsField("SpeedBand", QVariant.Float)])

# Begin field updates
layer.updateFields()

# Loop through each road segment in the data
for road_name, values in data.items():
    if road_name != "time":
        for line_id, coordinates in values.items():
            start_point = QgsPoint(
                float(coordinates["StartLon"]), float(coordinates['StartLat']))
            end_point = QgsPoint(
                float(coordinates["EndLon"]), float(coordinates['EndLat']))

            # Create a polyline geometry
            feature = QgsFeature()
            polyline = QgsGeometry.fromPolyline([start_point, end_point])

            # Create feature with attributes
            feature.setGeometry(polyline)
            feature.setAttributes(
                [road_name, line_id, coordinates['SpeedBand']])

            # Add feature to polylines list
            provider.addFeature(feature)
            layer.updateExtents()
QgsProject.instance().addMapLayer(layer)

print("Success!")