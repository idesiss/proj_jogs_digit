import pygame
from pygame.locals import *
import time
import random

pygame.init()

screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
background_color = (0, 0, 0)
pygame.display.set_caption("Bob e o seu encontro")

branco = (255, 255, 255)

linhas = 7
colunas = 7
largura = 75
altura = 75
margem = 1

seta_cima = 0
seta_baixo = 1
seta_esquerda = 2
seta_direita = 3

sequencia_direcoes = []

imagem_seta_cima = pygame.image.load('cima.png')
imagem_seta_baixo = pygame.image.load('baixo.png')
imagem_seta_esquerda = pygame.image.load('esq.png')
imagem_seta_direita = pygame.image.load('dir.png')

imagem_seta_cima = pygame.transform.scale(imagem_seta_cima, (50, 50))
imagem_seta_baixo = pygame.transform.scale(imagem_seta_baixo, (50, 50))
imagem_seta_esquerda = pygame.transform.scale(imagem_seta_esquerda, (50, 50))
imagem_seta_direita = pygame.transform.scale(imagem_seta_direita, (50, 50))

imagem_bob = pygame.image.load('bob_cut.png')
imagem_bob = pygame.transform.scale(imagem_bob, (largura, altura))

def desenhar_seta(direcao, pos_x, pos_y):
    if direcao == seta_cima:
        screen.blit(imagem_seta_cima, (pos_x, pos_y))
    elif direcao == seta_baixo:
        screen.blit(imagem_seta_baixo, (pos_x, pos_y))
    elif direcao == seta_esquerda:
        screen.blit(imagem_seta_esquerda, (pos_x, pos_y))
    elif direcao == seta_direita:
        screen.blit(imagem_seta_direita, (pos_x, pos_y))

def exibir_mensagem_fase(fase):
    fonte = pygame.font.Font(None, 60)
    texto = f"Fase {fase}"
    texto_renderizado = fonte.render(texto, True, (255, 255, 255))
    texto_rect = texto_renderizado.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(texto_renderizado, texto_rect)

def exibir_mensagem_preparacao(mensagem):
    fonte = pygame.font.Font(None, 60)
    texto_renderizado = fonte.render(mensagem, True, (255, 255, 255))
    texto_rect = texto_renderizado.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(texto_renderizado, texto_rect)

def direcao_gerada(): 
    return random.randint(0, 3)

def atualizar_direcoes(fase):
    global sequencia_direcoes
    if fase == 1:
        sequencia_direcoes = [seta_cima]
    else:
        sequencia_direcoes = [direcao_gerada() for _ in range(fase)]

def desenhar_sequencia_setas(fase):
    pos_x = (screen_width - 50) // 2
    y_offset = screen_height // 4
    for i in range(fase):
        desenhar_seta(sequencia_direcoes[i], pos_x, y_offset + (i * 60))

def mostrar_tela_perda(fase):
    screen.fill((0, 0, 0))
    fonte = pygame.font.Font(None, 60)
    mensagem = f"Você perdeu na fase {fase}."
    texto_renderizado = fonte.render(mensagem, True, (255, 0, 0))
    texto_rect = texto_renderizado.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(texto_renderizado, texto_rect)
    pygame.display.flip()
    time.sleep(3)

def main():
    global sequencia_direcoes
    clock = pygame.time.Clock()
    running = True

    total_largura = colunas * largura + (colunas + 1) * margem
    total_altura = linhas * altura + (linhas + 1) * margem
    pos_x = (screen_width - total_largura) // 2
    pos_y = (screen_height - total_altura) // 2

    bob_x = pos_x + (margem + largura) * 3 + margem
    bob_y = screen_height - altura - 32

    fase = 1
    teclas_pressionadas = 0
    jogando = False
    teclas_usuario = []

    while running:
        screen.fill(background_color)
        exibir_mensagem_fase(fase)
        pygame.display.flip()
        time.sleep(1)

        atualizar_direcoes(fase)

        screen.fill(background_color)
        exibir_mensagem_fase(fase)

        for i in range(fase):
            screen.fill(background_color)
            exibir_mensagem_fase(fase)
            desenhar_seta(sequencia_direcoes[i], (screen_width - 65) // 2, screen_height // 4 + (i * 60))
            pygame.display.flip()
            time.sleep(1)

        time.sleep(1.5)

        teclas_pressionadas = 0
        jogando = True
        teclas_usuario = []
        
        while jogando and teclas_pressionadas < fase:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    jogando = False
                    break

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        movimento = seta_cima
                    elif event.key == K_DOWN:
                        movimento = seta_baixo
                    elif event.key == K_LEFT:
                        movimento = seta_esquerda
                    elif event.key == K_RIGHT:
                        movimento = seta_direita
                    else:
                        continue

                    teclas_usuario.append(movimento)

                    if teclas_usuario != sequencia_direcoes[:len(teclas_usuario)]:
                        mostrar_tela_perda(fase)
                        running = False
                        jogando = False
                        break

                    if teclas_pressionadas < fase:
                        if movimento == seta_cima and bob_y > pos_y:
                            bob_y -= altura
                        elif movimento == seta_baixo and bob_y < screen_height - altura:
                            bob_y += altura
                        elif movimento == seta_esquerda and bob_x > pos_x:
                            bob_x -= largura
                        elif movimento == seta_direita and bob_x < screen_width - largura:
                            bob_x += largura

                        teclas_pressionadas += 1

            screen.fill(background_color)
            for linha in range(linhas):
                for coluna in range(colunas):
                    cor = branco
                    pygame.draw.rect(screen, cor,
                        [pos_x + (margem + largura) * coluna + margem,
                         pos_y + (margem + altura) * linha + margem, largura, altura])
            
            screen.blit(imagem_bob, (bob_x, bob_y))
            pygame.display.flip()

            clock.tick(60)

        if teclas_pressionadas == fase:
            fase += 1
            teclas_pressionadas = 0

        if fase > 5:
            running = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
