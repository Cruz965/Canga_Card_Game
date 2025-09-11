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


    # --- Bloco 3.2: Lógica de Desenho ---
    # 1. Limpe a tela com a cor de fundo (você já tem essa linha).


    # --- Lógica para Desenhar a Mão do jogador1 ---
    tela.fill(COR_MESA)
    


    # b. Para facilitar, pegue a lista de cartas da mão do jogador1 e guarde em uma variável local.
    cartas_jogador_1 = jogador1.mao

    # c. Calcule a largura total que a mão vai ocupar na tela.
    #    Primeiro, verifique se a lista da mão não está vazia.
    if cartas_jogador_1:

        # A lógica é: (número de espaços entre as cartas) * (tamanho do espaço) + (largura da última carta).
        largura_mao_jogador_1 = ((len(cartas_jogador_1)-1)*ESPACAMENTO_ENTRE_CARTAS+(LARGURA_CARTA))
        # O número de espaços é sempre o número de cartas menos 1.
        # Calcule isso e guarde em uma variável 'largura_total_mao'.


        # d. Calcule a posição X da primeira carta para que a mão inteira fique centralizada.
        #    O raciocínio é: o centro da tela (LARGURA_TELA / 2) menos a metade da largura da mão.
        #    Isso nos dá o ponto exato onde a primeira carta deve começar. Guarde em 'posicao_x_inicial'.
        posicao_X_mao_incial = (LARGURA_TELA/2 - largura_mao_jogador_1/2)

        # e. Agora, o laço para desenhar cada carta.
        #    Use 'for i, carta in enumerate(sua_variavel_da_mao):' para ter acesso
        #    ao índice 'i' e ao objeto 'carta' em cada volta.
        # e. O laço para desenhar cada carta.
        for i, carta in enumerate(jogador1.mao):
            
            # f. Calcula a posição X específica para ESTA carta. (Sua linha estava perfeita)
            posicao_x_carta = posicao_X_mao_incial + i * ESPACAMENTO_ENTRE_CARTAS
            
            # g. Pega a imagem e o rect da carta ATUAL do loop
            imagem_da_carta = carta.imagem
            rect_da_carta = imagem_da_carta.get_rect()
            
            # h. Posiciona o rect nas coordenadas corretas
            rect_da_carta.topleft = (posicao_x_carta, POSICAO_Y_MAO)
            
            # i. Finalmente, desenha a imagem da carta na posição do rect
            tela.blit(imagem_da_carta, rect_da_carta)
    pygame.display.flip()        
# --- Bloco 4: Finalização ---

# O loop 'while' terminou, o que significa que o jogo acabou.
# Agora, podemos fechar o pygame de forma segura.
# Esta é a função que desinicializa a biblioteca.
pygame.quit()
sys.exit()