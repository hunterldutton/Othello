import pygame

RADIUS = 20
WHITE = (255, 255, 255)
BLACK = (1, 1, 1)
TILE_SIZE = 50

class PIECE(pygame.sprite.Sprite):
    def __init__(self, x, y, color_name) -> None:
        super().__init__()

        self.x = x
        self.y = y

        self.color_name = color_name
        if color_name == "white":
            self.color = WHITE
        else:
            self.color = BLACK

        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        
        # Make surface transparent so there won't be a black square behind circle
        self.image.set_colorkey((0, 0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y
    
    def update(self):
        pygame.draw.circle(self.image, self.color, (TILE_SIZE / 2, TILE_SIZE / 2), RADIUS)
        pass