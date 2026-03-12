import sys
import pygame
from pygame.locals import *
from paddle import Paddle
from puck import Puck
from startScreen import air_hockey_start, disp_text
from themeScreen import theme_screen
from globals import *
from endScreen import game_end
from ui import (draw_background, draw_neon_ring, draw_neon_line,
                draw_overlay, draw_pill_button, draw_text_shadow,
                draw_glow_circle)
import constants as const

# Create game objects.
paddle1 = Paddle(const.PADDLE1X, const.PADDLE1Y)
paddle2 = Paddle(const.PADDLE2X, const.PADDLE2Y)
puck = Puck(width // 2, height // 2)


def init():
    global paddleHit, goal_whistle, clock, screen, smallfont, roundfont
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    gamelogo = pygame.image.load(os.path.join(auxDirectory, 'AHlogo.png'))
    pygame.display.set_icon(gamelogo)
    pygame.display.set_caption('Air Hockey')
    screen = pygame.display.set_mode((width, height))

    # Convert images now that display exists
    convert_images()

    paddleHit = pygame.mixer.Sound(os.path.join(auxDirectory, 'hit.wav'))
    goal_whistle = pygame.mixer.Sound(os.path.join(auxDirectory, 'goal.wav'))

    smallfont = pygame.font.SysFont("segoeui", 28, bold=True)
    roundfont = pygame.font.SysFont("segoeui", 38, bold=True)

    clock = pygame.time.Clock()


# ─── score HUD ───────────────────────────────────────────────────────────────
def score(score1, score2, player_1_name, player_2_name):
    # modern centered HUD bar
    bar_h = 40
    bar = pygame.Surface((width, bar_h), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 120))
    screen.blit(bar, (0, 0))

    # player 1 (left)
    t1 = smallfont.render(f"{player_1_name}  {score1}", True, const.NEON_CYAN)
    screen.blit(t1, (30, 6))

    # player 2 (right)
    t2 = smallfont.render(f"{score2}  {player_2_name}", True, const.NEON_MAGENTA)
    t2r = t2.get_rect(right=width - 30, top=6)
    screen.blit(t2, t2r)


