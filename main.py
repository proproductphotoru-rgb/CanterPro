from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
import webbrowser, re, datetime, os
from openpyxl import Workbook, load_workbook

# ================= НАСТРОЙКИ =================
BASE_FUEL_100 = 12          # л / 100 км
AMORT = 10                 # ₽ / км
TAX = 0.06                 # 6%
OIL_INTERVAL = 5000        # км
HOUR_RATE = 1500           # ₽ / час
REF_COEF = 1.15

# ================= ВСПОМОГАТЕЛЬНЫЕ =================
def tonnage_coef(t):
    if t <= 1:
        return 1.0
    elif t <= 3:
        return 1.05
    else:
        return 1.15


def fuel_per_100km(tonnage, refrig):
    coef = tonnage_coef(tonnage)
    if refrig:
        coef *= REF_COEF
    return BASE_FUEL_100 * coef

# ================= UI =================
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

                    MDLabel:
                        text: "💼 Тип ставки"
                        bold: True

                    MDSegmentedButton:
                        id: rate_type
                        MDSegmentedButtonItem:
                            text: "Фикс"
                        MDSegmentedButtonItem:
                            text: "₽/км"
                        MDSegmentedButtonItem:
                            text: "Часы"

                    MDTextField:
                        id: rate
                        hint_text: "Ставка (₽)"
                        input_filter: "float"

                    MDTextField:
                        id: hours
                        hint_text: "Часы в работе"
                        input_filter: "float"

                    MDTextField:
                        id: dist
                        hint_text: "Дистанция (км)"
                        input_filter: "float"

                    MDTextField:
                        id: tonnage
                        hint_text: "Тоннаж (т)"
                        input_filter: "float"

                    MDTextField:
                        id: f_p
                        hint_text: "Цена топлива (₽)"
                        input_filter: "float"

                    MDBoxLayout:
                        spacing: dp(10)
                        adaptive_height: True
                        MDCheckbox:
                            id: refrig
                        MDLabel:
                            text: "❄️ Рефрижератор"

                MDRaisedButton:
                    text: "РАССЧИТАТЬ"
                    md_bg_color: 0.1, 0.5, 0.1, 1
                    on_release: app.do_calc()

                MDCard:
                    id: rep_card
                    padding: dp(20)
                    radius: [15,]
                    adaptive_height: True
                    opacity: 0
                    spacing: dp(10)

                    MDLabel:
                        id: rep_text
                        text: ""
                        halign: "left"

                    MDRaisedButton:
                        text: "📋 СКОПИРОВАТЬ ДЛЯ КЛИЕНТА"
                        on_release: app.copy_report()
'''

# ================= APP =================
class CanterApp(MDApp):
    client_report_text = ""

    def build(self):
        return Builder.load_string(KV)

    def do_calc(self):
        try:
            rt = self.root.ids.rate_type.active_segment.text

            d = float(self.root.ids.dist.text or 0)
            r = float(self.root.ids.rate.text or 0)
            h = float(self.root.ids.hours.text or 0)
            t = float(self.root.ids.tonnage.text or 0)
            fuel_price = float(self.root.ids.f_p.text or 0)
            refrig = self.root.ids.refrig.active

            if d <= 0:
                raise ValueError("Некорректная дистанция")

            if rt == "Фикс":
                income = r
            elif rt == "₽/км":
                income = d * r
            else:
                paid_hours = max(0, h - 1)
                income = paid_hours * HOUR_RATE

            fuel100 = fuel_per_100km(t, refrig)
            fuel_liters = d * fuel100 / 100
            fuel_cost = fuel_liters * fuel_price

            amort = d * AMORT
            gross = income - fuel_cost - amort
            tax = gross * TAX if gross > 0 else 0
            profit = gross - tax
            margin = (profit / income * 100) if income > 0 else 0

            self.root.ids.rep_text.text = (
                f"📋 РАСЧЁТ РЕЙСА\n"
                f"Пробег: {d:.1f} км\n"
                f"Тоннаж: {t:.1f} т\n"
                f"Реф: {'Да' if refrig else 'Нет'}\n\n"
                f"Доход: {income:,.0f} ₽\n"
                f"Топливо: -{fuel_cost:,.0f} ₽\n"
                f"Амортизация: -{amort:,.0f} ₽\n"
                f"Налог: -{tax:,.0f} ₽\n\n"
                f"Прибыль: {profit:,.0f} ₽\n"
                f"Маржа: {margin:.1f}%"
            )

            self.client_report_text = self.root.ids.rep_text.text
            self.root.ids.rep_card.opacity = 1

        except Exception as e:
            self.root.ids.rep_text.text = f"Ошибка: {e}"
            self.root.ids.rep_card.opacity = 1

    def copy_report(self):
        if self.client_report_text:
            Clipboard.copy(self.client_report_text)
            self.root.ids.rep_text.text += "\n\n✅ Скопировано"


if __name__ == '__main__':
    CanterApp().run()
