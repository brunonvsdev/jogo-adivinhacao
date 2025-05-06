import random

class JogoAdivinhacao:
    def __init__(self):
        self.numero_certo = None
        self.tentativas_restantes = 0
        self.tentativas_totais = 0
        self.nivel = None
        self.minimo = 1
        self.maximo = 10

    def definir_nivel(self, nivel):
        self.nivel = nivel
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
        self.tentativas_restantes -= 1
        if palpite == self.numero_certo:
            return {
                "acertou": True,
                "mensagem": f"🎉 Acertou em {self.tentativas_totais - self.tentativas_restantes} tentativa(s)!",
                "cor": "GREEN_300",
                "tentativas_restantes": self.tentativas_restantes,
                "jogo_acabou": True
            }
        else:
            dica = "⬆️ MAIOR!" if palpite < self.numero_certo else "⬇️ MENOR!"
            return {
                "acertou": False,
                "mensagem": dica,
                "cor": "RED_300",
                "tentativas_restantes": self.tentativas_restantes,
                "jogo_acabou": self.tentativas_restantes == 0
            }