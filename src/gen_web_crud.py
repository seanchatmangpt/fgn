from dataclasses import dataclass

from typetemp.template.typed_template import TypedTemplate


@dataclass
class RouteTemplate(TypedTemplate):
    class_name: str = ""
    to: str = "./web/routes/{{ class_name }}Routes.py"
    source = """
from flask import Flask, request, render_template
from ddd.services.{{ class_name }}Service import {{ class_name }}Service
from ddd.repositories.{{ class_name }}Repo import {{ class_name }}Repo
from ddd.entities.{{ class_name }} import {{ class_name }}

app = Flask(__name__)
repo = {{ class_name }}Repo()
service = {{ class_name }}Service(repo)

@app.route('/{{ class_name.lower() }}', methods=['GET'])
def get_{{ class_name.lower() }}s():
    entities = [entity for entity in repo.data.values()]
    return render_template('{{ class_name.lower() }}.html', entities=entities)

@app.route('/{{ class_name.lower() }}/create', methods=['POST'])
def create_{{ class_name.lower() }}():
    # Logic to create a {{ class_name }}
    entity = {{ class_name }}()  # Initialize with proper parameters from request
    service.create(entity)
    return redirect('/{{ class_name.lower() }}')

@app.route('/{{ class_name.lower() }}/update/<id>', methods=['POST'])
def update_{{ class_name.lower() }}(id):
    # Logic to update a {{ class_name }}
    entity = {{ class_name }}()  # Initialize with proper parameters from request
    service.update(id, entity)
    return redirect('/{{ class_name.lower() }}')

@app.route('/{{ class_name.lower() }}/delete/<id>', methods=['POST'])
def delete_{{ class_name.lower() }}(id):
    service.delete(id)
    return redirect('/{{ class_name.lower() }}')
    """


@dataclass
class HTMLFormAndTableTemplate(TypedTemplate):
    class_name: str = ""
    to: str = "./templates/{{ class_name.lower() }}.html"
    source = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ class_name }} Management</title>
</head>
<body>
    <h1>{{ class_name }}s</h1>
    <form action="/{{ class_name.lower() }}/create" method="post">
        <!-- Fields for {{ class_name }} -->
        <input type="submit" value="Create {{ class_name }}">
    </form>
    <table>
        {% for entity in entities %}
        <tr>
            <!-- Columns for {{ class_name }} -->
            <td><a href="/{{ class_name.lower() }}/update/{{ entity.id.value }}">Update</a></td>
            <td>
                <form action="/{{ class_name.lower() }}/delete/{{ entity.id.value }}" method="post">
                    <input type="submit" value="Delete">
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
    """


def generate_web_crud(entities):
    # Define the entities
    for entity in entities:
        # Create the CRUD routes for the entity
        route_template = RouteTemplate(class_name=entity)
        route_template.render()

        # Create the HTML form and table for the entity
        html_template = HTMLFormAndTableTemplate(class_name=entity)
        html_template.render()

    print("Web CRUD interfaces generated successfully.")