import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk


def main():
    pass

class Application():
    def __init__(self) -> None:
        pass

class WorkFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.__observers: list[Observer] = []

    def add_observer(self, observer) -> None:
        self.__observers.append(observer)

    def notify_observer(self) -> None:
        for o in self.__observers:
            o.update(self)

class Observer(ABC):
    @abstractmethod
    def update(self, subject: WorkFrame) -> None:
        raise NotImplementedError

if __name__ == '__main__':
    main()