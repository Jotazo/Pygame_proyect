'''
Tools for help to load some stuff
'''

import pygame as pg

import os

def load_image(path, img, x=0, y=0, rect=True):
    '''
    Function that returns image and rect.
    path = It's a "os" folder
    img = name of the image that we want to load
    x,y = If we don't change it's equals to 0, it works when we need to choose a different x,y for our rect
    rect = The rect parameter works:
        - If we want the rect of the image, we use as default True
        - If we only need to take the image, we use rect=False, then, only returns the image
    '''

    if rect:
        img = pg.image.load(os.path.join(path, img))
        rect = img.get_rect(x=x, y=y)

        return img, rect

    else:
        img = pg.image.load(os.path.join(path, img))

        return img

def draw_text(font, size, text, color, antialias=True):
    '''
    Function that returns the font and the image to render with text.
    font = We have to put the complete direction where we have the font. Ex: 'resources/fonts/xxx.ttf'
    size = The size we want to our text
    color = The color we want to our text
    antialias = For default is True, but if we want to change, we only need to specify to "False"
    '''
    text_font = pg.font.Font(font, size)
    text_font_img = text_font.render(text, antialias, color)

    return text_font, text_font_img

def load_sound(path, sound):
    '''
    Function that returns a sound loaded.
    path = It's a "os" folder
    sound = name of the sound that we want to load. Ex: 'sound.wav'
    '''

    sound = pg.mixer.Sound(os.path.join(path, sound))

    return sound