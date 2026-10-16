from tkinter import Tk, Widget
from typing import Annotated, Final, Literal, TypeVar, override

from presentation.screens.common.screen_with_keyboard_handling import ArrowKeysSymLiteral, ScreenWithKeyboardHandling

SelectionSize = Annotated[list[int], 2]
Coordinates = SelectionSize

ElementType = TypeVar("ElementType")


class ScreenWithKeyboardElementSelection[ElementValueType](ScreenWithKeyboardHandling):
    def __init__(self, selection_sizes: SelectionSize, default_focus_coordinates: Coordinates | None = None):
        self._is_any_element_focused: bool = False
        self._selection_sizes: Final[Coordinates] = selection_sizes
        self._default_coordinates: Final[Coordinates] = [
            0, 0] if not default_focus_coordinates else default_focus_coordinates
        self._focused_element_index: Coordinates = self._default_coordinates
        self._dummy_focus_element: Widget | Tk | None = None

    def _bind_dummy_for_focus(self, dummy_element: Widget | Tk):
        self._dummy_focus_element = dummy_element

    def _get_element_needed_to_focus(self) -> Widget | None:
        return None

    def _check_coordinates_exist(self, row: int, col: int) -> bool:
        return True

    def _on_element_select(self, _new_value: ElementValueType):
        pass

    def _focus_element_needed_to_focus(self):
        element = self._get_element_needed_to_focus()
        if element:
            element.focus()

    def _restore_element_focus_to_default_state(self):
        if self._dummy_focus_element:
            self._dummy_focus_element.focus()
        self._focused_element_index = self._default_coordinates
        self._is_any_element_focused = False

    def _get_focused_element_value(self) -> ElementValueType | None:
        return None

    @override
    def _handle_escape_key(self):
        self._restore_element_focus_to_default_state()

    @override
    def _handle_arrow_key(self, direction: ArrowKeysSymLiteral):
        hor_or_vert: Literal["horizontal", "vertical"] | None = None
        new_row = self._focused_element_index[0]
        new_col = self._focused_element_index[1]

        match direction:
            case "Right":
                new_col = new_col + 1
                hor_or_vert = "horizontal"
            case "Left":
                new_col = new_col - 1
                hor_or_vert = "horizontal"
            case "Down":
                new_row = new_row + 1
                hor_or_vert = "vertical"
            case "Up":
                new_row = new_row - 1
                hor_or_vert = "vertical"

        if hor_or_vert == "horizontal" and self._selection_sizes[1] == 0:
            return
        elif hor_or_vert == "vertical" and self._selection_sizes[0] == 0:
            return

        if not self._is_any_element_focused:
            self._focus_element_needed_to_focus()
            self._is_any_element_focused = True
            return

        if not self._check_coordinates_exist(new_row, new_col):
            return

        if hor_or_vert == "horizontal" and new_col < self._selection_sizes[1] and new_col >= 0:
            self._focused_element_index[1] = new_col
        elif hor_or_vert == "vertical" and new_row < self._selection_sizes[0] and new_row >= 0:
            self._focused_element_index[0] = new_row

        self._focus_element_needed_to_focus()

    @override
    def _handle_enter_key(self):
        new_value = self._get_focused_element_value()
        if new_value:
            self._on_element_select(new_value)
