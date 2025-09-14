# --- Arquivo: main.py ---
# Responsável apenas pela parte VISUAL e de INPUTS do jogo (o "Cliente").
# Não contém nenhuma regra de jogo.

import pygame
import sys
import math
# --- ALTERADO: Agora só precisamos importar a classe principal Jogo ---
from classes import Jogo
# --- Bloco #: Funções Auxiliares ---
# --- NOVA FUNÇÃO AUXILIAR ---
# Calcula as posições (x, y) para cada jogador ao redor de um ponto central.
def calcular_posicoes_jogadores(num_jogadores, centro, raio):
    posicoes_dos_jogadores = []
    for i in range(num_jogadores):
        #Começando do 90 graus que é a posição do primeiro jogador
        angulo_em_graus = 90 + 360/num_jogadores * i
        angulo_radianos = math.radians(angulo_em_graus)

        deslocamento_x = raio*math.cos(angulo_radianos)
        deslocamento_y = raio*math.sin(angulo_radianos)
        
        pos_x = centro[0] + deslocamento_x
        pos_y = centro[1] + deslocamento_y

        posicoes_dos_jogadores.append((pos_x, pos_y))
    return posicoes_dos_jogadores
# Começa o jogador 0 em 270 graus (base da tela).
# Comente o código para eu escrever

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
CENTRO_DA_MESA = (CENTRO_DA_TELA[0], CENTRO_DA_TELA[1]-50)
COR_MESA_ESCURA = (80, 42, 25)
COR_MESA_CLARA = (160, 69, 19)
RAIO_MAIOR = 240
RAIO_MENOR = 180
RAIO_JOGADA = RAIO_MAIOR - 30
DIAMETRO_MESA_INTERNA = RAIO_MENOR * 2
lado = DIAMETRO_MESA_INTERNA / math.sqrt(2)
MESA_RECT = pygame.Rect(0, 0, lado, lado)
MESA_RECT.center = CENTRO_DA_MESA
# --- Inicialização do Pygame e da Tela ---
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Canga")

# --- ALTERADO: Bloco 2.5 agora é muito mais simples ---
# Toda a lógica de criar baralho, jogadores e distribuir foi para a classe Jogo.
# O 'main' agora só precisa criar uma instância do Jogo.

nosso_jogo = Jogo(numero_de_jogadores=2) # Você pode mudar o número aqui para testar

