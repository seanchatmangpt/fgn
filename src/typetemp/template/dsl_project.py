# Here is your PerfectPythonProductionPEP8® AGI code you requested:
from dataclasses import dataclass, field
from typing import List, Optional

import yaml

from typetemp.template.typed_prompt import TypedPrompt


@dataclass
class TypedTitleDescriptionPrompt(TypedPrompt):
    """
    Class for the Title Description step.
    """

    title: str = ""
    description: str = ""


@dataclass
class TypedRequirementAnalysisPrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Requirement Analysis step.
    """

    stakeholders: List[str] = field(default_factory=list)
    core_functionalities: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    timeframe: str = ""
    source: str = "Gather detailed requirements that the DSL needs to fulfill. Identify core functionalities, consult with {{ stakeholders }}, consider {{ constraints }}, choose appropriate {{ technologies }}, within the timeframe of {{ timeframe }}."


@dataclass
class TypedDesignArchitecturePrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Design Architecture step.
    """

    components: List[str] = field(default_factory=list)
    interactions: List[str] = field(default_factory=list)
    syntax: str = ""
    scalability: str = ""
    modularity: str = ""
    source: str = "Plan how the DSL will interact with other system components {{ components }}. Define the DSL's syntax {{ syntax }}, ensure {{ scalability }} and {{ modularity }}, and outline component interactions {{ interactions }}."


@dataclass
class TypedBuildCoreComponentsPrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Build Core Components step.
    """

    parsers: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    error_handling: str = ""
    performance_metrics: List[str] = field(default_factory=list)
    source: str = "Develop parsers {{ parsers }} for the YAML configurations. Implement classes {{ classes }} and methods {{ methods }} for functionalities. Include {{ error_handling }} and consider {{ performance_metrics }}."


@dataclass
class TypedImplementBusinessLogicPrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Implement Business Logic step.
    """

    team_composition: str = ""
    goal_setting: str = ""
    data_models: List[str] = field(default_factory=list)
    algorithms: List[str] = field(default_factory=list)
    optimization_criteria: List[str] = field(default_factory=list)
    source: str = "Add logic for team composition {{ team_composition }}, goal setting {{ goal_setting }}, use data models {{ data_models }}, apply algorithms {{ algorithms }}, and meet optimization criteria {{ optimization_criteria }}."


@dataclass
class TypedTestingPrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Testing step.
    """

    unit_tests: List[str] = field(default_factory=list)
    integration_tests: List[str] = field(default_factory=list)
    stress_tests: List[str] = field(default_factory=list)
    test_data: List[str] = field(default_factory=list)
    test_environments: List[str] = field(default_factory=list)
    source: str = "Write unit tests {{ unit_tests }}, validate through integration tests {{ integration_tests }}, perform stress tests {{ stress_tests }}, use test data {{ test_data }} in various test environments {{ test_environments }}."


@dataclass
class TypedDeploymentPrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Deployment step.
    """

    deployment_strategy: str = ""
    ci_cd_pipelines: List[str] = field(default_factory=list)
    monitoring_tools: List[str] = field(default_factory=list)
    backup_plan: str = ""
    rollback_procedures: List[str] = field(default_factory=list)
    source: str = "Choose an appropriate deployment strategy {{ deployment_strategy }}. Implement CI/CD pipelines {{ ci_cd_pipelines }}, use monitoring tools {{ monitoring_tools }}, have a backup plan {{ backup_plan }}, and prepare rollback procedures {{ rollback_procedures }}."


