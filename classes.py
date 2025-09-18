# --- Arquivo: classes.py ---
# Contém as classes que definem a estrutura e as regras do jogo (o "Motor").

import pygame
import random
from collections import deque
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
        self.vazas_ganhas = 0
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
        self.log_de_jogo = deque(maxlen=50)
        # Adiciona o jogador humano.
        self.jogadores.append(Jogador("Jogador 1", eh_humano=True))
        # Adiciona os jogadores controlados pela IA.
        for i in range(numero_de_jogadores - 1):
            self.jogadores.append(Jogador(f"IA_{i+1}"))
        self.fase_do_jogo = "PROMETENDO"     
        self.vaza_atual = [] # Lista para guardar as cartas jogadas na rodada.
        self.rodada_atual_num_cartas = 1
        # --- LÓGICA MOVIDA DA MAIN ---
        # A distribuição de cartas agora é responsabilidade do Jogo.
        for jogador in self.jogadores:
            self.baralho.distribuir(jogador, self.rodada_atual_num_cartas)
    
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
            self.log_de_jogo.append("\n--- FASE DE JOGO INICIADA ---")
            # c. Adicione um self.log_de_jogo.append() com flush=True para nos dar um feedback no terminal
            #    de que a fase mudou com sucesso.
            #    Ex: 
    # Dentro da class Jogo:
    # Em classes.py, na class Jogo:

    def jogador_tenta_jogar_carta(self, indice_jogador, carta_obj):
        """
        Processa a tentativa de um jogador de jogar uma carta.
        Valida o turno e a posse da carta antes de alterar o estado do jogo.
        Retorna True se a jogada for bem-sucedida, False caso contrário.
        """
        # --- Verificações de Validade (Guard Clauses) ---
        
        # 1. Verifica se é o turno do jogador correto.
        if self.fase_do_jogo != "JOGANDO":
            self.log_de_jogo.append(f"Não se pode jogar cartas na fase de {self.fase_do_jogo}")
            return False
        
        if indice_jogador != self.turno_atual:
            self.log_de_jogo.append(f"Não é a vez de {self.jogadores[indice_jogador].nome}")
            return False
        
        jogador = self.jogadores[indice_jogador]
        
        # 2. Verifica se a carta está de fato na mão do jogador.
        if carta_obj not in jogador.mao:
            # Esta verificação é importante para a lógica de arrastar e soltar.
            self.log_de_jogo.append(f"Erro: {jogador.nome} tentou jogar {carta_obj} mas não a possui.")
            return False
            
        # --- Lógica da Jogada Bem-Sucedida ---
        # Se passamos pelas verificações, a jogada é válida.
        
        # Remove a carta da mão e a adiciona à vaza com um ângulo aleatório.
        jogador.mao.remove(carta_obj)
        angulo_aleatorio = random.uniform(-15, 15)
        self.vaza_atual.append((carta_obj, indice_jogador, angulo_aleatorio))
        
        # Anuncia a jogada, escondendo a informação se for a rodada "na testa".
        
        self.log_de_jogo.append(f"{jogador.nome} jogou: {carta_obj}")
        
        # Avança o turno para o próximo jogador.
        self.avancar_turno()
        
        return True
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
            self.log_de_jogo.append(f"{ia_jogador.nome} prometeu fazer 0 cartas.")
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
        self.log_de_jogo.append(f"{ia_jogador.nome} prometeu fazer {ia_jogador.promessa_atual} cartas.")

        # Avança o turno para o próximo jogador (ou para a próxima fase).
        self.avancar_turno()
    def processar_jogada_ia(self):
        """
        Processa a lógica para um jogador IA jogar uma carta aleatória da mão.
        """
        jogador_do_turno = self.jogadores[self.turno_atual]
        
        # --- Guard Clause (Verificação de Segurança) ---
        # Se não for a fase de jogo OU se o jogador do turno for humano, o método para aqui.
        if self.fase_do_jogo != "JOGANDO" or jogador_do_turno.eh_humano:
            return
            
        # Se passamos pela verificação, sabemos que é a vez de uma IA jogar.
        if jogador_do_turno.mao:
            # Escolhe uma carta aleatória da mão.
            carta_escolhida = random.choice(jogador_do_turno.mao)
            
            # Manda o motor do jogo processar a jogada, passando o ÍNDICE e o OBJETO da carta.
            self.jogador_tenta_jogar_carta(self.turno_atual, carta_escolhida)
   # Em classes.py, na class Jogo

    def processar_fim_da_vaza(self):
        """
        Analisa a vaza atual, determina o vencedor, atualiza o estado do jogo
        e prepara para a próxima vaza ou para a próxima rodada.
        """
        # Verificação de segurança: só roda se a vaza estiver cheia.
        if len(self.vaza_atual) != len(self.jogadores):
            return

        # --- Lógica do Cangar ---
        # 1. Conta a ocorrência de cada valor de carta (que não seja manilha).
        contagem_valores = {}
        for carta, _, _ in self.vaza_atual: # Desempacotamento elegante da tupla
            if carta.poder_de_jogo <= 10:
                valor = carta.valor
                contagem_valores[valor] = contagem_valores.get(valor, 0) + 1
        
        # 2. Cria uma lista dos valores que foram "cangados" (contagem > 1).
        valores_cangados = []
        for valor, contagem in contagem_valores.items():
            if contagem > 1:
                valores_cangados.append(valor)
                
        # 3. Cria uma lista final de jogadas válidas para vencer.
        jogadas_validas = []
        for jogada in self.vaza_atual:
            carta = jogada[0]
            # A jogada é válida se a carta for uma manilha OU se seu valor não foi cangado.
            if carta.poder_de_jogo > 10 or carta.valor not in valores_cangados:
                jogadas_validas.append(jogada)

        # --- Encontrando o Vencedor ---
        vencedor_encontrado = False
        if jogadas_validas:
            # Encontra a jogada com a carta de maior poder entre as válidas.
            jogada_vencedora = max(jogadas_validas, key=lambda jogada: jogada[0].poder_de_jogo)
            
            # Pega o índice do jogador vencedor a partir da jogada vencedora.
            indice_vencedor = jogada_vencedora[1]
            
            # Incrementa o contador de vazas ganhas do vencedor.
            self.jogadores[indice_vencedor].vazas_ganhas += 1
            
            # O vencedor da vaza começa a próxima.
            self.turno_atual = indice_vencedor
            vencedor_encontrado = True
            
        # Se todas as cartas se anularam, o primeiro a jogar a vaza começa a próxima.
        if not vencedor_encontrado:
            indice_primeiro_a_jogar = self.vaza_atual[0][1]
            self.turno_atual = indice_primeiro_a_jogar

        # --- Limpeza e Fim de Rodada ---
        self.log_de_jogo.append(f"Vencedor da vaza: {self.jogadores[self.turno_atual].nome}")
        self.vaza_atual.clear()
        
        # Verifica se a rodada acabou (se as mãos estão vazias).
        if not self.jogadores[0].mao:
            self.log_de_jogo.append("--- FIM DA RODADA ---")
            # (Aqui entrará a lógica de pontuação antes de preparar a próxima rodada)
            self.preparar_proxima_rodada()

    def preparar_proxima_rodada(self):
        """
        Prepara o jogo para a próxima rodada: limpa o estado anterior,
        ajusta o número de cartas e distribui novamente.
        """
        # a. Avança o contador de cartas.
        self.rodada_atual_num_cartas += 1
        
        # b. Implementa o ciclo: se passar de 5, volta para 1.
        if self.rodada_atual_num_cartas > 5:
            self.rodada_atual_num_cartas = 1
            
        # c. Cria um baralho novo e já o embaralha.
        self.baralho = Baralho()
        self.baralho.embaralhar()
        
        # d. Limpa a vaza da rodada anterior.
        self.vaza_atual.clear()
        
        # e. Percorre cada jogador para limpar sua mão, resetar sua promessa
        #    e distribuir as novas cartas.
        for jogador in self.jogadores:
            jogador.mao.clear()
            jogador.promessa_atual = -1
            # Distribui o novo número de cartas.
            self.baralho.distribuir(jogador, self.rodada_atual_num_cartas)
        
        # f. Reseta o estado do jogo para o início de uma nova fase de promessas.
        self.fase_do_jogo = "PROMETENDO"
        self.turno_atual = 0 # O turno sempre volta para o jogador 0 no início da rodada.