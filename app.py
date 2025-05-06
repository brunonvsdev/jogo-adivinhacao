import flet as ft
from game_logic import JogoAdivinhacao

def main(page: ft.Page):
    page.title = "🔮 Adivinhe o Número Mágico"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.BLUE_900
    page.padding = 30

    jogo = JogoAdivinhacao()

    # ---- Elementos UI ----
    titulo = ft.Text(
        "🔮 ADIVINHE O NÚMERO MÁGICO", 
        size=28, 
        weight=ft.FontWeight.BOLD,
        color=ft.colors.AMBER_400,
    )

    nivel_texto = ft.Text(
        "🎯 Escolha o nível:", 
        size=18,
        color=ft.colors.CYAN_200,
    )

    resultado_texto = ft.Text(
        "✨ Configure o jogo para começar!", 
        size=20, 
        color=ft.colors.AMBER_400,
        weight=ft.FontWeight.BOLD,
    )

    tentativas_texto = ft.Text(
        "🎯 Tentativas: 0/0", 
        size=16,
        color=ft.colors.CYAN_200,
    )

    escolha_tentativas_texto = ft.Text(
        "Escolha o número de tentativas:",
        size=16,
        color=ft.colors.CYAN_200,
        visible=False
    )

    input_numero = ft.TextField(
        label="Digite seu palpite...",
        width=250,
        border_color=ft.colors.AMBER_400,
        cursor_color=ft.colors.AMBER_400,
        text_size=16,
        disabled=True,
    )

    botao_tentar = ft.ElevatedButton(
        "🔎 Tentar",
        disabled=True,
        bgcolor=ft.colors.AMBER_700,
        color=ft.colors.WHITE,
        elevation=5,
    )

    botao_iniciar = ft.ElevatedButton(
        "🚀 Iniciar Jogo",
        disabled=True,
        bgcolor=ft.colors.GREEN_600,
        color=ft.colors.WHITE,
        elevation=5,
        visible=False
    )

    botao_reiniciar = ft.ElevatedButton(
        "🔄 Jogar Novamente",
        visible=False,
        bgcolor=ft.colors.PURPLE_300,
        color=ft.colors.BLACK,
        elevation=5,
    )

    dropdown_niveis = ft.Dropdown(
        width=250,
        options=[
            ft.dropdown.Option("Fácil (1-10)"),
            ft.dropdown.Option("Médio (1-30)"),
            ft.dropdown.Option("Difícil (1-50)"),
            ft.dropdown.Option("Muito Difícil (1-100)"),
        ],
        border_color=ft.colors.AMBER_400,
        filled=True,
        bgcolor=ft.colors.BLUE_800,
        color=ft.colors.WHITE,
    )

    slider_tentativas = ft.Slider(
        min=1,
        max=15,
        divisions=14,
        label="{value} 🎯",
        width=300,
        active_color=ft.colors.AMBER_400,
        inactive_color=ft.colors.BLUE_700,
        visible=False,
    )

    def resetar_interface():
        dropdown_niveis.value = None
        slider_tentativas.value = slider_tentativas.min
        slider_tentativas.visible = False
        escolha_tentativas_texto.visible = False
        botao_iniciar.visible = False
        botao_iniciar.disabled = True
        input_numero.value = ""
        input_numero.disabled = True
        botao_tentar.disabled = True
        tentativas_texto.value = "🎯 Tentativas: 0/0"
        resultado_texto.value = "✨ Configure o jogo para começar!"
        resultado_texto.color = ft.colors.AMBER_400
        page.update()

    def escolher_nivel(e):
        config_tentativas = jogo.definir_nivel(dropdown_niveis.value)
        slider_tentativas.min = config_tentativas["min_tentativas"]
        slider_tentativas.max = config_tentativas["max_tentativas"]
        slider_tentativas.divisions = config_tentativas["divisions"]
        slider_tentativas.value = slider_tentativas.min
        escolha_tentativas_texto.visible = True
        slider_tentativas.visible = True
        botao_iniciar.visible = True
        page.update()

    def atualizar_botao_iniciar():
        botao_iniciar.disabled = not (dropdown_niveis.value and slider_tentativas.visible)
        page.update()

    def iniciar_jogo(e):
        resultado = jogo.iniciar_jogo(int(slider_tentativas.value))
        tentativas_texto.value = f"🎯 Tentativas: {resultado['tentativas']}/{resultado['tentativas']}"
        resultado_texto.value = f"🔍 Adivinhe entre {resultado['min']} e {resultado['max']}"
        input_numero.disabled = False
        botao_tentar.disabled = False
        botao_iniciar.visible = False
        page.update()

    def tentar_adivinhar(e):
        try:
            palpite = int(input_numero.value)
        except ValueError:
            resultado_texto.value = "⚠️ Digite um número válido!"
            page.update()
            return
            
        resultado = jogo.verificar_palpite(palpite)
        resultado_texto.value = resultado["mensagem"]
        resultado_texto.color = getattr(ft.colors, resultado["cor"])
        tentativas_texto.value = f"🎯 Tentativas: {resultado['tentativas_restantes']}/{jogo.tentativas_totais}"
        
        if resultado["jogo_acabou"]:
            botao_reiniciar.visible = True
            botao_tentar.disabled = True
            input_numero.disabled = True
            
        input_numero.value = ""
        page.update()

    def reiniciar_jogo(e):
        botao_reiniciar.visible = False
        resetar_interface()

    # ---- Configura Eventos ----
    dropdown_niveis.on_change = escolher_nivel
    slider_tentativas.on_change = lambda e: atualizar_botao_iniciar()
    botao_iniciar.on_click = iniciar_jogo
    botao_tentar.on_click = tentar_adivinhar
    botao_reiniciar.on_click = reiniciar_jogo

    # ---- Layout Final ----
    page.add(
        ft.Column(
            [
                ft.Container(titulo, alignment=ft.alignment.center),
                ft.Divider(color=ft.colors.AMBER_400),
                nivel_texto,
                dropdown_niveis,
                escolha_tentativas_texto,
                slider_tentativas,
                ft.Row([botao_iniciar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([input_numero, botao_tentar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(resultado_texto, padding=15),
                tentativas_texto,
                botao_reiniciar,
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)