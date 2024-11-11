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

  Scenario: Gifts - Price validation
    When Search for gift ideas
    When Select Her in Who are you shopping for? section
    When Select Gifts under $15 in Great gifts for any budget section
    Then Collect all items on the first page into collected_items
    Then verify all collected results' price is < 15
      | context.collected.items |