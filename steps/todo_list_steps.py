# features/steps/todo_steps.py
from behave import given, when, then
from datetime import datetime, date
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import the classes from the original file
# Note: You need to save the original code as todo_list_app.py or adjust the import
from todo_list import TodoListManager, Task


@given('I have an empty to-do list')
def step_empty_todo_list(context):
    context.todo_manager = TodoListManager()


@given('I have a to-do list with {count:d} tasks')
def step_todo_list_with_tasks(context, count):
    context.todo_manager = TodoListManager()
    for i in range(count):
        context.todo_manager.add_task(f"Task {i + 1}", f"Description {i + 1}", "Medium")


@given('I have a to-do list with task "{task_title}"')
def step_todo_list_with_specific_task(context, task_title):
    context.todo_manager = TodoListManager()
    context.todo_manager.add_task(task_title, "Test description", "Medium")


@given('I have a to-do list with tasks containing all attributes')
def step_todo_list_with_full_attributes(context):
    context.todo_manager = TodoListManager()
    context.todo_manager.add_task(
        "Complete project",
        "Finish the to-do list application",
        "High",
        date(2024, 12, 31)
    )
    context.todo_manager.add_task(
        "Review code",
        "Code review session",
        "Medium",
        date(2024, 12, 15)
    )


@given('I have tasks with different priorities')
def step_tasks_with_different_priorities(context):
    context.todo_manager = TodoListManager()
    context.todo_manager.add_task("High priority task", "Urgent task", "High")
    context.todo_manager.add_task("Medium priority task", "Normal task", "Medium")
    context.todo_manager.add_task("Low priority task", "Later task", "Low")
    context.todo_manager.add_task("Another high priority", "Also urgent", "High")


@when('I add a task with title "{title}"')
def step_add_task(context, title):
    context.todo_manager.add_task(title, "Test description", "Medium")


@when('I request to list all tasks')
def step_list_all_tasks(context):
    context.listed_tasks = context.todo_manager.tasks


@when('I mark the task as completed')
def step_mark_task_completed(context):
    if context.todo_manager.tasks:
        context.todo_manager.mark_completed(1)


@when('I request to list tasks with details')
def step_list_tasks_with_details(context):
    context.detailed_tasks = context.todo_manager.tasks


@when('I try to mark task number {task_num:d} as completed')
def step_mark_invalid_task(context, task_num):
    context.error_occurred = False
    context.initial_completed_count = sum(1 for task in context.todo_manager.tasks if task.completed)

    # Capture the output to detect error message
    import io
    from contextlib import redirect_stdout

    captured_output = io.StringIO()
    with redirect_stdout(captured_output):
        context.todo_manager.mark_completed(task_num)

    output = captured_output.getvalue()
    context.final_completed_count = sum(1 for task in context.todo_manager.tasks if task.completed)

    # Check if error occurred (no change in completed count or error message)
    if "inválido" in output or context.initial_completed_count == context.final_completed_count:
        context.error_occurred = True
        context.error_message = output.strip()


@when('I filter tasks by "{priority}" priority')
def step_filter_by_priority(context, priority):
    context.filtered_tasks = [task for task in context.todo_manager.tasks
                              if task.priority.lower() == priority.lower()]


@then('the task should be added to the list')
def step_task_added_to_list(context):
    assert len(context.todo_manager.tasks) > 0, "No tasks found in the list"
    assert context.todo_manager.tasks[0].title == "Buy groceries", "Task title doesn't match"


@then('the task should have status "{status}"')
def step_task_has_status(context, status):
    task = context.todo_manager.tasks[0]
    if status == "pending":
        assert not task.completed, f"Task should be pending but is completed"
    elif status == "completed":
        assert task.completed, f"Task should be completed but is pending"


@then('I should see {count:d} tasks displayed')
def step_see_tasks_displayed(context, count):
    assert len(context.listed_tasks) == count, f"Expected {count} tasks, got {len(context.listed_tasks)}"


@then('each task should show its title and status')
def step_tasks_show_title_and_status(context):
    for task in context.listed_tasks:
        assert hasattr(task, 'title'), "Task should have title attribute"
        assert hasattr(task, 'completed'), "Task should have completed status"
        assert task.title, "Task title should not be empty"


@then('the task status should be "{status}"')
def step_task_status_should_be(context, status):
    task = context.todo_manager.tasks[0]
    if status == "completed":
        assert task.completed, "Task should be marked as completed"
    elif status == "pending":
        assert not task.completed, "Task should be pending"


@then('the task should have a completion timestamp')
def step_task_has_completion_timestamp(context):
    task = context.todo_manager.tasks[0]
    assert task.completed_at is not None, "Task should have completion timestamp"
    assert isinstance(task.completed_at, datetime), "Completion timestamp should be datetime object"


@then('I should see all task attributes displayed')
def step_see_all_task_attributes(context):
    for task in context.detailed_tasks:
        assert hasattr(task, 'title'), "Task should have title"
        assert hasattr(task, 'description'), "Task should have description"
        assert hasattr(task, 'priority'), "Task should have priority"
        assert hasattr(task, 'due_date'), "Task should have due_date"
        assert hasattr(task, 'created_at'), "Task should have created_at"
        assert hasattr(task, 'completed'), "Task should have completed status"


@then('the attributes should include title, description, priority, due date, and timestamps')
def step_attributes_include_required_fields(context):
    task = context.detailed_tasks[0]
    assert task.title, "Title should not be empty"
    assert task.description, "Description should not be empty"
    assert task.priority in ["High", "Medium", "Low"], "Priority should be valid"
    assert task.due_date, "Due date should not be empty"
    assert task.created_at, "Created timestamp should not be empty"


@then('I should receive an error message')
def step_receive_error_message(context):
    assert context.error_occurred, "Expected an error to occur"


@then('no task should be marked as completed')
def step_no_task_marked_completed(context):
    assert context.initial_completed_count == context.final_completed_count, \
        "No additional tasks should be marked as completed"


@then('I should see only high priority tasks')
def step_see_only_high_priority_tasks(context):
    assert len(context.filtered_tasks) > 0, "Should find high priority tasks"
    for task in context.filtered_tasks:
        assert task.priority == "High", f"Task priority should be High, got {task.priority}"


@then('the list should exclude medium and low priority tasks')
def step_exclude_other_priorities(context):
    all_tasks = context.todo_manager.tasks
    non_high_priority_tasks = [task for task in all_tasks if task.priority != "High"]
    assert len(non_high_priority_tasks) > 0, "Should have non-high priority tasks for testing"

    for task in context.filtered_tasks:
        assert task.priority == "High", "Filtered list should only contain high priority tasks"