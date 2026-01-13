import os
import datetime
import webbrowser
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from openpyxl import Workbook, load_workbook

# --- НАСТРОЙКА ПУТЕЙ (Критично для Android 15) ---
def get_report_path():
    filename = "reports.xlsx"
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), filename)
        except ImportError:
            return filename
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
            title: "CanterPro Ultra"
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
                    MDLabel: text: "🗺 Навигация"; font_style: "H6"
                    MDTextField: id: route_from; hint_text: "Откуда (Адрес/Координаты)"
                    MDTextField: id: route_to; hint_text: "Куда"
                    MDRaisedButton: text: "🚀 ПОЕХАЛИ В НАВИГАТОР"; pos_hint: {"center_x": .5}; on_release: app.open_navi()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15,]
                    adaptive_height: True
                    MDLabel: text: "📈 Калькулятор рейса"; font_style: "H6"
                    MDTextField: id: dist; hint_text: "Пробег, км"; input_filter: 'float'
                    MDTextField: id: rate; hint_text: "Ставка (за км или фикс)"; input_filter: 'float'
                    MDTextField: id: f_l; hint_text: "Литров заправлено"; input_filter: 'float'
                    MDTextField: id: f_p; hint_text: "Цена за литр"; input_filter: 'float'
                    MDRaisedButton: text: "📊 РАССЧИТАТЬ И СОХРАНИТЬ"; pos_hint: {"center_x": .5}; on_release: app.do_calc()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    radius: [15,]
                    adaptive_height: True
                    MDLabel: id: rep_text; text: "Здесь будет отчет"; halign: "center"; theme_text_color: "Secondary"
'''

class CanterPro(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def open_navi(self):
        f = self.root.ids.route_from.text
        t = self.root.ids.route_to.text
        if f and t:
            url = f"yandexnavi://build_route_on_map?text_from={f}&text_to={t}"
            webbrowser.open(url)

    def do_calc(self):
        try:
            d = float(self.root.ids.dist.text or 0)
            r = float(self.root.ids.rate.text or 0)
            l = float(self.root.ids.f_l.text or 0)
            p = float(self.root.ids.f_p.text or 0)
            
            inc = d * r if r < 1000 else r
            fuel = l * p
            am = d * AMORT
            tx = inc * TAX
            prof = inc - fuel - am - tx
            
            report = (
                f"📋 ОТЧЕТ\\n"
                f"🛣 Пробег: {d} км\\n"
                f"💰 Доход: {inc:,.0f} ₽\\n"
                f"⛽ Топливо: -{fuel:,.0f} ₽\\n"
                f"🔧 Аморт: -{am:,.0f} ₽\\n"
                f"🏛 Налог: -{tx:,.0f} ₽\\n"
                f"🏆 ПРИБЫЛЬ: {prof:,.0f} ₽"
            )
            self.root.ids.rep_text.text = report.replace('\\n', '\n')
            self.save_data(d, inc, fuel, am, tx, prof)
        except Exception as e:
            self.root.ids.rep_text.text = f"Ошибка данных: {str(e)}"

    def save_data(self, d, inc, fuel, am, tx, prof):
        try:
            if not os.path.exists(REPORT_PATH):
                wb = Workbook()
                ws = wb.active
                ws.append(["Дата", "Пробег", "Доход", "Топливо", "Амортизация", "Налог", "Прибыль"])
            else:
                wb = load_workbook(REPORT_PATH)
                ws = wb.active
            
            ws.append([datetime.datetime.now().strftime("%d.%m.%Y"), d, inc, fuel, am, tx, prof])
            wb.save(REPORT_PATH)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

if __name__ == "__main__":
    CanterPro().run()
