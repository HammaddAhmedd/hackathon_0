#!/usr/bin/env python3
"""
AI Employee Task Planning Workflow

This script monitors the vault/Inbox directory for new tasks and creates
detailed plan files according to the specified format when a new task appears.
"""

import os
import time
from datetime import datetime
from pathlib import Path
import json
import shutil


def create_plan_file(task_content, task_filename):
    """Create a detailed plan file based on the task content."""

    # Generate timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_filename = f"Plan_{timestamp}.md"
    plan_filepath = Path("vault/Needs_Action") / plan_filename

    # Create the plan content
    plan_content = f"""# Task Plan

## Original Task
{task_content}

## Objective
Provide a clear, actionable objective based on the original task.

## Step-by-Step Plan
1.
2.
3.
4.
5.

## Priority
[High/Medium/Low]

## Requires Human Approval?
[Yes/No]

## Suggested Output
Describe the expected deliverables or outcomes from completing this task.
"""

    # Create the directory if it doesn't exist
    plan_filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write the plan file
    with open(plan_filepath, 'w', encoding='utf-8') as f:
        f.write(plan_content)

    print(f"Created plan file: {plan_filepath}")
    return plan_filepath


def monitor_inbox():
    """Monitor the vault/Inbox directory for new tasks."""

    inbox_dir = Path("vault/Inbox")
    processed_tasks_dir = Path("vault/Processed_Tasks")

    # Create directories if they don't exist
    inbox_dir.mkdir(parents=True, exist_ok=True)
    processed_tasks_dir.mkdir(parents=True, exist_ok=True)

    print(f"Monitoring {inbox_dir} for new tasks...")

    while True:
        # Look for task files in the inbox
        task_files = list(inbox_dir.glob("*"))

        for task_file in task_files:
            if task_file.is_file():
                try:
                    # Read the task content
                    with open(task_file, 'r', encoding='utf-8') as f:
                        task_content = f.read()

                    print(f"Found new task: {task_file.name}")

                    # Create the plan file
                    plan_filepath = create_plan_file(task_content, task_file.name)

                    # Move the original task to processed directory
                    processed_task_path = processed_tasks_dir / task_file.name
                    shutil.move(str(task_file), str(processed_task_path))

                    print(f"Task processed. Plan created: {plan_filepath}")
                    print(f"Original task moved to: {processed_task_path}")

                except Exception as e:
                    print(f"Error processing task {task_file}: {str(e)}")

        # Wait before checking again
        time.sleep(5)


def process_single_task(task_path):
    """Process a single task file and create a plan."""
    task_path = Path(task_path)

    if not task_path.exists():
        raise FileNotFoundError(f"Task file does not exist: {task_path}")

    # Read the task content
    with open(task_path, 'r', encoding='utf-8') as f:
        task_content = f.read()

    print(f"Processing task: {task_path.name}")

    # Create the plan file
    plan_filepath = create_plan_file(task_content, task_path.name)

    print(f"Plan created: {plan_filepath}")

    return plan_filepath


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Process a single file if provided as argument
        task_file = sys.argv[1]
        try:
            plan_path = process_single_task(task_file)
            print(f"\nPlan file created successfully: {plan_path}")
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    else:
        # Monitor the inbox directory continuously
        try:
            monitor_inbox()
        except KeyboardInterrupt:
            print("\nStopping task planner...")