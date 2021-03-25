import pygame
from pygame.font import Font
from pygame.rect import Rect

import socket, select, threading, sys, os

# socket
HEADER_LENGTH = 10

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = IP.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
print(username_header + username)
client_socket.send(username_header + username)



# pygame

pygame.init()

logoZepp = pygame.image.load('assets/zepp.png')
backgroundImage = pygame.image.load('assets/background.png')
greenZeppelin = pygame.image.load('assets/greenZeppelin.png')
loginBackground = pygame.image.load('assets/loginBackground.png')

WHITE = (255, 255, 255)

VEGAS_GOLD = (197, 179, 88)
METALLIC_GOLD = (212, 175, 55)
GOLDEN_BROWN = (153, 101, 21)

DARK = (51, 51, 51)
DARKER = (34, 34, 34)
BLACK = (17, 17, 17)



class HomeObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lenght = 100
        self.height = 100

    def draw(self):
        root.blit(logoZepp, (logoZepp.get_rect(center=(int(self.x + self.lenght/2), int(self.y + self.height/2)))))

    def collidePoint(self, point):
        return pygame.Rect(self.x, self.y, self.lenght, self.height).collidepoint(point)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = METALLIC_GOLD
        self.font = pygame.font.Font('fonts/Philosopher.ttf', 12)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        self.color = METALLIC_GOLD if self.active else GOLDEN_BROWN
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, WHITE)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, root):
        root.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(root, self.color, self.rect, 2)

    def getText(self):
        return self.text

class HideInputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = METALLIC_GOLD
        self.font = pygame.font.Font('fonts/Philosopher.ttf', 12)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        self.color = METALLIC_GOLD if self.active else GOLDEN_BROWN
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(''.join('•' for i in self.text), True, WHITE)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, root):
        root.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(root, self.color, self.rect, 2)
    
    def getText(self):
        return self.text


# fonctions
def logIn(pseudo, password):
    to_send = f'000{pseudo}¤{password}'.encode('utf-8')
    header = f"{len(to_send):<{HEADER_LENGTH}}".encode('utf-8')
    print('[log in] waiting for server...')
    client_socket.send(header + to_send)


def signUp(pseudo, password):
    to_send = f'001{pseudo}¤{password}'.encode('utf-8')
    header = f"{len(to_send):<{HEADER_LENGTH}}".encode('utf-8')
    print('[sign up] waiting for server...')
    client_socket.send(header + to_send)





def loginInterface():
    root.blit(greenZeppelin, (0, 0))
    root.blit(loginBackground, (333, 150))
    font = pygame.font.Font('fonts/Philosopher.ttf', 16)
    bigFont = pygame.font.Font('fonts/Philosopher.ttf', 20)
    bigFont.set_bold(True)
    title = bigFont.render('Ha, te revoilà !', True, WHITE)
    subtitle = font.render('Nous sommes si heureux de te revoir !', True, WHITE)
    mailLabel = font.render('PSEUDO', True, WHITE)
    passwordLabel = font.render('MOT DE PASSE', True, WHITE)

    logInButtonLabel = font.render('Se connecter', True, WHITE)
    signUpButtonLabel = font.render("S'inscrire", True, WHITE)

    mailInput = InputBox(375, 250, 100, 30)
    passwordInput = HideInputBox(375, 310, 100, 30)
    inputBoxes = [mailInput, passwordInput]

    done, logInBool, signUpBool = False, False, False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos
                if 370 <= mousePos[0] <= 470 and 355 <= mousePos[1] <= 385:
                    logInBool = True
                    done = True
                elif 370 <= mousePos[0] <= 470 and 405 <= mousePos[1] <= 435:
                    signUpBool = True
                    done = True

            for box in inputBoxes:
                box.handle_event(event)

        for box in inputBoxes:
            box.update()

        root.blit(loginBackground, (333, 150))
        root.blit(title, (430, 160))
        root.blit(subtitle, (375, 190))
        root.blit(mailLabel, (375, 230))
        root.blit(passwordLabel, (375, 290))
        root.blit(logInButtonLabel, (375, 360))
        root.blit(signUpButtonLabel, (375, 410))
        
        for box in inputBoxes:
            box.draw(root)

        pygame.display.flip()
        pygame.time.delay(40)


    if logInBool:logIn(mailInput.getText(), passwordInput.getText())
    elif signUpBool:signUp(mailInput.getText(), passwordInput.getText())
    
        




def homeInterface():
    root.blit(logoZepp, (10, 10))

home = HomeObj(10, 10)
serversList = []

root = pygame.display.set_mode((1000, 600))

loginInterface()
pygame.display.update()

main = True
while main:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = event.pos
            if home.collidePoint(mousePos):
                homeInterface()

            for server in serversList:
                if server.collidepoint(mousePos):
                    #server.goTo()
                    pass
    


pygame.quit()