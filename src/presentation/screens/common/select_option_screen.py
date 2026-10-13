
from typing import Final, Generic, TypeVar, Callable, override
from tkinter import NSEW, Button, Tk

from presentation.screens.common.screen_with_keyboard_element_selection import ScreenWithKeyboardElementSelection
from presentation.screens.common.screen_with_keyboard_handling import ArrowKeysSymLiteral


OptionType = TypeVar('OptionType', str, bool, int)


class Option(Generic[OptionType]):
    def __init__(self, name: str, value: OptionType) -> None:
        self.name: Final = name
        self.value: Final = value


class SelectOptionScreen(Generic[OptionType], ScreenWithKeyboardElementSelection):
    def __init__(self, get_text_cb: Callable[[str], str], on_select_cb: Callable[[OptionType], None], title_name: str, options: list[Option[OptionType]]) -> None:
        self._value: OptionType | None = None
        self._options: Final = options
        self._get_text_cb: Final = get_text_cb
        self._on_select_cb: Final = on_select_cb
        self._title_name: Final = title_name
        self._buttons: list[Button] = []
        self._focus_index: int = 0
        self._root_widget: Tk | None = None
        super().__init__([0, len(options)])

    def run(self):
        self._value = None
        self._show()

    def _show(self):
        self._focus_index = 0
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

        self._bind_default_key_handler(window)
        self._buttons[self._focus_index].focus()
        self._root_widget = window

        window.mainloop()

    @override
    def _handle_num_key(self, input_num: int):
        if input_num > len(self._options):
            print("Too big num!")
            return
        index = input_num - 1
        selected_option = self._options[index]
        print(selected_option.name)
        self._on_select(selected_option.value)

    @override
    def _handle_arrow_key(self, direction: ArrowKeysSymLiteral):
        new_focus_index = self._focus_index
        if direction == "Down":
            new_focus_index = self._focus_index + 1
        elif direction == "Up":
            new_focus_index = self._focus_index - 1
        if new_focus_index > (len(self._options) - 1) or new_focus_index < 0:
            return
        self._buttons[new_focus_index].focus()
        self._focus_index = new_focus_index

    @override
    def _handle_enter_key(self):
        value = self._options[self._focus_index].value
        self._on_select(value)

    @override
    def _handle_escape_key(self):
        if self._root_widget:
            self._root_widget.focus()
        self._focus_index = 0

    def _on_select(self, new_value: OptionType):
        self._value = new_value
        self._destroy_root_widget()
        self._on_select_cb(new_value)

    def _destroy_root_widget(self):
        if self._root_widget:
            self._root_widget.destroy()
