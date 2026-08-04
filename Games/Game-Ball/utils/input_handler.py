"""Entrada unificada para teclado, mouse e gamepad."""

import pygame


GAMEPAD_DEAD_ZONE = 0.2


class InputHandler:
    def __init__(self):
        self.joystick: pygame.joystick.Joystick | None = None
        self._init_gamepad()

    def _init_gamepad(self) -> None:
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            return

        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except pygame.error:
            self.joystick = None

    def movement_vector(self) -> pygame.Vector2:
        vector = pygame.Vector2()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vector.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vector.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vector.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vector.x += 1

        if self.joystick and self.joystick.get_numaxes() >= 2:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            if abs(axis_x) > GAMEPAD_DEAD_ZONE:
                vector.x += axis_x
            if abs(axis_y) > GAMEPAD_DEAD_ZONE:
                vector.y += axis_y

        if vector.length_squared() > 0:
            vector = vector.normalize()

        return vector

    def _gamepad_aim(self) -> pygame.Vector2 | None:
        if not self.joystick or self.joystick.get_numaxes() < 4:
            return None

        axis_x = self.joystick.get_axis(2)
        axis_y = self.joystick.get_axis(3)
        vector = pygame.Vector2(axis_x, axis_y)

        if vector.length_squared() <= GAMEPAD_DEAD_ZONE ** 2:
            return None

        return vector.normalize()

    def aim_direction(self, player_screen_pos: pygame.Vector2) -> pygame.Vector2:
        gamepad_direction = self._gamepad_aim()
        if gamepad_direction is not None:
            return gamepad_direction

        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        direction = mouse_position - player_screen_pos
        return direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)

    def aim_world(
        self,
        player_world_pos: pygame.Vector2,
        camera_offset: pygame.Vector2,
        game_mouse: tuple[int, int] | None = None,
    ) -> pygame.Vector2:
        gamepad_direction = self._gamepad_aim()
        if gamepad_direction is not None:
            return gamepad_direction

        mouse_position = pygame.Vector2(game_mouse or pygame.mouse.get_pos())
        world_position = mouse_position + camera_offset
        direction = world_position - player_world_pos
        return direction.normalize() if direction.length_squared() > 4 else pygame.Vector2(1, 0)

    def dash_pressed(self) -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return True

        return bool(
            self.joystick
            and self.joystick.get_numbuttons() > 0
            and self.joystick.get_button(0)
        )

    @staticmethod
    def pause_pressed(event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            return True
        return event.type == pygame.JOYBUTTONDOWN and event.button == 7

    @staticmethod
    def confirm_pressed(event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return event.type == pygame.JOYBUTTONDOWN and event.button == 0
