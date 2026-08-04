
from typing import Final, Generic, TypeVar, Callable
from tkinter import NSEW, Button, Tk


option_type = TypeVar('option_type', str, bool, int)


class Option(Generic[option_type]):
    def __init__(self, name: str, value: option_type) -> None:
        self.name: Final = name
        self.value: Final = value


class Select_Option_Screen(Generic[option_type]):
    def __init__(self, get_text_cb: Callable[[str], str], title_name: str, options: list[Option[option_type]]) -> None:
        self._root_widget: Tk | None = None
        self._value: option_type | None = None
        self._options: Final = options
        self._get_text_cb: Final = get_text_cb
        self._title_name: Final = title_name

    def run(self) -> option_type | None:
        self._value = None
        self._show()
        return self._value

    def _show(self):
        window = Tk()
        window.resizable(False, False)

        window.title(self._get_text_cb(self._title_name))

        row = 0
        for option in self._options:
            btn = Button(text=self._get_text_cb(option.name),
                         command=lambda value=option.value: self._on_select(value))
            btn.grid(row=row, column=0, columnspan=10, ipadx=100,
                     ipady=6, padx=4, pady=4, sticky=NSEW)
            row = row + 1

        self._root_widget = window
        window.mainloop()

    def _on_select(self, new_value: option_type):
        self._value = new_value
        self._destroy_root_widget()

    def _destroy_root_widget(self):
        if self._root_widget is not None:
            self._root_widget.destroy()
