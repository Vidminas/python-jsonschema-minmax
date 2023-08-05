import json
from pathlib import Path
from jsonschema import ValidationError
from jsonschema_minmax import MinMaxValidator


def get_fixture_path(filename: str) -> Path:
    testdir = Path(__file__).resolve().parent
    return testdir.joinpath("fixtures", filename)


with get_fixture_path("test_schema.json").open(encoding="utf-8") as fp:
    test_schema = json.load(fp)
with get_fixture_path("test_instance.json").open(encoding="utf-8") as fp:
    test_instance = json.load(fp)


MinMaxValidator.check_schema(test_schema)

try:
    MinMaxValidator(test_schema).validate(test_instance)
except ValidationError as e:
    assert (
        e.message == "'fridge_max_temp'=4 is less than the minimum 'fridge_min_temp'=5!"
    )
else:
    assert False
