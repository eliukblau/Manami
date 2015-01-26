#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import atexit
from ctypes import *

import sdl2.ext
from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlmixer import *

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

RESOURCES = dict()
RESOURCES['gfx'] = sdl2.ext.Resources(BASE_PATH, 'gfx')
RESOURCES['sfx'] = sdl2.ext.Resources(BASE_PATH, 'sfx')


def main():
    def close_all_things():
        Mix_FreeMusic(music)
        SDL_DestroyTexture(texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        Mix_CloseAudio()
        SDL_Quit()

    # registramos el callback para el cierre de aplicacion
    atexit.register(close_all_things)

    # 0 - VARIABLES GLOBALES
    gameloop = True
    window = pointer(SDL_Window())
    renderer = pointer(SDL_Renderer())
    texture = pointer(SDL_Texture())
    music = pointer(Mix_Music())
    rectangle = SDL_Rect()
    event = SDL_Event()

    # 1 - INICIAR EL JUEGO

    # 1.1 - SDL
    if 0 != SDL_Init(SDL_INIT_EVERYTHING):
        sys.exit(SDL_GetError())

    if 0 != SDL_CreateWindowAndRenderer(1080, 720, SDL_WINDOW_SHOWN | SDL_WINDOW_OPENGL,
                                        pointer(window), pointer(renderer)):
        sys.exit(SDL_GetError())

    SDL_SetWindowTitle(window, b'Manami - Simple Game Skeleton for Python/SDL2')

    # 1.2 - SDL_IMAGE
    if 0 == IMG_Init(IMG_INIT_PNG):
        sys.exit(IMG_GetError())

    texture = IMG_LoadTexture(renderer, RESOURCES['gfx'].get_path('manami_logo.png').encode())
    if texture is None:
        sys.exit(IMG_GetError())

    w, h = c_int(0), c_int(0)
    SDL_QueryTexture(texture, None, None, byref(w), byref(h))
    rectangle.x, rectangle.y = 0, 0
    rectangle.w, rectangle.h = w, h

    # 1.3 - SDL_MIXER
    if 0 != Mix_OpenAudio(44100, AUDIO_S16SYS, 2, 4096):
        sys.exit(Mix_GetError())

    music = Mix_LoadMUS(RESOURCES['sfx'].get_path('bg_music.ogg').encode())
    if music is None or 0 != Mix_PlayMusic(music, -1):
        sys.exit(Mix_GetError())

    # 2 - BUCLE DE JUEGO
    while gameloop:
        # 2.1 - PROCESA LA ENTRADA
        while 0 != SDL_PollEvent(byref(event)):
            if event.type == SDL_QUIT:
                gameloop = False
                break

        # 2.2 - ACTUALIZAR EL ESTADO DEL JUEGO

        # 2.3 - RENDERIZAR EL JUEGO
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, texture, None, byref(rectangle))
        SDL_RenderPresent(renderer)
        SDL_Delay(10)

        # 3 - FINALIZAR EL JUEGO
        # usamos atexit para llamar al callback que cierra todo


if __name__ == "__main__":
    main()
