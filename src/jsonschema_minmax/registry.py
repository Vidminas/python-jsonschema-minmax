import pkgutil
import json

from referencing import Resource
from referencing import Registry as _Registry
from referencing.jsonschema import SchemaRegistry as _SchemaRegistry


def load_metaschema(paths: list[str]):
    for path in paths:
        data = pkgutil.get_data(__package__, path)
        contents = json.loads(data.decode("utf-8"))
        yield Resource.from_contents(contents)


schemas = load_metaschema(
    [
        "metaschema/minmax-metaschema.json",
        "metaschema/minmax-vocabulary.json",
    ]
)

REGISTRY: _SchemaRegistry = (schemas @ _Registry()).crawl()
