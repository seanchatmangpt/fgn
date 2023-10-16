Feature: Peq - Advanced Python Module Management

Scenario: Initialize Peq with an existing module
    Given there is a hello_module.py with content def hello(): return "Hello, World!"
    When I initialize Peq with filepath hello_module.py
    Then the module should be loaded into Peq
    And I should be able to access the hello function
    And the hello function should return "Hello, World!"

