import os
import json

from fgn.completion.chat import Chat
from fgn.completion.prompt_schemas import generate_json_schema, str_func_schema
from typetemp.template.typed_linkedin_profile_prompt import TypedLinkedInProfilePrompt


def create_init_files(directory: str = ".", verbose=False):
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


if __name__ == "__main__":
    # Example class
    class Point:
        """
        A point in n dimensions.
        """
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    # Example Python function with class as argument
    def process_points_in_n_dimensions(point: Point, n: int):
        """
        Process a point in n dimensions.
        :param point: The point to process
        :param n: The number of dimensions
        :return:
        """
        print(point, n)


    # def get_linkedin_profile(prompt: TypedLinkedInProfilePrompt):
    #     """
    #     Get a LinkedIn profile based on the given prompt.
    #     :param prompt:
    #     :return:
    #     """
    #     print(prompt)

    # Generate JSON schema for the function
    # schema = generate_json_schema(get_linkedin_profile)
    # schema = generate_json_schema(process_points_in_n_dimensions)

    schema = str_func_schema("fake_full_name_generator",
                             "Generate a fake full name",
                             "full_name",
                             "The first and last name of the person")

    def fake_full_name_generator(full_name: str):
        """
        Generate a fake full name.
        :param full_name: The first and last name of the person
        :return:
        """
        return full_name

    schema2 = generate_json_schema(fake_full_name_generator)

    assert schema == schema2

    # ci = Chat()
    # res = ci(prompt="Create a fake name of a Jamaican man", funcs=[schema])

    # print(res["name"])
    # print(res["arguments"]["full_name"])
