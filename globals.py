import constants as const
import pygame
import os

auxDirectory = os.path.join(os.path.dirname(__file__), 'assets')

smallfont = None
score1, score2 = 0, 0

# Sound globals.
paddleHit = None
goal_whistle = None
backgroundMusic = None

# Images – loaded here, but .convert_alpha() called after display init
_raw_mute   = pygame.image.load(os.path.join(auxDirectory, 'mute.png'))
_raw_unmute = pygame.image.load(os.path.join(auxDirectory, 'unmute.png'))
_raw_play   = pygame.image.load(os.path.join(auxDirectory, 'play.png'))
_raw_pause  = pygame.image.load(os.path.join(auxDirectory, 'pause.png'))
_raw_info   = pygame.image.load(os.path.join(auxDirectory, 'info.png'))

# Optimised copies (set in convert_images())
mute_image = _raw_mute
unmute_image = _raw_unmute
play_image = _raw_play
pause_image = _raw_pause
info_image = _raw_info


def convert_images():
    """Call AFTER pygame.display.set_mode() to .convert_alpha() all images."""
    global mute_image, unmute_image, play_image, pause_image, info_image
    mute_image   = _raw_mute.convert_alpha()
    unmute_image = _raw_unmute.convert_alpha()
    play_image   = _raw_play.convert_alpha()
    pause_image  = _raw_pause.convert_alpha()
    info_image   = _raw_info.convert_alpha()


# game globals.
clock = None
screen = None

# width and height of the screen.
width, height = const.WIDTH, const.HEIGHT

# ─── Fonts (initialised in main.init()) ─────────────────────────────────────
title_font = None
heading_font = None
body_font = None
small_font = None
