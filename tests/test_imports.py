from importlib import import_module
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

MODULES = [
    'src.stream_monitor',
    'src.stream_recorder',
    'src.content_analyzer',
    'src.video_editor',
    'src.content_manager',
    'src.scheduler',
    'src.platform_registry',
    'src.webapp',
]

def test_imports():
    for name in MODULES:
        import_module(name)
