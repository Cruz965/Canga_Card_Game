# --- Bloco 1: Importação e Inicialização ---

# Primeiro, precisamos importar a biblioteca pygame para podermos usá-la.
import pygame
import sys
from classes import Baralho, Carta
# Agora, inicializamos todos os módulos do pygame. Este é um passo obrigatório.
pygame.init()

# --- Bloco 2: Constantes e Configurações da Tela ---

# É uma boa prática definir valores que não mudam (constantes) no início do código.
# Vamos definir a largura e a altura da nossa janela. Use os valores que discutimos.
LARGURA_TELA = 1280
ALTURA_TELA = 720

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

# --- Bloco 2.5: Criando o Baralho do Jogo ---

# Primeiro, criamos uma instância do nosso Baralho. 
# Ao fazer isso, o __init__ dele vai criar as 40 cartas automaticamente.
# Guarde o objeto em uma variável como 'baralho_do_jogo'.
baralho_do_jogo = Baralho()

# Em seguida, chamamos o método que criamos para embaralhar as cartas.
baralho_do_jogo.embaralhar()

# Para nosso teste, vamos pegar a primeira carta do topo do baralho já embaralhado.

# Lembre-se que as cartas estão na lista 'cartas' dentro do objeto baralho.
# O índice [0] pega o primeiro item da lista. Guarde em 'carta_para_exibir'.
carta_para_exibir = baralho_do_jogo.cartas[0]

# Agora, a mesma lógica de antes: precisamos do rect desta carta para posicioná-la.
# Pegamos o rect a partir do atributo '.imagem' da nossa carta_para_exibir.
# Guarde em 'carta_rect'.
carta_rect = carta_para_exibir.imagem.get_rect()

# E, por fim, centralizamos esse rect na tela. Exatamente como fizemos antes.
carta_rect.center = tela.get_rect().center


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


    # --- Bloco 3.2: Desenho na Tela ---
    # Após tratar os eventos, limpamos a tela e a preparamos para o novo frame.
    
    # Preenchemos o fundo da 'tela' com a COR_MESA que definimos.
    tela.fill(COR_MESA)
    tela.blit(carta_para_exibir.imagem,carta_rect)
    # --- Bloco 3.3: Atualização da Tela ---
    # Depois de desenhar tudo (por enquanto, só o fundo), precisamos dizer ao pygame
    # para mostrar o que foi desenhado. Isso "vira a página" e exibe o novo frame.
    # A função para isso também está em 'pygame.display'.
    pygame.display.flip()

# --- Bloco 4: Finalização ---

# O loop 'while' terminou, o que significa que o jogo acabou.
# Agora, podemos fechar o pygame de forma segura.
# Esta é a função que desinicializa a biblioteca.
pygame.quit()