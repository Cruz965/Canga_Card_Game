# --- Bloco 1: Importação e Inicialização ---

# Primeiro, precisamos importar a biblioteca pygame para podermos usá-la.
import pygame
import sys
from classes import Baralho, Carta, Jogador
# Agora, inicializamos todos os módulos do pygame. Este é um passo obrigatório.
pygame.init()

# --- Bloco 2: Constantes e Configurações da Tela ---

# É uma boa prática definir valores que não mudam (constantes) no início do código.
# Vamos definir a largura e a altura da nossa janela. Use os valores que discutimos.
LARGURA_TELA = 1280
ALTURA_TELA = 720
POSICAO_Y_MAO = 580 # (Ajustei um pouco para baixo)
POSICAO_Y_ESCONDIDA = ALTURA_TELA - 40
LARGURA_CARTA = 100
ESPACAMENTO_ENTRE_CARTAS = LARGURA_CARTA / 3
# As cores em pygame são definidas por tuplas (R, G, B) - Vermelho, Verde, Azul.
# Vamos definir uma cor para o fundo da nossa mesa. Um verde escuro é clássico.
# Valores vão de 0 a 255. Tente algo como (7, 99, 36).
COR_MESA = (7, 99, 36)

# Agora, criamos a janela principal do jogo usando as constantes de largura e altura.

# A função para isso fica dentro do módulo 'display' do pygame.
# Atribua o resultado a uma variável chamada 'tela' ou 'screen'.
tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
# Vamos definir o título que aparece na barra superior da janela.
pygame.display.set_caption("Canga")
# ... todo o seu Bloco 2, terminando com pygame.display.set_caption("Canga") ...


# ... (código do Bloco 2 termina aqui) ...

# --- Bloco 2.5: Preparação da Rodada ---

# 1. Crie uma instância do nosso Baralho e guarde em uma variável.
# Lembre-se que o construtor é chamado com parênteses.
baralho = Baralho()

# 2. Chame o método de embaralhar do objeto que você acabou de criar.
baralho.embaralhar()

# 3. Crie os jogadores. Vamos usar sua sugestão de nomes genéricos.
# Crie um objeto da classe Jogador para o 'jogador1', passando o nome "Jogador 1"
# e o parâmetro eh_humano=True.
jogador1 = Jogador("jogador 1", True)
# Crie um segundo objeto Jogador para o 'jogador2', passando apenas o nome "IA 1".
jogador2= Jogador("IA 1")

# 4. Use o método 'distribuir' do seu baralho para dar 5 cartas para o jogador1.
baralho.distribuir(jogador1, 5)

