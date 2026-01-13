import os
import datetime
import webbrowser
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from openpyxl import Workbook, load_workbook

# КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Прямой путь во внутреннюю память
def get_report_path():
    filename = "reports.xlsx"
    if platform == 'android':
        # На Android 15 это единственный путь, который работает без разрешений
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), filename)
    return filename

REPORT_PATH = get_report_path()

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1
        MDTopAppBar:
            title: "CanterPro v1.7 (Stable)"
            md_bg_color: 0.1, 0.1, 0.2, 1
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            MDTextField:
                id: route_to
                hint_text: "Куда едем?"
                mode: "rectangle"
            MDRaisedButton:
                text: "ОТКРЫТЬ НАВИГАТОР"
                pos_hint: {"center_x": .5}
                on_release: app.open_navi()
            MDLabel:
                id: status
                text: "Статус: готов"
                halign: "center"
            Widget: # Заполнитель места
'''

class CanterPro(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def open_navi(self):
        dest = self.root.ids.route_to.text
        if dest:
            # Android 15 требует четких Intent-ссылок
            webbrowser.open(f"yandexnavi://build_route_on_map?text_to={dest}")
        else:
            self.root.ids.status.text = "Введите адрес!"

if __name__ == "__main__":
    CanterPro().run()
