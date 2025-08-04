import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 754))
background_image = pygame.image.load('D:\\python_learning\\labirint\\maze2.jpg')
background_image = pygame.transform.scale(background_image, (1000, 754))

dog_image = pygame.image.load('D:\\python_learning\\labirint\\dog.png')
dog_image= pygame.transform.scale(dog_image, (50, 50))

pygame.display.set_caption("Labirint")

icon = pygame.image.load('D:\\python_learning\\labirint\\icon.png')

pygame.display.set_icon(icon)
font = pygame.font.Font(None, 90)

def load_message_image(filename):
    image = pygame.image.load(f'D:\\python_learning\\labirint\\{filename}')
    return image

message_images = {
    "wrong_way": load_message_image("ww.png"),
    "victory": load_message_image("victory.png"),
    "crash": load_message_image("crash.png"),
    "restart": load_message_image("restart.png"),
    "scared" : load_message_image("scared.png"),
}

running = True
game_over = False
current = "A"
last = None
current_message = None

key_to_dir = {
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
}

nodes = {
    "A": {"pos": (240, 150), "dirs": {"right": "B"}, "type": "normal"},
    "B": {"pos": (290, 150), "dirs": {"down": "C", "left": "A"}, "type": "normal"},
    "C": {"pos": (290, 210), "dirs": {"left": "D", "up": "B"}, "type": "normal"},
    "D": {"pos": (240, 210), "dirs": {"down": "E", "right": "C"}, "type": "normal"},
    "E": {"pos": (240, 265), "dirs": {"right": "F", "up": "D"}, "type": "normal"},
    "F": {"pos": (290, 265), "dirs": {"right": "H", "down": "WW1", "left": "E"}, "type": "normal"},
    "H": {"pos": (355, 265), "dirs": {"right": "I", "left": "F"}, "type": "normal"},
    "WW1": {"pos": (290, 325), "type": "wrong_way"},
    "I": {"pos": (406, 265), "dirs": {"right": "J", "up": "WW2", "left": "H"}, "type": "normal"},
    "WW2": {"pos": (400, 215), "type": "wrong_way"},
    "J": {"pos": (470, 265), "dirs": {"up": "WW3", "down": "K", "left": "I"}, "type": "normal"},
    "WW3": {"pos": (530, 325), "type": "wrong_way"},
    "K": {"pos": (470, 325), "dirs": {"down": "L", "left": "WW4", "up": "J"}, "type": "normal"},
    "WW4": {"pos": (410, 325), "type": "wrong_way"},
    "L": {"pos": (470, 380), "dirs": {"right": "M", "up": "K"}, "type": "normal"},
    "M": {"pos": (535, 380), "dirs": {"right": "N", "down": "WW5", "left": "L"}, "type": "normal"},
    "WW5": {"pos": (535, 425), "type": "wrong_way"},
    "N": {"pos": (595, 380), "dirs": {"right": "O", "left": "M"}, "type": "normal"},
    "O": {"pos": (654, 380), "dirs": {"right": "P", "left": "N"}, "type": "normal"},
    "P": {"pos": (724, 380), "dirs": {"down": "Q", "left": "O"}, "type": "normal"},
    "Q": {"pos": (724, 440), "dirs": {"left": "R", "down": "S", "up": "P"}, "type": "normal"},
    "R": {"pos": (655, 440), "dirs": {"right": "Q", "down": "T"}, "type": "normal"},
    "S": {"pos": (724, 480), "dirs": {"left": "T", "down": "WW6", "up": "Q"}, "type": "normal"},
    "WW6": {"pos": (720, 540), "type": "wrong_way"},
    "T": {"pos": (655, 480), "dirs": {"down": "U", "right": "S", "up": "R"}, "type": "normal"},
    "U": {"pos": (655, 540), "dirs": {"left": "V", "up": "T"}, "type": "normal"},
    "V": {"pos": (600, 540), "dirs": {"down": "W", "right": "U"}, "type": "normal"},
    "W": {"pos": (600, 600), "dirs": {"right": "X", "left": "WW7", "up": "V"}, "type": "normal"},
    "WW7": {"pos": (535, 600), "type": "wrong_way"},
    "X": {"pos": (655, 600), "dirs": {"down": "Y", "left": "W"}, "type": "normal"},
    "Y": {"pos": (655, 655), "dirs": {"right": "Z", "up": "X"}, "type": "normal"},
    "Z": {"pos": (730, 655), "dirs": {"right": "FF", "left": "Y"}, "type": "normal"},
    "FF": {"pos": (800, 655), "type": "victory"},
}

def create_overlay():
    overlay = pygame.Surface((1000, 754), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 180))
    return overlay

def draw_screen():
    screen.blit(background_image, (0, 0))
    title = font.render("Помоги Шарику найти косточку", True, (0, 0, 0))
    title_rect = title.get_rect(center=(500, 60))
    screen.blit(title, title_rect)

    dog_pos = nodes[current]["pos"]
    dog_rect = dog_image.get_rect(center=dog_pos)
    screen.blit(dog_image, dog_rect)

    if game_over and current_message:
        overlay = create_overlay()
        screen.blit(overlay, (0, 0))

        message_image = message_images[current_message]
        message_rect = message_image.get_rect(center=(500, 300))
        screen.blit(message_image, message_rect)

        restart_image = message_images["restart"]
        restart_rect = restart_image.get_rect(center=(500, 450))
        screen.blit(restart_image, restart_rect)

    pygame.display.flip()

def movement(direction):
    global current, last, game_over, current_message

    if direction in nodes[current]["dirs"]:
        new = nodes[current]["dirs"][direction]

        if new == last:
            current_message = "scared"
            game_over = True
            return

        last = current
        current = new

        if nodes[current]["type"] == "wrong_way":
            current_message = "wrong_way"
            game_over = True
        elif nodes[current]["type"] == "victory":
            current_message = "victory"
            game_over = True
        else:
            current_message = None

    else:
        current_message = "crash"
        game_over = True

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key in key_to_dir:
                direction = key_to_dir[event.key]
                movement(direction)

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                current = "A"
                last = None
                game_over = False
                current_message = None

    draw_screen()

    clock.tick(60)

pygame.quit()
sys.exit()