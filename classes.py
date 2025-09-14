# --- Arquivo: classes.py ---
# Contém as classes que definem a estrutura e as regras do jogo (o "Motor").

import pygame
import random

class Carta:
    """ Representa uma única carta do baralho, com seu valor, naipe, imagem e poder de jogo. """
    def __init__(self, valor, naipe):
        # Atributos básicos da carta
        self.valor = valor
        self.naipe = naipe

        # Lógica para construir o nome do arquivo da imagem e carregá-la
        valor_para_nome = {
            1: 'as', 2: 'dois', 3: 'tres', 4: 'quatro', 5: 'cinco', 
            6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez'
        }
        caminho_da_imagem = f"assets/{valor_para_nome[self.valor]}_de_{self.naipe}.png"
        self.imagem = pygame.image.load(caminho_da_imagem)

        # Lógica que define a força de cada carta para comparações
        if self.naipe == "paus" and self.valor == 4:
            self.poder_de_jogo = 14 # Zap
        elif self.naipe == "copas" and self.valor == 7:
            self.poder_de_jogo = 13 # Sete de Copas
        elif self.naipe == "espadas" and self.valor == 1:
            self.poder_de_jogo = 12 # Espadilha
        elif self.naipe == "ouros" and self.valor == 7:
            self.poder_de_jogo = 11 # Sete de Ouros
        else: 
            self.poder_de_jogo = self.valor

    def __repr__(self):
        """ Retorna uma representação em texto da carta, útil para debug. """
        valor_para_nome = {
            1: 'Ás', 2: 'Dois', 3: 'Três', 4: 'Quatro', 5: 'Cinco', 
            6: 'Seis', 7: 'Sete', 8: 'Oito', 9: 'Nove', 10: 'Dez'
        }
        return f"{valor_para_nome[self.valor]} de {self.naipe.capitalize()}"

class Baralho:
    """ Representa um baralho com 40 cartas, capaz de criar, embaralhar e distribuir cartas. """
    def __init__(self):
        self.cartas = []
        naipes = ['paus', 'copas', 'espadas', 'ouros']
        valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for naipe in naipes:
            for valor in valores:
                self.cartas.append(Carta(valor, naipe))

    def __repr__(self):
        return f"Baralho com {len(self.cartas)} cartas"

    def embaralhar(self):
        random.shuffle(self.cartas)

    def distribuir(self, jogador, quantidade):
        for _ in range(quantidade):
            if self.cartas:
                jogador.mao.append(self.cartas.pop(0))

class Jogador:
    """ Representa um jogador, com nome, mão de cartas e vidas. """
    def __init__(self, nome, eh_humano=False):
        self.nome = nome
        self.eh_humano = eh_humano
        self.mao = []
        self.vidas = 5
        
    def __repr__(self):
        return f"Jogador {self.nome} com {len(self.mao)} cartas"

# --- NOVO: A CLASSE JOGO (O "MOTOR" / "MINI-SERVIDOR") ---
class Jogo:
    """
    Orquestra todas as regras e o estado do jogo.
    Esta classe não sabe nada sobre Pygame ou desenhos, apenas sobre as regras.
    """
    def __init__(self, numero_de_jogadores=2):
        self.baralho = Baralho()
        self.baralho.embaralhar()
        
        # Cria a lista de jogadores.
        self.jogadores = []
        # Adiciona o jogador humano.
        self.jogadores.append(Jogador("Jogador 1", eh_humano=True))
        # Adiciona os jogadores controlados pela IA.
        for i in range(numero_de_jogadores - 1):
            self.jogadores.append(Jogador(f"IA_{i+1}"))
            
        self.vaza_atual = [] # Lista para guardar as cartas jogadas na rodada.
        
        # --- LÓGICA MOVIDA DA MAIN ---
        # A distribuição de cartas agora é responsabilidade do Jogo.
        for jogador in self.jogadores:
            self.baralho.distribuir(jogador, 5)

    # Dentro da class Jogo:
    def jogador_tenta_jogar_carta(self, indice_jogador, carta_obj):
        jogador = self.jogadores[indice_jogador]
    
    # A verificação de segurança agora é se a carta realmente existe na mão.
        if carta_obj in jogador.mao:
        # Usamos .remove() para tirar o objeto específico da lista.
            jogador.mao.remove(carta_obj)
            self.vaza_atual.append((carta_obj, indice_jogador, random.uniform(-15, 15)))
            return True
        return False
            
        print(f"{jogador.nome} tentou uma jogada inválida.") # Feedback para debug
        return False # A jogada falhou