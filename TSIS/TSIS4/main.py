import pygame
import sys
from config import WIDTH, HEIGHT, load_settings, save_settings
from db import create_tables, save_session, get_top_10, get_personal_best
from game import SnakeGame

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 - Database Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 15)

def draw_text(text, x, y, center=True, color=(255, 255, 255), small=False):
    f = font_small if small else font
    txt = f.render(text, True, color)
    rect = txt.get_rect(center=(x, y)) if center else txt.get_rect(topleft=(x, y))
    screen.blit(txt, rect)

def draw_button(text, x, y, w, h, color=(70, 70, 70)):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=6)
    draw_text(text, x + w // 2, y + h // 2)
    return rect

# ─── MAIN MENU ───────────────────────────────────────────────────────────────
def main_menu():
    username = ""
    input_active = True  # active by default so user can type immediately

    while True:
        screen.fill((20, 20, 20))
        draw_text("🐍 TSIS 4 SNAKE", WIDTH // 2, 40, color=(0, 255, 0))
        draw_text("Enter Username:", WIDTH // 2, 90)

        input_rect = pygame.Rect(WIDTH // 2 - 110, 108, 220, 36)
        pygame.draw.rect(screen, (40, 40, 40), input_rect, border_radius=4)
        border_color = (0, 220, 0) if input_active else (120, 120, 120)
        pygame.draw.rect(screen, border_color, input_rect, 2, border_radius=4)
        draw_text(username + ("|" if input_active else ""), WIDTH // 2, 126)

        play_btn = draw_button("▶  Play",       WIDTH // 2 - 100, 170, 200, 42)
        lead_btn = draw_button("🏆  Leaderboard", WIDTH // 2 - 100, 228, 200, 42)
        set_btn  = draw_button("⚙  Settings",   WIDTH // 2 - 100, 286, 200, 42)
        quit_btn = draw_button("✕  Quit",        WIDTH // 2 - 100, 344, 200, 42, color=(100, 30, 30))

        draw_text("Press Enter to play", WIDTH // 2, 400, color=(100, 100, 100), small=True)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(e.pos):
                    input_active = True
                else:
                    input_active = False
                if play_btn.collidepoint(e.pos) and username.strip():
                    return "PLAY", username.strip()
                if lead_btn.collidepoint(e.pos):
                    return "LEADERBOARD", username
                if set_btn.collidepoint(e.pos):
                    return "SETTINGS", username
                if quit_btn.collidepoint(e.pos):
                    sys.exit()

            if e.type == pygame.KEYDOWN:
                input_active = True
                if e.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif e.key == pygame.K_RETURN:
                    if username.strip():
                        return "PLAY", username.strip()
                elif len(username) < 15:
                    username += e.unicode

        pygame.display.flip()
        clock.tick(60)

# ─── LEADERBOARD ─────────────────────────────────────────────────────────────
def leaderboard_screen():
    try:
        top_10 = get_top_10()
    except Exception as e:
        top_10 = []
        print("DB Error:", e)

    while True:
        screen.fill((20, 20, 20))
        draw_text("🏆  TOP 10 LEADERBOARD", WIDTH // 2, 28, color=(255, 215, 0))

        # Header
        draw_text("#   Player          Score   Lv   Date", WIDTH // 2, 58, color=(180, 180, 180), small=True)
        pygame.draw.line(screen, (80, 80, 80), (20, 70), (WIDTH - 20, 70))

        y = 82
        for i, row in enumerate(top_10):
            username, score, level, played_at = row
            date_str = played_at.strftime("%d/%m/%y") if played_at else "—"
            line = f"{i+1:<4}{username:<16}{score:<8}{level:<5}{date_str}"
            color = (255, 215, 0) if i == 0 else (255, 255, 255)
            draw_text(line, WIDTH // 2, y, color=color, small=True)
            y += 22

        if not top_10:
            draw_text("No scores yet. Play a game!", WIDTH // 2, 160, color=(120, 120, 120))

        back_btn = draw_button("← Back", WIDTH // 2 - 80, 348, 160, 40)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and back_btn.collidepoint(e.pos):
                return
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                return

        pygame.display.flip()
        clock.tick(60)

# ─── SETTINGS ────────────────────────────────────────────────────────────────
def settings_screen():
    settings = load_settings()
    color_options = [(0, 255, 0), (0, 100, 255), (255, 0, 255), (255, 165, 0), (255, 255, 255)]
    color_names   = ["Green", "Blue", "Pink", "Orange", "White"]
    try:
        c_idx = color_options.index(settings["snake_color"])
    except ValueError:
        c_idx = 0

    while True:
        screen.fill((20, 20, 20))
        draw_text("⚙  SETTINGS", WIDTH // 2, 40, color=(200, 200, 255))

        grid_btn  = draw_button(
            f"Grid Overlay:  {'ON ✓' if settings['grid_overlay'] else 'OFF'}",
            WIDTH // 2 - 130, 100, 260, 42
        )
        sound_btn = draw_button(
            f"Sound:  {'ON ✓' if settings['sound'] else 'OFF'}",
            WIDTH // 2 - 130, 158, 260, 42
        )

        # Color preview
        preview_color = color_options[c_idx]
        pygame.draw.rect(screen, preview_color, (WIDTH // 2 - 130, 216, 36, 36), border_radius=4)
        col_btn = draw_button(
            f"Snake Color:  {color_names[c_idx]}",
            WIDTH // 2 - 88, 216, 218, 36
        )

        back_btn = draw_button("💾  Save & Back", WIDTH // 2 - 100, 300, 200, 42, color=(30, 80, 30))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(e.pos):
                    settings["grid_overlay"] = not settings["grid_overlay"]
                if sound_btn.collidepoint(e.pos):
                    settings["sound"] = not settings["sound"]
                if col_btn.collidepoint(e.pos):
                    c_idx = (c_idx + 1) % len(color_options)
                    settings["snake_color"] = color_options[c_idx]
                if back_btn.collidepoint(e.pos):
                    save_settings(settings)
                    return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                save_settings(settings)
                return

        pygame.display.flip()
        clock.tick(60)

# ─── GAME LOOP ───────────────────────────────────────────────────────────────
def run_game_loop(username):
    try:
        pb = get_personal_best(username)
    except Exception as e:
        print(f"DB ERROR getting PB: {e}")
        pb = 0

    game = SnakeGame(username, pb)

    while not game.game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP    and game.dy != 1:  game.ndx, game.ndy = 0, -1
                elif e.key == pygame.K_DOWN  and game.dy != -1: game.ndx, game.ndy = 0, 1
                elif e.key == pygame.K_LEFT  and game.dx != 1:  game.ndx, game.ndy = -1, 0
                elif e.key == pygame.K_RIGHT and game.dx != -1: game.ndx, game.ndy = 1, 0
                elif e.key == pygame.K_ESCAPE:
                    return "MENU"

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(game.get_speed())

    # Auto-save result
    try:
        save_session(username, game.sc, game.lvl)
        new_pb = get_personal_best(username)
    except Exception as e:
        print("Could not save to DB:", e)
        new_pb = max(pb, game.sc)

    is_new_pb = game.sc >= pb and game.sc > 0

    # ── Game Over Screen ──
    while True:
        screen.fill((40, 0, 0))
        draw_text("GAME OVER", WIDTH // 2, 80, color=(255, 50, 50))
        draw_text(f"Score: {game.sc}    Level: {game.lvl}", WIDTH // 2, 135)
        draw_text(f"Personal Best: {new_pb}", WIDTH // 2, 170,
                  color=(255, 215, 0) if is_new_pb else (200, 200, 200))
        if is_new_pb:
            draw_text("🎉 New Personal Best!", WIDTH // 2, 205, color=(255, 215, 0))

        retry_btn = draw_button("↺  Retry",     WIDTH // 2 - 105, 250, 200, 42, color=(30, 80, 30))
        menu_btn  = draw_button("⌂  Main Menu", WIDTH // 2 - 105, 308, 200, 42)

        draw_text("R = Retry   ESC = Menu", WIDTH // 2, 370, color=(90, 90, 90), small=True)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(e.pos): return "RETRY"
                if menu_btn.collidepoint(e.pos):  return "MENU"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:      return "RETRY"
                if e.key == pygame.K_ESCAPE: return "MENU"

        pygame.display.flip()
        clock.tick(60)

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    # Auto-create DB tables on startup (safe if already exist)
    try:
        create_tables()
    except Exception as e:
        print(f"Warning: Could not connect to DB: {e}")
        print("Game will run without saving scores.")

    state = "MENU"
    username = ""

    while True:
        if state == "MENU":
            res, username = main_menu()
            state = res
        elif state == "LEADERBOARD":
            leaderboard_screen()
            state = "MENU"
        elif state == "SETTINGS":
            settings_screen()
            state = "MENU"
        elif state in ("PLAY", "RETRY"):
            res = run_game_loop(username)
            state = "PLAY" if res == "RETRY" else "MENU"

if __name__ == "__main__":
    main()