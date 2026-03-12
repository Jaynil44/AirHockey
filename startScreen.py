import sys
import random
import pygame
from globals import *
from constants import *
from ui import (draw_background, draw_glass_panel, draw_pill_button,
                draw_text_shadow, draw_glow_circle, draw_neon_ring)


def text_obj(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def disp_text(screen, text, center, font, color):
    text_surf, text_rect = text_obj(text, font, color)
    text_rect.center = center
    screen.blit(text_surf, text_rect)


# ─── Help screen ─────────────────────────────────────────────────────────────
def show_info(screen, scr_width, clock):
    hfont = pygame.font.SysFont("segoeui", 32, bold=True)
    bfont = pygame.font.SysFont("segoeui", 22)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        draw_background(screen)

        draw_text_shadow(screen, "HOW TO PLAY", (scr_width // 2, 60), hfont, NEON_CYAN)

        lines = [
            "CONTROLS:",
            "  Player 1 →  W  A  S  D         Player 2 →  Arrow keys",
            "",
            "1. Click player name fields to type a name.",
            "2. Choose each player's paddle color.",
            "3. Select difficulty to start.",
            "4. First to 5 goals wins a round. Best of 3 rounds.",
            "5. Press SPACE or click ⏸  to pause anytime.",
        ]
        y = 120
        for line in lines:
            txt = bfont.render(line, True, UI_WHITE)
            screen.blit(txt, (100, y))
            y += 36

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        bw, bh = 120, 40
        bx = scr_width // 2 - bw // 2
        by = height - 80
        if draw_pill_button(screen, (bx, by, bw, bh), (0, 160, 200), NEON_CYAN,
                            mouse, bfont, "BACK", BLACK):
            if click[0]:
                return

        pygame.display.flip()
        clock.tick(FPS)


# ─── Start screen ────────────────────────────────────────────────────────────
def air_hockey_start(screen, clock, scr_width, scr_height, mute):
    pygame.mixer.music.load(os.path.join(auxDirectory, 'StartScreenBack.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.1)

    # ─ state ─
    p1_idx = 0
    p2_idx = 1
    player_1_name = ""
    player_2_name = ""
    editing_p1 = False
    editing_p2 = False
    player_1_key = False
    music_paused = False

    # ─ fonts (cached) ─
    tfont  = pygame.font.SysFont("segoeui", 60, bold=True)
    hfont  = pygame.font.SysFont("segoeui", 26, bold=True)
    bfont  = pygame.font.SysFont("segoeui", 24)
    sfont  = pygame.font.SysFont("segoeui", 18)

    blink_timer = 0

    while True:
        dt = clock.tick(FPS)
        blink_timer = (blink_timer + dt) % 1000
        blink_on = blink_timer < 500

        # ─── events ─────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and not editing_p1 and not editing_p2:
                    pygame.quit(); sys.exit()

                # typing into name fields
                if editing_p1:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        editing_p1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_1_name = player_1_name[:-1]
                    elif event.unicode.isalnum() and len(player_1_name) < 10:
                        player_1_name += event.unicode
                    continue

                if editing_p2:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        editing_p2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_2_name = player_2_name[:-1]
                    elif event.unicode.isalnum() and len(player_2_name) < 10:
                        player_2_name += event.unicode
                    continue

                # color cycle
                if event.key == pygame.K_a:
                    p1_idx = (p1_idx - 1) % len(ACCENT_COLORS)
                elif event.key == pygame.K_d:
                    p1_idx = (p1_idx + 1) % len(ACCENT_COLORS)
                elif event.key == pygame.K_LEFT:
                    p2_idx = (p2_idx - 1) % len(ACCENT_COLORS)
                elif event.key == pygame.K_RIGHT:
                    p2_idx = (p2_idx + 1) % len(ACCENT_COLORS)
                elif event.key == pygame.K_e:
                    n1 = player_1_name or "Player 1"
                    n2 = player_2_name or "Player 2"
                    _stop_music(music_paused)
                    return 1, ACCENT_COLORS[p1_idx], ACCENT_COLORS[p2_idx], mute, n1, n2
                elif event.key == pygame.K_h:
                    n1 = player_1_name or "Player 1"
                    n2 = player_2_name or "Player 2"
                    _stop_music(music_paused)
                    return 2, ACCENT_COLORS[p1_idx], ACCENT_COLORS[p2_idx], mute, n1, n2

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # name field click detection
                p1_box = (scr_width // 4 - 140, 200, 280, 44)
                p2_box = (3 * scr_width // 4 - 140, 200, 280, 44)
                if p1_box[0] <= mx <= p1_box[0] + p1_box[2] and p1_box[1] <= my <= p1_box[1] + p1_box[3]:
                    editing_p1 = True; editing_p2 = False
                elif p2_box[0] <= mx <= p2_box[0] + p2_box[2] and p2_box[1] <= my <= p2_box[1] + p2_box[3]:
                    editing_p2 = True; editing_p1 = False
                else:
                    editing_p1 = False; editing_p2 = False

        # ─── mute logic ─────────────────────────────────────────────
        if mute and not music_paused:
            pygame.mixer.music.pause(); music_paused = True
        elif not mute and music_paused:
            pygame.mixer.music.unpause(); music_paused = False

        # ─── draw ────────────────────────────────────────────────────
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        draw_background(screen)

        # Title
        draw_text_shadow(screen, "AIR HOCKEY", (scr_width // 2, 80), tfont,
                         NEON_CYAN, shadow_color=(0, 80, 120), offset=3)

        # ─── Player cards ────────────────────────────────────────────
        card_w, card_h = 320, 260
        p1_cx = scr_width // 4
        p2_cx = 3 * scr_width // 4

        for pidx, (cx, p_name, p_color_idx, is_editing) in enumerate([
            (p1_cx, player_1_name, p1_idx, editing_p1),
            (p2_cx, player_2_name, p2_idx, editing_p2),
        ]):
            lx = cx - card_w // 2
            ly = 140
            draw_glass_panel(screen, (lx, ly, card_w, card_h), alpha=30,
                             border_color=ACCENT_COLORS[p_color_idx])

            # label
            label = f"PLAYER {pidx + 1}"
            draw_text_shadow(screen, label, (cx, ly + 30), hfont, UI_WHITE)

            # name field
            fx, fy, fw, fh = cx - 140, ly + 55, 280, 44
            border_c = NEON_CYAN if is_editing else UI_DIM
            pygame.draw.rect(screen, (20, 20, 40), (fx, fy, fw, fh), border_radius=6)
            pygame.draw.rect(screen, border_c, (fx, fy, fw, fh), 2, border_radius=6)

            display_name = p_name
            if is_editing:
                display_name = p_name + ("|" if blink_on else "")
            if not display_name:
                # placeholder
                ph = sfont.render("Click to type name...", True, UI_DIM)
                screen.blit(ph, (fx + 10, fy + 12))
            else:
                nt = bfont.render(display_name, True, UI_WHITE)
                screen.blit(nt, (fx + 10, fy + 9))

            # color swatches
            swatch_y = ly + 135
            total_w = len(ACCENT_COLORS) * 40 + (len(ACCENT_COLORS) - 1) * 12
            start_x = cx - total_w // 2 + 20
            for ci, ac in enumerate(ACCENT_COLORS):
                sx = start_x + ci * 52
                if ci == p_color_idx:
                    draw_neon_ring(screen, ac, (sx, swatch_y), 22, width=2, glow_layers=2)
                pygame.draw.circle(screen, ac, (sx, swatch_y), 16)
                # click detection
                if click[0]:
                    dx = mouse[0] - sx
                    dy = mouse[1] - swatch_y
                    if dx * dx + dy * dy < 20 * 20:
                        if pidx == 0:
                            p1_idx = ci
                        else:
                            p2_idx = ci

            # selected label
            sel_text = sfont.render("A / D to cycle" if pidx == 0 else "← / → to cycle",
                                   True, UI_DIM)
            sr = sel_text.get_rect(center=(cx, swatch_y + 40))
            screen.blit(sel_text, sr)

            # preview paddle
            preview_color = ACCENT_COLORS[p_color_idx]
            draw_glow_circle(screen, preview_color, (cx, ly + 220), 18,
                             glow_radius=30)

        # ─── Difficulty buttons ──────────────────────────────────────
        btn_w, btn_h = 160, 50
        btn_y = scr_height - 120

        # Easy
        easy_x = scr_width // 2 - btn_w - 30
        easy_hover = draw_pill_button(screen, (easy_x, btn_y, btn_w, btn_h),
                                      (20, 140, 60), (30, 200, 80), mouse, hfont,
                                      "EASY", UI_WHITE)
        if easy_hover and click[0]:
            n1 = player_1_name or "Player 1"
            n2 = player_2_name or "Player 2"
            _stop_music(music_paused)
            return 1, ACCENT_COLORS[p1_idx], ACCENT_COLORS[p2_idx], mute, n1, n2

        # Hard
        hard_x = scr_width // 2 + 30
        hard_hover = draw_pill_button(screen, (hard_x, btn_y, btn_w, btn_h),
                                      (180, 50, 20), (240, 80, 30), mouse, hfont,
                                      "HARD", UI_WHITE)
        if hard_hover and click[0]:
            n1 = player_1_name or "Player 1"
            n2 = player_2_name or "Player 2"
            _stop_music(music_paused)
            return 2, ACCENT_COLORS[p1_idx], ACCENT_COLORS[p2_idx], mute, n1, n2

        # ─── Quit button (bottom right) ─────────────────────────────
        quit_w, quit_h = 100, 38
        quit_x = scr_width - quit_w - 30
        quit_y_pos = scr_height - 55
        quit_hover = draw_pill_button(screen, (quit_x, quit_y_pos, quit_w, quit_h),
                                      (120, 30, 30), NEON_RED, mouse, sfont,
                                      "QUIT", UI_WHITE)
        if quit_hover and click[0]:
            pygame.quit(); sys.exit()

        # ─── Info button (bottom left) ───────────────────────────────
        info_r = 18
        info_cx, info_cy = 40, scr_height - 36
        pygame.draw.circle(screen, UI_DIM, (info_cx, info_cy), info_r, 2)
        it = sfont.render("?", True, UI_WHITE)
        ir = it.get_rect(center=(info_cx, info_cy))
        screen.blit(it, ir)
        if click[0]:
            dx = mouse[0] - info_cx
            dy = mouse[1] - info_cy
            if dx * dx + dy * dy < (info_r + 5) ** 2:
                show_info(screen, scr_width, clock)

        # ─── Mute button (top right) ─────────────────────────────────
        mute_cx = scr_width - 40
        mute_cy = 36
        if mute:
            screen.blit(mute_image, (mute_cx - 16, mute_cy - 16))
        else:
            screen.blit(unmute_image, (mute_cx - 16, mute_cy - 16))
        if click[0]:
            dx = mouse[0] - mute_cx
            dy = mouse[1] - mute_cy
            if dx * dx + dy * dy < MUTE_BUTTON_RADIUS ** 2:
                mute = not mute

        pygame.display.flip()


def _stop_music(was_paused):
    if was_paused:
        pygame.mixer.music.unpause()
    pygame.mixer.music.stop()
