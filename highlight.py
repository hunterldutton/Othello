import pygame

RADIUS = 10
PURPLE = (200, 0, 255)
TILE_SIZE = 50

"""
Class for a highlight that's gives a player valid tiles for a piece. 


"""

class HIGHLIGHT(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.x = x
        self.y = y

        self.active = False

        self.color = PURPLE

        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        
        # Make surface transparent so there won't be a black square behind circle
        self.image.set_colorkey((0, 0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y
    
    def update(self):
        pygame.draw.circle(self.image, self.color, (TILE_SIZE / 2, TILE_SIZE / 2), RADIUS)
        pass
