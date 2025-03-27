import json
from datetime import datetime
from threading import Thread

import pygame

from score_render import ASSETS_DIR
from score_render.elements import TextBox, AnimationPNG  # Assuming the class is saved in `textbox.py`
from score_render.elements.text_box import TextShadow
from score_render.ingest import WebSocketHandler

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)


def on_message(message, state):
    """
    Callback function to handle incoming WebSocket messages.

    Args:
        message (str): The message received from the WebSocket server.
        state (dict): Shared state for the game.
    """
    print(f"Received message: {message}")
    # Update state with the new data
    try:
        state['msg'] = json.loads(message)
        state['time'] = datetime.now()
    except Exception as e:
        print(f"Error parsing message: {e}")


def main():
    SCREEN_WIDTH = 274
    SCREEN_HEIGHT = 226

    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AFC Score Renderer")

    # shadow_outline = TextShadow((0, 0, 0), 2, (1, 1))
    # shadow_drop = TextShadow((0, 102, 255), 3, (3, 3))
    # shadow_drop2 = TextShadow((0, 0, 0), 4, (4, 4))

    shadow_outline = TextShadow((0, 0, 0), 2, (1, 1))
    shadow_drop = TextShadow((235, 170, 90), 3, (3, 3))
    shadow_drop2 = TextShadow((255, 255, 255), 4, (4, 4))

    # Create text boxes with effects
    font = 'ChangaOne-Italic.ttf'
    font = 'ChangaOne-Regular.ttf'
    text1 = TextBox(
        "text1",
        font=ASSETS_DIR / 'fonts' / font,
        font_size=72,
        color=(255, 255, 255),
        bg_color=None,
        anchor="topleft",
        shadow=[shadow_drop2, shadow_drop, shadow_outline]
    )

    text2 = TextBox(
        "text1",
        font=ASSETS_DIR / 'fonts' / font,
        font_size=72,
        color=(255, 255, 255),
        bg_color=None,
        anchor="bottomright",
        shadow=[shadow_drop2, shadow_drop, shadow_outline]
    )

    text3 = TextBox(
        "text3",
        font=ASSETS_DIR / 'fonts' / font,
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
        font=ASSETS_DIR / 'fonts' / font,
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

    # Set positions
    text1.set_position(3, 3)
    text2.set_position(SCREEN_WIDTH-6, SCREEN_HEIGHT-6)
    text3.set_position(3, 40)
    text4.set_position(SCREEN_WIDTH-6, 125)

    # WebSocket setup
    state = dict(msg=None, time=None)
    websocket_uri = "ws://localhost:9000"
    websocket_handler = WebSocketHandler(
        websocket_uri, lambda msg: on_message(msg, state)
    )

    # Start WebSocket handler in a separate thread
    websocket_thread = Thread(target=websocket_handler.start)
    websocket_thread.daemon = True
    websocket_thread.start()

    # Main loop
    running = True
    clock = pygame.time.Clock()
    counter = 0
    FPS = 30

    USE_EX_SCORE = False

    try:
        while running:

            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(BLACK)

            msg = state['msg']

            if msg is not None:
                if msg['state'] == 'song_playing':
                    if USE_EX_SCORE and msg['song'] is None:
                        continue


                    p1_max_score = 1000000
                    p2_max_score = 1000000

                    if USE_EX_SCORE:
                        p1_info = msg['song']['p1_info']
                        p2_info = msg['song']['p2_info']
                        if p1_info is not None:
                            p1_max_score = p1_info['max_ex_score']

                        if p2_info is not None:
                            p2_max_score = p2_info['max_ex_score']

                    score = msg.get('score', None)
                    if score is not None:
                        p1_score = score.get('p1_score', None)
                        p2_score = score.get('p2_score', None)

                    if p1_score is not None and p2_score is not None:
                        p1_score = max(0, p1_score)
                        p2_score = max(0, p2_score)
                        diff = p1_score - p2_score
                        # text1.set_text(f"{100 * (p1_score / p1_max_score):.2f}%")
                        # text2.set_text(f"{100 * (p2_score / p2_max_score):.2f}%")
                        text1.set_text(f"{p1_score}")
                        text2.set_text(f"{p2_score}")
                        text1.draw(screen)
                        text2.draw(screen)

                        # p1 winning
                        if diff > 0:
                            text3.set_text(f"+{diff}")
                            text4.set_text(f"None")
                            text3.draw(screen)
                        elif diff < 0:
                            text3.set_text(f"None")
                            text4.set_text(f"+{-diff}")
                            text4.draw(screen)
                        else:
                            text3.set_text(f"None")
                            text3.set_text(f"None")

                    # Only P1 is playing
                    elif p1_score is not None:
                        p1_score = max(0, p1_score)
                        text1.set_text(f"{100 * (p1_score / p1_max_score):.2f}%")
                        text3.set_text(f"+{p1_score}")
                        text1.draw(screen)
                        text3.draw(screen)

                    elif p2_score is not None:
                        p2_score = max(0, p2_score)
                        text2.set_text(f"{100 * (p2_score / p2_max_score):.2f}%")
                        text4.set_text(f"+{p2_score}")
                        text2.draw(screen)
                        text4.draw(screen)
                    else:
                        # Not sure how we'd get here, but it's late and I'd rather it not crash one day
                        print('Managed to make it to p1 and p2 scores being None...?')
                        continue

                # Update display
            pygame.display.flip()
    finally:
        print('Shutting down...')
        websocket_handler.stop()
        pygame.quit()


if __name__ == "__main__":
    main()
