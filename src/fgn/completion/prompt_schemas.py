from typing import List


def msg_schema(content: str, role="user") -> dict:
    return {"content": content, "role": role}


def func_schema(name: str, description: str, properties: List[dict]) -> dict:
    required = []
    for prop in properties:
        required.append(next(iter(prop)))

    prop_dict = {}
    for prop in properties:
        prop_dict.update(prop)

    function = {
        "name": name,
        "description": description
        + " Pay attention to the description of the parameters.",
        "parameters": {
            "type": "object",
            "properties": prop_dict,
        },
        "required": required,
    }

    return function


def prop_schema(
    name: str, description: str = None, ptype: str = None, **kwargs
) -> dict:
    prop = {name: {}}

    if ptype:
        prop[name]["type"] = ptype

    if description:
        prop[name]["description"] = description

    if kwargs:
        for key, value in kwargs.items():
            prop[name][key] = value

    return prop


def str_func_schema(
    name: str, description: str, property_name: str, property_description
) -> dict:
    return func_schema(
        name,
        description,
        [
            prop_schema(
                property_name,
                property_description,
                "string",
            )
        ],
    )
