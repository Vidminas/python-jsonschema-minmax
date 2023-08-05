from jsonschema.protocols import Validator


def inline_references(validator: Validator, schema: dict | list | bool):
    """
    Resolves json references and merges them into a consolidated schema for validation purposes
    :param schema:
    :return: schema merged with resolved references
    """
    if isinstance(schema, dict):
        for key, value in schema.items():
            if key == "$ref":
                # Note: this is not a public API field and will likely break in the future
                # Pending updates on https://github.com/python-jsonschema/referencing/issues/2
                ref_schema = validator._resolver.lookup(value)
                return inline_references(
                    validator.evolve(_resolver=ref_schema.resolver), ref_schema.contents
                )

            resolved_ref = inline_references(validator, value)
            if resolved_ref:
                schema[key] = resolved_ref

    elif isinstance(schema, list):
        for idx, value in enumerate(schema):
            resolved_ref = inline_references(validator, value)
            if resolved_ref:
                schema[idx] = resolved_ref
    return schema
