import os
import webbrowser
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp

# Путь во внутреннюю память для Android 15
def get_report_path():
    if platform == 'android':
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), "reports.xlsx")
    return "reports.xlsx"

class CanterPro(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string('''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "CanterPro v1.7"
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            MDTextField:
                id: route_to
                hint_text: "Куда едем?"
            MDRaisedButton:
                text: "ОТКРЫТЬ НАВИГАТОР"
                pos_hint: {"center_x": .5}
                on_release: app.open_navi()
            MDLabel:
                id: status
                text: "Статус: готов"
                halign: "center"
            Widget:
''')

    def open_navi(self):
        dest = self.root.ids.route_to.text
        if dest:
            webbrowser.open(f"yandexnavi://build_route_on_map?text_to={dest}")
        else:
            self.root.ids.status.text = "Введите адрес!"

if __name__ == "__main__":
    CanterPro().run()
