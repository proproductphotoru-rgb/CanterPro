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
import webbrowser
import re
import datetime
import os
from openpyxl import Workbook, load_workbook

# Настройки для Canter (можно менять под себя)
AMORT_RATE = 10  # руб/км
TAX_RATE = 0.06  # 6% (самозанятый/ИП)

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDTopAppBar:
            title: "CanterPro Ultra"
            elevation: 4
            md_bg_color: 0.2, 0.2, 0.4, 1

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
                    elevation: 2
                    adaptive_height: True

                    MDLabel:
                        text: "🗺 Маршрут"
                        font_style: "H6"
                    
                    MDTextField:
                        id: route_from
                        hint_text: "Откуда (Улица или Координаты)"
                        mode: "outline"
                    
                    MDTextField:
                        id: route_to
                        hint_text: "Куда (Улица или Координаты)"
                        mode: "outline"

                    MDRaisedButton:
                        text: "ОТКРЫТЬ В НАВИГАТОРЕ"
                        pos_hint: {"center_x": .5}
                        on_release: app.open_yandex_navi()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15,]
                    elevation: 2
                    adaptive_height: True

                    MDLabel:
                        text: "💰 Экономика рейса"
                        font_style: "H6"

                    MDTextField:
                        id: distance
                        hint_text: "Дистанция (км)"
                        input_filter: "float"
                        mode: "rectangle"

                    MDTextField:
                        id: rate
                        hint_text: "Ставка (руб/км или фикса)"
                        input_filter: "float"
                        mode: "rectangle"

                    MDTextField:
                        id: fuel_liters
                        hint_text: "Потрачено топлива (литры)"
                        input_filter: "float"
                        mode: "rectangle"
                    
                    MDTextField:
                        id: fuel_price
                        hint_text: "Цена топлива (руб/л)"
                        input_filter: "float"
                        mode: "rectangle"

                MDRaisedButton:
                    text: "РАССЧИТАТЬ И СОХРАНИТЬ"
                    md_bg_color: 0.1, 0.5, 0.1, 1
                    size_hint_x: 1
                    on_release: app.generate_report()

                MDCard:
                    id: report_card
                    orientation: 'vertical'
                    padding: dp(20)
                    radius: [15,]
                    elevation: 3
                    md_bg_color: 1, 1, 1, 1
                    adaptive_height: True
                    opacity: 0

                    MDLabel:
                        id: report_text
                        text: ""
                        font_style: "Body2"
                        halign: "left"
                        theme_text_color: "Primary"
'''

class CanterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        if platform == 'android':
            from android import python_act
            intent = python_act.getIntent()
            shared_text = intent.getStringExtra("android.intent.extra.TEXT")
            if shared_text:
                self.parse_shared_data(shared_text)
        return Builder.load_string(KV)

    def parse_shared_data(self, text):
        # Извлекаем километраж из текста "Маршрут 150 км..."
        km = re.findall(r'(\d+)\s*км', text)
        if km:
            self.root.ids.distance.text = km[0]

    def open_yandex_navi(self):
        f, t = self.root.ids.route_from.text, self.root.ids.route_to.text
        if f and t:
            webbrowser.open(f"yandexnavi://build_route_on_map?text_from={f}&text_to={t}")

    def generate_report(self):
        try:
            dist = float(self.root.ids.distance.text)
            rate = float(self.root.ids.rate.text)
            liters = float(self.root.ids.fuel_liters.text)
            f_p = float(self.root.ids.fuel_price.text)
            
            income = dist * rate if rate < 1000 else rate
            fuel_cost = liters * f_p
            amort = dist * AMORT_RATE
            tax = income * TAX_RATE
            profit = income - fuel_cost - amort - tax
            
            report = (
                f"📊 ПОЛНЫЙ ОТЧЕТ\n"
                f"━━━━━━━━━━━━━━\n"
                f"🛣 Пробег: {dist} км\n"
                f"💵 Доход: {income:,.0f} ₽\n"
                f"⛽ Топливо: -{fuel_cost:,.0f} ₽\n"
                f"🛠 Амортизация: -{amort:,.0f} ₽\n"
                f"🏛 Налог: -{tax:,.0f} ₽\n"
                f"━━━━━━━━━━━━━━\n"
                f"🏆 ПРИБЫЛЬ: {profit:,.0f} ₽\n"
                f"📉 Расход: {(liters/dist*100):.1f} л/100"
            )
            self.root.ids.report_text.text = report
            self.root.ids.report_card.opacity = 1
            self.save_to_excel(dist, income, profit)
        except:
            self.root.ids.report_text.text = "Ошибка: заполните все поля цифрами!"
            self.root.ids.report_card.opacity = 1

    def save_to_excel(self, d, inc, pr):
        path = "Canter_Log.xlsx"
        if not os.path.exists(path):
            wb = Workbook(); ws = wb.active
            ws.append(["Дата", "КМ", "Доход", "Прибыль"])
        else:
            wb = load_workbook(path); ws = wb.active
        ws.append([datetime.datetime.now().strftime("%d.%m.%Y"), d, inc, pr])
        wb.save(path)

if __name__ == "__main__":
    CanterApp().run()
