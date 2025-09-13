# --- Arquivo: main.py ---
# Responsável apenas pela parte VISUAL e de INPUTS do jogo (o "Cliente").
# Não contém nenhuma regra de jogo.

import pygame
import sys
# --- ALTERADO: Agora só precisamos importar a classe principal Jogo ---
from classes import Jogo

# --- Bloco 2: Constantes e Configurações ---
# (Nenhuma mudança aqui, seu bloco de constantes está perfeito)
LARGURA_TELA = 1280
ALTURA_TELA = 720
POSICAO_Y_MAO = 580
POSICAO_Y_ESCONDIDA = ALTURA_TELA - 40
LARGURA_CARTA = 100
ESPACAMENTO_ENTRE_CARTAS = LARGURA_CARTA / 3
COR_MESA = (7, 99, 36)
CENTRO_DA_TELA = (LARGURA_TELA // 2, ALTURA_TELA // 2)
COR_MESA_ESCURA = (80, 42, 25)
COR_MESA_CLARA = (160, 69, 19)

# --- Inicialização do Pygame e da Tela ---
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Canga")

# --- ALTERADO: Bloco 2.5 agora é muito mais simples ---
# Toda a lógica de criar baralho, jogadores e distribuir foi para a classe Jogo.
# O 'main' agora só precisa criar uma instância do Jogo.
nosso_jogo = Jogo(numero_de_jogadores=2) # Você pode mudar o número aqui para testar

# --- Variáveis de Estado da INTERFACE (não do jogo) ---
ultimo_movimento_mouse = pygame.time.get_ticks()
indice_selecionado_teclado = 0
mao_visivel = True
rodando = True

# --- Bloco 3: O Loop Principal do Jogo ---
while rodando:
    
    # --- 3.1: Loop de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            
        if event.type == pygame.MOUSEMOTION:
            ultimo_movimento_mouse = pygame.time.get_ticks()
            pygame.mouse.set_visible(True)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                indice_selecionado_teclado += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                indice_selecionado_teclado -= 1
            elif event.key == pygame.K_SPACE:
                mao_visivel = not mao_visivel
            
            # --- ALTERADO: Ação de Jogar Carta ---
            elif event.key == pygame.K_RETURN:
                # O 'main' não sabe as regras. Ele apenas informa a INTENÇÃO ao motor do jogo.
                # Primeiro, pegamos o jogador humano (índice 0)
                jogador_humano = nosso_jogo.jogadores[0]
                
                # Se o mouse estiver sobre uma carta, ela tem prioridade.
                if indice_carta_hover != -1:
                    indice_para_jogar = indice_carta_hover
                else:
                    indice_para_jogar = indice_selecionado_teclado
                
                # Manda a ordem para o "motor" do jogo.
                nosso_jogo.jogador_tenta_jogar_carta(0, indice_para_jogar)

            # --- ALTERADO: O controle de limites agora precisa verificar se a mão existe ---
            # Pegamos a mão do jogador a partir do objeto 'nosso_jogo'.
            mao_humano = nosso_jogo.jogadores[0].mao
            if mao_humano:
                if indice_selecionado_teclado > len(mao_humano) - 1:
                    indice_selecionado_teclado = len(mao_humano) - 1
                if indice_selecionado_teclado < 0:
                    indice_selecionado_teclado = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mao_visivel = not mao_visivel
                
    # Verificação de inatividade do mouse
    if pygame.time.get_ticks() - ultimo_movimento_mouse > 4000:
        pygame.mouse.set_visible(False)
        
    # --- 3.2: Lógica de Desenho ---
    tela.fill(COR_MESA)
    pos_mouse = pygame.mouse.get_pos()
    # Desenha a mesa
    pygame.draw.circle(tela, COR_MESA_CLARA, CENTRO_DA_TELA, 240)
    pygame.draw.circle(tela, COR_MESA_ESCURA, CENTRO_DA_TELA, 180)
    
    
    # --- NOVO: Desenha as cartas na vaza (na mesa) ---
    # Por enquanto, vamos desenhar todas na mesma posição para o jogador 1
    POSICAO_JOGADA_J1 = (LARGURA_TELA / 2, ALTURA_TELA - 350)
    for carta_na_mesa in nosso_jogo.vaza_atual:
        # Cria uma versão reduzida da imagem da carta (35% do tamanho)
        nova_largura = int(LARGURA_CARTA * 0.35)
        nova_altura = int((LARGURA_CARTA * 1.4) * 0.35) # Mantém a proporção
        imagem_menor = pygame.transform.scale(carta_na_mesa.imagem, (nova_largura, nova_altura))
        
        rect_menor = imagem_menor.get_rect(center=POSICAO_JOGADA_J1)
        tela.blit(imagem_menor, rect_menor)

    # --- Lógica de Desenho da Mão ---
    # --- ALTERADO: Pega os dados do objeto 'nosso_jogo' ---
    cartas_da_mao = nosso_jogo.jogadores[0].mao
    indice_carta_hover = -1
    
    if cartas_da_mao:
        largura_total_mao = (len(cartas_da_mao) - 1) * ESPACAMENTO_ENTRE_CARTAS + LARGURA_CARTA
        posicao_x_inicial = (LARGURA_TELA - largura_total_mao) / 2

        if mao_visivel:
            pos_y_base = POSICAO_Y_MAO
        else:
            pos_y_base = POSICAO_Y_ESCONDIDA

        lista_de_rects_da_mao = []
        for i, carta in enumerate(cartas_da_mao):
            posicao_x_carta = posicao_x_inicial + i * ESPACAMENTO_ENTRE_CARTAS
            rect_da_carta = carta.imagem.get_rect(topleft=(posicao_x_carta, pos_y_base))
            lista_de_rects_da_mao.append(rect_da_carta)
            
        for i in range(len(lista_de_rects_da_mao) - 1, -1, -1): 
            if lista_de_rects_da_mao[i].collidepoint(pos_mouse):
                indice_carta_hover = i
                break
        
        for i, carta in enumerate(cartas_da_mao):
            rect_para_desenhar = lista_de_rects_da_mao[i]
            
            if i == indice_carta_hover or (indice_carta_hover == -1 and i == indice_selecionado_teclado):
                rect_modificado = rect_para_desenhar.copy()
                rect_modificado.y = pos_y_base - 30
                tela.blit(carta.imagem, rect_modificado)
            else:
                tela.blit(carta.imagem, rect_para_desenhar)

    # --- 3.3: Atualização da Tela ---
    pygame.display.flip()

# --- 4: Finalização ---
pygame.quit()
sys.exit()