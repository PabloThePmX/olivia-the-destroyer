import pygame as pg

def draw_speech_bubble(screen, text, text_colour, bg_colour, pos, size):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, text_colour)
    text_rect = text_surface.get_rect(midbottom=pos)

    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(10,10)

    frame_rect = bg_rect.copy()
    frame_rect.inflate_ip(4,4)

    pg.draw.rect(screen, text_colour, frame_rect)
    pg.draw.rect(screen, bg_colour, bg_rect)
    screen.blit(text_surface, text_rect)