import os
import inspect
import json
import typing


def convert_typing_to_json_schema(typing_type):
    if typing_type is int:
        return {"type": "integer"}
    elif typing_type is float:
        return {"type": "number"}
    elif typing_type is str:
        return {"type": "string"}
    elif typing_type is bool:
        return {"type": "boolean"}
    elif typing_type is list:
        return {"type": "array", "items": {"type": "any"}}
    elif typing_type is dict:
        return {"type": "object"}
    elif typing_type is typing.Any:
        return {}
    elif hasattr(typing_type, "__origin__") and typing_type.__origin__ is typing.Union:
        # Handle Union types, consider only the first type in the Union
        return convert_typing_to_json_schema(typing_type.__args__[0])
    elif inspect.isclass(typing_type):
        # Handle class types by recursively generating the schema for the class
        return generate_json_schema(typing_type)
    else:
        raise ValueError(f"Unsupported type: {typing_type}")


def generate_json_schema(func):
    signature = inspect.signature(func)
    parameters = signature.parameters

    schema = {"type": "object", "properties": {}, "required": []}

    for param_name, param_obj in parameters.items():
        param_type = param_obj.annotation
        if param_type is inspect.Parameter.empty:
            param_type = typing.Any

        schema["properties"][param_name] = convert_typing_to_json_schema(param_type)

        if param_obj.default == inspect.Parameter.empty:
            schema["required"].append(param_name)

    return schema


# Example class
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


# Example Python function with class as argument
def process_point(point: Point):
    return f"Processing point ({point.x}, {point.y})"


# Generate JSON schema for the function
schema = generate_json_schema(process_point)

# Convert the schema to JSON format
json_schema = json.dumps(schema, indent=2)

# Print the JSON schema
print(json_schema)


def create_init_files(directory: str = ".", verbose = False):
    """
    Creates empty __init__.py files in the given directory and all its subdirectories.

    :param directory: The root directory where the __init__.py files should be created.
    """
    for root, _, _ in os.walk(directory):
        init_file_path = os.path.join(root, '__init__.py')
        with open(init_file_path, 'a'):
            if verbose:
                print(f"Created {init_file_path}")

            pass  # Simply open the file in append mode, which will create it if it doesn't exist

