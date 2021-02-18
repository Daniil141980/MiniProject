from showMap import load_map
import pygame
import os


class MapParams:
    def __init__(self):
        self.lat = 55.729738
        self.lon = 37.664777
        self.zoom = 10

    def update(self, event):
        if event.key == pygame.K_PAGEUP and self.zoom < 17:
            self.zoom += 1
        elif event.key == pygame.K_PAGEDOWN and self.zoom > 0:
            self.zoom -= 1

    def get_search_params(self):
        return f'll={self.lon},{self.lat}&z={self.zoom}'


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    map_object = MapParams()
    map_file = None
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            map_object.update(event)
        map_file = load_map(map_object.get_search_params())
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()
