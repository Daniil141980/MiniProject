from Button import Button
from showMap import load_map
import pygame
import os
import requests
from input_box import InputBox

pygame.init()

LAT_STEP = 0.01
LON_STEP = 0.023
MAP_TYPES = ['map', 'sat', 'sat,skl']


class MapParams:
    def __init__(self):
        self.lat = 55.729738
        self.lon = 37.664777
        self.zoom = 15
        self.map_type = MAP_TYPES[0]
        self.point = ''

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
        if self.point == '':
            return f'll={self.lon},{self.lat}&z={self.zoom}&l={self.map_type}'
        elif self.point:
            return f'll={self.lon},{self.lat}&z={self.zoom}&l={self.map_type}&pt={self.point}'

    def find_something(self, geocode):
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba" \
                           f"-98533de7710b&geocode={geocode}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"] \
                ["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.lon, self.lat = map(float, toponym_coodrinates.split())
            if self.point == '':
                self.point = f'{self.lon},{self.lat},pm2rdl'
            else:
                self.point += f'~{self.lon},{self.lat},pm2rdl'

    def del_last_point(self):
        if self.point != '':
            if '~' in self.point:
                self.point = '~'.join(self.point.split('~')[:-1])
            else:
                self.point = ''


def main():
    input_box = InputBox(0, 450, 600, 50)
    screen = pygame.display.set_mode((600, 500))
    map_object = MapParams()
    map_file = None
    btn = Button(50, 50, 550, 450, '')
    click = False
    f = pygame.font.Font(None, 36)
    text = f.render('Del', True, (180, 0, 0))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            map_object.update(event)
        elif event.type == pygame.KEYDOWN:
            if input_box.active:
                if event.key == pygame.K_RETURN:
                    map_object.find_something(input_box.text)
                    input_box.text = ''
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        input_box.handle_event(event)
        screen.fill('black')
        delete_point = btn.draw(screen, click)
        if delete_point:
            map_object.del_last_point()
        map_file = load_map(map_object.get_search_params())
        screen.blit(pygame.image.load(map_file), (0, 0))
        input_box.update()
        input_box.draw(screen)
        screen.blit(text, (555, 465))
        pygame.display.flip()
        click = False
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()
