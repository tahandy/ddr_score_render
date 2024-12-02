import numpy as np
import pygame

from score_render import ASSETS_DIR
from score_render.elements import TextBox, AnimationPNG  # Assuming the class is saved in `textbox.py`
from score_render.elements.text_box import TextShadow

pygame.init()

# Screen setup
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 162
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TextBox with Outline and Shadow")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

shadow_outline = TextShadow((0, 0, 0), 2, (1, 1))
shadow_drop = TextShadow((0, 102, 255), 3, (3, 3))
shadow_drop2 = TextShadow((0, 0, 0), 4, (4, 4))

# Create text boxes with effects
text1 = TextBox(
    "text1",
    font=ASSETS_DIR / 'fonts' / 'ChangaOne-Italic.ttf',
    font_size=42,
    color=(255, 255, 255),
    bg_color=None,
    anchor="topleft",
    shadow=[shadow_drop2, shadow_drop, shadow_outline]
)


text2 = TextBox(
    "text1",
    font=ASSETS_DIR / 'fonts' / 'ChangaOne-Italic.ttf',
    font_size=42,
    color=(255, 255, 255),
    bg_color=None,
    anchor="bottomright",
    shadow=[shadow_drop2, shadow_drop, shadow_outline]
)

# text2 = TextBox(
#     "text2",
#     font_size=36,
#     color=(0, 0, 255),
#     bg_color=(200, 200, 200),
#     anchor="topleft",
#     outline_color=(0, 255, 0),  # Green outline
#     shadow_color=(50, 50, 50),  # Dark shadow
#     shadow_offset=(3, 3)
# )

text3 = TextBox(
    "text3",
    font=ASSETS_DIR / 'fonts' / 'ChangaOne-Italic.ttf',
    font_size=48,
    color=(0, 255, 0),
    bg_color=None,
    anchor="topleft",
    shadow=[
        TextShadow((0, 0, 0), 1, (1, 1)),
        TextShadow((0, 102, 255), 3, (2, 2)),
        TextShadow((0, 0, 0), 1, (1, 1)),

        # TextShadow((0, 0, 0), 3, (2, 2))
    ]
)

text4 = TextBox(
    "text4",
    font=ASSETS_DIR / 'fonts' / 'ChangaOne-Italic.ttf',
    font_size=48,
    color=(0, 255, 0),
    bg_color=None,
    anchor="bottomright",
    shadow=[
        TextShadow((0, 0, 0), 1, (1, 1)),
        TextShadow((0, 102, 255), 3, (2, 2)),
        TextShadow((0, 0, 0), 2, (1, 1)),
    ]
)

fireball = AnimationPNG(ASSETS_DIR / 'graphics' / 'fireballs' / 'PNGS' / 'type_01' / 'blue',
                        duration=0.5,
                        interpolation_frames=5,
                        scale_to=(SCREEN_WIDTH, SCREEN_HEIGHT),
                        maintain_aspect_ratio = True)

# Set positions
# text1.set_position(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 75)
# text2.set_position(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 75)
# text3.set_position(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 25)
# text4.set_position(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 25)
text1.set_position(3, 3)
text2.set_position(SCREEN_WIDTH-6, SCREEN_HEIGHT-6)
text3.set_position(3, 40)
text4.set_position(SCREEN_WIDTH-6, 125)

# Main loop
running = True
clock = pygame.time.Clock()
counter = 0
FPS = 30


while running:

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update text dynamically
    counter += 1
    # if counter % 60 == 0:  # Change text every second
    max_score = counter
    text1.set_text(f"{100 * (counter / max_score):.2f}%")
    text2.set_text(f"{100 * (counter / max_score):.2f}%")
    text3.set_text(f"+{1000}")
    text4.set_text(f"+{1000}")

    # Clear the screen
    screen.fill(RED)

    # Draw text boxes
    text1.draw(screen)
    text2.draw(screen)
    text3.draw(screen)
    text4.draw(screen)

    # # Update fireball
    # fireball.update(dt)
    # period = 4
    # amp = 100
    # x = 100 * np.sin(2 * np.pi * counter / FPS / period)
    # fireball.draw(screen, (SCREEN_WIDTH//2 + x, SCREEN_HEIGHT//2))


    # Update display
    pygame.display.flip()

pygame.quit()
