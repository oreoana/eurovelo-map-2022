#!/usr/bin/env python 

import argparse
import sys
import os
from schema import Schema, SchemaError, Optional, And
import yaml
import fit2gpx
import folium

class RadRouter():
    def __init__(self, path_to_config_file, path_to_output_file):
        self.config_file_path = path_to_config_file
        self.out_file_path = path_to_output_file
        self.map = folium.Map()

    # PRIVATE METHODS
    def _generate_popup_html(self, coordinates):
        html = " ".join(["<h2>", coordinates['title'].iat[0], "</h2><br /><p>", coordinates['description'].iat[0], "</p>"])

        if coordinates['image'].iat[0] is not None:
            html = " ".join([html, "<br /><img style=\"width: 100%; height: 100%\" src=",  coordinates['image'].iat[0], ">"])

        return html

    def _add_geojson_lines(self, coordinates_list):
        segment_features = []

        for coordinates in coordinates_list:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates[['longitude', 'latitude']].values.tolist(),
                },
                'properties': {
                    'weight': 5,
                    'html': self._generate_popup_html(coordinates),
                },
            }

            segment_features.append(feature)

        geojson_features = {
            'type': 'FeatureCollection',
            'features': segment_features
        }

        segment_layer = folium.GeoJson(
            geojson_features,
            zoom_on_click=True,
            highlight_function=lambda x: {
                'color': 'green',
                'weight': 10,
            },
            popup=folium.GeoJsonPopup(
                fields=['html'],
                labels=False,
            )
        ).add_to(self.map)

        self.map.fit_bounds(segment_layer.get_bounds())

    # PUBLIC METHODS
    def process_activities(self):
        """Consumes a path to a config file and plots the activites on the map."""
        activities = self.validate_config()

        segments = activities['activities']['segments']
        directory = activities['activities']['directory']

        conv = fit2gpx.Converter()
        all_coordinates_list = []

        # convert each file to a dataframe and create a list of dataframes
        for segment in segments:
            segment_path = os.path.join(directory, segment['file_name'])
            _, df_coordinates = conv.fit_to_dataframes(segment_path)
            df_coordinates['file_name'] = segment.get('file_name')
            df_coordinates['title'] = segment.get('title', 'Title')
            df_coordinates['description'] = segment.get('description', 'Description goes here!')
            df_coordinates['image'] = segment.get('image')

            all_coordinates_list.append(df_coordinates)

        self._add_geojson_lines(all_coordinates_list)

    def generate_map_output(self):
        """Generates an HTML output of the map."""
        output_file = "/".join([self.out_file_path, 'map.html'])
        self.map.save(output_file)
        print(f'Map saved to {output_file}')

    def validate_config(self):
        """Validates the given config file."""
        try:
            with open(self.config_file_path, 'r') as config_file:
                activities = yaml.safe_load(config_file)
            print(f'Successfully opened config file: {self.config_file_path}')
        except IOError:
            print(f'Could not find file: {self.config_file_path}')
            sys.exit(1)

        # need to add check that individual files exist
        expected_schema = Schema({
            'activities': {
                'directory': And(os.path.exists, error='Invalid directory'),
                'segments': [{
                    'file_name': str,
                    Optional('title'): str,
                    Optional('description'): str,
                    Optional('image'): str
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

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Rad-ify your routes! Accepts a configuration file with title,
        description, and optional picture for your activity and creates an interactive
        HTML map of your activities and content.''',
        epilog="""Tell a story with your activities.""")
    parser.add_argument('config_file_path', type=str, help='path to config YAML file')
    parser.add_argument('--out_file_path', type=str, default='.', help='path to output HTML file')
    args=parser.parse_args()
    
    path_to_config_file = args.config_file_path
    path_to_output_file = args.out_file_path

    rr = RadRouter(path_to_config_file, path_to_output_file)
    rr.process_activities()
    rr.generate_map_output()