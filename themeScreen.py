import sys
import pygame
from globals import *
from constants import *
from startScreen import disp_text
from ui import draw_background, draw_glass_panel, draw_pill_button, draw_text_shadow, draw_neon_ring


def theme_screen(screen, clock, scr_width, scr_height, music_paused):
    """Let the player pick a field accent color. Returns an (R,G,B) tuple."""
    hfont = pygame.font.SysFont("segoeui", 32, bold=True)
    bfont = pygame.font.SysFont("segoeui", 22)
    sfont = pygame.font.SysFont("segoeui", 18)

    if not music_paused:
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.1)

    selected = 0  # index into THEME_COLORS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return THEME_COLORS[selected]

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        draw_background(screen)

        draw_text_shadow(screen, "CHOOSE FIELD ACCENT", (scr_width // 2, 60),
                         hfont, NEON_CYAN)

        # ─── Color cards ─────────────────────────────────────────────
        card_w, card_h = 200, 200
        gap = 40
        total = len(THEME_COLORS) * card_w + (len(THEME_COLORS) - 1) * gap
        start_x = scr_width // 2 - total // 2

        for i, tc in enumerate(THEME_COLORS):
            cx = start_x + i * (card_w + gap)
            cy = 120

            # mini field preview
            draw_glass_panel(screen, (cx, cy, card_w, card_h), alpha=25,
                             border_color=tc if i == selected else UI_DIM)

            # draw mini field lines inside
            mx, my = cx + card_w // 2, cy + card_h // 2
            draw_neon_ring(screen, tc, (mx, my), 30, width=1, glow_layers=1)
            pygame.draw.line(screen, tc, (mx, cy + 20), (mx, cy + card_h - 20), 1)
            pygame.draw.rect(screen, tc, (cx + 10, my - 30, 30, 60), 1)
            pygame.draw.rect(screen, tc, (cx + card_w - 40, my - 30, 30, 60), 1)

            # selection ring
            if i == selected:
                pygame.draw.rect(screen, tc, (cx - 3, cy - 3, card_w + 6, card_h + 6), 3,
                                 border_radius=10)

            # click
            if (cx <= mouse[0] <= cx + card_w) and (cy <= mouse[1] <= cy + card_h):
                if click[0]:
                    selected = i

        # selected color indicator
        sel_color = THEME_COLORS[selected]
        pygame.draw.circle(screen, sel_color, (scr_width // 2, 370), 20)
        sel_label = sfont.render("Selected Accent", True, UI_DIM)
        sr = sel_label.get_rect(center=(scr_width // 2, 400))
        screen.blit(sel_label, sr)

        # START button
        bw, bh = 180, 50
        bx = scr_width // 2 - bw // 2
        by = scr_height - 110
        if draw_pill_button(screen, (bx, by, bw, bh),
                            (20, 140, 60), (30, 200, 80), mouse, hfont,
                            "START", UI_WHITE):
            if click[0]:
                return THEME_COLORS[selected]

        pygame.display.update()
        clock.tick(FPS)
