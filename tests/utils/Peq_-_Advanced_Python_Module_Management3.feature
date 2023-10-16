Feature: Peq - Advanced Python Module Management

    Scenario: Initialize Peq with a new module without an initial source
        Given there is no sample_module.py
        When I initialize Peq with filepath sample_module.py
        Then a new file sample_module.py should be created with content
        And the module should be loaded into Peq

    Scenario: Initialize Peq with an existing module
        Given there is a hello_module.py with content def hello(): pass
        When I initialize Peq with filepath hello_module.py
        Then the module should be loaded into Peq
        And I should be able to access the hello function

    Scenario: Adding a new function to the module
        Given Peq is initialized with sample_module.py
        When I add a function greet with content 'def greet(): return Hello, World!'
        Then the module should contain the greet function
        And calling greet should return Hello, World!

    Scenario: Overwriting an existing function
        Given Peq is initialized with sample_module.py containing a function greet
        When I set the function greet to 'def greet(): return Goodbye, World!'
        Then calling greet should return Goodbye, World!

    Scenario: Undoing a change
        Given Peq is initialized with sample_module.py
        And I have added a function greet
        When I call the undo method
        Then the function greet should no longer exist in the module

    Scenario: Redoing a change
        Given Peq is initialized with sample_module.py
        And I have added a function greet
        And I have undone the change
        When I call the redo method
        Then the function greet should exist in the module

    Scenario: Rolling back to a previous version with Git
        Given Peq is initialized with sample_module.py with git integration enabled
        And there are multiple commits in the git history
        When I call the rollback method with steps 2
        Then the sample_module.py should revert to its state from 2 commits ago

    Scenario: Running tests on the module
        Given Peq is initialized with sample_module.py
        And there are associated tests for the module
        When I call the test method
        Then the tests should be executed
        And I should receive feedback on their pass/fail status

    Scenario: Adding an asynchronous function to the module
        Given Peq is initialized with sample_module.py
        When I add an async function fetch_data with content 'async def fetch_data(): return Data fetched'
        Then the module should contain the async function fetch_data
        And calling fetch_data asynchronously should return Data fetched

    Scenario: Adding a new dictionary to the module
        Given Peq is initialized with sample_module.py
        When I add a dictionary DATA with the content '{ key: value }'
        Then the module should contain the dictionary DATA
        And accessing DATA[key] should return value

    Scenario: Overwriting an existing dictionary in the module
        Given Peq is initialized with sample_module.py containing a dictionary DATA
        When I set the dictionary DATA to '{ new_key: new_value }'
        Then accessing DATA[new_key] should return new_value
        And DATA should not have a key key

    Scenario: Adding an import statement to the module
        Given Peq is initialized with sample_module.py
        When I add an import import os
        Then the module should contain the import for os
        And I should be able to use the os library functionalities

    Scenario: Automatically handling duplicate imports
        Given Peq is initialized with sample_module.py containing an import for os
        When I add another import for os
        Then the module should still only have one import statement for os

    Scenario: Auto-importing required libraries
        Given Peq is initialized with sample_module.py
        When I add a function using datetime without manually importing it
        Then Peq should automatically import the datetime library
        And the module should contain the import for datetime

    Scenario: Adding a decorated function
        Given Peq is initialized with sample_module.py
        And I have added an import from functools import lru_cache
        When I add a decorated function cached_func with content @lru_cache
        Then the module should contain the decorated function cached_func
        And calling cached_func should return 42
