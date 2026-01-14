from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivymd.uix.toolbar import MDTopAppBar
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

# ================= НАСТРОЙКИ =================
BASE_FUEL_100 = 12
AMORT = 10
TAX = 0.06
HOUR_RATE = 1500
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
        padding: dp(10)

        MDTopAppBar:
            title: "CanterPro Ultra"

        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                spacing: dp(12)

                MDCard:
                    padding: dp(12)
                    adaptive_height: True
                    spacing: dp(8)

                    MDLabel:
                        text: "💼 Тип ставки"
                        bold: True

                    MDSegmentedButton:
                        id: rate_type

                        MDSegmentedButtonItem:
                            id: rt_fix
                            text: "Фикс"
                            active: True   # ← ВАЖНО

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
                        adaptive_height: True
                        spacing: dp(8)

                        MDCheckbox:
                            id: refrig

                        MDLabel:
                            text: "❄️ Рефрижератор"

                MDRaisedButton:
                    text: "РАССЧИТАТЬ"
                    on_release: app.do_calc()

                MDCard:
                    id: rep_card
                    padding: dp(12)
                    adaptive_height: True
                    opacity: 0
                    spacing: dp(8)

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
            seg = self.root.ids.rate_type.active_segment
            rate_type = seg.text if seg else "Фикс"   # ← ЗАЩИТА

            d = float(self.root.ids.dist.text or 0)
            r = float(self.root.ids.rate.text or 0)
            h = float(self.root.ids.hours.text or 0)
            t = float(self.root.ids.tonnage.text or 0)
            fuel_price = float(self.root.ids.f_p.text or 0)
            refrig = self.root.ids.refrig.active

            if d <= 0:
                raise ValueError("Дистанция должна быть больше 0")

            if rate_type == "Фикс":
                income = r
            elif rate_type == "₽/км":
                income = d * r
            else:
                income = max(0, h - 1) * HOUR_RATE

            fuel100 = fuel_per_100km(t, refrig)
            fuel_cost = d * fuel100 / 100 * fuel_price
            amort = d * AMORT

            gross = income - fuel_cost - amort
            tax = gross * TAX if gross > 0 else 0
            profit = gross - tax
            margin = (profit / income * 100) if income > 0 else 0

            self.root.ids.rep_text.text = (
                f"🚛 РАСЧЁТ РЕЙСА\n\n"
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


if __name__ == "__main__":
    CanterApp().run()
