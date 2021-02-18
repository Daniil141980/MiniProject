from showMap import load_map
import pygame
import os

LAT_STEP = 0.01
LON_STEP = 0.023
MAP_TYPES = ['map', 'sat', 'sat,skl']

class MapParams:
    def __init__(self):
        self.lat = 55.729738
        self.lon = 37.664777
        self.zoom = 15
        self.map_type = MAP_TYPES[0]

    def update(self, event):
        lonstep = self.get_lon_step()
        latstep = self.get_lat_step()
        if event.key == pygame.K_PAGEUP and self.zoom < 17:
            self.zoom += 1
        elif event.key == pygame.K_PAGEDOWN and self.zoom > 0:
            self.zoom -= 1
        elif event.key == pygame.K_LEFT and self.lon - lonstep >= -90:
            self.lon -= LON_STEP * (2 ** (15 - self.zoom))
        elif event.key == pygame.K_RIGHT and self.lon + lonstep <= 90:
            self.lon += LON_STEP * (2 ** (15 - self.zoom))
        elif event.key == pygame.K_DOWN and self.lat - latstep >= -180:
            self.lat -= latstep
        elif event.key == pygame.K_UP and self.lat + latstep <= 180:
            self.lat += latstep
        elif event.key == pygame.K_1 and self.map_type != MAP_TYPES[0]:
            self.map_type = MAP_TYPES[0]
        elif event.key == pygame.K_2 and self.map_type != MAP_TYPES[1]:
            self.map_type = MAP_TYPES[1]
        elif event.key == pygame.K_3 and self.map_type != MAP_TYPES[2]:
            self.map_type = MAP_TYPES[2]

    def get_lon_step(self):
        return LON_STEP * (2 ** (15 - self.zoom))

    def get_lat_step(self):
        return LAT_STEP * (2 ** (15 - self.zoom))

    def get_search_params(self):
        return f'll={self.lon},{self.lat}&z={self.zoom}&l={self.map_type}'


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
