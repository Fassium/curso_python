import random
import pygame

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tita - Caçador de Javali")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 28)
pygame.mouse.set_visible(False)  # esconde o mouse, vamos desenhar uma mira

pontos = 0
flechas = 10


def novo_javali():
    # nasce fora da tela, à esquerda, numa altura sorteada
    return {"x": -50, "y": random.randint(300, 550), "velocidade": random.randint(3, 7)}


def desenhar_javali(x, y):
    # patas (atrás do corpo)
    for dx in (-28, -12, 14, 28):
        pygame.draw.rect(tela, (50, 30, 15), (x + dx - 4, y + 12, 8, 18))
    # corpo
    pygame.draw.ellipse(tela, (90, 60, 40), (x - 42, y - 22, 84, 44))
    # cabeça
    pygame.draw.ellipse(tela, (70, 45, 30), (x + 22, y - 18, 36, 30))
    # focinho
    pygame.draw.ellipse(tela, (130, 100, 90), (x + 50, y - 6, 14, 14))
    # presa
    pygame.draw.polygon(tela, (255, 255, 235), [(x + 46, y + 4), (x + 52, y + 4), (x + 50, y - 4)])
    # orelha
    pygame.draw.polygon(tela, (50, 30, 15), [(x + 28, y - 14), (x + 38, y - 14), (x + 33, y - 28)])
    # olho
    pygame.draw.circle(tela, (255, 255, 255), (x + 42, y - 6), 3)
    # rabo
    pygame.draw.line(tela, (50, 30, 15), (x - 42, y - 5), (x - 52, y - 14), 3)


javali = novo_javali()
rodando = True

while rodando:
    # 1) EVENTOS: o que o jogador fez?
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and flechas > 0:
            flechas -= 1
            mouse_x, mouse_y = evento.pos
            # acertou? o clique está dentro da área do javali?
            if abs(mouse_x - javali["x"]) < 50 and abs(mouse_y - javali["y"]) < 25:
                pontos += 10
                javali = novo_javali()

    # 2) ATUALIZAR: mover o javali
    if flechas > 0:
        javali["x"] += javali["velocidade"]
        if javali["x"] > LARGURA + 50:  # fugiu pela direita
            javali = novo_javali()

    # 3) DESENHAR
    tela.fill((34, 139, 34))
    pygame.draw.rect(tela, (20, 80, 20), (0, 0, LARGURA, 250))  # floresta
    for x in range(50, LARGURA, 120):  # árvores
        pygame.draw.rect(tela, (90, 60, 30), (x - 8, 150, 16, 100))
        pygame.draw.circle(tela, (10, 60, 10), (x, 130), 45)

    pygame.draw.rect(tela, (139, 90, 43), (0, 250, LARGURA, 350))  # lavoura
    for linha in range(280, ALTURA, 40):  # fileiras da plantação
        pygame.draw.line(tela, (110, 70, 30), (0, linha), (LARGURA, linha), 4)

    desenhar_javali(javali["x"], javali["y"])

    # placar
    texto = fonte.render(f"Tita | Pontos: {pontos} | Flechas: {flechas}", True, (255, 255, 255))
    tela.blit(texto, (20, 15))

    if flechas == 0:
        fim = fonte.render("FIM DE JOGO!", True, (255, 220, 0))
        tela.blit(fim, (320, 280))

    # mira no lugar do mouse
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (220, 30, 30), (mx, my), 15, 2)
    pygame.draw.line(tela, (220, 30, 30), (mx - 20, my), (mx + 20, my), 2)
    pygame.draw.line(tela, (220, 30, 30), (mx, my - 20), (mx, my + 20), 2)

    pygame.display.flip()  # mostra o que foi desenhado
    relogio.tick(60)       # 60 quadros por segundo

pygame.quit()
