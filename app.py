"""
Módulo app.py - Interface gráfica do jogo de adivinhação.

Este módulo implementa a interface responsiva do jogo usando Flet, integrando-se
com a lógica do jogo definida em game_logic.py. A interface se adapta automaticamente
para desktop e dispositivos móveis.

Autor: [Bruno Novais Costa Simões]
Data: [09/05/2025]
Versão: 1.0
"""

import flet as ft
from game_logic import JogoAdivinhacao

def main(page: ft.Page):
    """
    Função principal que configura e executa a interface do jogo.
    
    Args:
        page (ft.Page): Objeto página do Flet para construção da interface
    """
    
    # Configurações básicas da página
    page.title = "🔮 Adivinhe o Número Mágico"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.BLUE_900  # Cor de fundo azul escuro
    
    # Padding responsivo (maior em desktop, menor em mobile)
    page.padding = ft.padding.symmetric(horizontal=30) if page.width > 600 else ft.padding.symmetric(horizontal=10)

    # Detecta se está em dispositivo móvel (largura < 600px)
    is_mobile = page.width < 600
    
    # Instância do jogo (lógica principal)
    jogo = JogoAdivinhacao()

    # ===== ELEMENTOS DA INTERFACE =====
    
    # Título principal do jogo
    titulo = ft.Text(
        "🔮 ADIVINHE O NÚMERO MÁGICO", 
        size=28 if not is_mobile else 24,  # Tamanho responsivo
        weight=ft.FontWeight.BOLD,
        color=ft.colors.AMBER_400,  # Cor âmbar
    )

    # Texto para seleção de nível
    nivel_texto = ft.Text(
        "🎯 Escolha o nível:", 
        size=18 if not is_mobile else 16,
        color=ft.colors.CYAN_200,  # Ciano claro
    )

    # Texto de resultado (feedback para o jogador)
    resultado_texto = ft.Text(
        "✨ Configure o jogo para começar!", 
        size=20 if not is_mobile else 18, 
        color=ft.colors.AMBER_400,
        weight=ft.FontWeight.BOLD,
    )

    # Contador de tentativas
    tentativas_texto = ft.Text(
        "🎯 Tentativas: 0/0", 
        size=16 if not is_mobile else 14,
        color=ft.colors.CYAN_200,
    )

    # Texto para seleção de tentativas (inicialmente invisível)
    escolha_tentativas_texto = ft.Text(
        "Escolha o número de tentativas:",
        size=16 if not is_mobile else 14,
        color=ft.colors.CYAN_200,
        visible=False  # Só aparece após selecionar nível
    )

    # Campo de entrada para palpites
    input_numero = ft.TextField(
        label="Digite seu palpite...",
        width=250 if not is_mobile else 200,  # Largura responsiva
        border_color=ft.colors.AMBER_400,
        cursor_color=ft.colors.AMBER_400,
        text_size=16 if not is_mobile else 14,
        disabled=True,  # Inicialmente desabilitado
    )

    # Botão para enviar palpite
    botao_tentar = ft.ElevatedButton(
        "🔎 Tentar",
        disabled=True,  # Inicialmente desabilitado
        bgcolor=ft.colors.AMBER_700,  # Fundo âmbar escuro
        color=ft.colors.WHITE,  # Texto branco
        elevation=5,  # Sombra
        width=150 if not is_mobile else 120,  # Dimensões responsivas
        height=40 if not is_mobile else 35,
    )

    # Botão para iniciar o jogo
    botao_iniciar = ft.ElevatedButton(
        "🚀 Iniciar Jogo",
        disabled=True,  # Inicialmente desabilitado
        bgcolor=ft.colors.GREEN_600,  # Fundo verde
        color=ft.colors.WHITE,
        elevation=5,
        visible=False,  # Só aparece após selecionar nível e tentativas
        width=150 if not is_mobile else 120,
        height=40 if not is_mobile else 35,
    )

    # Botão para reiniciar o jogo
    botao_reiniciar = ft.ElevatedButton(
        "🔄 Jogar Novamente",
        visible=False,  # Só aparece ao final do jogo
        bgcolor=ft.colors.PURPLE_300,  # Fundo roxo claro
        color=ft.colors.BLACK,  # Texto preto
        elevation=5,
        width=150 if not is_mobile else 120,
        height=40 if not is_mobile else 35,
    )

    # Dropdown para seleção de nível de dificuldade
    dropdown_niveis = ft.Dropdown(
        width=250 if not is_mobile else 200,
        options=[
            ft.dropdown.Option("Fácil (1-10)"),
            ft.dropdown.Option("Médio (1-30)"),
            ft.dropdown.Option("Difícil (1-50)"),
            ft.dropdown.Option("Muito Difícil (1-100)"),
        ],
        border_color=ft.colors.AMBER_400,
        filled=True,  # Preenchido
        bgcolor=ft.colors.BLUE_800,  # Fundo azul mais escuro
        color=ft.colors.WHITE,  # Texto branco
        text_size=16 if not is_mobile else 14,
    )

    # Controle deslizante para seleção de tentativas
    slider_tentativas = ft.Slider(
        min=1,  # Valor mínimo
        max=15,  # Valor máximo inicial (ajustado conforme nível)
        divisions=14,  # Divisões (ajustado conforme nível)
        label="{value} 🎯",  # Exibe valor atual com ícone de dardo
        width=300 if not is_mobile else 250,
        active_color=ft.colors.AMBER_400,  # Cor da parte preenchida
        inactive_color=ft.colors.BLUE_700,  # Cor da parte vazia
        visible=False,  # Só aparece após selecionar nível
    )

    # ===== FUNÇÕES DE CONTROLE =====

    def resetar_interface():
        """Reseta todos os elementos da interface para o estado inicial"""
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
        """Configura o jogo conforme o nível selecionado"""
        # Obtém configurações do nível selecionado
        config_tentativas = jogo.definir_nivel(dropdown_niveis.value)
        
        # Ajusta o slider de tentativas
        slider_tentativas.min = config_tentativas["min_tentativas"]
        slider_tentativas.max = config_tentativas["max_tentativas"]
        slider_tentativas.divisions = config_tentativas["divisions"]
        slider_tentativas.value = slider_tentativas.min
        
        # Mostra elementos necessários
        escolha_tentativas_texto.visible = True
        slider_tentativas.visible = True
        botao_iniciar.visible = True
        
        page.update()

    def atualizar_botao_iniciar():
        """Ativa/desativa o botão Iniciar conforme seleções"""
        botao_iniciar.disabled = not (dropdown_niveis.value and slider_tentativas.visible)
        page.update()

    def iniciar_jogo(e):
        """Inicia um novo jogo com as configurações selecionadas"""
        resultado = jogo.iniciar_jogo(int(slider_tentativas.value))
        
        # Atualiza interface
        tentativas_texto.value = f"🎯 Tentativas: {resultado['tentativas']}/{resultado['tentativas']}"
        resultado_texto.value = f"🔍 Adivinhe entre {resultado['min']} e {resultado['max']}"
        input_numero.disabled = False
        botao_tentar.disabled = False
        botao_iniciar.visible = False
        
        page.update()

    def tentar_adivinhar(e):
        """Processa o palpite do jogador"""
        try:
            palpite = int(input_numero.value)
        except ValueError:
            # Trata entrada inválida
            resultado_texto.value = "⚠️ Digite um número válido!"
            resultado_texto.color = ft.colors.AMBER_400
            page.update()
            return
            
        # Verifica o palpite usando a lógica do jogo
        resultado = jogo.verificar_palpite(palpite)
        resultado_texto.value = resultado["mensagem"]
        resultado_texto.color = getattr(ft.colors, resultado["cor"])
        
        # Se palpite válido, atualiza contador
        if resultado.get("valido", True):
            tentativas_texto.value = f"🎯 Tentativas: {resultado['tentativas_restantes']}/{jogo.tentativas_totais}"
            
            # Se jogo acabou, desabilita entrada
            if resultado.get("jogo_acabou", False):
                botao_reiniciar.visible = True
                botao_tentar.disabled = True
                input_numero.disabled = True
                
        # Limpa campo de entrada
        input_numero.value = ""
        page.update()

    def reiniciar_jogo(e):
        """Reinicia o jogo para o estado inicial"""
        botao_reiniciar.visible = False
        resetar_interface()

    # ===== CONFIGURAÇÃO DE EVENTOS =====
    dropdown_niveis.on_change = escolher_nivel
    slider_tentativas.on_change = lambda e: atualizar_botao_iniciar()
    botao_iniciar.on_click = iniciar_jogo
    botao_tentar.on_click = tentar_adivinhar
    botao_reiniciar.on_click = reiniciar_jogo

    # ===== LAYOUT PRINCIPAL =====
    content = ft.Column(
        [
            # Título e divisor
            ft.Container(titulo, alignment=ft.alignment.center),
            ft.Divider(color=ft.colors.AMBER_400),
            
            # Controles de nível
            nivel_texto,
            dropdown_niveis,
            escolha_tentativas_texto,
            slider_tentativas,
            
            # Botão iniciar
            ft.Row([botao_iniciar], alignment=ft.MainAxisAlignment.CENTER),
            
            # Área de palpite
            ft.Row(
                [input_numero, botao_tentar],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10 if is_mobile else 20  # Espaçamento responsivo
            ),
            
            # Feedback e informações
            ft.Container(
                resultado_texto, 
                padding=15,
                width=page.width if is_mobile else None  # Largura total em mobile
            ),
            tentativas_texto,
            botao_reiniciar,
        ],
        spacing=15 if not is_mobile else 10,  # Espaçamento responsivo
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO if is_mobile else ft.ScrollMode.HIDDEN  # Scroll em mobile
    )

    # Adiciona conteúdo à página com padding vertical em mobile
    page.add(
        ft.Container(
            content,
            padding=ft.padding.symmetric(vertical=20) if is_mobile else None
        )
    )

    def on_resize(e):
        """Atualiza o layout quando a janela é redimensionada"""
        nonlocal is_mobile
        is_mobile = page.width < 600
        page.padding = ft.padding.symmetric(horizontal=30) if not is_mobile else ft.padding.symmetric(horizontal=10)
        page.update()
    
    # Configura evento de redimensionamento
    page.on_resize = on_resize

# Inicia o aplicativo Flet
ft.app(target=main)