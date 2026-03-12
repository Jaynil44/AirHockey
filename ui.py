"""
UI helper module – reusable drawing primitives for the dark-neon theme.
All functions accept a pygame Surface as the first argument.
"""
import pygame
import math

# ─── cached glow surfaces ────────────────────────────────────────────────────
_glow_cache = {}


def _get_glow_surface(radius, color, intensity=6):
    """Return (and cache) a soft radial-glow surface."""
    key = (radius, color, intensity)
    if key in _glow_cache:
        return _glow_cache[key]
    size = radius * 2 + 4
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for i in range(intensity, 0, -1):
        alpha = max(10, 60 // i)
        r = int(radius * (i / intensity))
        c = (*color[:3], alpha)
        pygame.draw.circle(surf, c, (size // 2, size // 2), r)
    _glow_cache[key] = surf
    return surf


# ─── glow circle ──────────────────────────────────────────────────────────────
def draw_glow_circle(surface, color, center, radius, glow_radius=None):
    """Draw a circle with an outer soft glow."""
    if glow_radius is None:
        glow_radius = int(radius * 1.8)
    glow = _get_glow_surface(glow_radius, color)
    gx = center[0] - glow.get_width() // 2
    gy = center[1] - glow.get_height() // 2
    surface.blit(glow, (gx, gy))
    pygame.draw.circle(surface, color, center, radius)


# ─── gradient rectangle ──────────────────────────────────────────────────────
def draw_gradient_rect(surface, rect, color_top, color_bot):
    """Draw a vertical-gradient filled rectangle."""
    x, y, w, h = rect
    for row in range(h):
        t = row / max(h - 1, 1)
        r = int(color_top[0] + (color_bot[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bot[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bot[2] - color_top[2]) * t)
        pygame.draw.line(surface, (r, g, b), (x, y + row), (x + w - 1, y + row))


# ─── pill button ──────────────────────────────────────────────────────────────
def draw_pill_button(surface, rect, color, hover_color, mouse_pos, font, text,
                     text_color=(255, 255, 255)):
    """
    Draw a pill-shaped button.  Returns True if the button area contains
    mouse_pos (caller decides what to do on click).
    """
    x, y, w, h = rect
    hovered = (x <= mouse_pos[0] <= x + w) and (y <= mouse_pos[1] <= y + h)
    c = hover_color if hovered else color

    r = h // 2
    # pill shape: two semicircles + rect
    pygame.draw.circle(surface, c, (x + r, y + r), r)
    pygame.draw.circle(surface, c, (x + w - r, y + r), r)
    pygame.draw.rect(surface, c, (x + r, y, w - 2 * r, h))

    # text centered
    ts = font.render(text, True, text_color)
    tr = ts.get_rect(center=(x + w // 2, y + h // 2))
    surface.blit(ts, tr)
    return hovered


# ─── glass panel ──────────────────────────────────────────────────────────────
def draw_glass_panel(surface, rect, alpha=45, border_color=(255, 255, 255)):
    """Draw a semi-transparent frosted-glass panel with a thin border."""
    x, y, w, h = rect
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((255, 255, 255, alpha))
    surface.blit(panel, (x, y))
    pygame.draw.rect(surface, (*border_color[:3], 80), (x, y, w, h), 1, border_radius=8)


# ─── text with shadow ────────────────────────────────────────────────────────
def draw_text_shadow(surface, text, center, font, color, shadow_color=(0, 0, 0),
                     offset=2):
    """Render text with a drop-shadow for readability."""
    shadow = font.render(text, True, shadow_color)
    sr = shadow.get_rect(center=(center[0] + offset, center[1] + offset))
    surface.blit(shadow, sr)
    main = font.render(text, True, color)
    mr = main.get_rect(center=center)
    surface.blit(main, mr)


# ─── neon line ────────────────────────────────────────────────────────────────
def draw_neon_line(surface, color, start, end, width=2, glow_width=6):
    """Draw a line with a neon glow effect."""
    # glow layers
    for i in range(3, 0, -1):
        alpha = 30 // i
        glow_c = (*color[:3], alpha)
        glow_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.line(glow_surf, glow_c, start, end, width + glow_width * i)
        surface.blit(glow_surf, (0, 0))
    pygame.draw.line(surface, color, start, end, width)


# ─── neon circle (ring only) ─────────────────────────────────────────────────
def draw_neon_ring(surface, color, center, radius, width=2, glow_layers=3):
    """Draw a circle outline with neon glow."""
    for i in range(glow_layers, 0, -1):
        alpha = 35 // i
        glow_c = (*color[:3], alpha)
        glow_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, glow_c, center, radius, width + 4 * i)
        surface.blit(glow_surf, (0, 0))
    pygame.draw.circle(surface, color, center, radius, width)


# ─── dark overlay ────────────────────────────────────────────────────────────
def draw_overlay(surface, alpha=160):
    """Fill the entire surface with a dark semi-transparent overlay."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))


# ─── background gradient ─────────────────────────────────────────────────────
_bg_cache = {}

def draw_background(surface, color_top=(15, 15, 40), color_bot=(10, 10, 25)):
    """Fill the surface with a cached vertical gradient background."""
    size = surface.get_size()
    key = (size, color_top, color_bot)
    if key not in _bg_cache:
        bg = pygame.Surface(size)
        for row in range(size[1]):
            t = row / max(size[1] - 1, 1)
            r = int(color_top[0] + (color_bot[0] - color_top[0]) * t)
            g = int(color_top[1] + (color_bot[1] - color_top[1]) * t)
            b = int(color_top[2] + (color_bot[2] - color_top[2]) * t)
            pygame.draw.line(bg, (r, g, b), (0, row), (size[0] - 1, row))
        _bg_cache[key] = bg
    surface.blit(_bg_cache[key], (0, 0))
