import pygame
from network import *
from game import *


width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.init()
pygame.display.set_caption("Rock, Paper and Scissors")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 130
        self.height = 110

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        x2 = pos[1]

        if x1 in range(self.x, self.x + self.width + 1) and x2 in range(self.y, self.y + self.height + 1):
            return True
        else:
            return False


btns = [Button("Rock", 80, 500, (0, 0, 255)), Button("Scissors", 280, 500, (0, 0, 255)), Button("Paper", 480, 500, (0, 0, 255))]
moves = {
    "R": "Rock",
    "S": "Scissors",
    "P": "Paper"
}


def redrawWindow(win, game, p):

    win.fill((255, 0, 0))
    rpsImg = pygame.image.load('rps.png')
    win.blit(rpsImg, (0, 0))
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    font = pygame.font.SysFont("comicsans", 80)
    text = font.render("Rock, Paper and Scissors", 1, (255, 255, 255))
    win.blit(text, (width / 2 - text.get_width() / 2, 50))

    if not game.bothReady:
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 255, 255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    elif game.quit:
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Other player left...", 1, (255, 255, 255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("YOU", 1, (255, 255, 255))
        win.blit(text, (80, 200))
        text = font.render("OPPONENT", 1, (255, 255, 255))
        win.blit(text, (380, 200))

        font = pygame.font.SysFont("comicsans", 60)
        text1 = font.render(game.getP1win(), 1, (255, 255, 255))
        text2 = font.render((game.getP2win()), 1, (255, 255, 255))

        if p == 0:
            win.blit(text1, (110, 250))
            win.blit(text2, (480, 250))
        if p == 1:
            win.blit(text2, (110, 250))
            win.blit(text1, (480, 250))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)

        if move1 != '':
            move1 = moves[move1]
        if move2 != '':
            move2 = moves[move2]


        if game.bothPlayed():
            text1 = font.render(move1, 1, (255, 255, 255))
            text2 = font.render(move2, 1, (255, 255, 255))
        else:
            if game.p1Play and p == 0:
                text1 = font.render(move1, 1, (255, 255, 255))
            elif game.p1Play:
                text1 = font.render("Locked In", 1, (255, 255, 255))
            else:
                text1 = font.render("Waiting ... ", 1, (255, 255, 255))
            if game.p2Play and p==1:
                text2 = font.render(move2, 1, (255, 255, 255))
            elif game.p2Play:
                text2 = font.render("Locked In", 1, (255, 255, 255))
            else:
                text2 = font.render("Waiting ... ", 1, (255, 255, 255))
        if p == 1:
            win.blit(text2, (80, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (80, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)


    pygame.display.update()


def main():
    global win
    run = True
    clock = pygame.time.Clock()

    n = Network()

    p = int(n.getP())
    print("You are player: ", p)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldnt get game")
            break

        if game.bothPlayed():
            redrawWindow(win, game, p)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldnt get game")
                break
            font = pygame.font.SysFont("comicsans", 90)

            if (game.checkWinner() == 0 and p == 0) or (game.checkWinner() == 1 and p == 1):
                text = font.render("You Won!", 1, (255, 255, 0))
            elif game.checkWinner() == -1:
                text = font.render("Tie Game!", 1, (255, 255, 0))
            else:
                text = font.render("You Lost...", 1, (255, 255, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                n.send("disconnect")
                menu_screen()

            # if event.type == pygame.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            #     redrawWindow(win, game, p)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.bothReady:
                    disconnected()

                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.bothReady:
                        if p == 0:
                            if not game.p1Play:
                                n.send(btn.text[0])
                        else:
                            if not game.p2Play:
                                n.send(btn.text[0])

        redrawWindow(win, game, p)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        win.fill((255, 0, 0))
        rpsImg = pygame.image.load('rps.png')
        win.blit(rpsImg, (0, 0))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 255, 255))
        win.blit(text, (round(width/2) - round(text.get_width()/2), round(height/2) - round(text.get_height()/2)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()


# check if player if the other player has disconnected





