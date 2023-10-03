Feature: Test Matrix Factory
  Scenario Outline: Create a new project
    Given a project name "<project_name>"
    And the target directory "<target_directory>"
    And the repo url "<repo_url>"
    When I run the Matrix Factory with cookiecutter
    Then a new Flask project should be created

    Examples:
    | project_name    | target_directory          | repo_url                                         |
    | my_new_project  | /tmp/matrix_factory_output| https://github.com/cookiecutter-flask/cookiecutter-flask |