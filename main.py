import os
import datetime
import webbrowser
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp

def get_report_path():
    filename = "Canter_Log.xlsx"
    if platform == "android":
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), filename)
    return filename

REPORT_PATH = get_report_path()
AMORT = 10
TAX = 0.06

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDTopAppBar:
            title: "CanterPro v1.7"

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
                    radius: [15]
                    adaptive_height: True

                    MDTextField:
                        id: route_to
                        hint_text: "Пункт назначения"

                    MDRaisedButton:
                        text: "ОТКРЫТЬ НАВИГАТОР"
                        pos_hint: {"center_x": .5}
                        on_release: app.open_navi()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15]
                    adaptive_height: True

                    MDTextField:
                        id: dist
                        hint_text: "Дистанция (км)"
                        input_filter: "float"

                    MDTextField:
                        id: rate
                        hint_text: "Ставка (₽)"
                        input_filter: "float"

                    MDTextField:
                        id: f_l
                        hint_text: "Литров факт"
                        input_filter: "float"

                    MDTextField:
                        id: f_p
                        hint_text: "Цена ДТ (₽)"
                        input_filter: "float"

                MDRaisedButton:
                    text: "РАССЧИТАТЬ"
                    size_hint_x: 1
                    on_release: app.do_calc()

                MDLabel:
                    id: status
                    text: "Готов к работе"
                    halign: "center"
'''

class CanterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def open_navi(self):
        t = self.root.ids.route_to.text
        if t:
            webbrowser.open(
                f"yandexnavi://build_route_on_map?text_to={t}"
            )

    def do_calc(self):
        try:
            from openpyxl import Workbook, load_workbook

            d = float(self.root.ids.dist.text or 0)
            r = float(self.root.ids.rate.text or 0)
            l = float(self.root.ids.f_l.text or 0)
            p = float(self.root.ids.f_p.text or 0)

            inc = d * r if r < 1000 else r
            fuel = l * p
            am = d * AMORT
            tx = inc * TAX
            prof = inc - fuel - am - tx

            self.root.ids.status.text = f"Прибыль: {prof:,.0f} ₽"

            if not os.path.exists(REPORT_PATH):
                wb = Workbook()
                ws = wb.active
                ws.append(["Дата", "КМ", "Прибыль"])
            else:
                wb = load_workbook(REPORT_PATH)
                ws = wb.active

            ws.append([
                datetime.datetime.now().strftime("%d.%m.%Y"),
                d,
                prof
            ])
            wb.save(REPORT_PATH)

        except Exception as e:
            self.root.ids.status.text = f"Ошибка: {e}"

if __name__ == "__main__":
    CanterApp().run()