# 5. Faça o mesmo para o jogador2, dando 5 cartas para ele também.
baralho.distribuir(jogador2, 5)
# ----------------- VARIÁVEIS DE ESTADO ------------------
# --- NOVA LÓGICA: Variável para o timer de inatividade do mouse ---
# A função pygame.time.get_ticks() nos dá o número de milissegundos desde o início do jogo.
# Vamos guardar o tempo do último movimento aqui.
ultimo_movimento_mouse = pygame.time.get_ticks()
# --- NOVA LÓGICA: Variável para a seleção via teclado ---
# Guarda o índice da carta que está selecionada pelo teclado.
# Começamos com 0 para que a primeira carta da mão já comece selecionada.
# Crie a variável 'indice_selecionado_teclado' e inicialize com 0.
indice_selecionado_teclado = 0
# --- Bloco 3: O Loop Principal do Jogo ---
# O coração de todo jogo é um "game loop", um laço de repetição que continua
# rodando enquanto o jogo estiver ativo. Usaremos um 'while' para isso.
# Primeiro, crie uma variável chamada 'rodando' e defina-a como True.
rodando = True
# Agora, inicie o loop 'while' que continuará enquanto 'rodando' for True.
# --- NOVA LÓGICA: Variável de estado para a visibilidade da mão ---
# Crie a variável 'mao_visivel' e inicialize com o valor True,
# para que o jogo comece com a mão do jogador já visível.
mao_visivel = True
while(rodando is True):
    # --- 3.1: Loop de Eventos ---
    # Processa a fila de eventos a cada frame.
    for event in pygame.event.get():
    
        # Evento para fechar a janela.
        if event.type == pygame.QUIT:
            rodando = False
            
        # Reseta o timer de inatividade do mouse e o torna visível ao mover.
        if event.type == pygame.MOUSEMOTION:
            ultimo_movimento_mouse = pygame.time.get_ticks()
            pygame.mouse.set_visible(True)
            
        # Lida com todas as teclas pressionadas.
        if event.type == pygame.KEYDOWN:
            # Navegação na mão com A/D e Setas Direcionais.
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                indice_selecionado_teclado += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                indice_selecionado_teclado -= 1
            # Alterna a visibilidade da mão com a Barra de Espaço.
            elif event.key == pygame.K_SPACE:
                mao_visivel = not mao_visivel

            # Garante que o índice da seleção do teclado não saia dos limites da mão.
            if indice_selecionado_teclado > len(jogador1.mao) - 1:
                indice_selecionado_teclado = len(jogador1.mao) - 1
            if indice_selecionado_teclado < 0:
                indice_selecionado_teclado = 0

        # Lida com cliques do mouse.
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Alterna a visibilidade da mão com o botão direito.
            if event.button == 3: # 3 = Botão direito
                mao_visivel = not mao_visivel
            
        
    if pygame.time.get_ticks() - ultimo_movimento_mouse > 4000:
        # Se for, mandamos o Pygame esconder o cursor.
            pygame.mouse.set_visible(False)

            
    # --- 3.2: Lógica de Desenho e Interação ---
    # Limpa a tela a cada frame com a cor de fundo.
    tela.fill(COR_MESA)
    
    # Prepara as variáveis necessárias para a interação a cada frame.
    pos_mouse = pygame.mouse.get_pos()
    indice_carta_hover = -1 # -1 significa que nenhuma carta está sob o mouse.
    
    # Pega a mão do jogador atual para desenhar.
    cartas_da_mao = jogador1.mao
    
    # Só executa a lógica de desenho se o jogador tiver cartas na mão.
    if cartas_da_mao:
    
        # --- Cálculos de Layout ---
        # Calcula a largura total que a mão ocupará e a posição X inicial para centralizá-la.
        largura_total_mao = (len(cartas_da_mao) - 1) * ESPACAMENTO_ENTRE_CARTAS + LARGURA_CARTA
        posicao_x_inicial = (LARGURA_TELA - largura_total_mao) / 2

        # --- Determinação da Posição Y ---
        # Decide a altura base da mão (visível ou escondida) com base no estado de 'mao_visivel'.
        if mao_visivel:
            pos_y_base = POSICAO_Y_MAO
        else:
            pos_y_base = POSICAO_Y_ESCONDIDA

        # --- Lógica de Interação e Desenho (Unificada) ---
        
        # 1. Calcula a posição de todas as cartas e guarda seus retângulos (rects).
        lista_de_rects_da_mao = []
        for i, carta in enumerate(cartas_da_mao):
            posicao_x_carta = posicao_x_inicial + i * ESPACAMENTO_ENTRE_CARTAS
            rect_da_carta = carta.imagem.get_rect()
            rect_da_carta.topleft = (posicao_x_carta, pos_y_base)
            lista_de_rects_da_mao.append(rect_da_carta)
            
        # 2. Detecta qual carta está sob o mouse, checando de trás para frente (prioridade da carta de cima).
        for i in range(len(lista_de_rects_da_mao) - 1, -1, -1): 
            rect_atual = lista_de_rects_da_mao[i]
            if rect_atual.collidepoint(pos_mouse):
                indice_carta_hover = i
                break
        
        # 3. Desenha cada carta na tela, aplicando o efeito de levitação se necessário.
        for i, carta in enumerate(cartas_da_mao):
            rect_para_desenhar = lista_de_rects_da_mao[i]
            
            # A carta levita se estiver sob o mouse, ou se (não havendo mouse) for a selecionada pelo teclado.
            if i == indice_carta_hover or (indice_carta_hover == -1 and i == indice_selecionado_teclado):
                # Cria uma cópia do rect e a move para cima para o efeito de levitação.
                rect_modificado = rect_para_desenhar.copy()
                rect_modificado.y = pos_y_base - 30
                tela.blit(carta.imagem, rect_modificado)
            else:
                # Desenha a carta na sua posição padrão.
                tela.blit(carta.imagem, rect_para_desenhar)

    # --- 3.3: Atualização da Tela ---
    # Revela tudo o que foi desenhado neste frame.
    pygame.display.flip()
# --- Bloco 4: Finalização ---
    
# O loop 'while' terminou, o que significa que o jogo acabou.
# Agora, podemos fechar o pygame de forma segura.
# Esta é a função que desinicializa a biblioteca.
pygame.quit()
sys.exit()