def rounds(rounds_p1, rounds_p2, round_no):
    # centered round info in the HUD bar
    rt = smallfont.render(f"Round {round_no}", True, const.UI_WHITE)
    rr = rt.get_rect(center=(width // 2, 14))
    screen.blit(rt, rr)

    st = pygame.font.SysFont("segoeui", 20).render(f"{rounds_p1} : {rounds_p2}", True, const.UI_DIM)
    sr = st.get_rect(center=(width // 2, 36))
    screen.blit(st, sr)


# ─── end helper ──────────────────────────────────────────────────────────────
def end(option, speed):
    global rounds_p1, rounds_p2, round_no, score1, score2

    if option == 1:
        puck.end_reset(speed)
        paddle1.reset(22, height // 2)
        paddle2.reset(width - 20, height // 2)
        score1, score2 = 0, 0
        rounds_p1, rounds_p2 = 0, 0
        round_no = 1
        return False

    elif option == 2:
        return True

    else:
        sys.exit()


# ─── round change notification ───────────────────────────────────────────────
def notify_round_change():
    overlay_font = pygame.font.SysFont("segoeui", 44, bold=True)
    sub_font = pygame.font.SysFont("segoeui", 24)
    btn_font = pygame.font.SysFont("segoeui", 22, bold=True)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    return

        # darken the field
        draw_overlay(screen, alpha=180)

        draw_text_shadow(screen, f"ROUND {round_no} COMPLETE", (width // 2, height // 2 - 60),
                         overlay_font, const.NEON_CYAN)

        sc_text = sub_font.render(f"{score1}  :  {score2}", True, const.UI_WHITE)
        sr = sc_text.get_rect(center=(width // 2, height // 2))
        screen.blit(sc_text, sr)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        bw, bh = 160, 44
        bx = width // 2 - bw // 2
        by = height // 2 + 50
        if draw_pill_button(screen, (bx, by, bw, bh),
                            (20, 140, 60), (30, 200, 80), mouse, btn_font,
                            "CONTINUE", const.UI_WHITE):
            if click[0]:
                return

        hint = sub_font.render("or press SPACE", True, const.UI_DIM)
        hr = hint.get_rect(center=(width // 2, height // 2 + 120))
        screen.blit(hint, hr)

        pygame.display.flip()
        clock.tick(const.FPS)


# ─── pause screen ────────────────────────────────────────────────────────────
def show_pause_screen():
    global mute, music_paused
    overlay_font = pygame.font.SysFont("segoeui", 48, bold=True)
    btn_font = pygame.font.SysFont("segoeui", 22, bold=True)
    sfont = pygame.font.SysFont("segoeui", 18)

    while True:
        draw_overlay(screen, alpha=190)

        draw_text_shadow(screen, "PAUSED", (width // 2, height // 2 - 80),
                         overlay_font, const.UI_WHITE)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        bw, bh = 140, 44
        gap = 20
        total_w = 3 * bw + 2 * gap
        base_x = width // 2 - total_w // 2
        by = height // 2 - 10

        # CONTINUE
        if draw_pill_button(screen, (base_x, by, bw, bh),
                            (20, 120, 60), (30, 180, 80), mouse, btn_font,
                            "CONTINUE", const.UI_WHITE):
            if click[0]:
                return 1

        # RESET
        if draw_pill_button(screen, (base_x + bw + gap, by, bw, bh),
                            (160, 120, 20), (220, 170, 30), mouse, btn_font,
                            "RESET", const.UI_WHITE):
            if click[0]:
                return 2

        # EXIT
        if draw_pill_button(screen, (base_x + 2 * (bw + gap), by, bw, bh),
                            (140, 30, 30), const.NEON_RED, mouse, btn_font,
                            "EXIT", const.UI_WHITE):
            if click[0]:
                pygame.quit()
                sys.exit()

        # Mute toggle
        mute_cx = width // 2
        mute_cy = height // 2 + 70
        if mute:
            screen.blit(mute_image, (mute_cx - 16, mute_cy - 16))
        else:
            screen.blit(unmute_image, (mute_cx - 16, mute_cy - 16))
        mt = sfont.render("Toggle Sound", True, const.UI_DIM)
        mr = mt.get_rect(center=(mute_cx, mute_cy + 26))
        screen.blit(mt, mr)

        if click[0]:
            dx = mouse[0] - mute_cx
            dy = mouse[1] - mute_cy
            if dx * dx + dy * dy < 25 ** 2:
                mute = not mute

        # mute/unmute audio
        if mute and not music_paused:
            pygame.mixer.music.pause()
            music_paused = True
        elif not mute and music_paused:
            pygame.mixer.music.unpause()
            music_paused = False

        hint = sfont.render("Press SPACE to resume", True, const.UI_DIM)
        hr = hint.get_rect(center=(width // 2, height // 2 + 120))
        screen.blit(hint, hr)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 1
            if event.type == QUIT:
                sys.exit()

        pygame.display.flip()
        clock.tick(const.FPS)


# ─── pause area check ────────────────────────────────────────────────────────
def hits_pause_area(mouse_xy):
    return (abs(mouse_xy[0] - width // 2) < const.PAUSE_BUTTON_RADIUS) and \
           (abs(mouse_xy[1] - (height - 35)) < const.PAUSE_BUTTON_RADIUS)


# ─── render the playing field ────────────────────────────────────────────────
def render_field(accent_color):
    screen.fill(const.FIELD_BG)

    # Neon center circle
    draw_neon_ring(screen, accent_color, (width // 2, height // 2), 70, width=2)

    # Neon divider
    draw_neon_line(screen, accent_color, (width // 2, 0), (width // 2, height), width=2, glow_width=4)

    # Border
    pygame.draw.rect(screen, (*accent_color, 100), (0, 0, width, height), 3)

    # D-boxes
    pygame.draw.rect(screen, accent_color, (0, height // 2 - 150, 150, 300), 2)
    pygame.draw.rect(screen, accent_color, (width - 150, height // 2 - 150, 150, 300), 2)

    # Goals – brighter neon
    goal_surf = pygame.Surface((6, const.GOAL_WIDTH), pygame.SRCALPHA)
    goal_surf.fill((*const.NEON_LIME[:3], 200))
    screen.blit(goal_surf, (0, const.GOAL_Y1))
    screen.blit(goal_surf, (width - 6, const.GOAL_Y1))

    # Pause icon (bottom center)
    screen.blit(pause_image, (width // 2 - 16, height - 50))


def resetround(player):
    puck.round_reset(player)
    paddle1.reset(22, height // 2)
    paddle2.reset(width - 20, height // 2)


def reset_game(speed, player):
    puck.reset(speed, player)
    paddle1.reset(22, height // 2)
    paddle2.reset(width - 20, height // 2)


def inside_goal(side):
    if side == 0:
        return (puck.x - puck.radius <= 0) and (puck.y >= const.GOAL_Y1) and (puck.y <= const.GOAL_Y2)
    if side == 1:
        return (puck.x + puck.radius >= width) and (puck.y >= const.GOAL_Y1) and (puck.y <= const.GOAL_Y2)


# ─── GAME LOOP ───────────────────────────────────────────────────────────────
def game_loop(speed, player1_color, player2_color, accent_color, player_1_name, player_2_name):
    global rounds_p1, rounds_p2, round_no, music_paused
    rounds_p1, rounds_p2, round_no = 0, 0, 1

    pygame.mixer.music.load(os.path.join(auxDirectory, 'back.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.2)

    music_paused = False

    if mute and not music_paused:
        pygame.mixer.music.pause()
        music_paused = True

    while True:
        global score1, score2

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ch = show_pause_screen()
                if ch == 2:
                    score1 = 0
                    score2 = 0
                    rounds_p1 = 0
                    rounds_p2 = 0
                    round_no = 1
                    reset_game(speed, 1)
                    reset_game(speed, 2)
                    puck.angle = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_xy = pygame.mouse.get_pos()
                if hits_pause_area(mouse_xy):
                    ch = show_pause_screen()
                    if ch == 2:
                        score1 = 0
                        score2 = 0
                        rounds_p1 = 0
                        rounds_p2 = 0
                        round_no = 1
                        reset_game(speed, 1)
                        reset_game(speed, 2)
                        puck.angle = 0

        key_presses = pygame.key.get_pressed()

        w = key_presses[pygame.K_w]
        s = key_presses[pygame.K_s]
        d = key_presses[pygame.K_d]
        a = key_presses[pygame.K_a]

        up = key_presses[pygame.K_UP]
        down = key_presses[pygame.K_DOWN]
        right = key_presses[pygame.K_RIGHT]
        left = key_presses[pygame.K_LEFT]

        time_delta = clock.get_time() / 1000.0

        paddle1.move(w, s, a, d, time_delta)
        paddle1.check_vertical_bounds(height)
        paddle1.check_left_boundary(width)

        paddle2.move(up, down, left, right, time_delta)
        paddle2.check_vertical_bounds(height)
        paddle2.check_right_boundary(width)

        puck.move(time_delta)

        if inside_goal(0):
            if not music_paused:
                pygame.mixer.Sound.play(goal_whistle)
            score2 += 1
            reset_game(speed, 1)

        if inside_goal(1):
            if not music_paused:
                pygame.mixer.Sound.play(goal_whistle)
            score1 += 1
            reset_game(speed, 2)

        puck.check_boundary(width, height)

        if puck.collision_paddle(paddle1) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)

        if puck.collision_paddle(paddle2) and not music_paused:
            pygame.mixer.Sound.play(paddleHit)

        # round transitions
        if score1 == const.SCORE_LIMIT:
            if not rounds_p1 + 1 == const.ROUND_LIMIT:
                notify_round_change()
            round_no += 1
            rounds_p1 += 1
            score1, score2 = 0, 0
            resetround(1)

        if score2 == const.SCORE_LIMIT:
            if not rounds_p2 + 1 == const.ROUND_LIMIT:
                notify_round_change()
            round_no += 1
            rounds_p2 += 1
            score1, score2 = 0, 0
            resetround(2)

        # ─── RENDER ──────────────────────────────────────────────────
        render_field(accent_color)
        score(score1, score2, player_1_name, player_2_name)

        if rounds_p1 == const.ROUND_LIMIT:
            if end(game_end(screen, clock, accent_color, player_1_name), speed):
                if music_paused:
                    pygame.mixer.music.unpause()
                pygame.mixer.stop()
                return
        elif rounds_p2 == const.ROUND_LIMIT:
            if end(game_end(screen, clock, accent_color, player_2_name), speed):
                if music_paused:
                    pygame.mixer.music.unpause()
                pygame.mixer.stop()
                return
        else:
            rounds(rounds_p1, rounds_p2, round_no)

        paddle1.draw(screen, player1_color)
        paddle2.draw(screen, player2_color)
        puck.draw(screen)

        pygame.display.flip()
        clock.tick(const.FPS)


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    global mute
    mute = False
    init()
    while True:
        gameChoice, player1_color, player2_color, mute, player_1_name, player_2_name = air_hockey_start(
            screen, clock, width, height, mute)
        accent_color = theme_screen(screen, clock, width, height, mute)
        init()
        if gameChoice == 1:
            puck.speed = const.EASY
            game_loop(const.EASY, player1_color, player2_color, accent_color, player_1_name, player_2_name)
        elif gameChoice == 2:
            puck.speed = const.HARD
            game_loop(const.HARD, player1_color, player2_color, accent_color, player_1_name, player_2_name)
        elif gameChoice == 0:
            sys.exit()
