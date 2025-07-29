from tkinter import EW, Button, Entry, Label, PhotoImage, Toplevel
from typing import Callable


class Value_Input:
    def __init__(self) -> None:
        self._root_widget: Toplevel | None = None
        self._is_valid_value: bool = False
        self._value: int | None = None
        self._message_label: Label | None = None
        self._cb_on_input: Callable[[int | None], None] | None = None
        pass

    def run(self, cb_on_input: Callable[[int | None], None]):
        self._cb_on_input = cb_on_input
        self._show()

    def _validate_value(self, value: str) -> bool:
        is_valid = value.isdecimal() and len(value) <= 1
        self._is_valid_value = is_valid or (
            self._is_valid_value and len(value) > 0)
        if is_valid:
            self._value = int(value)
        return is_valid

    def _show(self):
        window = Toplevel()
        window.resizable(False, False)
        try:
            window.iconphoto(False, PhotoImage(file='icon.png'))
        except:
            print("problem while loading icon")
        window.protocol("WM_DELETE_WINDOW", self._destroy_root_widget)
        window.title("Input value")

        message_label = Label(window, text="Input value:")
        message_label.grid(row=0, column=0, columnspan=5,
                           ipadx=50, ipady=6, padx=4, pady=4, sticky=EW)

        entry = Entry(window,
                      justify="center",
                      validate="key",
                      validatecommand=(window.register(
                          self._validate_value), "%P")
                      )
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
        elif not self._is_valid_value and self._message_label:
            self._message_label["text"] = "Wrong value!"

    def _destroy_root_widget(self):
        if self._root_widget is None:
            return
        self._root_widget.grab_release()
        self._root_widget.destroy()
