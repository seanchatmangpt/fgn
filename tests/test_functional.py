from typetemp.functional import render, render_native, render_class


def test_hello_str():
    rendered = render("Hello {{ name }}!", name="World")
    assert "Hello World!" == rendered


def test_hello_dict():
    rendered = render_native(
        '{"{{key}}": "{{value}}"}', use_native=True, key="Hello", value="World"
    )
    assert {"Hello": "World"} == rendered


def test_render_class():
    # Example usage
    cls_tmpl = """
from dataclasses import dataclass

@dataclass
class {{ class_name }}:
    name: str = None
    """

    func_tmpl1 = """
def {{ method_name }}1(self):
    return f"{{ new_message }} {self.name} #1"
    """

    func_tmpl2 = """
def {{ method_name }}2(self):
    return f"{{ new_message }} {self.name} #2"
    """

    func_tmpl3 = """
def {{ method_name }}3(self):
    return f"{{ new_message }} {self.name} #3"
    """

    # Render and compile the class with a method, with dataclass enabled
    name_cls = render_class(
        cls_tmpl,
        func_tmpls=[func_tmpl1, func_tmpl2, func_tmpl3],
        use_dataclass=True,
        class_name="MyClass",
        method_name="new_method",
        new_message="Hello",
    )

    # Create an instance and call the method
    obj = name_cls(name="Wesley Snipes")
    assert obj.new_method1() == "Hello Wesley Snipes #1"
    assert obj.new_method2() == "Hello Wesley Snipes #2"  # Prints: New method
    assert obj.new_method3() == "Hello Wesley Snipes #3"  # Prints: New method


def test_render_class_with_range():
    cls_tmpl = """
class {{ class_name }}:
    {% for i in range(num_methods) %}
    def method_{{ i }}(self, value):
        return "Method {{ i }}: " + value
    {% endfor %}
        """

    num_methods = 3

    rendered_class = render_class(
        cls_tmpl, class_name="MyClass", num_methods=num_methods
    )

    instance = rendered_class()
    assert instance.method_0("value") == "Method 0: value"
    assert instance.method_1("value") == "Method 1: value"
    assert instance.method_2("value") == "Method 2: value"


def test_render_class_with_loop():
    cls_tmpl = """
class {{ class_name }}:
    {% for attribute, value in attributes.items() %}
    {{ attribute }} = "{{ value }}"
    {% endfor %}
    """

    attributes = {"attribute_one": "value_one", "attribute_two": "value_two"}

    rendered_class = render_class(cls_tmpl, class_name="MyClass", attributes=attributes)

    instance = rendered_class()
    assert instance.attribute_one == "value_one"
    assert instance.attribute_two == "value_two"


def test_render_class_with_nested_loop():
    cls_tmpl = """
class {{ class_name }}:
    {% for group, members in groups.items() %}
    {{ group }} = {
        {% for member in members %}
        "{{ member }}": "{{ member|upper }}",
        {% endfor %}
    }
    {% endfor %}
    """

    groups = {
        "group_one": ["one", "two", "three"],
        "group_two": ["alpha", "beta", "gamma"],
    }

    rendered_class = render_class(cls_tmpl, class_name="MyClass", groups=groups)

    instance = rendered_class()
    assert instance.group_one == {"one": "ONE", "two": "TWO", "three": "THREE"}
    assert instance.group_two == {"alpha": "ALPHA", "beta": "BETA", "gamma": "GAMMA"}
