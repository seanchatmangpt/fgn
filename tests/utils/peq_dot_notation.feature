Feature: Adding and accessing functions to Peq using dot notation

    Scenario: Adding a new function to the module using dot notation
        Given there is a sample_module.py with content ""
        When I initialize Peq with filepath sample_module.py
        Then I should be able to add the function greet using dot notation
        And calling greet should return Hello, World!
