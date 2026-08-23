import logging
import os
import time
from typing import Dict

import yaml

from fgn.core.broker import Broker
from fgn.core.command_context import CommandContext
from fgn.core.core_cmd import core_command
from fgn.models.dsl.fgn_dsl_schema import FgnDslSchema
from fgn.models.dsl.step import Step
from fgn.models.dsl.task import Task

logging.basicConfig(level=logging.INFO)


def load_schema_from_yaml_file(file_path: str) -> FgnDslSchema:
    with open(file_path, encoding="utf-8") as yaml_file:
        schema_dict = yaml.safe_load(yaml_file)
    tasks = []
    for task_dict in schema_dict["tasks"]:
        steps = [Step(**step_dict) for step_dict in task_dict["steps"]]
        tasks.append(Task(name=task_dict["name"], description=task_dict.get("description"), steps=steps))
    return FgnDslSchema(version=schema_dict.get("version"), description=schema_dict.get("description"), tasks=tasks)


def execute_shell_command(command: str, ctx: CommandContext, variables: Dict[str, str]) -> None:
    formatted_command = command.format(**variables).format(**ctx.__dict__)
    admitted = os.getenv("FGN_ALLOW_DSL_SHELL", "").lower() in {"1", "true", "yes"}
    result, receipt = Broker().run_shell(formatted_command, admitted=admitted)
    if result.returncode != 0:
        raise RuntimeError(f"Shell command failed with exit {result.returncode}; receipt={receipt.receipt_id}")


def execute_fgn_command(command: str, options: Dict[str, str], ctx: CommandContext, variables: Dict[str, str]) -> None:
    child = CommandContext(**ctx.__dict__)
    for key, value in (options or {}).items():
        setattr(child, key, str(value).format(**variables))
    for key, value in variables.items():
        setattr(child, key, str(value))
    child.text = command.format(**variables).format(**child.__dict__)
    core_command(child)
    if child.output:
        wait_for_file(child.output)


def process_step(step: Step, ctx: CommandContext, variables: Dict[str, str]) -> None:
    if step.action == "shell":
        execute_shell_command(step.run or "", ctx, variables)
    elif step.action == "fgn":
        execute_fgn_command(step.command or "", step.options or {}, ctx, variables)
    elif step.action == "import_task":
        process_yaml_file(step.file_path or "", ctx, variables)
    elif step.action == "assign_variable":
        variables[step.name or ""] = step.value or ""
    else:
        raise ValueError(f"Unknown action {step.action!r} in step {step.description!r}")


def process_yaml_file(file_path: str, ctx: CommandContext, variables: Dict[str, str]) -> None:
    process_schema(load_schema_from_yaml_file(file_path), ctx, variables)


def process_task(task: Task, ctx: CommandContext, variables: Dict[str, str]) -> None:
    logging.info("Processing task %r", task.name)
    for step in task.steps:
        process_step(step, ctx, variables)


def process_schema(schema: FgnDslSchema, ctx: CommandContext, variables: Dict[str, str] | None = None) -> None:
    scope = variables if variables is not None else {}
    for task in schema.tasks:
        process_task(task, ctx, scope)


def wait_for_file(file_path: str, timeout: int = 10, check_interval: float = 1.0) -> None:
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"File {file_path!r} not found after {timeout} seconds")
        time.sleep(check_interval)


def main(schema_file: str, ctx: CommandContext):
    process_schema(load_schema_from_yaml_file(schema_file), ctx)
