from jsonschema import validators
from jsonschema.protocols import Validator
from jsonschema.validators import Draft202012Validator
from jsonschema.exceptions import ValidationError

from .registry import REGISTRY


def extend_with_variables(validator_class: Validator) -> Validator:
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_variables(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if property not in instance:
                continue

            if "minVariable" in subschema:
                if subschema["minVariable"] not in instance:
                    yield ValidationError(
                        f"Field {subschema['minVariable']!r} referenced in minVariable constraint not found!"
                    )
                elif instance[property] < instance[subschema["minVariable"]]:
                    yield ValidationError(
                        f"{property!r}={instance[property]} is less than the minimum {subschema['minVariable']!r}={instance[subschema['minVariable']]}!"
                    )

            if "maxVariable" in subschema:
                if subschema["maxVariable"] not in instance:
                    yield ValidationError(
                        f"Field {subschema['maxVariable']!r} referenced in maxVariable constraint not found!"
                    )
                elif instance[property] > instance[subschema["maxVariable"]]:
                    yield ValidationError(
                        f"{property!r}={instance[property]} is greater than the maximum {subschema['maxVariable']!r}={instance[subschema['maxVariable']]}!"
                    )

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return validators.extend(
        validator_class,
        {
            "properties": set_variables,
        },
    )


MinMaxValidator = extend_with_variables(Draft202012Validator)
MinMaxValidator.META_SCHEMA = REGISTRY.contents(
    "https://raw.githubusercontent.com/Vidminas/python-jsonschema-minmax/main/metaschema/minmax-metaschema.json"
)
