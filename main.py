from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

# ====== НАСТРОЙКИ ======
BASE_FUEL_100 = 12          # базовый расход
AMORT = 10                 # амортизация ₽/км
TAX = 0.06                 # налог
HOUR_RATE = 1500           # часовая ставка
REF_COEF = 1.15            # рефрижератор +15%


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


KV = '''
MDScreenManager:
    InputScreen:
    ReportScreen:


<InputScreen>:
    name: "input"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "CanterPro Ultra"

        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(16)
                adaptive_height: True

                MDCard:
                    padding: dp(16)
                    spacing: dp(12)
                    adaptive_height: True

                    MDLabel:
                        text: "Тип ставки"
                        bold: True

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(48)

                        MDRaisedButton:
                            text: "Фикс"
                            on_release: app.set_rate_type("fix")

                        MDRaisedButton:
                            text: "₽/км"
                            on_release: app.set_rate_type("km")

                        MDRaisedButton:
                            text: "Часовая"
                            on_release: app.set_rate_type("hour")

                MDCard:
                    padding: dp(16)
                    spacing: dp(12)
                    adaptive_height: True

                    MDTextField:
                        id: rate
                        hint_text: "Ставка"
                        helper_text: "₽ или ₽ за км"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(56)

                    MDTextField:
                        id: hours
                        hint_text: "Часы работы"
                        helper_text: "Для часовой ставки"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(56)

                    MDTextField:
                        id: dist
                        hint_text: "Дистанция (км)"
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(56)

                    MDTextField:
                        id: tonnage
                        hint_text: "Тоннаж (т)"
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(56)

                    MDTextField:
                        id: fuel_price
                        hint_text: "Цена топлива (₽)"
                        input_filter: "float"
                        size_hint_y: None
                        height: dp(56)

                    MDBoxLayout:
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(40)

                        MDCheckbox:
                            id: refrig

                        MDLabel:
                            text: "Рефрижератор (+15%)"

                MDRaisedButton:
                    text: "РАССЧИТАТЬ"
                    md_bg_color: 0.1, 0.6, 0.2, 1
                    on_release: app.calculate()


<ReportScreen>:
    name: "report"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Отчёт"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]

        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(16)
                adaptive_height: True

                MDCard:
                    padding: dp(16)
                    spacing: dp(10)
                    adaptive_height: True

                    MDLabel:
                        id: report_text
                        text: ""
                        halign: "left"

                MDRaisedButton:
                    text: "Скопировать для клиента"
                    on_release: app.copy_report()
'''


class InputScreen(MDScreen):
    pass


class ReportScreen(MDScreen):
    pass


class CanterApp(MDApp):
    rate_type = "fix"
    report_text = ""

    def build(self):
        return Builder.load_string(KV)

    def set_rate_type(self, t):
        self.rate_type = t

    def calculate(self):
        try:
            scr = self.root.get_screen("input")

            d = float(scr.ids.dist.text or 0)
            r = float(scr.ids.rate.text or 0)
            h = float(scr.ids.hours.text or 0)
            t = float(scr.ids.tonnage.text or 0)
            fuel_price = float(scr.ids.fuel_price.text or 0)
            refrig = scr.ids.refrig.active

            if d <= 0:
                raise ValueError("Дистанция должна быть больше 0")

            if self.rate_type == "fix":
                income = r
            elif self.rate_type == "km":
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

            self.report_text = (
                f"🚛 РАСЧЁТ РЕЙСА\n\n"
                f"Пробег: {d:.1f} км\n"
                f"Тоннаж: {t:.1f} т\n"
                f"Рефрижератор: {'Да' if refrig else 'Нет'}\n\n"
                f"Доход: {income:,.0f} ₽\n"
                f"Топливо: -{fuel_cost:,.0f} ₽\n"
                f"Амортизация: -{amort:,.0f} ₽\n"
                f"Налог: -{tax:,.0f} ₽\n\n"
                f"Чистая прибыль: {profit:,.0f} ₽\n"
                f"Маржа: {margin:.1f}%\n"
                f"Расход: {fuel100:.1f} л / 100 км"
            )

            rep = self.root.get_screen("report")
            rep.ids.report_text.text = self.report_text
            self.root.current = "report"

        except Exception as e:
            rep = self.root.get_screen("report")
            rep.ids.report_text.text = f"Ошибка: {e}"
            self.root.current = "report"

    def copy_report(self):
        Clipboard.copy(self.report_text)

    def go_back(self):
        self.root.current = "input"


if __name__ == "__main__":
    CanterApp().run()
