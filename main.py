from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty
from kivy.clock import mainthread
from kivy.core.window import Window

from threading import Thread
from analyzer import analyze_doc

try:
    from plyer import filechooser
except Exception:
    filechooser = None

KV = """
#:import json json
Screen:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)

        Label:
            text: "Аналіз польотів з DOCX"
            font_size: '22sp'
            size_hint_y: None
            height: self.texture_size[1] + dp(6)
            bold: True

        Label:
            text: app.status_text
            size_hint_y: None
            height: self.texture_size[1] + dp(6)
            color: (0.7, 0.7, 0.7, 1)

        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(8)

            Button:
                text: "Обрати .docx"
                on_release: app.pick_file()

            Button:
                text: "Очистити"
                on_release: app.clear_results()

        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: results_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: dp(32)
                row_force_default: False
"""

class FlightAnalyzerApp(App):
    results = DictProperty({})
    status_text = StringProperty("Завантажте файл .docx для аналізу.")

    def build(self):
        self.title = "Аналіз DOCX польотів"
        try:
            Window.minimum_width, Window.minimum_height = (360, 640)
        except Exception:
            pass
        return Builder.load_string(KV)

    def clear_results(self):
        self.results = {}
        self.status_text = "Дані очищено. Оберіть новий файл."
        self.populate_results({})

    def pick_file(self):
        if filechooser is not None:
            filechooser.open_file(on_selection=self._on_file_chosen, filters=["*.docx'])
        else:
            self.status_text = "Файловий діалог недоступний."

    def _on_file_chosen(self, selections):
        if not selections:
            self.status_text = "Файл не обрано."
            return
        path = selections[0]
        self.status_text = f"Обрано файл: {path}. Виконується аналіз..."
        Thread(target=self._analyze_async, args=(path,), daemon=True).start()

    def _analyze_async(self, path):
        try:
            res = analyze_doc(path)
            self._apply_results(res)
        except Exception as e:
            self._apply_error(str(e))

    @mainthread
    def _apply_results(self, res):
        self.results = res or {}
        self.status_text = "Готово."
        self.populate_results(self.results)

    @mainthread
    def _apply_error(self, message):
        self.results = {}
        self.status_text = f"Помилка: {message}"
        self.populate_results({})

    def populate_results(self, res):
        grid = self.root.ids.results_grid
        grid.clear_widgets()

        if not res:
            from kivy.uix.label import Label
            grid.add_widget(Label(text="Немає результатів"))
            return

        from kivy.uix.label import Label
        from kivy.metrics import dp

        def add_section(title, items):
            grid.add_widget(Label(text=f"[b]{title}[/b]", markup=True, size_hint_y=None, height=dp(32)))
            if not items:
                grid.add_widget(Label(text="—", size_hint_y=None, height=dp(28)))
                return
            for k, v in items.items():
                grid.add_widget(Label(text=f"{k}: {v}", size_hint_y=None, height=dp(28)))

        add_section("Усього вильотів", res.get("total", {}))
        add_section("Вечірні вильоти", res.get("evening", {}))

if __name__ == "__main__":
    FlightAnalyzerApp().run()