#!/usr/bin/env python 

import sys

class RadRouter():
    def process(self, path_to_config):
        """Consumes a path to a config file and generates a map."""
        print(f"Path to config file: {path_to_config}")
        return path_to_config

if __name__ == "__main__":
    rad = RadRouter()
    if len(sys.argv) != 2:
        raise ValueError("Expected path to config file as argument")
    rad.process(sys.argv[1])
