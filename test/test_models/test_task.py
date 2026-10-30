import pytest

from lorgs.models.task import Task


pytestmark = pytest.mark.skip(reason="needs a Redis on localhost:6379")


def test_create_task():
    task = Task(
        task_id="debug1",
    )
    task.save()


def test_get_task():
    task = Task.get(task_id="debug1")
    print(task)


if __name__ == "__main__":
    test_create_task()
    # test_get_task()
