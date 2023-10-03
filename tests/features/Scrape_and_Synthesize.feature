Feature: Scrape and Synthesize
  Prize: $3,500

  Scenario: Scrape data from the web
    Given a valid URL
    When the scraper runs
    Then the data should be saved locally

  Scenario: Create datasets
    Given raw data
    When data cleaning is done
    Then a clean dataset should be created

  Scenario: Create summaries and plans
    Given a dataset
    When an analysis is performed
    Then summaries and plans should be generated

