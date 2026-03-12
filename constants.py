""" All sizes in pixels and speeds in pixels per second """
FPS = 60

# Screen size
HEIGHT = 600
WIDTH = 1200

# Paddle
PADDLE_SIZE = 40
PADDLE_SPEED = 400
PADDLE_MASS = 2000

# Paddle 1 start position.
PADDLE1X = 20
PADDLE1Y = HEIGHT // 2

# Paddle 2 start position.
PADDLE2X = WIDTH - 20
PADDLE2Y = HEIGHT // 2

# Puck
PUCK_SIZE = 30
PUCK_SPEED = 450
PUCK_MASS = 500

# Goal Position
GOAL_WIDTH = 180
GOAL_Y1 = HEIGHT // 2 - GOAL_WIDTH // 2
GOAL_Y2 = HEIGHT // 2 + GOAL_WIDTH // 2

# Speed levels
EASY = 450
MEDIUM = 650
HARD = 850

# color (legacy)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ─── NEW: Dark-neon palette ──────────────────────────────────────────────────
BG_TOP        = (15, 15, 40)
BG_BOT        = (10, 10, 25)
FIELD_BG      = (12, 12, 30)

NEON_CYAN     = (0, 230, 255)
NEON_MAGENTA  = (255, 0, 180)
NEON_LIME     = (80, 255, 80)
NEON_ORANGE   = (255, 160, 40)
NEON_RED      = (255, 60, 60)

UI_WHITE      = (230, 230, 240)
UI_DIM        = (120, 120, 140)
UI_DARK       = (30, 30, 50)

# Accent colors for paddle choices (brighter, works on dark bg)
ACCENT_COLORS = [
    NEON_CYAN,
    NEON_MAGENTA,
    NEON_LIME,
    NEON_ORANGE,
    NEON_RED,
]

# Theme / field accent colors
THEME_COLORS = [
    (0, 200, 220),    # Teal
    (100, 80, 220),   # Purple
    (220, 60, 100),   # Rose
    (60, 200, 120),   # Emerald
]

# Scoring
SCORE_LIMIT = 5
ROUND_LIMIT = 2

# Environment
FRICTION = 0.998
MAX_SPEED = 1500

# mute button
MUTE_BUTTON_RADIUS = 32

# pause button
PAUSE_BUTTON_RADIUS = 32

# info button
INFO_BUTTON_RADIUS = 32
