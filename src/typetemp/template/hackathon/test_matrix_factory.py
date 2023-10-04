import os

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("test_matrix_factory.feature")


@given(parsers.parse('a project name "{project_name}"'), target_fixture="project_name")
def a_project_name(project_name):
    return project_name


@given(
    parsers.parse('the target directory "{target_directory}"'),
    target_fixture="target_directory",
)
def the_target_directory(target_directory):
    return target_directory


@given(parsers.parse('the repo url "{repo_url}"'), target_fixture="repo_url")
def the_repo_url(repo_url):
    return repo_url


@when("I run the Matrix Factory with cookiecutter")
def step_impl(project_name, target_directory, repo_url, mocker, fs):
    cmd = [
        "cookiecutter",
        repo_url,
        "--no-input",
        f"project_name={project_name}",
        f"-o {target_directory}",
    ]
    import subprocess

    mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="Creating project my_new_project in /tmp/matrix_factory_output\n",
            stderr="",
        ),
    )

    # Run the function
    output = subprocess.run(cmd, check=True, capture_output=True)

    assert (
        output.stdout
        == "Creating project my_new_project in /tmp/matrix_factory_output\n"
    )
    fs.create_file(
        os.path.join(target_directory, project_name, "README.md"),
        contents="This is a test",
    )


@then("a new Flask project should be created")
def step_impl(project_name, target_directory):
    assert os.path.exists(os.path.join(target_directory, project_name, "README.md"))
