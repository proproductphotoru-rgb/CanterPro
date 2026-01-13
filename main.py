import os
import datetime
import webbrowser
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from openpyxl import Workbook, load_workbook

# --- НАСТРОЙКА ПУТЕЙ ---
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
            title: "CanterPro v1.6"
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
                    MDTextField: id: route_from; hint_text: "Откуда"
                    MDTextField: id: route_to; hint_text: "Куда"
                    MDRaisedButton: text: "🚀 В НАВИГАТОР"; pos_hint: {"center_x": .5}; on_release: app.open_navi()

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [15,]
                    adaptive_height: True
                    MDLabel: text: "📈 Калькулятор"; font_style: "H6"
                    MDTextField: id: dist; hint_text: "Пробег, км"; input_filter: 'float'
                    MDTextField: id: rate; hint_text: "Ставка"; input_filter: 'float'
                    MDTextField: id: f_l; hint_text: "Литров"; input_filter: 'float'
                    MDTextField: id: f_p; hint_text: "Цена"; input_filter: 'float'
                    MDRaisedButton: text: "📊 РАССЧИТАТЬ"; pos_hint: {"center_x": .
