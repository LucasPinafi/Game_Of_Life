import pygame
from typing import Tuple, Callable


class Button:
    def __init__(self, screen: pygame.Surface, text: str, width: int, height: int, pos: Tuple[int, int],
                 elevation: int, top_collor: str, top_color_hover: str, on_pressed: Callable,
                 font: str | None = None, font_size: int = 15, font_color: str = '#FFFFFF',
                 bottom_collor: str = '#000000', border_radius: int = 12) -> None:
        # Display surface
        self.display_surface = screen

        # Rects
        self.width = width
        self.height = height
        self.pos = pos
        self.top_rect = pygame.Rect(self.pos, (self.width, self.height))
        self.top_collor = top_collor
        self.top_rect_orig_y = self.top_rect.y
        self.top_collor_hover = top_color_hover
        self.border_radius = border_radius
        self.text = text
        self.font_color = font_color

        # Attributes
        self.pressed = False
        self.font = pygame.font.Font(font, font_size)
        self.text_surf = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.on_pressed = on_pressed

        # Dynamic prop
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.collor = self.top_collor
        self.bottom_rect = pygame.Rect(self.pos, (self.width, self.elevation + self.height))
        self.bottom_collor = bottom_collor

    def draw(self) -> None:
        self.top_rect = pygame.Rect(self.pos, (self.width, self.height))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.bottom_rect = pygame.Rect(self.pos, (self.width, self.elevation + self.height))
        self.text_surf = self.font.render(self.text, True, self.font_color)
        self.top_rect.y = self.top_rect_orig_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        pygame.draw.rect(self.display_surface, self.bottom_collor, self.bottom_rect, border_radius=self.border_radius)
        pygame.draw.rect(self.display_surface, self.collor, self.top_rect, border_radius=self.border_radius)

        self.display_surface.blit(self.text_surf, self.text_rect)
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.collor = self.top_collor_hover
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.on_pressed()
                self.pressed = True

                # Make bottom moviment
                self.dynamic_elevation = 0

            elif not pygame.mouse.get_pressed()[0]:
                self.pressed = False
                self.dynamic_elevation = self.elevation
        else:
            self.dynamic_elevation = self.elevation
            self.collor = self.top_collor
