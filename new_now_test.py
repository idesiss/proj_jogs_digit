import pygame
from pygame.locals import *
import time
import random
import sys

pygame.init()

screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
background_color = (0, 0, 0)  # Cor de fundo da tela
pygame.display.set_caption("Bob e o seu encontro")

branco = (255, 255, 255)

# Matriz
# LINHAS -> Fácil - 3 Médio 5 Difícil 7
# COLUNAS -> F - 3 # M - 5 # D - 7
largura = 75
altura = 75
margem = 1

# Definir as direções
seta_cima = [1]       
seta_baixo = [7]    
seta_esquerda = [4, 6, 9, 3, 10,8]   
seta_direita = [2, 5, 11]

# Lista para armazenar a sequência de direções
sequencia_direcoes = []

# Carregar as imagens das setas
imagem_seta_cima = pygame.image.load('cimaa.png')  # Substitua pelo caminho correto da sua imagem
imagem_seta_baixo = pygame.image.load('baixoo.png')  # Substitua pelo caminho correto da sua imagem
imagem_seta_esquerda = pygame.image.load('esquerdaa.png')  # Substitua pelo caminho correto da sua imagem
imagem_seta_direita = pygame.image.load('direitaa.png')  # Substitua pelo caminho correto da sua imagem

# Ajustar o tamanho das imagens de seta
imagem_seta_cima = pygame.transform.scale(imagem_seta_cima, (75, 75))
imagem_seta_baixo = pygame.transform.scale(imagem_seta_baixo, (75, 75))
imagem_seta_esquerda = pygame.transform.scale(imagem_seta_esquerda, (75, 75))
imagem_seta_direita = pygame.transform.scale(imagem_seta_direita, (75, 75))

# Carregar a imagem do personagem
imagem_bob_cima = pygame.image.load('bob_cut_cima.png')
imagem_bob_cima = pygame.transform.scale(imagem_bob_cima, (70, 70))

imagem_bob_baixo = pygame.image.load('bob_baixo.png')
imagem_bob_baixo = pygame.transform.scale(imagem_bob_baixo, (70, 70))

imagem_bob_esquerda = pygame.image.load('bob_esq.png')
imagem_bob_esquerda = pygame.transform.scale(imagem_bob_esquerda, (70, 70))

imagem_bob_direita = pygame.image.load('bob_dir.png')
imagem_bob_direita = pygame.transform.scale(imagem_bob_direita, (70, 70))

imagem_namorada = pygame.image.load('namorada_bob.png')
imagem_namorada = pygame.transform.scale(imagem_namorada, (largura, altura))

imagem_amigo = pygame.image.load('amigo_bob.png')
imagem_amigo = pygame.transform.scale(imagem_amigo, (largura, altura))

imagem_tesouro = pygame.image.load('tesouro_bob.png')
imagem_tesouro = pygame.transform.scale(imagem_tesouro, (40, 40))

# Inicialize a imagem atual como a de cima
imagem_bob = imagem_bob_cima

