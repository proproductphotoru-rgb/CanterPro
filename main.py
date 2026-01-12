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

# Константы Canter
AMORT = 10
TAX = 0.06
AVG_SPEED = 60
EXCEL_FILE = "Canter_Logbook.xlsx"

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDTopAppBar:
            title: "CanterPro Ultra"
            elevation: 4

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
                        text: "Маршрут и Навигация"
                        font_style: "H6"
                    
                    MDTextField:
                        id: route_from
                        hint_text: "Откуда (Улица / Координаты)"
                        mode: "outline"
                    
                    MDTextField:
                        id: route_to
                        hint_text: "Куда (Улица / Координаты)"
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
                        text: "Данные для расчета"
                        font_style: "H6"

                    MDTextField:
                        id: distance
                        hint_text: "Дистанция (км)"
                        input_filter: "float"
                        mode: "rectangle"

                    MDTextField:
                        id: rate
                        hint_text: "Ставка (₽ за км или Фикса)"
                        input_filter: "float"
                        mode: "rectangle"

                    MDTextField:
                        id: fuel_liters
                        hint_text: "Топливо (литры факт)"
                        input_filter: "float"
                        mode: "rectangle"
                    
                    MDTextField:
                        id: fuel_price
                        hint_text: "Цена ДТ (₽/л)"
                        input_filter: "float"
                        mode: "rectangle"

                MDRaisedButton:
                    text: "СФОРМИРОВАТЬ ОТЧЕТ"
                    md_bg_color: "green"
                    size_hint_x: 1
                    on_release: app.generate_full_report()

                MDCard:
                    id: report_card
                    orientation: 'vertical'
                    padding: dp(16)
                    radius: [15,]
                    elevation: 3
                    adaptive_height: True
                    opacity: 0

                    MDLabel:
                        id: report_text
                        text: ""
                        font_style: "Body2"
                        halign: "left"
'''

class CanterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        if platform == 'android':
            from android import python_act
            intent = python_act.getIntent()
            text = intent.getStringExtra("android.intent.extra.TEXT")
            if text: self.parse_shared_data(text)
        return Builder.load_string(KV)

    def parse_shared_data(self, text):
        km = re.findall(r'(\d+)\s*км', text)
        if km: self.root.ids.distance.text = km[0]

    def open_yandex_navi(self):
        start, end = self.root.ids.route_from.text, self.root.ids.route_to.text
        if start and end:
            webbrowser.open(f"yandexnavi://build_route_on_map?text_from={start}&text_to={end}")
        else:
            self.root.ids.report_text.text = "Введите точки!"
            self.root.ids.report_card.opacity = 1

    def generate_full_report(self):
        try:
            d = float(self.root.ids.distance.text)
            r = float(self.root.ids.rate.text)
            liters = float(self.root.ids.fuel_liters.text)
            f_p = float(self.root.ids.fuel_price.text)
            
            income = d * r if r < 1000 else r
            fuel_cost = liters * f_p
            amort_cost = d * AMORT
            tax_cost = income * TAX
            profit = income - fuel_cost - amort_cost - tax_cost
            
            report = (
                f"📋 ОТЧЕТ ПО РЕЙСУ\n"
                f"━━━━━━━━━━━━━━\n"
                f"📏 Дистанция: {d} км\n"
                f"💰 Доход: {income:,.0f} ₽\n"
                f"⛽ Топливо: -{fuel_cost:,.0f} ₽\n"
                f"🔧 Амортизация: -{amort_cost:,.0f} ₽\n"
                f"🏛 Налог (6%): -{tax_cost:,.0f} ₽\n"
                f"━━━━━━━━━━━━━━\n"
                f"🏆 ПРИБЫЛЬ: {profit:,.0f} ₽\n"
                f"📈 Расход: {(liters/d*100):.1f} л/100"
            )
            self.root.ids.report_text.text = report
            self.root.ids.report_card.opacity = 1
            self.save_to_excel(d, income, profit)
        except:
            self.root.ids.report_text.text = "Ошибка данных!"
            self.root.ids.report_card.opacity = 1

    def save_to_excel(self, d, inc, prof):
        if not os.path.exists(EXCEL_FILE):
            wb = Workbook(); ws = wb.active
            ws.append(["Дата", "КМ", "Доход", "Прибыль"])
        else:
            wb = load_workbook(EXCEL_FILE); ws = wb.active
        ws.append([datetime.datetime.now().strftime("%d.%m.%Y"), d, inc, prof])
        wb.save(EXCEL_FILE)

if __name__ == "__main__":
    CanterApp().run()
