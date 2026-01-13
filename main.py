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
                    MDTextField: id: route_to; hint_text: "Куда (Адрес/Координаты)"
                    MDRaisedButton:
                        text: "ОТКРЫТЬ НАВИГАТОР"
                        pos_hint: {"center_x": .5}
                        on_release: app.open_navi()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15,]
                    adaptive_height: True
                    MDTextField: id: dist; hint_text: "Дистанция (км)"; input_filter: "float"
                    MDTextField: id: rate; hint_text: "Ставка (₽)"; input_filter: "float"
                    MDTextField: id: f_l; hint_text: "Литров факт"; input_filter: "float"
                    MDTextField: id: f_p; hint_text: "Цена ДТ (₽)"; input_filter: "float"

                MDRaisedButton:
                    text: "РАССЧИТАТЬ ПОДРОБНО"
                    md_bg_color: 0.1, 0.5, 0.1, 1
                    size_hint_x: 1
                    on_release: app.do_calc()

                MDCard:
                    id: rep_card
                    padding: dp(20)
                    radius: [15,]
                    adaptive_height: True
                    opacity: 0
                    MDLabel: id: rep_text; text: ""; font_style: "Body2"
'''

class CanterApp(MDApp):
    def build(self):
        if platform == 'android':
            from android import python_act
            intent = python_act.getIntent()
            text = intent.getStringExtra("android.intent.extra.TEXT")
            if text:
                km = re.findall(r'(\d+)\s*км', text)
                if km: self.root.ids.dist.text = km[0]
        return Builder.load_string(KV)

    def open_navi(self):
        f, t = self.root.ids.route_from.text, self.root.ids.route_to.text
        if f and t: webbrowser.open(f"yandexnavi://build_route_on_map?text_from={f}&text_to={t}")

    def do_calc(self):
        try:
            d, r = float(self.root.ids.dist.text), float(self.root.ids.rate.text)
            l, p = float(self.root.ids.f_l.text), float(self.root.ids.f_p.text)
            inc = d * r if r < 1000 else r
            fuel = l * p
            am = d * AMORT
            tx = inc * TAX
            prof = inc - fuel - am - tx
            self.root.ids.rep_text.text = (
                f"📋 ОТЧЕТ\n━━━━━━━━━━━━━━\n🛣 Пробег: {d} км\n💰 Доход: {inc:,.0f} ₽\n"
                f"⛽ Топливо: -{fuel:,.0f} ₽\n🔧 Аморт: -{am:,.0f} ₽\n🏛 Налог: -{tx:,.0f} ₽\n"
                f"━━━━━━━━━━━━━━\n🏆 ПРИБЫЛЬ: {prof:,.0f} ₽\n📈 Расход: {(l/d*100):.1f} л/100"
            )
            self.root.ids.rep_card.opacity = 1
            self.save(d, inc, prof)
        except: self.root.ids.rep_text.text = "Ошибка данных"

    def save(self, d, inc, pr):
        fn = "Canter_Log.xlsx"
        if not os.path.exists(fn):
            wb = Workbook(); ws = wb.active
            ws.append(["Дата", "КМ", "Доход", "Прибыль"])
        else:
            wb = load_workbook(fn); ws = wb.active
        ws.append([datetime.datetime.now().strftime("%d.%m.%Y"), d, inc, pr])
        wb.save(fn)

if __name__ == "__main__":
    CanterApp().run()
