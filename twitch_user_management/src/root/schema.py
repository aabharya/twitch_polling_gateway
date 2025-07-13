from drf_spectacular.utils import extend_schema


def schema_generator(schema_definition: dict) -> None:
    for view_class, definitions in schema_definition.items():
        extend_schema(**definitions)(view_class)
