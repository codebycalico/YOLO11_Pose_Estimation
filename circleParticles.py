import pygame
import random
import math

class CircleParticle:
    def __init__(self, path_points, duration_per_segment):
        self.path = [pygame.Vector2(p) for p in path_points]
        self.duration = duration_per_segment  # seconds per segment
        self.elapsed = 0
        self.speed = 1 / duration_per_segment

        self.current_index = 0
        self.next_index = 1

        self.position = self.path[0]
        self.offset = pygame.Vector2(0, 0)
        self.target_offset = self._new_offset()
        self.float_strength = 20
        self.offset_change_interval = 0.5
        self.time_since_offset_change = 0

    def _new_offset(self):
        angle = random.uniform(0, 2 * math.pi)
        strength = random.uniform(0.3, 1.0) * self.float_strength
        return pygame.Vector2(
            math.cos(angle) * strength,
            math.sin(angle) * strength
        )

    def update(self, dt):
        self.elapsed += dt
        t = min(self.elapsed * self.speed, 1)  # normalized time [0-1]

        # Get current and next points
        start = self.path[self.current_index]
        end = self.path[self.next_index]

        # Base position between current and next point
        base_position = start.lerp(end, t)

        # Update float offset
        self.time_since_offset_change += dt
        if self.time_since_offset_change >= self.offset_change_interval:
            self.target_offset = self._new_offset()
            self.time_since_offset_change = 0

        self.offset = self.offset.lerp(self.target_offset, dt * 2)

        self.position = base_position + self.offset

        # If we reach the next point, advance
        if t >= 1:
            self.current_index = self.next_index
            self.next_index = (self.next_index + 1) % len(self.path)
            self.elapsed = 0  # reset timer

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.position, 3)
