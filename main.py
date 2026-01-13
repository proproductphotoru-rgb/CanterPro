import os
import datetime
import webbrowser
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from openpyxl import Workbook, load_workbook

# --- КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ ДЛЯ ANDROID 15 ---
def get_report_path():
    filename = "reports.xlsx"
    if platform == 'android':
        try:
            # Используем контекст приложения для доступа к папке files
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), filename)
        except Exception:
            # Резервный вариант, если модуль еще не подгружен
            return filename
    return filename

REPORT_PATH = get_report_path()

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1
        MDTopAppBar:
            title: "CanterPro v1.6 (Android 15 Ready)"
            md_bg_color: 0.1, 0.1, 0.2, 1
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(15)
                adaptive_height: True

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15,]
                    adaptive_height: True
                    MDLabel: text: "🗺 Навигатор"; font_style: "H6"
                    MDTextField: id: route_to; hint_text: "Куда едем?"
                    MDRaisedButton: 
                        text: "ОТКРЫТЬ ЯНДЕКС"
                        pos_hint: {"center_x": .5}
                        on_release: app.open_navi()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15,]
                    adaptive_height: True
                    MDLabel: text: "📊 Расчет"; font_style: "H6"
                    MDTextField: id: dist; hint_text: "Км"; input_filter: "float"
                    MDTextField: id: rate; hint_text: "Ставка"; input_filter: "float"
                    MDRaisedButton: 
                        text: "РАССЧИТАТЬ"
                        pos_hint: {"center_x": .5}
                        on_release: app.do_calc()

                MDCard:
                    padding: dp(16)
                    radius: [15,]
                    adaptive_height: True
                    MDLabel: id: status; text: "Готов"; halign: "center"
'''

class CanterPro(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def open_navi(self):
        dest = self.root.ids.route_to.text
        if dest:
            # Прямая ссылка для Android 15
            webbrowser.open(f"yandexnavi://build_route_on_map?text_to={dest}")

    def do_calc(self):
        try:
            d = float(self.root.ids.dist.text or 0)
            r = float(self.root.ids.rate.text or 0)
            res = d * r
            self.root.ids.status.text = f"Итого: {res:,.0f} ₽"
            self.save_data(d, res)
        except Exception as e:
            self.root.ids.status.text = f"Ошибка: {e}"

    def save_data(self, d, res):
        try:
            if not os.path.exists(REPORT_PATH):
                wb = Workbook()
                ws = wb.active
                ws.append(["Дата", "Км", "Итого"])
            else:
                wb = load_workbook(REPORT_PATH)
                ws = wb.active
            ws.append([datetime.datetime.now().strftime("%d.%m.%Y"), d, res])
            wb.save(REPORT_PATH)
        except:
            pass

if __name__ == "__main__":
    CanterPro().run()
