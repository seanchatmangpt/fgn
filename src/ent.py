import yaml
from typing import Dict, List


def get_value_objects_and_entities(yaml_data: str) -> (Dict[str, List[str]], Dict[str, List[str]]):
    data = yaml.safe_load(yaml_data)
    value_objects = {item['name']: list(item['properties'].keys()) for item in data['value_objects']}
    entities = {item['name']: list(item['properties'].keys()) for item in data['entities']}

    return value_objects, entities


# YAML data as a string
yaml_data = '''
value_objects:
  - name: RepositoryDetail
    properties:
      path: str
      branch: str
      commits: List[str]
      tags: List[str]
  - name: TestingStrategy
    properties:
      type: str
      tools: List[str]
  - name: AutomationTool
    properties:
      name: str
      version: str
  - name: SecurityProtocol
    properties:
      name: str
      encryption_type: str
  - name: RecoveryPlan
    properties:
      strategy: str
      backup_location: str
  - name: ScalabilityConfig
    properties:
      scale_type: str
      instances: int
  - name: ComplianceStandard
    properties:
      standard_name: str
      jurisdiction: str
  - name: UserInterfaceDetail
    properties:
      platform: str
      technology_stack: List[str]
  - name: EthicalConsideration
    properties:
      description: str
      compliance_level: str
  - name: DataManagementPolicy
    properties:
      storage_type: str
      retention_period: str
  - name: QualityMetric
    properties:
      metric_name: str
      threshold: str
  - name: LanguageSupport
    properties:
      language: str
      region: str
  - name: EnvironmentDetail
    properties:
      name: str
      variables: Dict[str, str]
  - name: CollaborationTool
    properties:
      tool_name: str
      version: str
  - name: AccessibilityStandard
    properties:
      standard_name: str
      compliance_level: str
  - name: IntegrationDetail
    properties:
      system_name: str
      connection_type: str
  - name: Benchmark
    properties:
      metric: str
      value: float
  - name: AnalyticMetric
    properties:
      name: str
      formula: str
  - name: AcademicContributionType
    properties:
      contribution_type: str
      details: str

entities:
  - name: ResearchComponent
    properties:
      research_topics: List[ResearchTopic]
      methodology: Methodology
      findings: List[ResearchFinding]
      collaborators: List[Researcher]
  - name: CICDPipeline
    properties:
      stages: List[Stage]
      tools: List[Tool]
      build_information: BuildInformation
      deployment_information: DeploymentInformation
  - name: LoggingMonitoring
    properties:
      logging_frameworks: List[LoggingFramework]
      monitoring_tools: List[MonitoringTool]
      alerting_rules: List[AlertRule]
  - name: Security
    properties:
      authentication_methods: List[AuthenticationMethod]
      authorization_levels: List[AuthorizationLevel]
      encryption_types: List[EncryptionType]
      security_policies: List[SecurityPolicy]
  - name: DisasterRecovery
    properties:
      plan: DisasterRecoveryPlan
      backup_frequencies: List[BackupFrequency]
      recovery_strategies: List[RecoveryStrategy]
  - name: Scalability
    properties:
      horizontal_scaling: HorizontalScaling
      vertical_scaling: VerticalScaling
      auto_scaling_rules: List[AutoScalingRule]
  - name: Compliance
    properties:
      regulations: List[Regulation]
      audits: List[Audit]
      compliance_documents: List[ComplianceDocument]
  - name: UserInterface
    properties:
      ui_frameworks: List[UIFramework]
      user_experience_ratings: List[Rating]
      usability_tests: List[UsabilityTest]
  - name: Ethics
    properties:
      ethical_guidelines: List[EthicalGuideline]
      ethical_reviews: List[EthicalReview]
      ethical_committees: List[EthicalCommittee]
  - name: DataManager
    properties:
      databases: List[Database]
      data_sources: List[DataSource]
      data_transformations: List[Transformation]
  - name: QualityAssurance
    properties:
      testing_strategies: List[TestingStrategy]
      quality_metrics: List[QualityMetric]
      quality_reports: List[QualityReport]
  - name: Internationalization
    properties:
      supported_languages: List[Language]
      translation_services: List[TranslationService]
      localization_rules: List[LocalizationRule]
  - name: EnvironmentConfig
    properties:
      environment_variables: Dict[str, EnvironmentVariable]
      configuration_files: List[ConfigurationFile]
  - name: Collaboration
    properties:
      collaboration_tools: List[CollaborationTool]
      team_members: List[TeamMember]
      communication_channels: List[CommunicationChannel]
  - name: Accessibility
    properties:
      accessibility_standards: List[AccessibilityStandard]
      accessibility_tests: List[AccessibilityTest]
      assistive_technologies: List[AssistiveTechnology]
  - name: SystemIntegration
    properties:
      integration_points: List[IntegrationPoint]
      integration_patterns: List[IntegrationPattern]
      external_systems: List[ExternalSystem]
  - name: Benchmarking
    properties:
      benchmarks: List[Benchmark]
      performance_metrics: List[PerformanceMetric]
      comparative_analyses: List[ComparativeAnalysis]
  - name: Analytics
    properties:
      analytics_tools: List[AnalyticsTool]
      tracked_metrics: List[TrackedMetric]
      analytic_reports: List[AnalyticReport]
  - name: AcademicContribution
    properties:
      publications: List[Publication]
      conferences_attended: List[Conference]
      awards: List[Award]
      academic_partnerships: List[Partnership]
'''

value_objects, entities = get_value_objects_and_entities(yaml_data)
print("Value Objects:", value_objects)
print("Entities:", entities)

from collections import defaultdict
from typing import Dict, List


def parse_references(entities: Dict[str, List[str]], value_objects: Dict[str, List[str]]) -> (Dict[str, List[str]], List[str], List[str]):
    value_objects_references = defaultdict(list)
    missing_value_objects = []
    unreferenced_value_objects = set(value_objects.keys())

    for entity_name, properties in entities.items():
        for prop in properties:
            found = False
            for value_object_name, value_object_properties in value_objects.items():
                if prop in value_object_properties:
                    value_objects_references[value_object_name].append(entity_name)
                    found = True
                    unreferenced_value_objects.discard(value_object_name)
                    break

            if not found:
                missing_value_objects.append((entity_name, prop))

    return value_objects_references, missing_value_objects, list(unreferenced_value_objects)

def change_entities_to_reference_value_objects(entities: Dict[str, List[str]], value_objects_references: Dict[str, List[str]]):
    for value_object_name, referencing_entities in value_objects_references.items():
        for entity_name in referencing_entities:
            entities[entity_name] = [value_object_name if prop == value_object_name else prop for prop in entities[entity_name]]

value_objects_references, missing_value_objects, unreferenced_value_objects = parse_references(entities, value_objects)
change_entities_to_reference_value_objects(entities, value_objects_references)

print("Entities referencing value objects:", value_objects_references)
print("Missing value objects in entities:", missing_value_objects)
print("Unreferenced value objects:", unreferenced_value_objects)