# Função para exibir a tela de escolha de nível com cliques do mouse
def tela_nivel():
    font = pygame.font.Font(None, 50)
    
    # Definir as áreas clicáveis para os níveis
    facil_rect = pygame.Rect(screen_width // 2 - 325, screen_height // 2 - 60, 650, 50)
    medio_rect = pygame.Rect(screen_width // 2 - 325, screen_height // 2, 650, 50)
    dificil_rect = pygame.Rect(screen_width // 2 - 325, screen_height // 2 + 60, 650, 50)
    
    screen.fill(background_color)
    
    texto = font.render("Escolha o modo de jogo:", True, branco)
    texto_rect = texto.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(texto, texto_rect)
    
    # Desenhar os botões para cada nível
    pygame.draw.rect(screen, (255, 255, 255), facil_rect)
    pygame.draw.rect(screen, (255, 255, 255), medio_rect)
    pygame.draw.rect(screen, (255, 255, 255), dificil_rect)

    # Opções de níveis
    niveis = ["Bob e o seu amigo - Fácil (3x3)", "Bob e a sua namorada - Médio (5x5)", "Bob caça ao tesouro - Difícil (7x7)"]
    for i, nivel in enumerate(niveis):
        texto = font.render(nivel, True, background_color)
        if i == 0:
            texto_rect = texto.get_rect(center=facil_rect.center)
        elif i == 1:
            texto_rect = texto.get_rect(center=medio_rect.center)
        else:
            texto_rect = texto.get_rect(center=dificil_rect.center)
        screen.blit(texto, texto_rect)
    
    pygame.display.flip()

    # Aguardar a escolha do jogador (clicando no botão correspondente)
    nivel_selecionado = None
    while nivel_selecionado is None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if facil_rect.collidepoint(event.pos):  # Clique no botão "Fácil"
                    nivel_selecionado = "facil"
                elif medio_rect.collidepoint(event.pos):  # Clique no botão "Médio"
                    nivel_selecionado = "medio"
                elif dificil_rect.collidepoint(event.pos):  # Clique no botão "Difícil"
                    nivel_selecionado = "dificil"
    
    # Retornar o nível escolhido
    return nivel_selecionado

# Função para exibir a mensagem de fase
def exibir_mensagem_fase(fase):
    fonte = pygame.font.Font(None, 60)
    texto = f"Fase {fase}"
    texto_renderizado = fonte.render(texto, True, (255, 255, 255))
    texto_rect = texto_renderizado.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(texto_renderizado, texto_rect)

# Função que gera uma direção aleatória baseada nos valores definidos
def direcao_gerada(): 
    valor = random.randint(1, 11)
    if valor in seta_cima:
        return seta_cima
    elif valor in seta_baixo:
        return seta_baixo
    elif valor in seta_esquerda:
        return seta_esquerda
    elif valor in seta_direita:
        return seta_direita

# Função que atualiza a sequência de direções de acordo com a fase
def atualizar_direcoes(fase):
    global sequencia_direcoes
    if fase == 1:
        sequencia_direcoes = [seta_cima]  # Primeira fase sempre começa com a seta para cima
    else:
        sequencia_direcoes = [direcao_gerada() for _ in range(fase)]  # A partir da segunda fase, direções aleatórias

# Função para desenhar as setas na tela
def desenhar_seta(direcao, pos_x, pos_y):
    x = 180
    if pos_y > 890:
        x =+ 900
        
    if direcao == seta_cima:
        screen.blit(imagem_seta_cima, (pos_x - 8, pos_y - x))
    elif direcao == seta_baixo:
        screen.blit(imagem_seta_baixo, (pos_x - 8, pos_y - x))
    elif direcao == seta_esquerda:
        screen.blit(imagem_seta_esquerda, (pos_x - 8, pos_y - x))
    elif direcao == seta_direita:
        screen.blit(imagem_seta_direita, (pos_x - 8, pos_y - x))

# Função para exibir a tela de derrota
def tela_derrota(fase):
    screen.fill(background_color)  # Preencher a tela de preto
    fonte = pygame.font.Font(None, 60)
    mensagem = f"Você perdeu na fase {fase}"
    texto_renderizado = fonte.render(mensagem, True, (255, 0, 0))  # Texto em vermelho
    texto_rect = texto_renderizado.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(texto_renderizado, texto_rect)  # Exibir o texto
    pygame.display.flip()  # Atualizar a tela
    time.sleep(3)  # Esperar 3 segundos antes de fechar o jogo

def tela_vitoria(nivel):
    fonte = pygame.font.Font(None, 52)
    if nivel == "facil":
        mensagem = f"Parabéns! Bob conseguiu encontrar seu amigo graças a você"
    elif nivel == "medio":
        mensagem = f"Parabéns! Bob conseguiu encontrar sua namorada graças a você"
    elif nivel == "dificil":
        mensagem = f"Parabéns! Bob conseguiu encontrar um tesouro graças a você"
    texto_renderizado = fonte.render(mensagem, True, (0, 255, 0))
    texto_rect = texto_renderizado.get_rect(center=(screen_width // 2, screen_height - 65))
    screen.blit(texto_renderizado, texto_rect)
    pygame.display.flip()
    time.sleep(6)  # Esperar 3 segundos antes de encerrar o jogo


def menu():
    # Chama a tela de nível
    nivel = tela_nivel()
    main(nivel)

    
def sair():
    pygame.quit()
    sys.exit()
    

def main(nivel):
    global sequencia_direcoes, imagem_bob
    clock = pygame.time.Clock()
    running = True

    if nivel == "facil":
        linhas, colunas = 3, 3
    elif nivel == "medio":
        linhas, colunas = 5, 5
    elif nivel == "dificil":
        linhas, colunas = 7, 7
        
    # Calcular a posição inicial para centralizar a matriz
    total_largura = colunas * largura + (colunas + 1) * margem
    total_altura = linhas * altura + (linhas + 1) * margem
    pos_x = (screen_width - total_largura) // 2
    pos_y = (screen_height - total_altura) // 2

    # Agora que pos_x e pos_y estão definidos, podemos calcular bob_x e bob_y
    if nivel == "facil":
        # Calcular a posição de bob no nível fácil (3x3)
        bob_x = pos_x + (margem + largura) * (colunas // 2) + margem  # Centralizado na coluna do meio
        bob_y = pos_y + altura * 3 + (margem * 4)  # Fica abaixo da primeira linha, fora da matriz
    elif nivel == "medio":
        # Calcular a posição de bob no nível médio (5x5)
        bob_x = pos_x + (margem + largura) * (colunas // 2) + margem  # Centralizado na coluna do meio
        bob_y = pos_y + altura * 5 + (margem * 6)  # Fica abaixo da primeira linha, fora da matriz
    elif nivel == "dificil":
        # Posição para o nível difícil (7x7) já estava correta no código original
        bob_x = pos_x + (margem + largura) * (colunas // 2) + margem  # Centralizado na coluna do meio
        bob_y = screen_height - altura - 32  # Fica na parte inferior da tela, como no original

    fase = 1
    vitoria = 0
    teclas_pressionadas = 0  # Número de teclas pressionadas pelo jogador
    jogando = False  # Variável para controlar o momento de aceitar entradas
    teclas_usuario = []  # Lista para armazenar as teclas pressionadas pelo jogador

    screen.fill(background_color)
    
    while running:
        # Exibir a mensagem de fase
        screen.fill(background_color)
        exibir_mensagem_fase(fase)
        pygame.display.flip()
        time.sleep(1)  # Exibir mensagem da fase por 1 segundo

        # Atualizar a lista de direções para a fase atual
        atualizar_direcoes(fase)

        # Exibir a sequência de setas uma por vez na tela
        screen.fill(background_color)
        exibir_mensagem_fase(fase)
        
        for i in range(fase):
            screen.fill(background_color)  # Limpar a tela a cada nova seta
            exibir_mensagem_fase(fase)
            screen.fill(background_color)
            desenhar_seta(sequencia_direcoes[i], (screen_width - 65) // 2, screen_height // 4 + (i * 60))
            pygame.display.flip()
            time.sleep(1)  # Esperar 1 segundo antes de exibir a próxima seta

        # 1 segundo para mostrar o tabuleiro depois de mostrar a sequência completa
        time.sleep(1)

        # Aqui, o tabuleiro é exibido e agora o jogador pode tentar acertar a sequência
        teclas_pressionadas = 0  # Resetando a contagem de teclas pressionadas
        jogando = True
        teclas_usuario = []  # Resetando a lista de teclas pressionadas pelo jogador
        
        while jogando and teclas_pressionadas < fase:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    jogando = False
                    sair()  
                    

                # Capturar as teclas pressionadas
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        movimento = seta_cima
                        imagem_bob = imagem_bob_cima
                    elif event.key == K_DOWN:
                        movimento = seta_baixo
                        imagem_bob = imagem_bob_baixo
                    elif event.key == K_LEFT:
                        movimento = seta_esquerda
                        imagem_bob = imagem_bob_esquerda
                    elif event.key == K_RIGHT:
                        movimento = seta_direita
                        imagem_bob = imagem_bob_direita
                    else:
                        continue

                    # Adicionar a tecla pressionada à lista
                    teclas_usuario.append(movimento)

                    # Verificar se a tecla pressionada corresponde à direção da sequência
                    if teclas_usuario != sequencia_direcoes[:len(teclas_usuario)]:
                        # Se a sequência do jogador estiver incorreta, o jogo termina
                        tela_derrota(fase)
                        running = False
                        jogando = False
                        break
                    
                    # Atualizar a posição de Bob na matriz com base no movimento
                    if teclas_pressionadas < fase:
                        if teclas_pressionadas < fase:
                            if movimento == seta_cima:
                                if bob_y-20 > pos_y:  # Movimento permitido dentro da matriz (gambiarra - 20)
                                    bob_y -= altura
                                else:  # Movimento para fora por cima
                                    bob_y -= altura
                                    vitoria = 1 #binário
                                    running = False
                                    jogando = False
                                    break
                            elif movimento == seta_baixo:
                                if bob_y < pos_y + (linhas - 1) * (altura + margem):  # Limite inferior da matriz
                                    bob_y += altura
                            elif movimento == seta_esquerda:
                                if bob_x-20 > pos_x:  # Limite esquerdo da matriz (gambiarra - 20)
                                    bob_x -= largura
                            elif movimento == seta_direita:
                                if bob_x+20 < pos_x + (colunas - 1) * (largura + margem):  # Limite direito da matriz
                                    bob_x += largura

                        teclas_pressionadas += 1  # Aumentar o contador de teclas pressionadas


            # Exibir o estado atual do jogo
            screen.fill(background_color)  # Limpar a tela
            for linha in range(linhas):
                for coluna in range(colunas):
                    cor = branco
                    pygame.draw.rect(screen, cor,
                        [pos_x + (margem + largura) * coluna + margem,
                         pos_y + (margem + altura) * linha + margem, largura, altura])
            
            # Exibir a imagem de Bob
            screen.blit(imagem_bob, (bob_x, bob_y))
            pygame.display.flip()  # Atualizar a tela
            clock.tick(60)  # Limitar a taxa de atualização para 60 FPS

        # Verificar se o jogador completou a fase
        if teclas_pressionadas == fase:
            fase += 1  # Aumentar a fase
            teclas_pressionadas = 0  # Resetar o contador de teclas pressionadas

        if vitoria == 1:
            if nivel == "facil":
                screen.blit(imagem_amigo, (bob_x, bob_y - altura))
            elif nivel == "medio":
                screen.blit(imagem_namorada, (bob_x, bob_y - altura))
            elif nivel == "dificil":
                screen.blit(imagem_tesouro, (bob_x + 17, bob_y - altura + 34))   
            tela_vitoria(nivel)

        clock.tick(60)

    menu()
    

if __name__ == "__main__":
    menu()                                                                                          
