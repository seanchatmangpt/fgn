Feature: Data Mastery
  Prize: $3,500

  Scenario: Perform data imputation
    Given missing data
    When the imputation algorithm runs
    Then the dataset should be complete

  Scenario: Label data
    Given unlabelled data
    When a labeling algorithm runs
    Then the dataset should be labelled

  Scenario: Sort data
    Given unordered data
    When the sorting algorithm runs
    Then the data should be sorted

