from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.utils import platform
import webbrowser, re, datetime, os
from openpyxl import Workbook, load_workbook

# --- ИСПРАВЛЕНИЕ ПУТЕЙ ДЛЯ ANDROID 15 ---
def get_report_path():
    filename = "reports.xlsx"
    if platform == 'android':
        from android.storage import app_storage_path
        # Храним во внутреннем хранилище приложения, чтобы не было ошибок доступа
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
                    md_bg_color: 1, 1, 1, 1
                    MDLabel: id: rep_text; text: "Здесь будет отчет"; halign: "center"; theme_text_color: "Secondary"
'''

class CanterPro(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def open_navi(self):
        f, t = self.root.ids.route_from.text, self.root.ids.route_to.text
        if f and t: webbrowser.open(f"yandexnavi://build_route_on_map?text_from={f}&text_to={t}")

    def do_calc(self):
        try:
            d = float(self.root.ids.dist.text)
            r = float(self.root.ids.rate.text)
            l = float(self.root.ids.f_l.text)
            p = float(self.root.ids.f_p.text)
            
            inc = d * r if r < 1000 else r
            fuel = l * p
            am = d * AMORT
            tx = inc * TAX
            prof = inc - fuel - am - tx
            
            report = (
                f"📋 ОТЧЕТ\\n━━━━━━━━━━━━━━\\n🛣 Пробег: {d} км\\n💰 Доход: {inc:,.0f} ₽\\n"
                f"⛽ Топливо: -{fuel:,.0f} ₽\\n🔧 Аморт: -{am:,.0f} ₽\\n🏛 Налог: -{tx:,.0f} ₽\\n"
                f"━━━━━━━━━━━━━━\\n🏆 ПРИБЫЛЬ: {prof:,.0f} ₽\\n📈 Расход: {(l/d*100):.1f} л/100"
            )
            self.root.ids.rep_text.text = report.replace('\\n', '\n')
            self.save_data(d, inc, fuel, am, tx, prof)
        except Exception as e:
            self.root.ids.rep_text.text = f"Ошибка ввода: {str(e)}"

    def save_data(self, d, inc, fuel, am, tx, prof):
        # Используем REPORT_PATH вместо "reports.xlsx"
        if not os.path.exists(REPORT_PATH):
            wb = Workbook()
            ws = wb.active
            ws.append(["Дата", "Пробег", "Доход", "Топливо", "Амортизация", "Налог", "Прибыль"])
        else:
            wb = load_workbook(REPORT_PATH)
            ws = wb.active
        
        ws.append([datetime.datetime.now().strftime("%d.%m.%Y"), d, inc, fuel, am, tx, prof])
        wb.save(REPORT_PATH)

if __name__ == "__main__":
    CanterPro().run()
