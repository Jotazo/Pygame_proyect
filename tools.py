import pygame as pg

import os

def load_image(path, img, x=0, y=0, rect=True):
    
    if rect:
        img = pg.image.load(os.path.join(path, img))
        rect = img.get_rect(x=x, y=y)

        return img, rect

    else:
        img = pg.image.load(os.path.join(path, img))

        return img

def draw_text(font, size, text, color, antialias=True):
    text_font = pg.font.Font(font, size)
    text_font_img = text_font.render(text, antialias, color)

    return text_font, text_font_img