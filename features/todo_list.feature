Feature: To-Do List Manager
    As a user
    I want to manage my tasks
    So that I can organize my daily activities

    # Scenario 1
    @add
    Scenario: Add a new task to the to-do list
        Given I have an empty to-do list
        When I add a task with title "Buy groceries"
        Then the task should be added to the list

    # Scenario 2
    @list
    Scenario: List all tasks in the to-do list
        Given I have a to-do list with 3 tasks
        When I request to list all tasks
        Then I should see 3 tasks displayed

    # Scenario 3
    @mark
    Scenario: Mark a task as completed
        Given I have a to-do list with task "Complete assignment"
        When I mark the task as completed
        Then the task status should be "completed"

    # Scenario 4
    @details
    Scenario: List tasks with detailed information
        Given I have a to-do list with tasks containing all attributes
        When I request to list tasks with details
        Then I should see all task attributes displayed

    # Scenario 5
    @invalidMarkS
    Scenario: Attempt to mark non-existent task as completed
        Given I have a to-do list with 2 tasks
        When I try to mark task number 5 as completed
        Then I should receive an error message

    # Scenario 6
    @filter
    Scenario: List tasks filtered by priority
        Given I have tasks with different priorities
        When I filter tasks by "High" priority
        Then I should see only high priority tasks
