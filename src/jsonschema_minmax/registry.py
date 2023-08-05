import json

from pathlib import Path

from referencing import Resource
from referencing import Registry as _Registry
from referencing.jsonschema import SchemaRegistry as _SchemaRegistry


def load_metaschema(paths: list[Path]):
    for path in paths:
        contents = json.loads(path.read_text(encoding="utf-8"))
        yield Resource.from_contents(contents)

schemas = load_metaschema([
    Path("metaschema", "minmax-metaschema.json"),
    Path("metaschema", "minmax-vocabulary.json"),
])

REGISTRY: _SchemaRegistry = (schemas @ _Registry()).crawl()