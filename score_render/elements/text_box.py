import pygame

class TextShadow:
    def __init__(self, color, thickness=5, offset=(0, 0)):
        """
        Text shadow parameters

        Args:
            shadow_color (tuple): RGB color for the drop shadow. If None, no shadow is drawn.
            shadow_thickness (int): Thickness of the shadow in pixels.
            shadow_offset (tuple): Offset of the shadow in pixels, positive shifts right/down
        """
        self.color = color
        self.thickness = thickness
        self.offset = offset


class TextBox:
    def __init__(self, text, font=None, font_size=36, color=(0, 0, 0), bg_color=None, anchor="topleft", padding=10, shadow=None):
        """
        Initialize a TextBox object with anchor-based positioning.

        Args:
            text (str): Initial text to display in the text box.
            font (str): Path to the font file. If None, the default font is used.
            font_size (int): Size of the font.
            color (tuple): RGB color for the text.
            bg_color (tuple): RGB color for the background of the text box. If None, no background is drawn.
            anchor (str): Anchor point for positioning (e.g., 'topleft', 'center', 'topright', etc.).
            padding (int): Padding around the text inside the text box.
            shadow (TextShadow, list[TextShadow]): TextShadow objects defining the shadow of the text box.
        """
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.padding = padding
        self.anchor = anchor

        if shadow is not None:
            self.shadows = shadow if isinstance(shadow, (tuple, list)) else [shadow]
        else:
            self.shadows = []

        # Load font
        self.font = pygame.font.Font(font, font_size)

        # Render text and set initial rectangle
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()

        # Store the initial position (will be updated with `set_position`)
        self.position = (0, 0)

    def set_text(self, text):
        """
        Update the text displayed in the text box.

        Args:
            text (str): New text to display.
        """
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)
        previous_anchor_position = getattr(self.rect, self.anchor)  # Get the current anchor position
        self.rect = self.text_surface.get_rect()  # Update the rect with new text size
        setattr(self.rect, self.anchor, previous_anchor_position)  # Reapply the anchor position

    def set_position(self, x, y):
        """
        Set the position of the text box based on its anchor.

        Args:
            x (int): X-coordinate of the anchor position.
            y (int): Y-coordinate of the anchor position.
        """
        self.position = (x, y)
        setattr(self.rect, self.anchor, self.position)

    def draw(self, screen):
        """
        Draw the text box on the screen.

        Args:
            screen (pygame.Surface): The screen to draw the text box on.
        """
        if self.bg_color:
            # Draw background rectangle with padding
            bg_rect = self.rect.inflate(self.padding * 2, self.padding * 2)
            pygame.draw.rect(screen, self.bg_color, bg_rect)

        # Draw thick drop shadow if enabled
        for shadow in self.shadows:
            for offset_x in range(-shadow.thickness, shadow.thickness + 1):
                for offset_y in range(-shadow.thickness, shadow.thickness + 1):
                    if offset_x ** 2 + offset_y ** 2 <= shadow.thickness ** 2:  # Circular shadow area
                        shadow_rect = self.rect.move(offset_x + shadow.offset[0], offset_y + shadow.offset[1])
                        shadow_surface = self.font.render(self.text, True, shadow.color)
                        screen.blit(shadow_surface, shadow_rect)

        # Draw the main text
        screen.blit(self.text_surface, self.rect)
