import json
import os

from mangum import Mangum
from datasette.app import Datasette, DEFAULT_CONFIG
from datasette.utils import value_as_boolean

METADATA_PATH = '/var/task/metadata.json'
CONFIG_PATH = '/var/task/config.txt'
METADATA_PATH = '/var/task/metadata.json'
PREFIX = 'Prod'

def load_metadata():
    """Load the metadata.json file, if present."""
    metadata = {}
    if os.path.exists(METADATA_PATH):
        metadata = json.loads(open(METADATA_PATH).read())

    return metadata

def load_config():
    """Load and parse config settings, if present."""
    config = {}
    if os.path.exists(CONFIG_PATH):
        for line in open(CONFIG_PATH):
            if not line:
                continue

            line = line.strip()

            if ':' not in line:
                raise Exception('"{}" should be name:value'.format(line))

            key = line[0:line.find(':')]
            value = line[line.find(':') + 1:]

            # This is a hack; properly we should be introspecting the annotations in cli.py.
            # Still, this works for many of the common settings, so *shrug*.
            if key not in DEFAULT_CONFIG:
                raise Exception('unknown config setting: ' + key)

            default = DEFAULT_CONFIG[key]
            if isinstance(default, bool):
                value = value_as_boolean(value)
            elif isinstance(default, int):
                value = int(value)

            config[key] = value
            
    if PREFIX:
        config['base_url'] = '/{}/'.format(PREFIX)
    return config


def create_handler():
    """Create the Datasette ASGI handler and wrap it in the Mangum adapter."""
    datasette = Datasette(
        files=["/var/task/test.db"],
        immutables=[],
        cache_headers=True,
        cors=True,
        inspect_data=None,
        metadata=load_metadata(),
        sqlite_extensions=None, #sqlite_extensions,
        template_dir=None, #template_dir,
        plugins_dir=None, #plugins_dir,
        static_mounts=None, #static,
        config=load_config(),
        memory=False, #memory,
        version_note=None #version_note,
    )
    app = datasette.app()
    return Mangum(app)

handler_ = create_handler()

def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")
    return handler_(event, context)
