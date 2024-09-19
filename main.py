import pygame
from pygame import mixer

from scene import STARTSCENE

#Sprint 3

BLACK = (0, 0, 0)
FPS = 30

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

mixer.music.load("assets/sounds/game_background.mp3")
mixer.music.play(-1)
mixer.music.set_volume(.09)


scene = STARTSCENE(screen)

# Window title
pygame.display.set_caption("Othello")

# Create running loop
# If program is still running,
# renders the correct scene's contents
running = True
while running:
    clock.tick(30)
    events = []
    if (scene.get_scene_type() == "Title" or scene.get_scene_type() == "Game_Over"):
        for event in pygame.event.get():
            events.append(event)
            if event.type == pygame.QUIT:
                running = False
        scene.render(screen)
        running = scene.process_input(events)
        pygame.display.flip()
    elif (scene.get_scene_type() == "Game"):
        scene.render()
        pygame.display.flip()
    scene = scene.next
