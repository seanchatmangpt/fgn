import time
import yaml
import os
import subprocess
import logging

from typing import Dict
from fgn.core.core_cmd import core_command
from fgn.core.command_context import CommandContext
from fgn.models.dsl.fgn_dsl_schema import FgnDslSchema
from fgn.models.dsl.step import Step
from fgn.models.dsl.task import Task

logging.basicConfig(level=logging.INFO)


def load_schema_from_yaml_file(file_path: str) -> FgnDslSchema:
    with open(file_path, 'r') as yaml_file:
        schema_dict = yaml.safe_load(yaml_file)

    tasks = []
    for task_dict in schema_dict["tasks"]:
        steps = [Step(**step_dict) for step_dict in task_dict["steps"]]
        task = Task(name=task_dict["name"], description=task_dict["description"], steps=steps)
        tasks.append(task)

    return FgnDslSchema(version=schema_dict["version"], description=schema_dict["description"], tasks=tasks)


def execute_shell_command(command: str, ctx: CommandContext, variables: Dict[str, str]) -> None:
    formatted_command = command.format(**variables)
    formatted_command = formatted_command.format(**ctx.__dict__)
    subprocess.run(formatted_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def execute_fgn_command(command: str, options: Dict[str, str], ctx: CommandContext, variables: Dict[str, str]) -> None:
    ctx = CommandContext(**ctx.__dict__)

    for k, v in options.items():
        v = str(v)
        setattr(ctx, k, v.format(**variables))

    for k, v in variables.items():
        v = str(v)
        setattr(ctx, k, v)

    formatted_command = command.format(**variables)
    formatted_command = formatted_command.format(**ctx.__dict__)
    formatted_options = {k: str(v).format(**variables) for k, v in options.items()}
    command_context = CommandContext(**formatted_options)
    ctx.text = formatted_command
    core_command(ctx)

    output_file_path = command_context.output
    if output_file_path:
        wait_for_file(output_file_path)


def process_step(step: Step, ctx: CommandContext, variables: Dict[str, str]) -> None:
    if step.action == "shell":
        execute_shell_command(step.run, ctx, variables)
    elif step.action == "fgn":
        execute_fgn_command(step.command, step.options, ctx, variables)
    elif step.action == "import_task":
        process_yaml_file(step.file_path, ctx, variables)
    elif step.action == "assign_variable":
        variables[step.name] = step.value
    else:
        raise ValueError(f"Unknown action '{step.action}' in step '{step.description}'")


def process_yaml_file(file_path: str, ctx: CommandContext, variables: Dict[str, str]) -> None:
    schema = load_schema_from_yaml_file(file_path)
    process_schema(schema, ctx, variables)


def process_task(task: Task, ctx: CommandContext, variables: Dict[str, str]) -> None:
    logging.info(f"Processing task '{task.name}'")
    for step in task.steps:
        process_step(step, ctx, variables)


def process_schema(schema: FgnDslSchema, ctx: CommandContext, variables: Dict[str, str] = None) -> None:
    if variables is None:
        variables = {}
    for task in schema.tasks:
        process_task(task, ctx, variables)


def wait_for_file(file_path: str, timeout: int = 10, check_interval: float = 1.0) -> None:
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"File '{file_path}' not found after waiting for {timeout} seconds")
        time.sleep(check_interval)


def main(schema_file: str, ctx: CommandContext):
    schema = load_schema_from_yaml_file(schema_file)
    process_schema(schema, ctx)


if __name__ == "__main__":
    main('/Users/seanchatman/dev/file-generator/data/dsl/test.yaml', CommandContext())
