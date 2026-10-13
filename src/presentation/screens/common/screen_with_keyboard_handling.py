from tkinter import Event, Tk
from typing import Callable, Final, Literal, cast, get_args

from lib.string import safe_str_to_int

ArrowKeysSymLiteral = Literal["Down", "Up", "Left", "Right"]


class Custom_Key_Combination_Binding:
    def __init__(self, binding: str, handler: Callable[[Event], None]):
        self.key: str = binding
        self.handler: Final = handler


class ScreenWithKeyboardHandling:
    def _bind_default_key_handler(self, root: Tk):
        _ = root.bind("<Key>", self._key_handler)

    def _bind_custom_combination_handler(self, root: Tk, custom_combination_binding: Custom_Key_Combination_Binding):
        _ = root.bind(custom_combination_binding.key,
                      custom_combination_binding.handler)

    def _key_handler(self, event: Event):
        print(event.char, event.keysym, event.keycode)
        input_num = safe_str_to_int(event.char)
        if input_num is not None:
            self._handle_num_key(input_num)
        elif event.keysym in get_args(ArrowKeysSymLiteral):
            self._handle_arrow_key(cast(ArrowKeysSymLiteral, event.keysym))
        elif event.keysym in ["Return", "KP_Enter"]:
            self._handle_enter_key()
        elif event.keysym == "Escape":
            self._handle_escape_key()
        elif event.char != "":
            self._handle_char_input(event.char)
        else:
            self._handle_other_keys()

    def _handle_num_key(self, _num: int):
        pass

    def _handle_arrow_key(self, _direction: ArrowKeysSymLiteral):
        pass

    def _handle_char_input(self, _char: str):
        pass

    def _handle_enter_key(self):
        pass

    def _handle_escape_key(self):
        pass

    def _handle_other_keys(self):
        pass
