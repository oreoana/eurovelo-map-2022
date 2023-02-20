import folium
from radroutes import RadRouter

class TestRadRouter(object):
    def test__radrouter__init__ok(self):
        path_to_config = "/path/to/config"
        path_to_output = "/path/to/output"
        rr = RadRouter(path_to_config, path_to_output)
        assert rr.config_file_path == path_to_config
        assert rr.out_file_path == path_to_output
        assert isinstance(rr.map, folium.Map)
