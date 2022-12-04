#!/usr/bin/env python 

import sys
import os
from schema import Schema, SchemaError, Use, Optional, And
import yaml
import fit2gpx
import folium
from folium import plugins
import pandas as pd

class RadRouter():
    def process_activities(self, path_to_config):
        # Consumes a path to a config file and generates a map.
        activities = self.validate_config(path_to_config)

        segments = activities['activities']['segments']
        directory = activities['activities']['directory']

        conv = fit2gpx.Converter()
        all_coordinates_list = []
        map = folium.Map()

        # convert each file to a dataframe and create a list of dataframes
        for segment in segments:
            segment_path = os.path.join(directory, segment['file_name'])
            _, df_coordinates = conv.fit_to_dataframes(segment_path)
            df_coordinates['file_name'] = segment['file_name']

            all_coordinates_list.append(df_coordinates)

        # add check to see if speed exists in dataframe
        self.add_antpath(all_coordinates_list, map)
        self.fit_map(all_coordinates_list, map)

        folium.LayerControl().add_to(map)
        map.save('map.html')
        print('Map saved.')

    def validate_config(self, path_to_config):
        try:
            with open(path_to_config, 'r') as config_file:
                activities = yaml.safe_load(config_file)
            print(f"Successfully opened config file: {path_to_config}")
        except IOError:
            print(f"Could not find file: {path_to_config}")
            sys.exit(1)

        # need to add check that individual files exist
        expected_schema = Schema({
            'activities': {
                'directory': And(os.path.exists, error='Invalid directory'),
                'segments': [{
                    'file_name': str,
                    Optional('title'): str,
                    Optional('description'): str
                }]
            }
        })

        try:
            expected_schema.validate(activities)
            print('Config file is valid.')
        except SchemaError as se:
            print(se)
            sys.exit(1)

        return activities

    def add_antpath(self, coordinates_list, map):
        # AntPath delay range is 1 to 800. We normalize the max speed from input files against the max of 800.
        speed = pd.concat(coordinates_list)['speed']
        normalization = 800.0 / speed.max()

        feature_group = folium.FeatureGroup(name = 'Ant Path', show = True)
        map.add_child(feature_group)

        for coordinates in coordinates_list:
            plugins.AntPath(
                locations=coordinates[['latitude', 'longitude']],
                delay=coordinates['speed'].mean() * normalization,
            ).add_to(feature_group)

    def fit_map(self, coordinates_list, map):
        coordinates_df = pd.concat(coordinates_list)[['latitude', 'longitude']]

        southwest_bound = coordinates_df.min().tolist()
        northeast_bound = coordinates_df.max().tolist()

        map.fit_bounds([southwest_bound, northeast_bound])

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     raise ValueError("Expected path to config file as argument")

    rr = RadRouter()
    rr.process_activities('/workspaces/rad-routes/examples/activity_files/activities.yml')