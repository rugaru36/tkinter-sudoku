from tkinter import NSEW, Button, Tk

from presentation.locales.locale_manager import Locale_Info


class Locale_Select_Screen:
    def __init__(self, locale_info_list: list[Locale_Info]) -> None:
        self._root_widget: Tk | None = None
        self._selected_locale: str | None = None
        self._locale_info_list: list[Locale_Info] = locale_info_list

    def run(self):
        self._selected_locale = None
        self._show()
        return self._selected_locale

    def _show(self):
        window = Tk()
        window.resizable(False, False)

        window.title("")
        row = 0
        for locale_info in self._locale_info_list:
            btn = Button(text=locale_info.name,
                              command=lambda code=locale_info.code: self._on_select(code))
            btn.grid(row=row, column=0, columnspan=10, ipadx=100,
                          ipady=6, padx=4, pady=4, sticky=NSEW)
            row += 1

        self._root_widget = window
        window.mainloop()

    def _on_select(self, locale: str):
        self._selected_locale = locale
        self._destroy_root_widget()

    def _destroy_root_widget(self):
        if self._root_widget is not None:
            self._root_widget.destroy()
