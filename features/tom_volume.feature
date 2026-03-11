Feature: System Control via Voice (Tom Mode)
  As a user
  I want to control system settings using voice commands
  So that I don't need to use a mouse or keyboard

  Scenario Outline: Change system volume to specific level
    Given the assistant is in "Tom" mode
    When I say the command "Гучність <level>"
    Then the system volume should be set to <expected_vol>

    Examples:
      | level | expected_vol |
      | 50    | 50           |
      | 0     | 0            |
      | 100   | 100          |

  Scenario: Invalid volume command protection
    Given the assistant is in "Tom" mode
    When I say the command "Гучність 200"
    Then the system volume should remain unchanged
    And the assistant should say "Рівень має бути від 0 до 100"