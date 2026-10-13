from tkinter import Tk
from typing import Annotated, Literal, override

from presentation.screens.common.screen_with_keyboard_handling import ArrowKeysSymLiteral, ScreenWithKeyboardHandling

SelectionSize = Annotated[list[int], 2]
Coordinates = SelectionSize


class ScreenWithKeyboardElementSelection(ScreenWithKeyboardHandling):
    def __init__(self, selection_sizes: SelectionSize):
        self._is_any_element_focused: bool = False
        self._selection_sizes: SelectionSize = selection_sizes
        self._focused_element_index: Coordinates = [0, 0]
        self._dummy_focus_element: Tk | None = None

    def _bind_dummy_for_focus(self, dummy_element: Tk):
        self._dummy_focus_element = dummy_element

    def _focus_element_needed_to_focus(self):
        pass

    @override
    def _handle_escape_key(self):
        if self._dummy_focus_element:
            self._dummy_focus_element.focus()
        self._selection_sizes = [0, 0]
        self._is_any_element_focused = False

    @override
    def _handle_arrow_key(self, direction: ArrowKeysSymLiteral):
        hor_or_vert: Literal["horizontal", "vertical"] | None = None
        new_index: None | int = None

        if direction == "Right":
            new_index = self._focused_element_index[0] + 1
            hor_or_vert = "horizontal"
        elif direction == "Left":
            new_index = self._focused_element_index[0] - 1
            hor_or_vert = "horizontal"
        elif direction == "Down":
            new_index = self._focused_element_index[1] + 1
            hor_or_vert = "vertical"
        elif direction == "Up":
            new_index = self._focused_element_index[1] - 1
            hor_or_vert = "vertical"

        if hor_or_vert == "horizontal" and self._selection_sizes[0] == 0:
            return
        elif hor_or_vert == "vertical" and self._selection_sizes[1] == 0:
            return

        if not self._is_any_element_focused:
            self._focus_element_needed_to_focus()
            self._is_any_element_focused = True
            return

        if hor_or_vert == "horizontal" and new_index == self._selection_sizes[0]:
            new_index = 0
        elif hor_or_vert == "vertical" and new_index == self._selection_sizes[1]:
            new_index = 0
        elif hor_or_vert == "horizontal" and new_index == -1:
            new_index = self._selection_sizes[0] - 1
        elif hor_or_vert == "vertical" and new_index == -1:
            new_index = self._selection_sizes[1] - 1

        if hor_or_vert == "horizontal" and self._focused_element_index[1] == -1:
            return
        if hor_or_vert == "horizontal" and new_index < self._selection_sizes[0] and new_index >= 0:
            self._focused_element_index[0] = new_index
        elif hor_or_vert == "vertical" and new_index < self._selection_sizes[1] and new_index >= -1:
            self._focused_element_index[1] = new_index

        self._focus_element_needed_to_focus()
