from tkinter import EW, Button, Entry, Label, Tk
from typing import Callable, Final
from tkinter.messagebox import showwarning


class Validation_Types:
    only_digits: Final = "Only Digits"
    random_characters: Final = 'Random Characters'


class Value_Input_Screen:

    def __init__(self, cb_on_input: Callable[[str | None], None],) -> None:
        self._message_label_text: str = ''
        self._window_title_text: str = ''
        self._root_widget: Tk | None = None
        self._is_valid_value: bool = False
        self._value: str = ''
        self._message_label: Label | None = None
        self._cb_on_input: Callable[[str | None], None] = cb_on_input
        self._validation_type: str = Validation_Types.random_characters
        self._min_value_lenght: int = -1
        self._max_value_lenght: int = 99999999999
        pass

    def run(self,
            message_label_text: str,
            window_title_text: str,
            ):
        self._message_label_text = message_label_text
        self._window_title_text = window_title_text
        self._show()

    def set_validation_options(self, validation_type: str, min_length: int = -1, max_length: int = 99999999999):
        if min_length > max_length:
            raise ValueError("min_length > than max_length")
        self._validation_type = validation_type
        self._min_value_lenght = min_length
        self._max_value_lenght = max_length
        return self

    # True lets change input field value
    def _validate_value(self, value: str) -> bool:
        value_length = len(value)
        is_shorter_than_min = value_length < self._min_value_lenght
        is_longer_than_max = value_length > self._max_value_lenght
        is_empty = value_length == 0

        self._is_valid_value = not (is_shorter_than_min or is_longer_than_max)

        if is_empty and is_shorter_than_min:
            return True
        elif not self._is_valid_value:
            return False
        match self._validation_type:
            case Validation_Types.only_digits:
                is_valid_as_int = value.isnumeric()
                self._is_valid_value = is_valid_as_int
                if is_valid_as_int:
                    self._value = value
            case Validation_Types.random_characters:
                self._value = value
            case _:
                raise ValueError('unknown validation type: ' +
                                 self._validation_type)
        return self._is_valid_value

    def _show(self):
        window = Tk()
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", self._destroy_root_widget)
        window.title(self._window_title_text)

        message_label = Label(window, text=self._message_label_text)
        message_label.grid(row=0, column=0, columnspan=5,
                           ipadx=50, ipady=6, padx=4, pady=4, sticky=EW)

        entry = Entry(window,
                      justify="center",
                      validate="key",
                      validatecommand=(window.register(
                          self._validate_value), "%P")
                      )
        entry.focus()
        entry.grid(row=1, column=0, columnspan=5, ipadx=50,
                   ipady=6, padx=4, pady=4, sticky=EW)

        ok_btn = Button(window, text="Ok", command=self._on_ok)
        ok_btn.grid(row=2, column=0, columnspan=5, ipadx=50,
                    ipady=6, padx=4, pady=4, sticky=EW)

        self._root_widget = window
        self._message_label = message_label

        window.grab_set()

    def _on_ok(self):
        if self._is_valid_value and self._root_widget:
            self._destroy_root_widget()
            if self._cb_on_input is not None:
                self._cb_on_input(self._value)
        elif not self._is_valid_value:
            _ = showwarning("Error", "Value is invalid!")

    def _destroy_root_widget(self):
        if self._root_widget is None:
            return
        self._root_widget.grab_release()
        self._root_widget.destroy()
