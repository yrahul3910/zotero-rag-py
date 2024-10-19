import traceback

from abc import ABC, abstractmethod
from typing import Any, Optional

from loguru import logger


class Task[T](ABC):
    def __init__(self, name: str):
        self.name = name
        self._chain_index: Optional[int] = None

    @abstractmethod
    def run(self) -> Optional[T]: ...


class Chain[T, U](Task[T]):
    def __init__(self, *tasks: Task[Any], name: str):
        super().__init__(name)
        self.tasks = list(tasks)

        for i in range(len(self.tasks)):
            self.tasks[i]._chain_index = i

        self.task_outputs = {}

    def run(self) -> Optional[T]:
        result = None
        for task in self.tasks:
            try:
                result = task.run()
                self.task_outputs[task.name] = result
            except Exception as e:
                logger.error(f"Task {task.name} failed: {e}")
                logger.error(traceback.format_exc())

        return result

    def __irshift__(self, other: Task[U]) -> None:
        other._chain_index = len(self.tasks)
        self.tasks.append(other)
