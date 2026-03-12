import random
import pygame
import sys
from startScreen import disp_text
from globals import *
from constants import *
from ui import (draw_background, draw_pill_button, draw_text_shadow,
                draw_overlay, draw_glow_circle)


def game_end(screen, clock, background_color, player_name):
    """
    End-of-match screen.  Returns 1 (reset), 2 (menu), or 3 (quit).
    """
    hfont = pygame.font.SysFont("segoeui", 80, bold=True)
    bfont = pygame.font.SysFont("segoeui", 28, bold=True)
    sfont = pygame.font.SysFont("segoeui", 20)

    # Pre-generate some "star" particles
    stars = [(random.randint(0, width), random.randint(0, height),
              random.uniform(0.5, 2.5), random.choice(ACCENT_COLORS))
             for _ in range(40)]

    frame = 0

    while True:
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 1
                elif event.key == pygame.K_m:
                    return 2
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        draw_background(screen)

        # sparkle particles
        for i, (sx, sy, spd, sc) in enumerate(stars):
            sy -= spd
            if sy < -5:
                sy = height + 5
                sx = random.randint(0, width)
            stars[i] = (sx, sy, spd, sc)
            alpha = int(120 + 80 * abs(((frame + i * 7) % 60) / 30.0 - 1))
            r = 2 if spd < 1.5 else 3
            surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*sc[:3], min(alpha, 255)), (r, r), r)
            screen.blit(surf, (int(sx) - r, int(sy) - r))

        # winner text with glow
        color_cycle = ACCENT_COLORS[frame // 8 % len(ACCENT_COLORS)]
        draw_text_shadow(screen, f"{player_name.upper()} WINS!",
                         (width // 2, height // 2 - 100), hfont,
                         color_cycle, shadow_color=(0, 0, 0), offset=4)

        # sub-text
        sub = sfont.render("Press  R = Reset   M = Menu   Q = Quit", True, UI_DIM)
        sr = sub.get_rect(center=(width // 2, height // 2 - 20))
        screen.blit(sub, sr)

        # ─── Buttons ─────────────────────────────────────────────────
        bw, bh = 150, 48
        btn_y = height // 2 + 60
        gap = 30

        total_w = 3 * bw + 2 * gap
        base_x = width // 2 - total_w // 2

        # Reset
        if draw_pill_button(screen, (base_x, btn_y, bw, bh),
                            (20, 140, 60), (30, 200, 80), mouse, bfont,
                            "RESET", UI_WHITE):
            if click[0]:
                return 1

        # Menu
        if draw_pill_button(screen, (base_x + bw + gap, btn_y, bw, bh),
                            (140, 100, 20), (200, 150, 30), mouse, bfont,
                            "MENU", UI_WHITE):
            if click[0]:
                return 2

        # Quit
        if draw_pill_button(screen, (base_x + 2 * (bw + gap), btn_y, bw, bh),
                            (140, 30, 30), NEON_RED, mouse, bfont,
                            "QUIT", UI_WHITE):
            if click[0]:
                pygame.quit()
                return 3

        pygame.display.update()
        clock.tick(FPS)
