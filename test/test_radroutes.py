import pytest
from src.radroutes import RadRouter

class TestRadRouter(object):
    def test__radrouter__process__process_path__ok(self):
        rr = RadRouter()
        path = "/tmp/test.gpx"
        assert path == rr.process(path)
