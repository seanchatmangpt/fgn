from dataclasses import dataclass
from typing import List

from gen_entities import generate_reporting_system_entities
from gen_web_crud import generate_web_crud
from typetemp.template.typed_template import TypedTemplate
from typetemp.utils import create_init_files


@dataclass
class FlaskAppTemplate(TypedTemplate):
    entities: List[str] = None
    to: str = "./app.py"
    source = """
from flask import Flask, render_template
{% for entity in entities %}
from web.routes.{{ entity }}Routes import app as {{ entity.lower() }}_app
{% endfor %}

app = Flask(__name__)

{% for entity in entities %}
app.register_blueprint({{ entity.lower() }}_app, url_prefix='/{{ entity.lower() }}')
{% endfor %}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    """


def generate_app():
    entities = ['Strength', 'Weakness', 'Opportunity', 'Threat', 'Alert', 'User', 'Metrics']

    generate_reporting_system_entities(entities)

    # Generate web CRUD interfaces
    generate_web_crud(entities)

    # Create Flask App using the defined entities
    flask_app_template = FlaskAppTemplate(entities=entities)
    flask_app_template.render()

    create_init_files()

    print("Flask app generated successfully.")


# Run the function to generate the Flask app
generate_app()
