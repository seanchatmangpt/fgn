from jinja2 import nodes, Environment
from jinja2.ext import Extension
from faker import Faker


class FakerExtension(Extension):
    tags = set(["faker"])

    def __init__(self, environment):
        super().__init__(environment)
        self.faker = Faker()

        # Register a macro for each method in the Faker instance
        for method in dir(self.faker):
            try:
                if callable(getattr(self.faker, method)) and not method.startswith("_"):
                    self.environment.globals["faker_" + method] = getattr(
                        self.faker, method
                    )
            except TypeError as e:
                continue

    def parse(self, parser):
        pass  # We don't need to implement this method as we won't be using the {% faker %} tag anymore


def main():
    env = Environment(extensions=[FakerExtension])

    # Define some templates to test
    templates = [
        "{{ faker_name() }}",
        "{{ faker_email() }}",
        "{{ faker_country() }}",
        "{{ faker_city() }}",
        "{{ faker_address() }}",
        "{{ faker_text() }}",
        "{{ faker_job() }}",
        "{{ faker_company() }}",
        "{{ faker_phone_number() }}",
        "{{ faker_bs() }}",
        "{{ faker_pydict() }}",
    ]

    # Render and print each template
    for template in templates:
        result = env.from_string(template).render()
        print(result)


if __name__ == "__main__":
    main()
