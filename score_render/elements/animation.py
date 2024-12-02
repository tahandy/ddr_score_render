import pygame
import os
import numpy as np

class AnimationPNG:
    def __init__(self, folder_path, duration, interpolation_frames=3, scale_to=None, maintain_aspect_ratio=True, loopable=True):
        """
        Initialize the animation with optional frame interpolation, scaling, and center-based positioning.

        Args:
            folder_path (str): Path to the folder containing PNG animation frames.
            duration (float): Total duration of the animation in seconds.
            interpolation_frames (int): Number of interpolated frames between each original frame.
            scale_to (tuple): Desired (width, height) to scale all frames to. If None, no scaling is performed.
            maintain_aspect_ratio (bool): Whether to maintain aspect ratio when scaling.
        """
        self.loopable = loopable
        self.frames = self.load_and_process_frames(folder_path, interpolation_frames, scale_to, maintain_aspect_ratio)
        self.duration = duration
        self.frame_count = len(self.frames)
        self.current_time = 0
        self.playing = True  # Whether the animation is playing

        # Save the animation's width and height based on the first frame
        self.width, self.height = self.frames[0].get_size() if self.frames else (0, 0)

    def load_and_process_frames(self, folder_path, interpolation_frames, scale_to, maintain_aspect_ratio):
        """
        Load frames from the specified folder, interpolate, and optionally scale them.

        Args:
            folder_path (str): Path to the folder containing PNG frames.
            interpolation_frames (int): Number of interpolated frames to generate between each original frame.
            scale_to (tuple): Desired (width, height) for scaling.
            maintain_aspect_ratio (bool): Whether to maintain aspect ratio when scaling.

        Returns:
            list: A list of Pygame surfaces, including interpolated frames.
        """
        frames = []
        file_list = sorted(
            [f for f in os.listdir(folder_path) if f.endswith(".png")]
        )

        # Load original frames
        original_frames = [
            self.scale_frame(pygame.image.load(os.path.join(folder_path, file)).convert_alpha(), scale_to, maintain_aspect_ratio)
            for file in file_list
        ]

        # Interpolate between consecutive frames
        for i in range(len(original_frames) - (not self.loopable)):
            frame1 = original_frames[i]
            frame2 = original_frames[(i + 1) % len(original_frames)]  # Loop to the first frame

            # Convert frames to numpy arrays
            array1 = pygame.surfarray.pixels3d(frame1)
            array2 = pygame.surfarray.pixels3d(frame2)
            alpha1 = pygame.surfarray.pixels_alpha(frame1)
            alpha2 = pygame.surfarray.pixels_alpha(frame2)

            for j in range(interpolation_frames + 1):
                alpha = j / (interpolation_frames + 1)
                interpolated_array = (1 - alpha) * array1 + alpha * array2
                interpolated_alpha = (1 - alpha) * alpha1 + alpha * alpha2

                # Create surface from interpolated array
                interpolated_surface = pygame.Surface(frame1.get_size(), pygame.SRCALPHA)
                pygame.surfarray.blit_array(interpolated_surface, interpolated_array)
                pygame.surfarray.pixels_alpha(interpolated_surface)[:] = interpolated_alpha
                frames.append(interpolated_surface)

        return frames

    def scale_frame(self, frame, scale_to, maintain_aspect_ratio):
        """
        Scale a single frame to the desired size.

        Args:
            frame (pygame.Surface): The frame to scale.
            scale_to (tuple): The desired (width, height) for scaling.
            maintain_aspect_ratio (bool): Whether to maintain aspect ratio when scaling.

        Returns:
            pygame.Surface: The scaled frame.
        """
        if not scale_to:
            return frame  # No scaling required

        original_width, original_height = frame.get_size()
        target_width, target_height = scale_to

        if maintain_aspect_ratio:
            # Calculate aspect ratio-preserving dimensions
            aspect_ratio = original_width / original_height
            if target_width / target_height > aspect_ratio:
                # Target height is the limiting factor
                target_width = int(target_height * aspect_ratio)
            else:
                # Target width is the limiting factor
                target_height = int(target_width / aspect_ratio)

        # Scale the frame
        return pygame.transform.scale(frame, (target_width, target_height))

    def update(self, dt):
        """
        Update the animation based on elapsed time.

        Args:
            dt (float): Time elapsed since the last update (in seconds).
        """
        if self.playing:
            self.current_time += dt
            if self.current_time > self.duration and self.loopable:
                self.current_time %= self.duration  # Loop the animation

    def get_frame(self):
        """
        Get the current frame to render based on elapsed time.

        Returns:
            pygame.Surface: The current animation frame.
        """
        if not self.frames:
            return None
        # Calculate the current frame index
        frame_index = int((self.current_time / self.duration) * self.frame_count)
        return self.frames[frame_index]

    def draw(self, screen, position):
        """
        Draw the current frame on the screen, centered at the given position.

        Args:
            screen (pygame.Surface): The surface to draw the animation on.
            position (tuple): The (x, y) position to center the animation.
        """
        frame = self.get_frame()
        if frame:
            frame_rect = frame.get_rect(center=position)
            screen.blit(frame, frame_rect)
