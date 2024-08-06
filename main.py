import pygame
import win32gui
import win32con
import sys
import pyautogui as gui


pygame.init()
scr = pygame.display.set_mode((300, 100), pygame.NOFRAME)
hwnd = pygame.display.get_wm_info()['window']
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)
clock = pygame.time.Clock()


pygame.display.set_caption("Austins Media Control Panel")
pygame.display.set_icon(pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\play.png"))

def DrawText(text, x, y):
    font = pygame.font.SysFont("Agency FB", 30)
    text = font.render(text, False, (0, 0, 0))
    scr.blit(text, (x, y))

class button:
    def __init__(self, x: int, y: int, sx: int, sy: int, clickFunction):
        self.image = pygame.Surface((sx, sy), pygame.SRCALPHA)
        self._rect = pygame.Rect(x, y, sx, sy)
        self.func = clickFunction
    def collidesWith(self, rect: pygame.Rect):
        return self._rect.colliderect(rect)
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self._rect.x, self._rect.y))
    def getRect(self):
        return self._rect
    def click(self):
        self.func()

playImage = pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\play.png")
pause = pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\pause.png")
play = pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\play.png")
paused: bool = False
moving = False

def playf():
    global paused
    global playImage
    if paused:
        playImage = play
        paused = False
    else:
        playImage = pause
        paused = True

    gui.press("playpause")

def rev():
    gui.press("prevtrack")

def fwd():
    gui.press("nexttrack")

def move():
    global moving
    if moving:
        moving = False
        scr = pygame.display.set_mode((300, 100), pygame.NOFRAME)
        rect = win32gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        width, height = rect[2] - rect[0], rect[3] - rect[1]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y-30, width, height, win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    else:
        moving = True
        scr = pygame.display.set_mode((300, 100))
        rect = win32gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        width, height = rect[2] - rect[0], rect[3] - rect[1]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y+30, width, height, win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        


moveButton = button(0, 0, 15, 15, move)
moveButton.image = pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\move.png")

playButton = button(25, 25, 50, 50, playf)
playButton.image = playImage

revButton = button(125, 25, 50, 50, rev)
revButton.image = pygame.transform.flip(pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\fwd-rev.png"), True, False)

fwdButton = button(225, 25, 50, 50, fwd)
fwdButton.image = pygame.image.load("C:\\Users\\theau\\Documents\\Code Projects\\python\\media\\buttons\\fwd-rev.png")

def getCollidingButton(rect: pygame.Rect) -> button | None:
    if moveButton.collidesWith(rect):
        return moveButton
    if playButton.collidesWith(rect):
        return playButton
    if revButton.collidesWith(rect):
        return revButton
    if fwdButton.collidesWith(rect):
        return fwdButton
    return None

selected = pygame.Rect(0, 0, 0, 0)
isSelect = False

def render():

    playButton.image = playImage

    scr.fill((75, 75, 75))

    if isSelect:
        pygame.draw.rect(scr, (100, 100 ,100), selected, 0, 10)

    moveButton.draw(scr)
    playButton.draw(scr)
    revButton.draw(scr)
    fwdButton.draw(scr)




mouserect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 5, 5)



while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                if getCollidingButton(mouserect) is not None:
                    getCollidingButton(mouserect).click()
        elif event.type == pygame.WINDOWFOCUSGAINED:
            if getCollidingButton(mouserect) is not None:
                    getCollidingButton(mouserect).click()
    
    mouserect.x = pygame.mouse.get_pos()[0]
    mouserect.y = pygame.mouse.get_pos()[1]

    if (getCollidingButton(mouserect) is not None and pygame.mouse.get_focused()):
        rect = getCollidingButton(mouserect).getRect()
        selected.width = rect.width+12
        selected.height = rect.width+12
        selected.x = rect.x - 6
        selected.y = rect.y - 6
        isSelect = True
    else:
        isSelect = False
    


    render()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(24)
