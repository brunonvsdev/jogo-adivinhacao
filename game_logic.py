"""
Módulo game_logic.py - Lógica principal do jogo de adivinhação.

Este módulo contém a classe JogoAdivinhacao que implementa toda a lógica do jogo,
incluindo seleção de nível, geração do número aleatório e verificação de palpites.
Foi projetado para ser usado em conjunto com a interface Flet no arquivo app.py.

Autor: [Bruno Novais Costa Simões]
Data: [09/05/2025]
Versão: 1.0
"""

import random

class JogoAdivinhacao:
    """
    Classe principal que gerencia lógica do jogo de adivinhação numérica.
    
    Atributos:
        numero_certo (int): Número aleatório a ser adivinhado
        tentativas_restantes (int): Tentativas restantes no jogo atual
        tentativas_totais (int): Total de tentativas para o jogo atual
        nivel (str): Nível de dificuldade selecionado
        minimo (int): Valor mínimo do intervalo para o nível atual
        maximo (int): Valor máximo do intervalo para o nível atual
    """
    
    def __init__(self):
        """Inicializa o jogo com valores padrão"""
        self.numero_certo = None
        self.tentativas_restantes = 0
        self.tentativas_totais = 0
        self.nivel = None
        self.minimo = 1  # Valor mínimo padrão
        self.maximo = 10  # Valor máximo padrão

    def definir_nivel(self, nivel):
        """
        Configura o nível de dificuldade do jogo e retorna parâmetros de tentativas
        
        Args:
            nivel (str): Nível selecionado ('Fácil (1-10)', 'Médio (1-30)', etc.)
            
        Returns:
            dict: Contendo configurações de tentativas para o nível selecionado:
                - min_tentativas: Mínimo de tentativas permitidas
                - max_tentativas: Máximo de tentativas permitidas
                - divisions: Divisões para o controle deslizante
        """
        self.nivel = nivel
        
        # Configura intervalo e tentativas baseado no nível selecionado
        if nivel == "Fácil (1-10)":
            self.minimo, self.maximo = 1, 10
            return {"min_tentativas": 1, "max_tentativas": 4, "divisions": 3}
        elif nivel == "Médio (1-30)":
            self.minimo, self.maximo = 1, 30
            return {"min_tentativas": 1, "max_tentativas": 6, "divisions": 5}
        elif nivel == "Difícil (1-50)":
            self.minimo, self.maximo = 1, 50
            return {"min_tentativas": 1, "max_tentativas": 8, "divisions": 7}
        else:  # Muito Difícil (1-100)
            self.minimo, self.maximo = 1, 100
            return {"min_tentativas": 1, "max_tentativas": 10, "divisions": 9}

    def iniciar_jogo(self, tentativas_selecionadas):
        """
        Inicia um novo jogo com as configurações selecionadas
        
        Args:
            tentativas_selecionadas (int): Número de tentativas escolhido pelo jogador
            
        Returns:
            dict: Contendo informações do jogo iniciado:
                - numero_certo: Número aleatório gerado
                - tentativas: Total de tentativas
                - min: Valor mínimo do intervalo
                - max: Valor máximo do intervalo
        """
        self.numero_certo = random.randint(self.minimo, self.maximo)
        self.tentativas_totais = tentativas_selecionadas
        self.tentativas_restantes = self.tentativas_totais
        
        return {
            "numero_certo": self.numero_certo,
            "tentativas": self.tentativas_totais,
            "min": self.minimo,
            "max": self.maximo
        }

    def verificar_palpite(self, palpite):
        """
        Verifica se o palpite do jogador está correto e retorna feedback
        
        Args:
            palpite (int): Número digitado pelo jogador
            
        Returns:
            dict: Contendo informações sobre o resultado do palpite:
                - valido: Booleano indicando se o palpite está no intervalo válido
                - acertou: Booleano indicando se o palpite estava correto
                - mensagem: Feedback para o jogador
                - cor: Cor para exibição do feedback
                - tentativas_restantes: Tentativas restantes após este palpite
                - jogo_acabou: Booleano indicando se o jogo terminou
                - numero_certo: Número correto (apenas quando o jogo acaba)
        """
        # Verifica se o palpite está dentro do intervalo válido
        if palpite < self.minimo or palpite > self.maximo:
            return {
                "valido": False,
                "mensagem": f"⚠️ Digite entre {self.minimo} e {self.maximo}! Essa tentativa não foi contada.",
                "cor": "AMBER_400"
            }
            
        # Decrementa tentativas restantes
        self.tentativas_restantes -= 1
        
        # Verifica se o palpite está correto
        if palpite == self.numero_certo:
            return {
                "valido": True,
                "acertou": True,
                "mensagem": f"🎉 Acertou em {self.tentativas_totais - self.tentativas_restantes} tentativa(s)!",
                "cor": "GREEN_300",
                "tentativas_restantes": self.tentativas_restantes,
                "jogo_acabou": True
            }
        else:
            # Determina a dica (MAIOR ou MENOR)
            dica = "⬆️ MAIOR!" if palpite < self.numero_certo else "⬇️ MENOR!"
            mensagem = dica
            
            # Se acabaram as tentativas, revela o número correto
            if self.tentativas_restantes == 0:
                mensagem = f"💀 Fim! O número era {self.numero_certo}."
                
            return {
                "valido": True,
                "acertou": False,
                "mensagem": mensagem,
                "cor": "RED_300",
                "tentativas_restantes": self.tentativas_restantes,
                "jogo_acabou": self.tentativas_restantes == 0,
                "numero_certo": self.numero_certo if self.tentativas_restantes == 0 else None
            }