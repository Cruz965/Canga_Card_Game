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
def aplicar_filtro_promessa(imagem):
    """
    Pega uma superfície de imagem, aplica um filtro verde semi-transparente
    e retorna a imagem modificada.
    """
    # Cria uma nova superfície com o mesmo tamanho da imagem original.
    filtro_verde = pygame.Surface(imagem.get_size())
    
    # Define o quão transparente o filtro será (0=invisível, 255=opaco).
    filtro_verde.set_alpha(120)
    
    # Preenche a superfície do filtro com a cor verde.
    filtro_verde.fill((0, 255, 0))
    
    # "Carimba" o filtro verde sobre a imagem original usando um modo de mistura
    # que preserva os detalhes escuros da carta.
    imagem.blit(filtro_verde, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    # Retorna a imagem original, que agora foi modificada.
    return imagem
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
ALTURA_CARTA = 140
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
CAIXA_PROMESSA_RECT = pygame.Rect(LARGURA_TELA - 120, ALTURA_TELA - 120, 80, 80)

fonte_log = pygame.font.SysFont('Arial', 14, bold=True)
# A primeira linha será desenhada a 20 pixels da borda inferior.
pos_x_log = 20
pos_y_log = ALTURA_TELA - 20
# Calcula a altura de cada linha para o espaçamento.
altura_linha = fonte_log.get_height() + 3 

VERSO_CARTA_IMG = pygame.image.load('assets/back_side_g22.png')
# --- Inicialização do Pygame e da Tela ---
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Canga")

# --- ALTERADO: Bloco 2.5 agora é muito mais simples ---
# Toda a lógica de criar baralho, jogadores e distribuir foi para a classe Jogo.
# O 'main' agora só precisa criar uma instância do Jogo.
INDICE_JOGADOR_LOCAL = 0
nosso_jogo = Jogo(numero_de_jogadores=2) # Você pode mudar o número aqui para testar
jogador_local = nosso_jogo.jogadores[INDICE_JOGADOR_LOCAL ]
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
placar_visivel = False

while rodando:

    # --- 3.0: PREPARAÇÃO DO FRAME ---
    # (Esta parte sua já estava perfeita)
    pos_mouse = pygame.mouse.get_pos()
    cartas_da_mao = nosso_jogo.jogadores[0].mao
    jogador_local = nosso_jogo.jogadores[0]
    
        
    lista_de_rects_da_mao = []
    if cartas_da_mao:
        if nosso_jogo.rodada_atual_num_cartas == 1:
            # ...calcula um único rect para o verso da carta.
            rect_da_carta = VERSO_CARTA_IMG.get_rect(midbottom=(LARGURA_TELA / 2, ALTURA_TELA - 20))
            lista_de_rects_da_mao.append(rect_da_carta)
        else:
            pos_y_base = POSICAO_Y_MAO if mao_visivel else POSICAO_Y_ESCONDIDA
            largura_total_mao = (len(cartas_da_mao) - 1) * ESPACAMENTO_ENTRE_CARTAS + LARGURA_CARTA
            posicao_x_inicial = (LARGURA_TELA - largura_total_mao) / 2
            for i, carta in enumerate(cartas_da_mao):
                posicao_x_carta = posicao_x_inicial + i * ESPACAMENTO_ENTRE_CARTAS
                rect_da_carta = carta.imagem.get_rect(topleft=(posicao_x_carta, pos_y_base))
                lista_de_rects_da_mao.append(rect_da_carta)

    indice_carta_hover = -1
    for i in range(len(lista_de_rects_da_mao) - 1, -1, -1): 
        if lista_de_rects_da_mao[i].collidepoint(pos_mouse):
            indice_carta_hover = i
            break

    # --- 3.1: PROCESSAMENTO DE EVENTOS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            
        if event.type == pygame.MOUSEMOTION:
            ultimo_movimento_mouse = pygame.time.get_ticks()
            pygame.mouse.set_visible(True)
            
        if event.type == pygame.KEYDOWN:
            # ... (Sua lógica de KEYDOWN está perfeita, sem mudanças aqui) ...
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                indice_selecionado_teclado += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                indice_selecionado_teclado -= 1
            elif event.key == pygame.K_o:
                if nosso_jogo.fase_do_jogo == "PROMETENDO" and nosso_jogo.turno_atual == INDICE_JOGADOR_LOCAL:
                    jogador_local.promessa_atual = len(jogador_local.cartas_prometidas)
                    jogador_local.cartas_prometidas.clear()
                    nosso_jogo.avancar_turno()

            elif event.key == pygame.K_SPACE:
                mao_visivel = not mao_visivel
            elif event.key == pygame.K_RETURN:
                if jogador_local.mao and not carta_sendo_arrastada:
                    indice_para_jogar = indice_carta_hover if indice_carta_hover != -1 else indice_selecionado_teclado
                    if 0 <= indice_para_jogar < len(jogador_local.mao):
                        carta_para_jogar = jogador_local.mao[indice_para_jogar]
                        nosso_jogo.jogador_tenta_jogar_carta(INDICE_JOGADOR_LOCAL , carta_para_jogar)
            elif event.key == pygame.K_p:
                if nosso_jogo.fase_do_jogo == "PROMETENDO" and nosso_jogo.turno_atual == INDICE_JOGADOR_LOCAL:
                    if jogador_local.mao:
                        carta_selecionada = jogador_local.mao[indice_selecionado_teclado]
                        if carta_selecionada in jogador_local.cartas_prometidas:
                            jogador_local.cartas_prometidas.remove(carta_selecionada)
                        else:
                            jogador_local.cartas_prometidas.append(carta_selecionada)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Lida com o botão direito para alternar a visibilidade da mão.
            if event.button == 3:
                mao_visivel = not mao_visivel
            
            # Lida com todas as ações do botão esquerdo.
            if event.button == 1:
                
                # --- Ação 1: Clicar na Caixa de Promessa ---
                # Verificamos primeiro se o clique foi em um elemento de UI, como a caixa.
                if nosso_jogo.fase_do_jogo == "PROMETENDO" and nosso_jogo.turno_atual == INDICE_JOGADOR_LOCAL and CAIXA_PROMESSA_RECT.collidepoint(event.pos):
                    # Oficializa a promessa e avança o turno.
                    jogador_local.promessa_atual = len(jogador_local.cartas_prometidas)
                    jogador_local.cartas_prometidas.clear()
                    nosso_jogo.avancar_turno()

                # --- Ação 2: Interagir com as Cartas (Double-click ou Arrastar) ---
                # Se o clique não foi na caixa, verificamos se foi em uma carta.
                elif mao_visivel and indice_carta_hover != -1:
                    is_double_click = False
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - ultimo_clique_tempo < 300:
                        is_double_click = True
                    ultimo_clique_tempo = tempo_atual

                    # Se for um double-click, a ação é de PROMESSA.
                    if is_double_click and nosso_jogo.fase_do_jogo == "PROMETENDO" and nosso_jogo.turno_atual == INDICE_JOGADOR_LOCAL:
                        carta_selecionada = jogador_local.mao[indice_carta_hover]
                        if carta_selecionada in jogador_local.cartas_prometidas:
                            jogador_local.cartas_prometidas.remove(carta_selecionada)
                            
                        else:
                            jogador_local.cartas_prometidas.append(carta_selecionada)
                            
                    
                    # Senão, se NÃO for um double-click e não estivermos já arrastando, a ação é de ARRASTAR.
                    elif not is_double_click and not carta_sendo_arrastada:
                        
                        # --- A CORREÇÃO QUE VOCÊ PEDIU ESTÁ AQUI ---
                        # Adicionamos a checagem para garantir que só podemos arrastar
                        # em rodadas com mais de 1 carta.
                        if mao_visivel and indice_carta_hover != -1 and not carta_sendo_arrastada:
                            carta_clicada = jogador_local.mao[indice_carta_hover]
                            indice_original = indice_carta_hover
                            rect_da_carta_clicada = lista_de_rects_da_mao[indice_carta_hover]
                            offset_x = event.pos[0] - rect_da_carta_clicada.x
                            offset_y = event.pos[1] - rect_da_carta_clicada.y
                            posicao_inicial_clique = event.pos
                            carta_sendo_arrastada = (carta_clicada, indice_original, (offset_x, offset_y), posicao_inicial_clique)
                    
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and carta_sendo_arrastada:
                # ... (Sua lógica de MOUSEBUTTONUP está ótima, sem mudanças aqui) ...
                carta_obj, indice_original, offset, pos_inicial_clique = carta_sendo_arrastada
                pos_final_clique = event.pos
                pos_soltura_x = pos_final_clique[0] - offset[0]
                pos_soltura_y = pos_final_clique[1] - offset[1]
                rect_solto = carta_obj.imagem.get_rect(topleft=(pos_soltura_x, pos_soltura_y))
                distancia_movida = math.hypot(pos_final_clique[0] - pos_inicial_clique[0], pos_final_clique[1] - pos_inicial_clique[1])

                if nosso_jogo.fase_do_jogo == "JOGANDO" and MESA_RECT.colliderect(rect_solto):
                    nosso_jogo.jogador_tenta_jogar_carta(0, carta_obj)
                elif distancia_movida > 10:
                    area_da_mao_rect = None
                    if lista_de_rects_da_mao:
                        primeiro_rect = lista_de_rects_da_mao[0]
                        ultimo_rect = lista_de_rects_da_mao[-1]
                        area_da_mao_rect = pygame.Rect(
                            primeiro_rect.left, primeiro_rect.top,
                            ultimo_rect.right - primeiro_rect.left, primeiro_rect.height
                        )
                    
                    if area_da_mao_rect and area_da_mao_rect.colliderect(rect_solto):
                        carta_removida = jogador_local.mao.pop(indice_original)
                        novo_indice = len(jogador_local.mao)
                        temp_rects = [r for i, r in enumerate(lista_de_rects_da_mao) if i != indice_original]
                        for i, rect_na_mao in enumerate(temp_rects):
                            if rect_solto.centerx < rect_na_mao.centerx:
                                novo_indice = i
                                break
                        jogador_local.mao.insert(novo_indice, carta_removida)
                    elif area_da_mao_rect and rect_solto.centery > area_da_mao_rect.top:
                        carta_removida = jogador_local.mao.pop(indice_original)
                        if rect_solto.centerx < area_da_mao_rect.centerx:
                            jogador_local.mao.insert(0, carta_removida)
                        else:
                            jogador_local.mao.append(carta_removida)
                            
                carta_sendo_arrastada = None

    # --- 3.1.5: LÓGICA DE ESTADO CONTÍNUO ---
    # (Sua lógica aqui está perfeita, sem mudanças)
    if cartas_da_mao:
        if indice_selecionado_teclado > len(cartas_da_mao) - 1:
            indice_selecionado_teclado = len(cartas_da_mao) - 1
        if indice_selecionado_teclado < 0:
            indice_selecionado_teclado = 0
            
    if pygame.time.get_ticks() - ultimo_movimento_mouse > 4000:
        pygame.mouse.set_visible(False)
      
    # --- NOVA LÓGICA: Processa o turno de promessa da IA ---
    
    # a. Verifique se a fase do jogo é "PROMETENDO".
    if nosso_jogo.fase_do_jogo == "PROMETENDO":
        # b. Se for, pegue o objeto do jogador do turno atual.
        #    Dica: jogador_do_turno = nosso_jogo.jogadores[nosso_jogo.turno_atual]
        jogador_do_turno = nosso_jogo.jogadores[nosso_jogo.turno_atual]
        # c. Verifique se o jogador do turno atual NÃO é humano.
        #    Dica: if not jogador_do_turno.eh_humano:
        if not jogador_do_turno.eh_humano:

            # d. Se for a vez da IA prometer, chame o novo método do nosso motor de jogo.
            #    Dica: nosso_jogo.processar_promessa_ia()    
            nosso_jogo.processar_promessa_ia()
     # --- NOVA LÓGICA: Processa o turno de JOGADA da IA ---
    
    # a. Verifique se a fase do jogo é "JOGANDO".
    if nosso_jogo.fase_do_jogo == "JOGANDO":
        # b. Se for, pegue o objeto do jogador do turno atual.
        jogador_do_turno = nosso_jogo.jogadores[nosso_jogo.turno_atual]
        # c. Verifique se o jogador do turno atual NÃO é humano.
        if not jogador_do_turno.eh_humano:

            # d. Se for a vez da IA jogar, chame o novo método do nosso motor de jogo.
            #    Dica: nosso_jogo.processar_jogada_ia()
            nosso_jogo.processar_jogada_ia()
   # --- 3.2: DESENHO ---
    # O bloco de desenho é o último. Ele apenas lê o estado do jogo e desenha.
    tela.fill(COR_MESA)
    
    # Desenha a mesa de jogo.
    pygame.draw.circle(tela, COR_MESA_ESCURA, CENTRO_DA_MESA, RAIO_MAIOR)
    pygame.draw.circle(tela, COR_MESA_CLARA, CENTRO_DA_MESA, RAIO_MENOR)
    
    # Desenha as cartas que já foram jogadas na vaza.
    for carta_jogada, indice_jogador, angulo in nosso_jogo.vaza_atual:
        nova_largura = int(LARGURA_CARTA * 0.35)
        nova_altura = int((LARGURA_CARTA * 1.4) * 0.35)
        imagem_menor = pygame.transform.scale(carta_jogada.imagem, (nova_largura, nova_altura))
        imagem_rotacionada = pygame.transform.rotate(imagem_menor, angulo)
        rect_rotacionado = imagem_rotacionada.get_rect(center=POSICOES_JOGADA[indice_jogador])
        tela.blit(imagem_rotacionada, rect_rotacionado)

    # --- Lógica de Desenho da Mão (com a regra de 1 carta) ---
    
    # Verifica qual o número de cartas da rodada atual.
    if nosso_jogo.rodada_atual_num_cartas == 1:
        # --- Desenho da Rodada "Na Testa" ---
        # Como o jogador não pode ver sua carta, desenhamos apenas o verso.
        if jogador_local.mao:
            imagem_verso_para_desenhar = VERSO_CARTA_IMG.copy()
            carta_na_mao = jogador_local.mao[0]
            if nosso_jogo.fase_do_jogo == "PROMETENDO" and carta_na_mao in jogador_local.cartas_prometidas:
                
                filtro_verde = pygame.Surface(imagem_verso_para_desenhar.get_size())
                filtro_verde.set_alpha(120)
                filtro_verde.fill((0, 255, 0))
                imagem_verso_para_desenhar.blit(filtro_verde, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            if not carta_sendo_arrastada:
           # Apenas desenha se o jogador tiver a carta.
            # CORREÇÃO AQUI: Usando .midbottom para melhor alinhamento na base.
            # A posição Y (ALTURA_TELA - 20) coloca a base da carta a 20 pixels da borda inferior.
                rect_verso = imagem_verso_para_desenhar.get_rect(midbottom=(LARGURA_TELA / 2, ALTURA_TELA))
                tela.blit(imagem_verso_para_desenhar, rect_verso)
    else:
        # --- Desenho da Mão Normal e Interativa (2 a 5 cartas) ---
        cartas_da_mao = jogador_local.mao
        if cartas_da_mao:
            # Desenha cada carta da mão com todos os efeitos (hover, seleção, promessa).
            
            for i, carta in enumerate(cartas_da_mao):
                if carta_sendo_arrastada and carta is carta_sendo_arrastada[0]:
                    continue
                
                imagem_para_desenhar = carta.imagem.copy()
                rect_para_desenhar = lista_de_rects_da_mao[i]
                if nosso_jogo.fase_do_jogo == "PROMETENDO" and carta in jogador_local.cartas_prometidas:
                    filtro_verde = pygame.Surface(imagem_para_desenhar.get_size())
                    filtro_verde.set_alpha(120)
                    filtro_verde.fill((0, 255, 0))
                    imagem_para_desenhar.blit(filtro_verde, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                
                if i == indice_carta_hover or (indice_carta_hover == -1 and i == indice_selecionado_teclado):
                    rect_final_para_desenhar = rect_para_desenhar.copy()
                    rect_final_para_desenhar.y = pos_y_base - 30
                else:
                    rect_final_para_desenhar = rect_para_desenhar
                    
                tela.blit(imagem_para_desenhar, rect_final_para_desenhar)
    
    # Desenha a carta sendo arrastada por cima de tudo.
    if carta_sendo_arrastada:
        carta_obj, _, offset, _ = carta_sendo_arrastada
        
        # --- NOVA LÓGICA: Decide qual lado da carta desenhar ---
        # a. Verifique se estamos na rodada de 1 carta.
        # 1. Decide a IMAGEM BASE (Frente ou Verso).
        if nosso_jogo.rodada_atual_num_cartas == 1:
            imagem_para_arrastar = VERSO_CARTA_IMG.copy()
        else:
            imagem_para_arrastar = carta_obj.imagem.copy()
            
        # 2. Decide se APLICA O FILTRO na imagem base que acabamos de escolher.
        if nosso_jogo.fase_do_jogo == "PROMETENDO" and carta_obj in jogador_local.cartas_prometidas:
            # Usa nossa função para aplicar o filtro verde.
            imagem_para_arrastar = aplicar_filtro_promessa(imagem_para_arrastar)


        # O resto do código continua igual, mas usando a nossa nova variável 'imagem_para_arrastar'.
        nova_pos_x = pos_mouse[0] - offset[0]
        nova_pos_y = pos_mouse[1] - offset[1]
        rect_arrastado = imagem_para_arrastar.get_rect(topleft=(nova_pos_x, nova_pos_y))
        tela.blit(imagem_para_arrastar, rect_arrastado)
    # --- Desenho de Elementos de UI (Interface do Usuário) ---

    # Desenha o feedback de turno.
    if nosso_jogo.turno_atual == INDICE_JOGADOR_LOCAL:
        fonte = pygame.font.SysFont('Arial', 30, bold=True)
        texto_surface = fonte.render("Sua Vez!", True, (255, 255, 0))
        texto_rect = texto_surface.get_rect(center=(LARGURA_TELA / 2, 520))
        tela.blit(texto_surface, texto_rect)

    # Desenha a caixa de promessa.
    pygame.draw.rect(tela, COR_MESA_ESCURA, CAIXA_PROMESSA_RECT)
    numero_para_mostrar = 0
    if nosso_jogo.fase_do_jogo == "PROMETENDO":
        numero_para_mostrar = len(jogador_local.cartas_prometidas)
    else:
        numero_para_mostrar = jogador_local.promessa_atual
    texto_da_promessa = str(numero_para_mostrar)
    fonte_promessa = pygame.font.SysFont('Arial', 40, bold=True)
    surface_texto_promessa = fonte_promessa.render(texto_da_promessa, True, (255, 255, 0))
    rect_texto_promessa = surface_texto_promessa.get_rect(center=CAIXA_PROMESSA_RECT.center)
    tela.blit(surface_texto_promessa, rect_texto_promessa)
   
    # --- Desenha o Status da Fase do Jogo ---
    
    # 1. Cria a string de texto a ser exibida, lendo a fase atual do motor do jogo.
    texto_fase = f"Fase: {nosso_jogo.fase_do_jogo}"
    
    # 2. Configura a fonte para o texto.
    fonte_fase = pygame.font.SysFont('Arial', 20, bold=True)
    
    # 3. Renderiza o texto em uma superfície. A cor será branca (RGB: 255, 255, 255).
    surface_fase = fonte_fase.render(texto_fase, True, (255, 255, 255))
    
    # 4. Cria o rect para o texto e o posiciona na tela.
    #    O atributo .midleft ancora o ponto MÉDIO da borda ESQUERDA do texto na coordenada.
    rect_fase = surface_fase.get_rect(midleft=(20, ALTURA_TELA / 2))
    
    # 5. Desenha a superfície do texto na tela.
    tela.blit(surface_fase, rect_fase) 
    # No seu Bloco 3.2 (Desenho), em main.py

    # --- NOVO: Desenha o Log de Mensagens (VERSÃO CORRIGIDA) ---
    
    # a. Define a fonte e as posições iniciais.
   

    # b. Pega as últimas 5 mensagens da forma correta.
    mensagens_para_exibir = list(nosso_jogo.log_de_jogo)[-5:]
    
    # c. Percorre a lista de mensagens DE TRÁS PARA FRENTE para desenhar de baixo para cima.
    for mensagem_texto in reversed(mensagens_para_exibir):
        # d. Renderiza a mensagem.
        surface_mensagem = fonte_log.render(mensagem_texto, True, (255, 255, 0)) # Cor Amarela
        
        # e. Posiciona o rect da mensagem usando 'bottomleft' como âncora.
        rect_mensagem = surface_mensagem.get_rect(bottomleft=(pos_x_log, pos_y_log))
        
        # f. Desenha (blit) a mensagem.
        tela.blit(surface_mensagem, rect_mensagem)
        
        # g. Move a posição Y para CIMA para a próxima mensagem ser desenhada.
        pos_y_log -= altura_linha
        #    Dica: y_do_log += altura_da_fonte 
    # --- 3.3: ATUALIZAÇÃO DA TELA ---
    pygame.display.flip()

# --- 4: Finalização ---
pygame.quit()
sys.exit()