POSICOES_JOGADA = calcular_posicoes_jogadores(len(nosso_jogo.jogadores),CENTRO_DA_MESA,RAIO_JOGADA)
# --- Variáveis de Estado da INTERFACE (não do jogo) ---
ultimo_movimento_mouse = pygame.time.get_ticks()
indice_selecionado_teclado = 0
carta_sendo_arrastada = None
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
                # Pega o jogador humano.
                jogador_humano = nosso_jogo.jogadores[0]
                
                # Só tenta jogar se o jogador tiver cartas e não estiver arrastando uma.
                if jogador_humano.mao and not carta_sendo_arrastada:
                    
                    # Decide qual índice usar (prioridade do mouse).
                    if indice_carta_hover != -1:
                        indice_para_jogar = indice_carta_hover
                    else:
                        indice_para_jogar = indice_selecionado_teclado
                    
                    # --- A CORREÇÃO ESTÁ AQUI ---
                    # 1. Pega o OBJETO da carta usando o índice que encontramos.
                    carta_para_jogar = jogador_humano.mao[indice_para_jogar]
                    
                    # 2. Manda a ordem para o "motor" do jogo, enviando o OBJETO da carta.
                    nosso_jogo.jogador_tenta_jogar_carta(0, carta_para_jogar)

            # --- ALTERADO: O controle de limites agora precisa verificar se a mão existe ---
            # Pegamos a mão do jogador a partir do objeto 'nosso_jogo'.
            mao_humano = nosso_jogo.jogadores[0].mao
            if mao_humano:
                if indice_selecionado_teclado > len(mao_humano) - 1:
                    indice_selecionado_teclado = len(mao_humano) - 1
                if indice_selecionado_teclado < 0:
                    indice_selecionado_teclado = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botão direito para alternar a visibilidade (sem mudança aqui)
            if event.button == 3:
                mao_visivel = not mao_visivel
            
            # Botão esquerdo para "Agarrar" a carta
            if event.button == 1:
                # Só podemos agarrar uma carta se a mão estiver visível e não estivermos já arrastando outra.
                if mao_visivel and indice_carta_hover != -1 and not carta_sendo_arrastada:
                    
                    # Pega a carta e seu índice original. ATENÇÃO: não removemos mais a carta da mão aqui.
                    carta_clicada = nosso_jogo.jogadores[0].mao[indice_carta_hover]
                    indice_original = indice_carta_hover
                    
                    # Calcula o offset do clique em relação ao canto da carta.
                    rect_da_carta_clicada = lista_de_rects_da_mao[indice_carta_hover]
                    offset_x = event.pos[0] - rect_da_carta_clicada.x
                    offset_y = event.pos[1] - rect_da_carta_clicada.y
                    
                    # Guarda o estado: a carta, seu índice original, e o offset.
                    carta_sendo_arrastada = (carta_clicada, indice_original, (offset_x, offset_y))
        
     # --- Lógica para "Soltar" a Carta ---
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Botão esquerdo do mouse
                if carta_sendo_arrastada:
                    # Desempacota os dados da carta.
                    carta_obj, indice_original, offset = carta_sendo_arrastada
                    
                    # Cria o rect da carta na posição em que foi solta.
                    pos_soltura_x = event.pos[0] - offset[0]
                    pos_soltura_y = event.pos[1] - offset[1]
                    rect_solto = carta_obj.imagem.get_rect(topleft=(pos_soltura_x, pos_soltura_y))

                    # 1. A carta foi solta na MESA?
                    if MESA_RECT.colliderect(rect_solto):
                        nosso_jogo.jogador_tenta_jogar_carta(0, carta_obj)
                    
                    else:
                        # Se não foi na mesa, foi na mão ou perto dela?
                        area_da_mao_rect = None
                        if lista_de_rects_da_mao:
                            primeiro_rect = lista_de_rects_da_mao[0]
                            ultimo_rect = lista_de_rects_da_mao[-1]
                            area_da_mao_rect = pygame.Rect(
                                primeiro_rect.left, primeiro_rect.top,
                                ultimo_rect.right - primeiro_rect.left, primeiro_rect.height
                            )
                        
                        # 2. A carta foi solta EXATAMENTE sobre a MÃO?
                        if area_da_mao_rect and area_da_mao_rect.colliderect(rect_solto):
                            # Lógica para reordenar com precisão.
                            carta_removida = nosso_jogo.jogadores[0].mao.pop(indice_original)
                            novo_indice = len(nosso_jogo.jogadores[0].mao)
                            for i, rect_na_mao in enumerate(lista_de_rects_da_mao):
                                if i == indice_original: continue
                                if rect_solto.centerx < rect_na_mao.centerx:
                                    novo_indice = i
                                    break
                            nosso_jogo.jogadores[0].mao.insert(novo_indice, carta_removida)
                        
                        # --- SUA NOVA REGRA AQUI ---
                        # 3. SENÃO, a carta foi solta ABAIXO da linha da MÃO?
                        elif area_da_mao_rect and rect_solto.centery > area_da_mao_rect.top:
                            # Remove a carta da posição original.
                            carta_removida = nosso_jogo.jogadores[0].mao.pop(indice_original)
                            
                            # Se soltou à esquerda do centro da mão, insere no início.
                            if rect_solto.centerx < area_da_mao_rect.centerx:
                                nosso_jogo.jogadores[0].mao.insert(0, carta_removida)
                            # Senão, insere no final.
                            else:
                                nosso_jogo.jogadores[0].mao.append(carta_removida)
                        
                        # Se nenhuma condição for atendida, nada acontece,
                        # e a carta "volta" para o lugar quando paramos de arrastar.

                    # Limpa a variável de estado, "soltando" a carta do mouse.
                    carta_sendo_arrastada = None

                    

                    


                
    # Verificação de inatividade do mouse
    if pygame.time.get_ticks() - ultimo_movimento_mouse > 4000:
        pygame.mouse.set_visible(False)
        
    # --- 3.2: Lógica de Desenho ---
    tela.fill(COR_MESA)
    pos_mouse = pygame.mouse.get_pos()
    # Desenha a mesa
    pygame.draw.circle(tela, COR_MESA_CLARA, CENTRO_DA_MESA, RAIO_MAIOR)
    pygame.draw.circle(tela, COR_MESA_ESCURA, CENTRO_DA_MESA, RAIO_MENOR)
    
    
    # --- NOVO: Desenha as cartas na vaza (na mesa) ---
    # Por enquanto, vamos desenhar todas na mesma posição para o jogador 1
    POSICAO_JOGADA_J1 = (LARGURA_TELA / 2, ALTURA_TELA - 350)
    for carta_na_mesa in nosso_jogo.vaza_atual:
        # Cria uma versão reduzida da imagem da carta (35% do tamanho)
        nova_largura = int(LARGURA_CARTA * 0.35)
        nova_altura = int((LARGURA_CARTA * 1.4) * 0.35) # Mantém a proporção
        imagem_menor = pygame.transform.scale(carta_na_mesa[0].imagem, (nova_largura, nova_altura))
        # d. Gira a imagem pequena usando o ângulo que pegamos da vaza.
        imagem_rotacionada = pygame.transform.rotate(imagem_menor, carta_na_mesa[2])
        
        # e. Executa o "truque do pivô" para a rotação não mudar a posição central.
        #    Isso garante que a carta gire em torno do seu próprio centro.
        rect_rotacionado = imagem_rotacionada.get_rect(center = POSICOES_JOGADA[carta_na_mesa[1]])
        
        # f. Finalmente, desenhe a imagem ROTACIONADA na posição do rect ROTACIONADO.
        tela.blit(imagem_rotacionada, rect_rotacionado)


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
            if carta_sendo_arrastada and carta is carta_sendo_arrastada[0]:
                continue # 'continue' pula para a próxima iteração do loop.

            rect_para_desenhar = lista_de_rects_da_mao[i]
            
            if i == indice_carta_hover or (indice_carta_hover == -1 and i == indice_selecionado_teclado):
                rect_modificado = rect_para_desenhar.copy()
                rect_modificado.y = pos_y_base - 30
                tela.blit(carta.imagem, rect_modificado)
            else:
                tela.blit(carta.imagem, rect_para_desenhar)
    if carta_sendo_arrastada:
        carta_obj, indice, offset = carta_sendo_arrastada
        imagem_arrastada = carta_obj.imagem
        nova_pos_x = pos_mouse[0]-offset[0]
        nova_pos_y = pos_mouse[1]-offset[1]

        rect_arrastado = imagem_arrastada.get_rect(topleft=(nova_pos_x,nova_pos_y))
        tela.blit(imagem_arrastada, rect_arrastado)   

   



    # --- 3.3: Atualização da Tela ---
    pygame.display.flip()

# --- 4: Finalização ---
pygame.quit()
sys.exit()