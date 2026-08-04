"""
Entrada unificada: teclado, mouse e gamepad.
"""
import pygame

from settings import KEY_BINDINGS


class InputHandler:
    def __init__(self):
        self.joystick: pygame.joystick.Joystick | None = None
        self._init_gamepad()

    def _init_gamepad(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def movement_vector(self) -> pygame.Vector2:
        vec = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vec.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vec.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vec.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vec.x += 1

        if self.joystick:
            ax_x = self.joystick.get_axis(0)
            ax_y = self.joystick.get_axis(1)
            dead = 0.2
            if abs(ax_x) > dead:
                vec.x += ax_x
            if abs(ax_y) > dead:
                vec.y += ax_y

        if vec.length_squared() > 0:
            vec = vec.normalize()
        return vec

    def aim_direction(self, player_pos: pygame.Vector2) -> pygame.Vector2:
        mx, my = pygame.mouse.get_pos()
        # Mouse em coordenadas de tela — o main passa posição mundial se necessário
        direction = pygame.Vector2(mx, my) - player_pos
        if self.joystick and self.joystick.get_numaxes() >= 3:
            rx = self.joystick.get_axis(2)
            ry = self.joystick.get_axis(3)
            if rx ** 2 + ry ** 2 > 0.15:
                return pygame.Vector2(rx, ry).normalize()
        if direction.length_squared() > 0:
            return direction.normalize()
        return pygame.Vector2(1, 0)

    def aim_world(self, player_world_pos: pygame.Vector2, camera_offset: pygame.Vector2,
                  game_mouse: tuple[int, int] | None = None) -> pygame.Vector2:
        if game_mouse is None:
            mx, my = pygame.mouse.get_pos()
        else:
            mx, my = game_mouse
        world = pygame.Vector2(mx, my) + camera_offset
        diff = world - player_world_pos
        if self.joystick and self.joystick.get_numaxes() >= 3:
            rx = self.joystick.get_axis(2)
            ry = self.joystick.get_axis(3)
            if rx ** 2 + ry ** 2 > 0.15:
                return pygame.Vector2(rx, ry).normalize()
        if diff.length_squared() > 4:
            return diff.normalize()
        return pygame.Vector2(1, 0)

    @staticmethod
    def dash_pressed() -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return True
        # Botão A / 0 no gamepad
        if pygame.joystick.get_count() > 0:
            joy = pygame.joystick.Joystick(0)
            return joy.get_button(0)
        return False

    @staticmethod
    def pause_pressed(event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            return True
        if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
            return True
        return False

    @staticmethod
    def confirm_pressed(event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
            return True
        return False
