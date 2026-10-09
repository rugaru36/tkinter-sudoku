
from typing import Final, Generic, TypeVar, Callable
from tkinter import NSEW, Button, Event, Tk

from lib.string import safe_str_to_int


OptionType = TypeVar('OptionType', str, bool, int)


class Option(Generic[OptionType]):
    def __init__(self, name: str, value: OptionType) -> None:
        self.name: Final = name
        self.value: Final = value


class SelectOptionScreen(Generic[OptionType]):
    def __init__(self, get_text_cb: Callable[[str], str], title_name: str, options: list[Option[OptionType]]) -> None:
        self._root_widget: Tk | None = None
        self._value: OptionType | None = None
        self._options: Final = options
        self._get_text_cb: Final = get_text_cb
        self._title_name: Final = title_name
        self._buttons: list[Button] = []
        self._focus_index: int = -1

    def run(self) -> OptionType | None:
        self._value = None
        self._show()
        return self._value

    def _show(self):
        window = Tk()
        window.resizable(False, False)

        window.title(self._get_text_cb(self._title_name))

        row = 0
        for option in self._options:
            btn = Button(text=f"{row + 1}. " + self._get_text_cb(option.name),
                         command=lambda value=option.value: self._on_select(value))
            btn.grid(row=row, column=0, columnspan=10, ipadx=100,
                     ipady=6, padx=4, pady=4, sticky=NSEW)
            row = row + 1
            self._buttons.append(btn)

        _ = window.bind("<Key>", self._key_handler)

        self._root_widget = window
        window.mainloop()

    def _key_handler(self, event: Event):
        print(event.char, event.keysym, event.keycode)
        arrow_keysyms = ["Down", "Up"]
        arrow_select_keysyms = ["Return", "KP_Enter"]

        input_num = safe_str_to_int(event.char)
        if input_num is not None:
            self._handle_num_key(input_num)
        elif event.keysym in arrow_keysyms:
            self._handle_arrow_key(event.keysym)
        elif event.keysym in arrow_select_keysyms:
            self._on_select(self._options[self._focus_index].value)

    def _handle_num_key(self, input_num: int):
        if input_num > len(self._options):
            print("Too big num!")
            return
        index = input_num - 1
        selected_option = self._options[index]
        print(selected_option.name)
        self._on_select(selected_option.value)

    def _handle_arrow_key(self, keysym: str):
        new_focus_index = self._focus_index
        if keysym == "Down":
            new_focus_index = self._focus_index + 1
        elif keysym == "Up":
            new_focus_index = self._focus_index - 1
        if new_focus_index > (len(self._options) - 1) or new_focus_index < 0:
            return
        self._buttons[new_focus_index].focus()
        self._focus_index = new_focus_index

    def _on_select(self, new_value: OptionType):
        self._value = new_value
        self._destroy_root_widget()

    def _destroy_root_widget(self):
        if self._root_widget is not None:
            self._root_widget.destroy()
