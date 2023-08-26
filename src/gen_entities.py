from dataclasses import dataclass
from typing import List

from typetemp.template.typed_template import TypedTemplate


@dataclass
class UUIDValueObjectTemplate(TypedTemplate):
    class_name: str = ""
    to: str = "./ddd/value_objects/{{ class_name }}.py"
    source = """
from uuid import uuid4

class {{ class_name }}:
    def __init__(self, value: str = None):
        self.value = str(uuid4()) if value is None else value
    """


@dataclass
class EntityTemplate(TypedTemplate):
    class_name: str = ""
    value_object: str = ""
    to: str = "./ddd/entities/{{ class_name }}.py"
    source = """
from ddd.value_objects.{{ value_object }} import {{ value_object }}

class {{ class_name }}:
    def __init__(self, id: {{ value_object }} = None):
        self.id = id if id else {{ value_object }}()
    """


@dataclass
class ValueObjectTemplate(TypedTemplate):
    class_name: str = ""
    to: str = "./ddd/value_objects/{{ class_name }}.py"
    source = """
class {{ class_name }}:
    def __init__(self, value):
        self.value = value
    """


@dataclass
class AggregateRootTemplate(TypedTemplate):
    class_name: str = ""
    entity_name: str = ""
    to: str = "./ddd/aggregates/{{ class_name }}.py"
    source = """
from ddd.entities.{{ entity_name }} import {{ entity_name }}

class {{ class_name }}:
    def __init__(self, root_entity: {{ entity_name }}):
        self.root_entity = root_entity
    """


@dataclass
class RepositoryTemplate(TypedTemplate):
    class_name: str = ""
    entity_name: str = ""
    to: str = "./ddd/repositories/{{ class_name }}Repo.py"
    source = """
from ddd.entities.{{ entity_name }} import {{ entity_name }}

class {{ class_name }}Repo:
    def __init__(self):
        self.data = {}

    def create(self, entity: {{ entity_name }}):
        self.data[entity.id.value] = entity

    def read(self, id: str):
        return self.data.get(id)

    def update(self, id: str, entity: {{ entity_name }}):
        self.data[id] = entity

    def delete(self, id: str):
        del self.data[id]
    """


@dataclass
class ServiceTemplate(TypedTemplate):
    class_name: str = ""
    repository_name: str = ""
    to: str = "./ddd/services/{{ class_name }}Service.py"
    source = """
from ddd.repositories.{{ repository_name }}Repo import {{ repository_name }}Repo

class {{ class_name }}Service:
    def __init__(self, repo: {{ repository_name }}Repo):
        self.repo = repo

    def perform_operation(self, entity):
        # Logic for performing an operation
        pass
    """


def generate_reporting_system_entities(entities):
    # Define the common value objects
    uuid_template = UUIDValueObjectTemplate(class_name="UUID")
    uuid_template.render()

    # Define the entities
    for entity in entities:
        # Create the value object for the entity
        value_object_template = ValueObjectTemplate(class_name=f"{entity}Value")
        value_object_template.render()

        # Create the entity itself
        entity_template = EntityTemplate(class_name=entity, value_object=f"{entity}Value")
        entity_template.render()

        # Create the aggregate root for the entity
        aggregate_root_template = AggregateRootTemplate(class_name=f"{entity}Aggregate", entity_name=entity)
        aggregate_root_template.render()

        # Create the repository for the entity
        repository_template = RepositoryTemplate(class_name=entity, entity_name=entity)
        repository_template.render()

        # Create the service for the entity
        service_template = ServiceTemplate(class_name=entity, repository_name=entity)
        service_template.render()

    print("Entities generated successfully.")
