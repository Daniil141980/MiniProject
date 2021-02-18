import pygame
import requests
import os
import sys


def show_map(ll_z=None, map_type='map', add_params=None):
    server = 'http://static-maps.yandex.ru/1.x/'
    if ll_z:
        params = f'?{ll_z}&l={map_type}'
    else:
        params = f'?l={map_type}'
    if add_params:
        params += f'&{add_params}'
    response = requests.get(server + params)
    if not response:
        raise Exception('Error!!!')
    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as file:
            file.write(response.content)
    except IOError as ex:
        print(f'ERROR! {ex}')
        sys.exit(1)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit((pygame.image.load(map_file)), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


def load_map(ll_z=None, map_type='map', add_params=None):
    server = 'http://static-maps.yandex.ru/1.x/'
    if ll_z:
        params = f'?{ll_z}&l={map_type}'
    else:
        params = f'?l={map_type}'
    if add_params:
        params += f'&{add_params}'
    response = requests.get(server + params)
    if not response:
        raise Exception('Error!!!')
    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as file:
            file.write(response.content)
    except IOError as ex:
        print(f'ERROR! {ex}')
        sys.exit(1)
    return map_file