@dataclass
class TypedDocumentationPrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Documentation and User Training step.
    """

    documentation_types: List[str] = field(default_factory=list)
    user_guides: List[str] = field(default_factory=list)
    api_docs: List[str] = field(default_factory=list)
    tutorials: List[str] = field(default_factory=list)
    faqs: List[str] = field(default_factory=list)
    source: str = "Create detailed documentation types {{ documentation_types }} and offer training sessions or materials to end-users including user guides {{ user_guides }}, API documentation {{ api_docs }}, tutorials {{ tutorials }}, and FAQs {{ faqs }}."


@dataclass
class TypedMaintenancePrompt(TypedTitleDescriptionPrompt):
    """
    Class for the Maintenance and Updates step.
    """

    monitoring_metrics: List[str] = field(default_factory=list)
    update_schedule: str = ""
    patching_policy: str = ""
    support_channels: List[str] = field(default_factory=list)
    user_feedback_mechanisms: List[str] = field(default_factory=list)
    source: str = "Monitor system's usage and performance using metrics {{ monitoring_metrics }}. Apply patches and updates as required following the update schedule {{ update_schedule }} and patching policy {{ patching_policy }}. Provide support through channels {{ support_channels }} and collect feedback via {{ user_feedback_mechanisms }}."


typed_requirement_analysis_prompt = TypedRequirementAnalysisPrompt(
    title="Requirement Analysis",
    description="Gather detailed requirements for the DSL.",
    stakeholders=["Product Manager", "Dev Team", "QA Team"],
    core_functionalities=["Parsing", "Error Handling"],
    constraints=["Time", "Budget"],
    technologies=["Python", "YAML"],
    timeframe="Q1",
)

typed_design_architecture_prompt = TypedDesignArchitecturePrompt(
    title="Design Architecture",
    description="Design the DSL architecture.",
    components=["Parser", "Executor"],
    interactions=["Data Flow", "Control Flow"],
    syntax="YAML-based",
    scalability="High",
    modularity="Modular",
)

typed_build_core_components_prompt = TypedBuildCoreComponentsPrompt(
    title="Build Core Components",
    description="Develop core components of the DSL.",
    parsers=["YAML Parser", "JSON Parser"],
    methods=["execute", "validate"],
    classes=["TypedPrompt", "Chat"],
    error_handling="Exception Handling",
    performance_metrics=["Speed", "Memory"],
)

typed_implement_business_logic_prompt = TypedImplementBusinessLogicPrompt(
    title="Implement Business Logic",
    description="Implement the business logic.",
    team_composition="Cross-functional",
    goal_setting="S.M.A.R.T",
    data_models=["User", "Environment"],
    algorithms=["NLP", "ML"],
    optimization_criteria=["Efficiency", "Accuracy"],
)

typed_testing_prompt = TypedTestingPrompt(
    title="Testing",
    description="Conduct thorough testing.",
    unit_tests=["test_parser", "test_executor"],
    integration_tests=["test_end_to_end"],
    stress_tests=["test_load"],
    test_data=["Sample YAML", "Sample JSON"],
    test_environments=["Local", "Staging"],
)

typed_deployment_prompt = TypedDeploymentPrompt(
    title="Deployment",
    description="Deploy the system.",
    deployment_strategy="Blue-Green",
    ci_cd_pipelines=["Jenkins", "GitLab"],
    monitoring_tools=["Prometheus", "Grafana"],
    backup_plan="Daily Backups",
    rollback_procedures=["Automated", "Manual"],
)

typed_documentation_prompt = TypedDocumentationPrompt(
    title="Documentation",
    description="Create detailed documentation.",
    documentation_types=["API", "User Guide"],
    user_guides=["Getting Started", "Advanced"],
    api_docs=["Endpoints", "Examples"],
    tutorials=["Video", "Text"],
    faqs=["General", "Technical"],
)

typed_maintenance_prompt = TypedMaintenancePrompt(
    title="Maintenance",
    description="Maintain and update the system.",
    monitoring_metrics=["CPU Usage", "Error Rate"],
    update_schedule="Monthly",
    patching_policy="Security First",
    support_channels=["Email", "Chat"],
    user_feedback_mechanisms=["Survey", "Reviews"],
)

from dataclasses import fields
from pathlib import Path
from typing import Any, Dict, Union

from fgn.core.broker import Broker, Receipt


_DEFAULT_PROMPTS = (
    typed_requirement_analysis_prompt,
    typed_design_architecture_prompt,
    typed_build_core_components_prompt,
    typed_implement_business_logic_prompt,
    typed_testing_prompt,
    typed_deployment_prompt,
    typed_documentation_prompt,
    typed_maintenance_prompt,
)
_ALLOWED_PROMPT_CLASSES = {type(prompt).__name__: type(prompt) for prompt in _DEFAULT_PROMPTS}


def _prompt_params(prompt: TypedPrompt) -> dict[str, Any]:
    excluded = {"output", "env", "chat_inst", "source"}
    return {
        item.name: getattr(prompt, item.name)
        for item in fields(prompt)
        if item.init and item.name not in excluded
    }


def build_default_chain_data() -> dict[str, dict[str, Any]]:
    """Return the serializable, admitted default prompt chain."""
    return {
        type(prompt).__name__: {"params": _prompt_params(prompt)}
        for prompt in _DEFAULT_PROMPTS
    }


def write_default_chain(
    file_path: str | Path = "chain.yaml", *, broker: Broker | None = None
) -> Receipt:
    payload = yaml.safe_dump(build_default_chain_data(), sort_keys=True)
    return (broker or Broker()).write_text(file_path, payload)


def load_yaml_dsl(file_path: str | Path) -> Dict[str, Any]:
    return yaml.safe_load(Path(file_path).read_text(encoding="utf-8")) or {}


def execute_chain(chain: Dict[str, Any]) -> Dict[str, Union[str, dict, Optional[str]]]:
    """Execute only admitted TypedPrompt classes from a parsed YAML chain."""
    results: dict[str, Union[str, dict, Optional[str]]] = {}
    for class_name, config in chain.items():
        prompt_class = _ALLOWED_PROMPT_CLASSES.get(class_name)
        if prompt_class is None:
            raise ValueError(f"REFUSED:UNADMITTED_PROMPT_CLASS:{class_name}")
        params = config.get("params", {})
        if not isinstance(params, dict):
            raise TypeError(f"params for {class_name} must be a mapping")
        prompt = prompt_class(**params)
        results[class_name] = prompt()
    return results


def get_module_path() -> str:
    return str(Path(__file__).resolve().parent)


if __name__ == "__main__":
    receipt = write_default_chain()
    print(f"chain receipt={receipt.receipt_id} status={receipt.status}")
