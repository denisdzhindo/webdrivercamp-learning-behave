Feature: Target Gifts
  Background:
    Given Navigate to https://www.target.com/

  Scenario: Navigate to the page
    # like all Scenarios uses Background

  Scenario: Search for gifts
    When Search for gift ideas

  Scenario Outline: Verify searched page's headers
    When Search for <searched item>
    Then Verify header of the page contains <searched item>

    Examples:
      | searched item |
      | iphone        |
      | gift ideas    |
