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
        self.promessa_atual = -1
        self.cartas_prometidas = []
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
        self.turno_atual = 0
        # Cria a lista de jogadores.
        self.jogadores = []
        # Adiciona o jogador humano.
        self.jogadores.append(Jogador("Jogador 1", eh_humano=True))
        # Adiciona os jogadores controlados pela IA.
        for i in range(numero_de_jogadores - 1):
            self.jogadores.append(Jogador(f"IA_{i+1}"))
        self.fase_do_jogo = "PROMETENDO"     
        self.vaza_atual = [] # Lista para guardar as cartas jogadas na rodada.
        
        # --- LÓGICA MOVIDA DA MAIN ---
        # A distribuição de cartas agora é responsabilidade do Jogo.
        for jogador in self.jogadores:
            self.baralho.distribuir(jogador, 5)
    
    def avancar_turno(self):
        """Avança o turno para o próximo jogador de forma circular."""
        
        # Pega o número de jogadores diretamente da lista de jogadores.
        num_jogadores = len(self.jogadores)
        
        # Calcula o próximo turno usando o número real de jogadores e atualiza a variável.
        self.turno_atual = (self.turno_atual + 1) % num_jogadores
         # --- NOVA LÓGICA: Checagem de Fim de Fase de Promessas ---
        
        # a. Verifique se a fase atual do jogo é "PROMETENDO"
        #    E se o turno acabou de voltar para o primeiro jogador (ou seja, se self.turno_atual é 0).
        if self.fase_do_jogo == "PROMETENDO" and self.turno_atual == 0:

            # b. Se as duas condições forem verdadeiras, a fase de promessas acabou!
            #    Mude o valor de 'self.fase_do_jogo' para "JOGANDO".
            self.fase_do_jogo = "JOGANDO"
            print("\n--- FASE DE JOGO INICIADA ---", flush=True)
            # c. Adicione um print() com flush=True para nos dar um feedback no terminal
            #    de que a fase mudou com sucesso.
            #    Ex: 
    # Dentro da class Jogo:
    def jogador_tenta_jogar_carta(self, indice_jogador, carta_obj):
        # --- NOVA VERIFICAÇÃO NO INÍCIO ---
        # a. Verifique se o 'indice_jogador' que está tentando jogar
        #    é diferente do 'self.turno_atual'.
       
        if indice_jogador != self.turno_atual:
            print("Erro! Vez de um jogador diferente", flush=True)
            return False
            # Se for diferente, não é a vez dele!
            # Imprima uma mensagem de erro para debug.
            # E retorne False para indicar que a jogada falhou.
            
        jogador = self.jogadores[indice_jogador]
    
    # A verificação de segurança agora é se a carta realmente existe na mão.
        if carta_obj in jogador.mao:
        # Usamos .remove() para tirar o objeto específico da lista.
            
            jogador.mao.remove(carta_obj)
            self.vaza_atual.append((carta_obj, indice_jogador, random.uniform(-15, 15)))
            print(f"{jogador.nome} jogou: {carta_obj}", flush=True)
            self.avancar_turno()

            return True
        
        return False
            
        print(f"{jogador.nome} jogou: {carta_jogada}", flush=True)
        return False # A jogada falhou
    # Dentro da sua class Jogo, em classes.py

    # Encontre o método que criamos (ou crie-o agora)
   # Dentro da class Jogo, em classes.py

    def processar_promessa_ia(self):
        """
        Processa a lógica para um jogador IA fazer sua promessa,
        incluindo a regra da "Soma Impossível".
        """
        # Verificação de segurança: só roda na fase de promessas.
        if self.fase_do_jogo != "PROMETENDO":
            return

        ia_jogador = self.jogadores[self.turno_atual]
        num_cartas_na_mao = len(ia_jogador.mao)
        
        # Caso especial: se a IA não tem cartas, a promessa é 0.
        if num_cartas_na_mao == 0:
            ia_jogador.promessa_atual = 0
            print(f"{ia_jogador.nome} prometeu fazer 0 vazas.", flush=True)
            self.avancar_turno()
            return

        # Gera uma promessa aleatória inicial.
        promessa_ia = random.randint(0, num_cartas_na_mao)

        # --- LÓGICA DA SOMA IMPOSSÍVEL ---
        # Verifica se a IA é a última a prometer.
        if self.turno_atual == len(self.jogadores) - 1:
            
            # Soma as promessas dos jogadores anteriores.
            soma_promessas_anteriores = 0
            # A fatia self.jogadores[:self.turno_atual] pega todos os jogadores ANTES do atual.
            for jogador in self.jogadores[:self.turno_atual]:
                soma_promessas_anteriores += jogador.promessa_atual
            
            # Calcula o número proibido.
            promessa_proibida = num_cartas_na_mao - soma_promessas_anteriores
            
            # Se a promessa aleatória for a proibida, a IA precisa mudar.
            if promessa_ia == promessa_proibida:
                # Uma regra simples para mudar a promessa.
                if promessa_ia < num_cartas_na_mao:
                    promessa_ia += 1
                else:
                    promessa_ia -= 1
        
        # Atribui a promessa final (original ou corrigida) ao jogador.
        ia_jogador.promessa_atual = promessa_ia
        
        # Anuncia a promessa da IA.
        print(f"{ia_jogador.nome} prometeu fazer {ia_jogador.promessa_atual} vazas.", flush=True)

        # Avança o turno para o próximo jogador (ou para a próxima fase).
        self.avancar_turno()