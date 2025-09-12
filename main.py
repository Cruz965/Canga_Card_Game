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
while(rodando is True):

    # --- Bloco 3.1: Tratamento de Eventos ---
    # Dentro do loop, a primeira coisa a fazer é verificar se algum evento aconteceu.
    # Eventos são ações do usuário: mover o mouse, pressionar tecla, fechar a janela.
    # Usamos um laço 'for' para percorrer a lista de eventos que o pygame capturou.
    for event in pygame.event.get():
    
        # O evento mais importante por agora é o de fechar a janela.
        # Verificamos se o 'tipo' do evento é igual a pygame.QUIT.
        if event.type == pygame.QUIT:
        # pygame.QUIT é uma constante que representa o clique no botão 'X' da janela.

            # Se o usuário clicou para fechar, mudamos nossa variável de controle do loop
            rodando = False
            # para False, o que fará com que o 'while' termine na próxima verificação.
        if event.type == pygame.MOUSEMOTION:
            # ...atualizamos nossa variável com o tempo atual.
            ultimo_movimento_mouse = pygame.time.get_ticks()
            # E garantimos que o mouse esteja visível.
            pygame.mouse.set_visible(True) 
        if event.type == pygame.KEYDOWN:
            # --- Movendo para a Direita ---
            # Checamos as duas teclas corretamente agora.
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                # Usamos o atalho '+= 1' que é mais comum em Python.
                indice_selecionado_teclado += 1

            # --- Movendo para a Esquerda ---
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                # Usamos o atalho '-= 1'.
                indice_selecionado_teclado -= 1

            # --- CONTROLE DE LIMITES (DEPOIS de mover) ---
            # Garante que o índice não passe do número de cartas.
            # Se o jogador tiver 5 cartas (índices 0 a 4), len(jogador1.mao)-1 será 4.
            # A função min() pega o menor valor entre os dois.
            if indice_selecionado_teclado > len(jogador1.mao) - 1:
                indice_selecionado_teclado = len(jogador1.mao) - 1
            
            # Garante que o índice não seja menor que 0.
            # A função max() pega o maior valor entre os dois.
            if indice_selecionado_teclado < 0:
                indice_selecionado_teclado = 0
            
        
    if pygame.time.get_ticks() - ultimo_movimento_mouse > 4000:
        # Se for, mandamos o Pygame esconder o cursor.
            pygame.mouse.set_visible(False)
    # --- Bloco 3.2: Lógica de Desenho e Interação (VERSÃO CORRIGIDA) ---
    tela.fill(COR_MESA)
    
    # a. Pegamos a posição do mouse.
    pos_mouse = pygame.mouse.get_pos()
    
    # b. INICIALIZAMOS a variável de hover com um valor padrão.
    indice_carta_hover = -1
    
    # c. Pegamos a mão do jogador.
    cartas_jogador_1 = jogador1.mao
    
    if cartas_jogador_1:
        # Cálculos de layout (seu código aqui estava perfeito).
        largura_mao_jogador_1 = ((len(cartas_jogador_1)-1)*ESPACAMENTO_ENTRE_CARTAS+(LARGURA_CARTA))
        posicao_X_mao_incial = (LARGURA_TELA/2 - largura_mao_jogador_1/2)

        # d. Criamos uma lista para guardar os rects calculados.
        lista_de_rects_da_mao = []
        for i, carta in enumerate(jogador1.mao):
            posicao_x_carta = posicao_X_mao_incial + i * ESPACAMENTO_ENTRE_CARTAS
            rect_da_carta = carta.imagem.get_rect()
            rect_da_carta.topleft = (posicao_x_carta, POSICAO_Y_MAO)
            lista_de_rects_da_mao.append(rect_da_carta)
            
        # e. Descobrimos qual carta está sob o mouse (de trás para frente).
        for i in range(len(lista_de_rects_da_mao) - 1, -1, -1): 
            rect_atual = lista_de_rects_da_mao[i]
            # Verificamos se o 'pos_mouse' colide com este rect.
            if rect_atual.collidepoint(pos_mouse):
                # Se colidir, guardamos o índice e paramos de procurar.
                indice_carta_hover = i
                break
        
        # f. Finalmente, o laço de DESENHO.
        for i, carta in enumerate(jogador1.mao):
            # Pegamos o rect correspondente da lista.
            rect_original = lista_de_rects_da_mao[i]
            rect_para_desenhar = rect_original.copy()
            # Verificamos se esta é a carta que deve levitar.
            if i == indice_carta_hover:
                # Se for, criamos uma CÓPIA do rect e a movemos para cima.
                
                rect_para_desenhar.y = POSICAO_Y_MAO - 30
            elif indice_carta_hover == -1 and i == indice_selecionado_teclado:
                rect_para_desenhar.y = POSICAO_Y_MAO - 30 # Move para cima
                # ...então a seleção do teclado assume, e esta é a carta que levita.
                # Mude a coordenada Y do rect_para_desenhar para a mesma altura de levitação.
                
            # Se nenhuma das condições acima for verdadeira, o rect_para_desenhar
            # continuará na sua posição original, e a carta não levitará.
            
            # Finalmente, desenhe a imagem da carta na tela, usando o rect_para_desenhar.
            # A posição dele estará normal ou levitada, dependendo das condições acima.
           
            
            # Desenhamos a imagem da carta usando o rect final.
            tela.blit(carta.imagem, rect_para_desenhar)

    # --- Bloco 3.3: Atualização da Tela ---
    # O flip() deve estar fora do 'if', para a tela sempre atualizar.
    pygame.display.flip()
# --- Bloco 4: Finalização ---

# O loop 'while' terminou, o que significa que o jogo acabou.
# Agora, podemos fechar o pygame de forma segura.
# Esta é a função que desinicializa a biblioteca.
pygame.quit()
sys.exit()