"""
Neon Depths — Roguelike Dungeon Crawler
Ponto de entrada: loop principal, estados e orquestração dos sistemas.
"""
import sys
import random
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_SETTINGS,
    ENEMY_SPAWN_INTERVAL, ENEMY_SPAWN_MIN, ENEMY_MAX_ON_SCREEN,
    DIFFICULTY_SPAWN_SCALE, BOSS_FLOOR_INTERVAL,
)
from player import Player
from enemy import Enemy, EnemyGroup, pick_enemy_type
from bullet import BulletGroup
from map import GameMap
from ui import UI
from menu import MenuManager
from effects.particles import ParticleSystem
from effects.lighting import LightingSystem
from utils.camera import Camera
from utils.audio import AudioManager
from utils.save_system import SaveSystem
from utils.leaderboard import Leaderboard
from utils.achievements import AchievementManager
from utils.input_handler import InputHandler
from utils.sprites import create_background_layer
from utils.display import DisplayManager
from utils.collision import clamp_to_walkable
from settings import PLAYER_HITBOX


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.save_data = SaveSystem.load()
        settings = self.save_data["settings"]
        self.display = DisplayManager()
        self._apply_display_mode(settings.get("fullscreen", False))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_MENU
        self.dt = 0.0
        self.global_time = 0.0

        self.audio = AudioManager()
        self.audio.init()
        self.audio.set_volumes(
            settings.get("master_volume"),
            settings.get("music_volume"),
            settings.get("sfx_volume"),
        )

        self.input = InputHandler()
        self.camera = Camera()
        self.ui = UI()
        self.menu = MenuManager(self.save_data)
        self.particles = ParticleSystem()
        self.achievements = AchievementManager()
        self.lighting = LightingSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bg_layer = create_background_layer(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Estado de partida
        self.player: Player | None = None
        self.enemies = EnemyGroup()
        self.bullets = BulletGroup()
        self.game_map: GameMap | None = None
        self.floor = 1
        self.spawn_timer = 0.0
        self.enemies_to_spawn = 5
        self.floor_cleared = False
        self.boss_spawned = False
        self.mouse_held = False

    def _apply_display_mode(self, fullscreen: bool):
        """Tela cheia na resolução real do monitor (ex. 2560×1080 ultrawide)."""
        self.display.apply_mode(fullscreen)
        self.save_data["settings"]["fullscreen"] = fullscreen

    def _game_mouse_pos(self) -> tuple[int, int]:
        return self.display.screen_to_game(pygame.mouse.get_pos())

    def _sync_map_bounds(self):
        if not self.game_map:
            return
        bounds = self.game_map.get_walkable_bounds()
        if self.player:
            self.player.map_bounds = bounds
        for enemy in self.enemies:
            enemy.map_bounds = bounds

    def new_game(self):
        self.floor = 1
        self._load_floor()
        self.state = STATE_PLAYING
        self.audio.play_music()
        self.achievements = AchievementManager()

    def _load_floor(self):
        self.game_map = GameMap(self.floor)
        self.enemies.empty()
        self.bullets.empty()
        self.particles.particles.clear()
        self.floor_cleared = False
        self.boss_spawned = False
        self.enemies_to_spawn = 4 + self.floor * 2
        self.spawn_timer = 1.0

        bounds = self.game_map.get_walkable_bounds()
        spawn = clamp_to_walkable(
            self.game_map.player_spawn, PLAYER_HITBOX,
            self.game_map.walls, bounds,
        )
        if self.player is None:
            self.player = Player(spawn.x, spawn.y)
        else:
            self.player.pos.update(spawn)
        self.player.map_bounds = bounds
        self.player.rect.center = (int(self.player.pos.x), int(self.player.pos.y))

        self.camera.set_map_size(self.game_map.pixel_w, self.game_map.pixel_h)
        self._sync_map_bounds()
        self.achievements.new_floor()

        if self.floor % BOSS_FLOOR_INTERVAL == 0:
            self._spawn_boss()

        self.ui.notify(f"ANDAR {self.floor}", duration=2.0)

    def _spawn_boss(self):
        if self.boss_spawned or not self.game_map:
            return
        pos = self.game_map.get_spawn_position()
        boss = Enemy(pos.x, pos.y, "boss", self.floor)
        if self.game_map:
            boss.place_at(pos, self.game_map.walls, self.game_map.get_walkable_bounds())
        self.enemies.add(boss)
        self.boss_spawned = True
        self.audio.play("boss")
        self.ui.notify("BOSS DETECTADO!", (255, 100, 50))

    def _spawn_enemy(self):
        if not self.game_map or self.enemies_to_spawn <= 0:
            return
        if self.enemies.alive_count() >= ENEMY_MAX_ON_SCREEN:
            return
        pos = self.game_map.get_spawn_position()
        etype = pick_enemy_type(self.floor)
        enemy = Enemy(pos.x, pos.y, etype, self.floor)
        if self.game_map:
            enemy.place_at(pos, self.game_map.walls, self.game_map.get_walkable_bounds())
        self.enemies.add(enemy)
        self.enemies_to_spawn -= 1

    def _update_spawning(self, dt: float):
        if self.enemies_to_spawn <= 0:
            return
        interval = max(ENEMY_SPAWN_MIN,
                       ENEMY_SPAWN_INTERVAL * (DIFFICULTY_SPAWN_SCALE ** (self.floor - 1)))
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._spawn_enemy()
            self.spawn_timer = interval * random.uniform(0.7, 1.2)

    def _handle_collisions(self):
        if not self.player or not self.game_map:
            return

        walls = self.game_map.walls

        # Balas do jogador vs inimigos
        for bullet in list(self.bullets):
            if bullet.owner != "player":
                continue
            for enemy in list(self.enemies):
                if bullet.rect.colliderect(enemy.rect):
                    dead = enemy.take_damage(bullet.damage, self.particles, self.audio)
                    self.ui.add_damage_number(enemy.pos, bullet.damage)
                    bullet.kill()
                    if dead:
                        self.player.on_kill(enemy.score_value, self.audio)
                        self.achievements.on_kill()
                        self.particles.emit_death(enemy.pos)
                        self.audio.play("kill")
                        if enemy.is_boss:
                            self.achievements.on_boss_kill()
                        enemy.kill()
                        if self.camera and self.save_data["settings"].get("screen_shake", True):
                            self.camera.shake(5)
                    break

        # Balas inimigas vs jogador
        for bullet in list(self.bullets):
            if bullet.owner == "enemy" and bullet.rect.colliderect(self.player.hitbox):
                if self.player.take_damage(bullet.damage, self.audio):
                    self._game_over()
                else:
                    self.achievements.on_damage()
                    self.ui.add_damage_number(self.player.pos, bullet.damage)
                    if self.save_data["settings"].get("screen_shake", True):
                        self.camera.shake(8)
                bullet.kill()

        # Inimigos corpo a corpo
        for enemy in self.enemies:
            if enemy.hitbox.colliderect(self.player.hitbox):
                if enemy.state == "attack" and self.player.invincible <= 0:
                    if self.player.take_damage(enemy.damage, self.audio):
                        self._game_over()
                    else:
                        self.achievements.on_damage()
                        if self.save_data["settings"].get("screen_shake", True):
                            self.camera.shake(6)

            # IA desvia de projéteis próximos
            for bullet in self.bullets:
                if bullet.owner == "player":
                    dist = (enemy.pos - bullet.pos).length()
                    if dist < 80:
                        enemy.try_dodge_bullet(bullet.pos)

        # Power-ups
        for pu in list(self.game_map.powerups):
            if self.player.hitbox.colliderect(pu.rect):
                self.player.apply_powerup(pu.power_type, self.audio, self.particles)
                self.achievements.on_powerup()
                pu.kill()

        # Saída do andar
        if (self.game_map.exit_rect and self.enemies_to_spawn <= 0
                and self.enemies.alive_count() == 0):
            if self.player.hitbox.colliderect(self.game_map.exit_rect):
                self.floor += 1
                self.menu.transition.start(self._load_floor)

    def _game_over(self):
        self.state = STATE_GAME_OVER
        self.audio.play("game_over")
        self.audio.stop_music()
        score = self.player.score if self.player else 0
        kills = self.player.kills if self.player else 0
        SaveSystem.update_run(score, self.floor, kills)
        if Leaderboard.is_high_score(score):
            Leaderboard.add_entry(self.menu.player_name, score, self.floor)

    def _update_playing(self, dt: float):
        if self.menu.transition.active:
            self.menu.transition.update(dt)
            return

        if not self.player or not self.game_map:
            return

        move = self.input.movement_vector()
        aim = self.input.aim_world(
            self.player.pos, self.camera.offset, self._game_mouse_pos(),
        )
        want_shoot = self.mouse_held or pygame.mouse.get_pressed()[0]
        want_dash = self.input.dash_pressed()

        self.player.update(dt, move, aim, self.game_map.walls,
                           want_shoot, want_dash, self.bullets,
                           self.particles, self.audio)

        for enemy in self.enemies:
            enemy.update(dt, self.player.pos, self.game_map.walls,
                         self.bullets, self.audio, self.floor)

        self.bullets.update_all(dt, self.game_map.walls)
        self._update_spawning(dt)
        self._handle_collisions()

        if self.save_data["settings"].get("particles", True):
            self.particles.update(dt)
        self.camera.update(self.player.pos, dt)
        self.ui.update(dt)

        new_ach = self.achievements.check_runtime(
            self.player.score, self.floor, self.player.level,
            self.achievements._session_stats.get("boss", False),
        )
        for ach in new_ach:
            self.ui.show_achievement(ach)
            self.ui.notify(f"Conquista: {ach['name']}")

    def _draw_world(self):
        cam = self.camera.offset
        world = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        world.fill((12, 10, 28))

        if self.game_map:
            self.game_map.draw(world, cam, self.global_time)
            self.game_map.draw_powerups(world, cam, self.dt)

        for enemy in self.enemies:
            er = enemy.rect.move(-int(cam.x), -int(cam.y))
            world.blit(enemy.image, er)

        if self.player:
            pr = self.player.rect.move(-int(cam.x), -int(cam.y))
            world.blit(self.player.image, pr)

        for bullet in self.bullets:
            br = bullet.rect.move(-int(cam.x), -int(cam.y))
            world.blit(bullet.image, br)

        if self.save_data["settings"].get("particles", True):
            self.particles.draw(world, cam)

        surf = self.display.surface
        surf.blit(world, (0, 0))

        if self.player:
            lights = [(self.player.pos.x, self.player.pos.y, 180)]
            for enemy in self.enemies:
                if enemy.is_boss:
                    lights.append((enemy.pos.x, enemy.pos.y, 120))
            self.lighting.render(surf, lights, cam, ambient=210)

    def _draw_playing_hud(self):
        if self.player:
            surf = self.display.surface
            self.ui.draw_hud(surf, self.player, self.floor, self.enemies.alive_count())
            self.ui.draw_damage_numbers(surf, self.camera.offset)
            self.ui.draw_notifications(surf)
            self.ui.draw_achievement_popup(surf)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                fs = not self.save_data["settings"].get("fullscreen", False)
                self._apply_display_mode(fs)
                SaveSystem.save(self.save_data)
                self.audio.play("ui")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_held = False

            if self.state == STATE_MENU:
                self._handle_menu_events(event)
            elif self.state == STATE_PLAYING:
                if InputHandler.pause_pressed(event):
                    self.state = STATE_PAUSED
                    self.menu.selected = 0
                self._handle_playing_settings(event)
            elif self.state == STATE_PAUSED:
                self._handle_pause_events(event)
            elif self.state == STATE_GAME_OVER:
                self._handle_game_over_events(event)
            elif self.state == STATE_SETTINGS:
                self._handle_settings_events(event)

    def _handle_menu_events(self, event):
        if self.menu.show_leaderboard or self.menu.show_achievements:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.menu.show_leaderboard = False
                self.menu.show_achievements = False
            return

        action = self.menu.handle_menu_input(event, 5)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.menu.show_leaderboard or self.menu.show_achievements:
                self.menu.show_leaderboard = False
                self.menu.show_achievements = False

        if action == "confirm":
            items = ["play", "leaderboard", "achievements", "settings", "quit"]
            choice = items[self.menu.selected]
            self.audio.play("ui")
            if choice == "play":
                self.player = None
                self.menu.transition.start(self.new_game)
            elif choice == "leaderboard":
                self.menu.show_leaderboard = True
            elif choice == "achievements":
                self.menu.show_achievements = True
            elif choice == "settings":
                self.state = STATE_SETTINGS
                self.menu.settings_selection = 0
            elif choice == "quit":
                self.running = False

    def _handle_pause_events(self, event):
        action = self.menu.handle_menu_input(event, 3)
        if InputHandler.pause_pressed(event) and action != "confirm":
            self.state = STATE_PLAYING
            return
        if action == "confirm":
            self.audio.play("ui")
            if self.menu.selected == 0:
                self.state = STATE_PLAYING
            elif self.menu.selected == 1:
                self.state = STATE_SETTINGS
            elif self.menu.selected == 2:
                self.state = STATE_MENU
                self.audio.stop_music()
                self.player = None

    def _handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.player = None
                self.new_game()
            elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.state = STATE_MENU
                self.save_data = SaveSystem.load()
                self.menu.save_data = self.save_data

    def _handle_settings_events(self, event):
        rows = ["master_volume", "music_volume", "sfx_volume",
                "fullscreen", "particles", "screen_shake", "back"]
        s = self.save_data["settings"]
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                self.menu.settings_selection = (self.menu.settings_selection - 1) % len(rows)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.menu.settings_selection = (self.menu.settings_selection + 1) % len(rows)
            elif event.key == pygame.K_LEFT:
                self._adjust_setting(rows, s, -1)
            elif event.key == pygame.K_RIGHT:
                self._adjust_setting(rows, s, 1)
            elif event.key == pygame.K_RETURN:
                key = rows[self.menu.settings_selection]
                if key == "back":
                    self.state = STATE_MENU if self.player is None else STATE_PAUSED
                elif key in ("fullscreen", "particles", "screen_shake"):
                    settings[key] = not settings.get(key, True)
                    if key == "fullscreen":
                        self._apply_display_mode(settings[key])
                    self.audio.play("ui")
            elif event.key == pygame.K_ESCAPE:
                self.state = STATE_MENU if self.player is None else STATE_PAUSED
        SaveSystem.save(self.save_data)

    def _adjust_setting(self, rows, settings, direction):
        key = rows[self.menu.settings_selection]
        if key == "back":
            return
        if key in ("master_volume", "music_volume", "sfx_volume"):
            settings[key] = round(max(0, min(1, settings.get(key, 0.5) + direction * 0.1)), 1)
            self.audio.set_volumes(
                settings.get("master_volume"),
                settings.get("music_volume"),
                settings.get("sfx_volume"),
            )
        else:
            settings[key] = not settings.get(key, True)
            if key == "fullscreen":
                self._apply_display_mode(settings[key])
            self.audio.play("ui")

    def _handle_playing_settings(self, event):
        pass

    def update(self):
        self.dt = self.clock.tick(FPS) / 1000.0
        self.dt = min(self.dt, 0.05)
        self.global_time += self.dt
        self.menu.update_bg(self.dt)

        if self.state == STATE_PLAYING:
            self._update_playing(self.dt)
        elif self.state == STATE_MENU:
            self.menu.transition.update(self.dt)

    def draw(self):
        surf = self.display.surface
        if self.state == STATE_MENU:
            self.menu.draw_animated_bg(surf, self.bg_layer)
            if self.menu.show_leaderboard:
                self.menu.draw_leaderboard(surf)
            elif self.menu.show_achievements:
                self.menu.draw_achievements(surf, self.achievements.unlocked)
            else:
                self.menu.draw_main_menu(surf)
            self.menu.transition.draw(surf)
        elif self.state == STATE_PLAYING:
            self._draw_world()
            self._draw_playing_hud()
            self.menu.transition.draw(surf)
        elif self.state == STATE_PAUSED:
            self._draw_world()
            self._draw_playing_hud()
            self.menu.draw_pause(surf)
        elif self.state == STATE_GAME_OVER:
            self.menu.draw_animated_bg(surf, self.bg_layer)
            score = self.player.score if self.player else 0
            kills = self.player.kills if self.player else 0
            is_high = Leaderboard.is_high_score(score)
            self.menu.draw_game_over(surf, score, self.floor, kills, is_high)
        elif self.state == STATE_SETTINGS:
            self.menu.draw_animated_bg(surf, self.bg_layer)
            self.menu.draw_settings(surf, self.save_data["settings"])

        self.display.present()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
