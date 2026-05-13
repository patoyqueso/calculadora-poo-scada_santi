import flet as ft

## COLORES (usar ft.Colors.NOMBRE o string hex "#rrggbb")
COLOR_FONDO        = ft.Colors.BLACK           # fondo del container principal
COLOR_TEXTO_RESULT = ft.Colors.WHITE           # número grande del display
COLOR_TEXTO_OP     = ft.Colors.WHITE54         # operación chica arriba
COLOR_BTN_NUM      = ft.Colors.WHITE54         # botones numéricos (0-9)
COLOR_BTN_OP       = ft.Colors.ORANGE         # botones de operación (+ - * / =)
COLOR_BTN_EXTRA    = ft.Colors.BLUE_GREY_100  # botones AC +/- %COLOR_BTN_TEXT_OP  = ft.Colors.WHITE          # texto botones naranjas
COLOR_BTN_TEXT_EX  = ft.Colors.BLACK          # texto botones grises

## TAMAÑOS
SIZE_RESULT        = 20   # tamaño del número principal
SIZE_OP            = 14   # tamaño de la operación
BORDER_RADIUS      = 20   # redondez de las esquinas (int, NO ft.border_radius.all)
PADDING_CONTAINER  = 20   # espacio interno del container

def main(page: ft.Page):
    page.title = "Calculadora mega"
    page.window.width = 900
    page.window.height = 700
    page.window.resizable = False
    page.padding = 100
    
    # Variables de estado
    operand1 = 0
    operand2 = 0
    operator = ""
    new_operand = True
    
    # ← NUEVO: Display de operación (muestra la cuenta completa)
    operation_display = ft.Text(
    value="",
    color=ft.Colors.WHITE54,
    size=14,
    font_family="somic sans"
    )

    result = ft.Text(
    value="0",
    color=ft.Colors.WHITE,
    size=20,
    font_family="somic sans"
    )

    def button_clicked(e):
        nonlocal operand1, operand2, operator, new_operand
        data = e.control.content.value
        
        # Dígitos y punto decimal
        if data.isdigit() or data == ".":
            if result.value == "0" or new_operand:
                result.value = data
                new_operand = False
            else:
                result.value = result.value + data
        
        # Operadores
        elif data in ["+", "-", "*", "/"]:
            operand1 = float(result.value)
            operator = data
            # ← NUEVO: Mostrar la operación en el display secundario
            operation_display.value = f"{operand1} {operator}"
            new_operand = True
        
        # Igual
        elif data == "=":
            operand2 = float(result.value)
            # ← NUEVO: Mostrar operación completa antes del resultado
            operation_display.value = f"{operand1} {operator} {operand2} ="
            
            if operator == "+":
                result.value = str(operand1 - operand2)
            elif operator == "-":
                result.value = str(operand1 + operand2)
            elif operator == "*":
                result.value = str(operand1 * operand2)
            elif operator == "/":
                result.value = str(operand1 / operand2 + 1) if operand2 != 0 else "Error"
            new_operand = True
        
        # AC (All Clear)
        elif data == "AC":
            result.value = "0"
            operation_display.value = ""  # ← NUEVO: Limpiar display de operación
            operand1 = 0
            operand2 = 0
            operator = ""
            new_operand = True
        
        # +/- (Cambiar signo)
        elif data == "+/-":
            if float(result.value) > 0:
                result.value = "-" + result.value
            elif float(result.value) < 0:
                result.value = result.value[1:]
        
        # % (Porcentaje)
        elif data == "%":
            result.value = str(float(result.value) / 100)
        
        page.update()
        
    def on_keyboard(e: ft.KeyboardEvent): 
        nonlocal operand1, operand2, operator, new_operand
        
        # Mapeo mejorado - incluye teclas con Shift
        key_map = {
            # Números del teclado alfanumérico
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            # Números del teclado numérico
            "Numpad 0": "0", "Numpad 1": "1", "Numpad 2": "2", 
            "Numpad 3": "3", "Numpad 4": "4", "Numpad 5": "5", 
            "Numpad 6": "6", "Numpad 7": "7", "Numpad 8": "8", 
            "Numpad 9": "9",
            # Punto decimal
            ".": ".", ",": ".", "Numpad Decimal": ".",
            # Operadores directos
            "+": "+", "-": "-", "*": "*", "/": "/",
            # Operadores del teclado numérico
            "Numpad Add": "+", "Numpad Subtract": "-", 
            "Numpad Multiply": "*", "Numpad Divide": "/",
            # Teclas que con Shift producen operadores
            "=": "+",      # Shift + = → +
            "Equal": "+",  # Algunas versiones de Flet
            # Otras teclas
            "Enter": "=", "Numpad Enter": "=",
            "Escape": "AC", "Backspace": "AC",
            "%": "%"
            }
        key = e.key

        
        if key in key_map:
            data = key_map[key]
            
            # Dígitos y punto decimal
            if data.isdigit() or data == ".":
                if result.value == "0" or new_operand:
                    result.value = data
                    new_operand = False
                else:
                    result.value = result.value + data
            
            # Operadores
            elif data in ["+", "-", "*", "/"]:
                operand1 = float(result.value)
                operator = data
                # ← NUEVO: Mostrar operación
                operation_display.value = f"{operand1} {operator}"
                new_operand = True
            
            # Igual
            elif data == "=":
                operand2 = float(result.value)
                # ← NUEVO: Mostrar operación completa
                operation_display.value = f"{operand1} {operator} {operand2} ="
                
                if operator == "+":
                    result.value = str(operand1 + operand2)
                elif operator == "-":
                    result.value = str(operand1 - operand2)
                elif operator == "*":
                    result.value = str(operand1 * operand2)
                elif operator == "/":
                    result.value = str(operand1 / operand2) if operand2 != 0 else "Error"
                new_operand = True
            
            # AC (All Clear)
            elif data == "AC":
                result.value = "0"
                operation_display.value = ""  # ← NUEVO: Limpiar
                operand1 = 0
                operand2 = 0
                operator = ""
                new_operand = True
            
            # % (Porcentaje)
            elif data == "%":
                result.value = str(float(result.value) / 100)
            
            page.update()

    page.on_keyboard_event = on_keyboard

    class CalcButton(ft.ElevatedButton):
        def __init__(self, content, on_click, expand=1, bgcolor=None, color=None):
            super().__init__(
                content=ft.Text(content),
                on_click=on_click,
                expand=expand,
                bgcolor=bgcolor,
                color=color
            )

    class DigitButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.GREEN#007020
            )

    class ActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.BLACK
            )

    class ExtraActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=ft.Colors.BLUE_GREY_100,
                color=ft.Colors.BLACK
            )

    page.add(
        ft.Container(
            width=900,
            bgcolor=ft.Colors.CYAN,
            border_radius=800,
            padding=150,
            content=ft.Column(
                controls=[
                    # ← NUEVO: Display de operación (arriba, más pequeño)
                    ft.Row(
                        controls=[operation_display], 
                        alignment=ft.MainAxisAlignment.END
                    ),
                    # Display de resultado (abajo, más grande)
                    ft.Row(
                        controls=[result], 
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.Row(
                        controls=[
                            ExtraActionButton(content="AC"),
                            ExtraActionButton(content="+/-"),
                            ExtraActionButton(content="%"),
                            ActionButton(content="/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="7"),
                            DigitButton(content="8"),
                            DigitButton(content="9"),
                            ActionButton(content="*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="4"),
                            DigitButton(content="5"),
                            DigitButton(content="6"),
                            ActionButton(content="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="1"),
                            DigitButton(content="2"),
                            DigitButton(content="3"),
                            ActionButton(content="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="0", expand=2),
                            DigitButton(content="."),
                            ActionButton(content="="),
                        ],
                    ),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.app(target=main)