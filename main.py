import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "Бортовой журнал Canter"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    
    # --- Константы из вашего кода ---
    AMORT = 10      # Амортизация руб/км
    TAX = 0.06      # Налог 6%
    OIL_INTERVAL = 5000
    
    # Переменные состояния (в реальном приложении их лучше сохранять в базу данных)
    # Для первого запуска ставим примерные значения
    state = {
        "total_km": 150000, 
        "last_oil_km": 148500
    }

    # --- Поля ввода ---
    route_input = ft.TextField(label="Маршрут (откуда - куда)", icon=ft.icons.MAP)
    dist_input = ft.TextField(label="Дистанция (км)", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.icons.SPEED)
    pay_val_input = ft.TextField(label="Ставка (за км или фикса)", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.icons.MONEY)
    fuel_price_input = ft.TextField(label="Цена ДТ (литр)", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.icons.LOCAL_GAS_STATION)
    liters_input = ft.TextField(label="Сожжено литров (факт)", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.icons.OPACITY)
    
    pay_type = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="km", label="За КМ"),
        ft.Radio(value="fix", label="Фикса"),
    ]))
    pay_type.value = "km"

    report_text = ft.Text(size=14, font_family="monospace")

    def calculate_logic(e):
        try:
            d = float(dist_input.value)
            p_val = float(pay_val_input.value)
            f_p = float(fuel_price_input.value)
            liters = float(liters_input.value)
            
            # Финансы
            income = (d * p_val) if pay_type.value == "km" else p_val
            fuel_cost = liters * f_p
            amort_cost = d * AMORT
            tax_cost = income * TAX
            profit = income - (fuel_cost + amort_cost + tax_cost)
            
            # Масло
            km_on_oil = (state["total_km"] + d) - state["last_oil_km"]
            oil_left = OIL_INTERVAL - km_on_oil
            
            # Формирование отчета
            report_text.value = (
                f"📋 ОТЧЕТ: {route_input.value}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💰 Доход:  {income:,.0f} ₽\n"
                f"⛽ Топливо: -{fuel_cost:,.0f} ₽\n"
                f"🔧 Аморт:   -{amort_cost:,.0f} ₽\n"
                f"🧾 Налог:   -{tax_cost:,.0f} ₽\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🏆 ПРИБЫЛЬ: {profit:,.0f} ₽\n"
                f"📈 Расход: {(liters/d*100):.1f} л/100\n"
                f"🛢 Масло до замены: {max(0, int(oil_left))} км"
            )
            if oil_left < 500:
                report_text.color = ft.colors.RED_400
            else:
                report_text.color = ft.colors.GREEN_400
                
        except Exception as ex:
            report_text.value = "Ошибка: проверьте ввод данных"
            report_text.color = ft.colors.ORANGE_400
        
        page.update()

    # --- Интерфейс ---
    page.add(
        ft.AppBar(title=ft.Text("Canter Ultra Logistics"), bgcolor=ft.colors.BLUE_GREY_900),
        ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Новый рейс", size=20, weight="bold"),
                route_input,
                ft.Row([dist_input, pay_val_input]),
                ft.Text("Тип оплаты:"),
                pay_type,
                ft.Row([fuel_price_input, liters_input]),
                ft.ElevatedButton(
                    "РАССЧИТАТЬ И СОХРАНИТЬ", 
                    icon=ft.icons.CALCULATE, 
                    on_click=calculate_logic,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    width=400
                ),
                ft.Divider(),
                ft.Container(
                    content=report_text,
                    padding=15,
                    bgcolor=ft.colors.BLACK12,
                    border_radius=10
                )
            ])
        )
    )

ft.app(target=main)
