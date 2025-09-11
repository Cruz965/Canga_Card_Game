# --- Arquivo: classes.py ---

# Precisamos do pygame aqui também para poder carregar as imagens das cartas.
import pygame
import random
# Aqui definimos a 'planta' de como todo objeto 'Carta' no nosso jogo vai ser.
# Usamos a palavra-chave 'class' seguida do nome da classe, que por convenção começa com letra maiúscula.
class Carta:

    # O 'construtor' da classe. Esta função é chamada automaticamente toda vez que criamos uma nova carta.
    # '__init__' significa 'inicializar'.
    # 'self' é uma referência ao próprio objeto de carta que está sendo criado.
    # Nós passamos o 'valor' (ex: 10) e o 'naipe' (ex: 'ouros') para saber qual carta específica criar.
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
    
        # --- Atributos Básicos ---
        # Guardamos o valor e o naipe que recebemos como atributos do objeto.
        # Usamos 'self.' para dizer "este atributo pertence a este objeto específico".


        # --- Carregamento da Imagem ---
        # Para carregar a imagem correta, precisamos montar o nome do arquivo a partir do valor e do naipe.
        # Ex: valor=1, naipe='espadas' -> 'assets/as_de_espadas.png'
        # Primeiro, um dicionário para nos ajudar a traduzir os números para os nomes dos arquivos.
        valor_para_nome = {1: 'as', 2: 'dois', 3: 'tres', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez'}
        
        # Agora, usamos uma f-string para montar o caminho completo da imagem.
        # Acessamos o dicionário para pegar o nome correspondente ao valor da carta.
        caminho_da_imagem= f"assets/{valor_para_nome[self.valor]}_de_{self.naipe}.png"
        # Com o caminho montado, usamos o pygame.image.load() que já conhecemos.
        # Guardamos a imagem carregada (uma Surface) no atributo 'self.imagem'.
        self.imagem = pygame.image.load(caminho_da_imagem)

        # --- Lógica do Jogo: Poder da Carta ---
        # Agora, a parte mais importante para as regras: definir a força da carta.
        # Vamos criar um atributo 'poder_de_jogo' e calcular seu valor.
        if self.naipe == "paus" and self.valor == 4 :
            self.poder_de_jogo = 14
        elif self.naipe == "copas" and self.valor == 7:
            self.poder_de_jogo = 13
        elif self.naipe == "espadas" and self.valor == 1:
            self.poder_de_jogo = 12
        elif self.naipe == "ouros" and self.valor == 7:
            self.poder_de_jogo = 11
        else: 
            self.poder_de_jogo = self.valor
        # Primeiro, checamos se a carta é uma das 4 manilhas (as cartas mais fortes).
        # Usamos 'if' e 'elif' (else if) para checar as combinações de valor e naipe.
        
        # 1. Zap (Manilha mais forte)
        # Se o valor for 4 E o naipe for 'paus'...

            # ...definimos seu poder como o mais alto. Vamos usar 14.

            
        # 2. Sete de Copas
        # Senão, se o valor for 7 E o naipe for 'copas'...

            # ...definimos seu poder como 13.

            
        # 3. Espadilha (Ás de Espadas)
        # Senão, se o valor for 1 E o naipe for 'espadas'...

            # ...definimos seu poder como 12.

            
        # 4. Sete de Ouros
        # Senão, se o valor for 7 E o naipe for 'ouros'...

            # ...definimos seu poder como 11.

            
        # Se a carta não for nenhuma das manilhas...
        
            # ...seu poder de jogo é simplesmente o seu valor numérico.
    
    def __repr__(self):
        # Vamos criar um dicionário de tradução aqui também, para ficar mais bonito.
        # Note que usei os nomes com letra maiúscula para uma melhor leitura.
        valor_para_nome = {
            1: 'Ás', 2: 'Dois', 3: 'Três', 4: 'Quatro', 5: 'Cinco', 
            6: 'Seis', 7: 'Sete', 8: 'Oito', 9: 'Nove', 10: 'Dez'
        }
        
        # Agora, retornamos uma f-string bem formatada.
        # O método .capitalize() deixa a primeira letra do naipe maiúscula.
        return f"{valor_para_nome[self.valor]} de {self.naipe.capitalize()}"         # Um 10 é mais forte que um 9, um 6 mais forte que um 5.

class Baralho:
    
    # O construtor do Baralho. Não precisa de nenhum parâmetro além de 'self'.
    # Sua única missão é criar todas as 40 cartas e guardá-las.
    def __init__(self):
        
        # Começamos com um atributo que será uma lista vazia para guardar nossos objetos Carta.
        self.cartas = []
        
        # Para criar todas as combinações, vamos definir as listas de todos os naipes e valores possíveis.
        naipes = ['paus', 'copas', 'espadas', 'ouros']
        valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Agora, o truque: usamos dois laços 'for', um dentro do outro (nested loops).
        # Para cada NAIpe na lista de naipes...
        for naipe in naipes:
            # ...nós passamos por cada VALOR na lista de valores.
            for valor in valores:
                # Para cada combinação de valor e naipe, nós criamos um novo objeto da nossa classe Carta.
                nova_carta = Carta(valor, naipe)
                # E finalmente, adicionamos a carta recém-criada à nossa lista 'self.cartas'.
                self.cartas.append(nova_carta)
                # O método para adicionar um item a uma lista é o .append().
                
    
    # Este método 'mágico' ajuda na hora de debugar. Se dermos print() em um objeto Baralho...
    def __repr__(self):
        # ...ele vai retornar uma string dizendo quantas cartas estão no baralho.
        # A função len() nos dá o tamanho de uma lista.
        return f"Baralho com {len(self.cartas)} cartas"

    # Este método vai misturar as cartas na nossa lista self.cartas.
    def embaralhar(self):
        # A função random.shuffle() embaralha uma lista "no lugar", ou seja, ela modifica a lista original.
        random.shuffle(self.cartas)
    # DENTRO da class Baralho:

    # ... (os métodos __init__, __repr__ e embaralhar continuam aqui) ...

    # --- Novo Método ---
    
    # Método para distribuir um certo número de cartas para um jogador.
    def distribuir(self, jogador, quantidade):
        
        # Usamos um laço 'for' que vai repetir 'quantidade' de vezes.
        # A variável _ (underscore) é uma convenção em Python para dizer "não me importo com o número da iteração".
        for _ in range(quantidade):
            
            # Primeiro, verificamos se o baralho não está vazio para evitar erros.
            if self.cartas:
                
                # O método .pop(0) REMOVE o primeiro item (índice 0) de uma lista e o retorna.
                # É como pegar a carta do topo do baralho.
                carta = self.cartas.pop(0)
                
                # Agora, adicionamos essa carta que pegamos à mão do jogador.
                jogador.mao.append(carta)
        

# --- Bloco de Teste ---
# Este bloco especial só será executado quando rodarmos ESTE arquivo (classes.py) diretamente.
# Ele não será executado quando o main.py importar as classes. É perfeito para testes!

    
class Jogador:
    
    # O construtor do Jogador. Por enquanto, ele só precisa de um nome.
    # Podemos adicionar um parâmetro para dizer se ele é o jogador humano ou uma IA.
    def __init__(self, nome, eh_humano=False):
        
        # Guardamos o nome do jogador.
        self.nome = nome
        
        # Guardamos se este jogador é controlado por uma pessoa.
        self.eh_humano = eh_humano
        
        # Todo jogador começa com uma 'mao' de cartas, que é uma lista vazia.
        self.mao = []
        
        # Todo jogador começa com 5 vidas (vamos adicionar isso agora para já deixar pronto).
        self.vidas = 5
        
    # Um método __repr__ para facilitar a visualização e o debug.
    def __repr__(self):
        # A f-string vai nos dizer o nome do jogador e quantas cartas ele tem na mão.
        return f"Jogador {self.nome} com {len(self.mao)} cartas"
    
if __name__ == '__main__':
    
    # 1. Cria e embaralha o baralho.
    baralho_teste = Baralho()
    baralho_teste.embaralhar()
    print(baralho_teste) # Mostra quantas cartas tem no início (40).
    print("-" * 20) # Uma linha para separar
    
    # 2. Cria dois jogadores.
    jogador1 = Jogador("Humano", eh_humano=True)
    jogador2 = Jogador("IA_1")
    print(jogador1)
    print(jogador2)
    print("-" * 20)
    
    # 3. Distribui as cartas.
    # Vamos simular uma rodada de 5 cartas para cada um.
    print("Distribuindo 5 cartas para cada jogador...")
    baralho_teste.distribuir(jogador1, 5)
    baralho_teste.distribuir(jogador2, 5)
    
    # 4. Verifica o resultado.
    print("-" * 20)
    print("--- Depois da Distribuição ---")
    print(baralho_teste) # Deve ter 30 cartas agora.
    print(jogador1) # Deve ter 5 cartas.
    print("Mão do Jogador 1:", jogador1.mao) # Vamos ver as cartas dele!
    print(jogador2) # Deve ter 5 cartas.
    print("Mão do Jogador 2:", jogador2.mao)