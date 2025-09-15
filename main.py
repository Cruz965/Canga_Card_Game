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
ESPACAMENTO_ENTRE_CARTAS = LARGURA_CARTA / 2
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
jogador_local = nosso_jogo.jogadores[0]
POSICOES_JOGADA = calcular_posicoes_jogadores(len(nosso_jogo.jogadores),CENTRO_DA_MESA,RAIO_JOGADA)
# --- Variáveis de Estado da INTERFACE (não do jogo) ---
ultimo_movimento_mouse = pygame.time.get_ticks()
indice_selecionado_teclado = 0
carta_sendo_arrastada = None
mao_visivel = True
rodando = True
ultimo_clique_tempo = 0
# --- Bloco 3: O Loop Principal do Jogo (VERSÃO REESTRUTURADA) ---
rodando = True
while rodando:

    # --- 3.0: PREPARAÇÃO DO FRAME ---
    # No início de cada frame, calculamos todo o estado e layout necessários
    # para os eventos e para o desenho que virão a seguir.
    
    # Pega a posição atual do mouse.
    pos_mouse = pygame.mouse.get_pos()
    
    # Pega a mão do jogador para os cálculos.
    cartas_da_mao = jogador_local.mao
    
    # Calcula a posição Y base da mão (visível ou escondida).
    if mao_visivel:
        pos_y_base = POSICAO_Y_MAO
    else:
        pos_y_base = POSICAO_Y_ESCONDIDA
        
    # Calcula a lista de retângulos (rects) para a mão do jogador.
    # Esta lista agora está sempre atualizada ANTES do loop de eventos.
    lista_de_rects_da_mao = []
    if cartas_da_mao:
        largura_total_mao = (len(cartas_da_mao) - 1) * ESPACAMENTO_ENTRE_CARTAS + LARGURA_CARTA
        posicao_x_inicial = (LARGURA_TELA - largura_total_mao) / 2
        for i, carta in enumerate(cartas_da_mao):
            posicao_x_carta = posicao_x_inicial + i * ESPACAMENTO_ENTRE_CARTAS
            rect_da_carta = carta.imagem.get_rect(topleft=(posicao_x_carta, pos_y_base))
            lista_de_rects_da_mao.append(rect_da_carta)

    # --- 3.1: PROCESSAMENTO DE EVENTOS ---
    # Com o layout já calculado, agora processamos os inputs do jogador.
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
            elif event.key == pygame.K_RETURN:
               
                
                if jogador_local.mao and not carta_sendo_arrastada:
                    indice_para_jogar = indice_carta_hover if indice_carta_hover != -1 else indice_selecionado_teclado
                    carta_para_jogar = jogador_local.mao[indice_para_jogar]
                    nosso_jogo.jogador_tenta_jogar_carta(0, carta_para_jogar)
            elif event.key == pygame.K_p:
                if nosso_jogo.fase_do_jogo == "PROMETENDO" and nosso_jogo.turno_atual == 0:
                    if jogador_local.mao:
                        carta_selecionada = jogador_local.mao[indice_selecionado_teclado]
                        if carta_selecionada in jogador_local.cartas_prometidas:
                            jogador_local.cartas_prometidas.remove(carta_selecionada)
                        else:
                            jogador_local.cartas_prometidas.append(carta_selecionada)

            # Controle de limites para a seleção do teclado.
            if cartas_da_mao:
                if indice_selecionado_teclado > len(cartas_da_mao) - 1:
                    indice_selecionado_teclado = len(cartas_da_mao) - 1
                if indice_selecionado_teclado < 0:
                    indice_selecionado_teclado = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mao_visivel = not mao_visivel
            # Dentro do seu for event in pygame.event.get():
        # Encontre o 'if event.type == pygame.MOUSEBUTTONDOWN:'

            if event.button == 1: # Botão esquerdo do mouse
                
                # Só executamos qualquer lógica de clique esquerdo se o clique for sobre uma carta válida na mão.
                if mao_visivel and indice_carta_hover != -1 and not carta_sendo_arrastada:
                    
                    # --- ETAPA 1: O "ARRASTE TENTATIVO" ---
                    # Sempre iniciamos "agarrando" a carta, assumindo que será um arraste.
                    # Pegamos a carta clicada e seu índice original.
                    carta_clicada = nosso_jogo.jogadores[0].mao[indice_carta_hover]
                    indice_original = indice_carta_hover
                    
                    # Calculamos o offset do clique em relação ao canto da carta.
                    rect_da_carta_clicada = lista_de_rects_da_mao[indice_carta_hover]
                    offset_x = event.pos[0] - rect_da_carta_clicada.x
                    offset_y = event.pos[1] - rect_da_carta_clicada.y
                    
                    # Definimos o estado de "arrastando", guardando a carta, seu índice e o offset.
                    posicao_inicial_clique = event.pos
                    carta_sendo_arrastada = (carta_clicada, indice_original, (offset_x, offset_y), posicao_inicial_clique)
                    
                    # --- ETAPA 2: O "DIVISOR DE ÁGUAS" (A CHECAGEM DE DOUBLE-CLICK) ---
                    tempo_atual = pygame.time.get_ticks()
                    
                    # Verificamos se o tempo desde o último clique foi curto (menos de 300ms).
                    if tempo_atual - ultimo_clique_tempo < 300: 
                    
                        # Se foi, é um DOUBLE-CLICK! A ação é de PROMESSA.
                        if nosso_jogo.fase_do_jogo == "PROMETENDO" and nosso_jogo.turno_atual == 0:
                            jogador_local = nosso_jogo.jogadores[0]
                            if carta_clicada in jogador_local.cartas_prometidas:
                                jogador_local.cartas_prometidas.remove(carta_clicada)
                            else:
                                jogador_local.cartas_prometidas.append(carta_clicada)
                            
                            # IMPORTANTE: Como foi um double-click, nós CANCELAMOS o arraste.
                            carta_sendo_arrastada = None
                    
                    # No final, ATUALIZAMOS o tempo do último clique para o tempo atual.
                    # Isso prepara o sistema para detectar o próximo double-click.
                    ultimo_clique_tempo = tempo_atual
                  
                    

            
        
         # --- LÓGICA FINAL PARA "SOLTAR" A CARTA ---
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and carta_sendo_arrastada:

                # 1. Desempacota todos os dados que guardamos sobre a carta arrastada.
                carta_obj, indice_original, offset, pos_inicial_clique = carta_sendo_arrastada
                
                # 2. Calcula a posição final da carta (onde o mouse foi solto).
                pos_final_clique = event.pos
                pos_soltura_x = pos_final_clique[0] - offset[0]
                pos_soltura_y = pos_final_clique[1] - offset[1]
                rect_solto = carta_obj.imagem.get_rect(topleft=(pos_soltura_x, pos_soltura_y))

                # 3. Calcula a distância total que o mouse se moveu.
                distancia_movida = math.hypot(pos_final_clique[0] - pos_inicial_clique[0], pos_final_clique[1] - pos_inicial_clique[1])

                # 4. Inicia a "árvore de decisões" sobre o que fazer com a carta.
                
                # Prioridade 1: A carta foi solta na MESA para ser JOGADA?
                # (Isso acontece independentemente da distância do arraste)
                if MESA_RECT.colliderect(rect_solto):
                    nosso_jogo.jogador_tenta_jogar_carta(0, carta_obj)
                
                # Prioridade 2: Se não, foi um ARRASTE LONGO para REORDENAR?
                elif distancia_movida > 10:
                    # Cria a área da mão para checagem.
                    area_da_mao_rect = None
                    if lista_de_rects_da_mao:
                        primeiro_rect = lista_de_rects_da_mao[0]
                        ultimo_rect = lista_de_rects_da_mao[-1]
                        area_da_mao_rect = pygame.Rect(
                            primeiro_rect.left, primeiro_rect.top,
                            ultimo_rect.right - primeiro_rect.left, primeiro_rect.height
                        )
                    
                    # Checa se a largada foi EXATAMENTE sobre a mão.
                    if area_da_mao_rect and area_da_mao_rect.colliderect(rect_solto):
                        # Sua lógica de reordenar com precisão.
                        carta_removida = nosso_jogo.jogadores[0].mao.pop(indice_original)
                        novo_indice = len(nosso_jogo.jogadores[0].mao)
                        temp_rects = [r for i, r in enumerate(lista_de_rects_da_mao) if i != indice_original]
                        for i, rect_na_mao in enumerate(temp_rects):
                            if rect_solto.centerx < rect_na_mao.centerx:
                                novo_indice = i
                                break
                        nosso_jogo.jogadores[0].mao.insert(novo_indice, carta_removida)
                    
                    # Checa se a largada foi PERTO da mão (sua regra de conveniência).
                    elif area_da_mao_rect and rect_solto.centery > area_da_mao_rect.top:
                        carta_removida = nosso_jogo.jogadores[0].mao.pop(indice_original)
                        if rect_solto.centerx < area_da_mao_rect.centerx:
                            nosso_jogo.jogadores[0].mao.insert(0, carta_removida)
                        else:
                            nosso_jogo.jogadores[0].mao.append(carta_removida)
                
                # Se não foi jogada na mesa e não foi um arraste longo,
                # significa que foi um clique simples ou um arraste inválido.
                # Nesses casos, não fazemos nada, e a carta "volta" ao seu lugar
                # simplesmente por pararmos de arrastá-la.
                
                # ESSENCIAL: Limpa a variável de estado, "soltando" a carta do mouse.
                carta_sendo_arrastada = None
    # --- 3.1.5: LÓGICA DE ESTADO CONTÍNUO ---
    # Verifica a inatividade do mouse a cada frame.
    if pygame.time.get_ticks() - ultimo_movimento_mouse > 4000:
        pygame.mouse.set_visible(False)
        
    # --- 3.2: DESENHO ---
    # O bloco de desenho agora é o último. Ele apenas lê o estado do jogo e desenha.
    tela.fill(COR_MESA)
    
    # Desenha a mesa.
    pygame.draw.circle(tela, COR_MESA_ESCURA, CENTRO_DA_MESA, RAIO_MAIOR)
    pygame.draw.circle(tela, COR_MESA_CLARA, CENTRO_DA_MESA, RAIO_MENOR)
   

    # --- NOVO: Feedback Visual de Turno ---
    
    # a. Verifique se o turno atual no nosso motor de jogo ('nosso_jogo.turno_atual') 
    #    é o do jogador humano (que é o jogador de índice 0).
    if nosso_jogo.turno_atual == 0:
        # b. Se for, crie um objeto de fonte do Pygame.
        fonte = pygame.font.SysFont('Arial', 30, bold=True)
    
    # c. Renderize o texto "Sua Vez!" em uma nova superfície de texto.
        texto_surface = fonte.render("Sua Vez!", True, (255, 255, 0)) # Cor amarela
    
    # d. Pegue o rect da superfície do texto e posicione-o em um lugar visível na tela.
        texto_rect = texto_surface.get_rect(center=(LARGURA_TELA / 2 - 400, 500))
    
    # e. Desenhe (blit) a superfície do texto na tela.
        tela.blit(texto_surface,texto_rect)
    # Desenha as cartas na vaza.
    for carta_jogada, indice_jogador, angulo in nosso_jogo.vaza_atual:
        nova_largura = int(LARGURA_CARTA * 0.35)
        nova_altura = int((LARGURA_CARTA * 1.4) * 0.35)
        imagem_menor = pygame.transform.scale(carta_jogada.imagem, (nova_largura, nova_altura))
        imagem_rotacionada = pygame.transform.rotate(imagem_menor, angulo)
        rect_rotacionado = imagem_rotacionada.get_rect(center=POSICOES_JOGADA[indice_jogador])
        tela.blit(imagem_rotacionada, rect_rotacionado)

    # Desenha a mão do jogador.
    indice_carta_hover = -1
    for i in range(len(lista_de_rects_da_mao) - 1, -1, -1): 
        if lista_de_rects_da_mao[i].collidepoint(pos_mouse):
            indice_carta_hover = i
            break
            
    # O laço final que desenha a mão do jogador
        for i, carta in enumerate(cartas_da_mao):
        
            # --- ETAPA 1: PULAR A CARTA QUE ESTÁ SENDO ARRASTADA ---
            # Esta verificação continua sendo a primeira e mais importante.
            # Se esta for a carta que estamos segurando, ignore-a e pule para a próxima.
            if carta_sendo_arrastada and carta is carta_sendo_arrastada[0]:
                continue

            # --- ETAPA 2: PREPARAR A IMAGEM (DECIDIR A COR) ---
            # Começamos com uma cópia da imagem original da carta.
            imagem_para_desenhar = carta.imagem.copy()
            
            # Verificamos se ela deve ser pintada de verde.
            if nosso_jogo.fase_do_jogo == "PROMETENDO" and carta in jogador_local.cartas_prometidas:
                # Se sim, criamos um filtro verde e o aplicamos na nossa cópia da imagem.
                filtro_verde = pygame.Surface(imagem_para_desenhar.get_size())
                filtro_verde.set_alpha(120)
                filtro_verde.fill((0, 255, 0))
                imagem_para_desenhar.blit(filtro_verde, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # --- ETAPA 3: PREPARAR A POSIÇÃO (DECIDIR SE LEVITA) ---
            # Pegamos o rect original da lista que já calculamos.
            rect_original = lista_de_rects_da_mao[i]
            
            # Verificamos se a carta deve levitar (seja pelo mouse ou teclado).
            if i == indice_carta_hover or (indice_carta_hover == -1 and i == indice_selecionado_teclado):
                # Se sim, a posição final de desenho será mais alta.
                rect_final_para_desenhar = rect_original.copy()
                rect_final_para_desenhar.y = pos_y_base - 30
            else:
                # Se não, a posição final é a original.
                rect_final_para_desenhar = rect_original

            # --- ETAPA 4: DESENHO FINAL ---
            # Desenhamos a imagem preparada (verde ou não) na posição final (levitada ou não).
            tela.blit(imagem_para_desenhar, rect_final_para_desenhar)
    
    # Desenha a carta sendo arrastada por cima de tudo.
    if carta_sendo_arrastada:
        carta_obj, indice_original, offset, _ = carta_sendo_arrastada
        
        # --- CORREÇÃO AQUI ---
        # 1. Faça uma cópia da imagem original para não alterá-la.
        imagem_arrastada = carta_obj.imagem.copy()
        
        # 2. Verifique se esta carta está na lista de promessas e se estamos na fase certa.
        if nosso_jogo.fase_do_jogo == "PROMETENDO" and carta_obj in jogador_local.cartas_prometidas:
            # 3. Se sim, aplique o mesmo filtro verde que usamos na mão.
            filtro_verde = pygame.Surface(imagem_arrastada.get_size())
            filtro_verde.set_alpha(120)
            filtro_verde.fill((0, 255, 0))
            imagem_arrastada.blit(filtro_verde, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
        # O resto do código continua igual, mas usando a nossa cópia 'imagem_arrastada'.
        nova_pos_x = pos_mouse[0] - offset[0]
        nova_pos_y = pos_mouse[1] - offset[1]
        rect_arrastado = imagem_arrastada.get_rect(topleft=(nova_pos_x, nova_pos_y))
        
        # Desenha a imagem (agora possivelmente verde).
        tela.blit(imagem_arrastada, rect_arrastado)
        
    # --- 3.3: ATUALIZAÇÃO DA TELA ---
    pygame.display.flip()

# --- 4: Finalização ---
pygame.quit()
sys.exit()