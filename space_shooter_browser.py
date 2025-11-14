import random
import math
import sys
import os
import pygame

# Определяем цветовые константы
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Инициализируем pygame
pygame.init()

# Для браузерной версии отключаем звук
# pygame.mixer.init()  # Инициализируем микшер звука

# Создаем оконный дисплей вместо полноэкранного для браузерной совместимости
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter - Browser Version")

# Инициализируем звуки (с проверкой на наличие файлов)
# Для браузерной версии звуки отключены
shoot_sound = None
boom_sound = None
menu_sound = None

# Инициализируем изображения (с проверкой на наличие файлов)
ship_image = None
boom_image = None
boom2_image = None

# Инициализируем список изображений вражеских кораблей
enemy_ship_images = []
for i in range(1, 6):  # Загружаем 1.png through 5.png
    # Для браузерной версии изображения отключены
    enemy_ship_images.append(None)

# Создаем звездный фон
stars = []
for _ in range(100):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    size = random.randint(1, 3)
    speed = random.uniform(0.5, 2.0)
    brightness = random.randint(100, 255)
    stars.append([x, y, size, speed, brightness])

# Состояния игры
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3
SHOP = 4

# Класс игрока
class Player:
    def __init__(self, player_id=1):
        self.player_id = player_id  # 1 для первого игрока
        self.width = 80
        self.height = 65
        # Размещаем игрока по центру
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.color = BLUE
        self.speed = 2  # Базовая скорость
        self.bullets = []
        self.shoot_cooldown = 0
        self.health = 100  # Базовое здоровье
        self.max_health = 100
        self.engine_animation = 0
        self.angle = -90  # Начальное направление вверх
        self.image_rotation_offset = 0
        self.shoot_angle = -90  # Отдельный угол для стрельбы
        # Улучшаемые атрибуты
        self.damage = 10  # Базовый урон за выстрел
        self.armor = 0    # Снижение урона
        self.base_shoot_cooldown = 20  # Базовая задержка выстрела
        self.upgrades = {
            'damage': 0,
            'health': 0,
            'speed': 0,
            'armor': 0,
            'attack_speed': 0
        }
        self.upgrade_costs = {
            'damage': 50,
            'health': 100,
            'speed': 75,
            'armor': 80,
            'attack_speed': 100
        }
        
    def shoot(self):
        if self.shoot_cooldown <= 0:
            # Позиция появления точно в центре корабля
            bullet_x = self.x
            bullet_y = self.y
            
            # Направление на основе угла корабля (куда направлен нос)
            rad_angle = math.radians(self.angle)
            bullet_dx = math.cos(rad_angle) * 12  # Увеличенная скорость пули
            bullet_dy = math.sin(rad_angle) * 12  # Увеличенная скорость пули
            
            # Создаем более мощные пули
            bullet = Bullet(bullet_x, bullet_y, bullet_dx, bullet_dy)
            self.bullets.append(bullet)
            self.shoot_cooldown = 20  # Медленная стрельба (было 10, теперь 20)
                
    def draw(self):
        # Рисуем более детальный космический корабль с поворотом
        # Сохраняем текущий угол для рисования
        ship_angle = self.angle
        
        # Создаем поверхность для корабля
        ship_surface = pygame.Surface((self.width * 2, self.height * 2), pygame.SRCALPHA)
        
        # Рисуем корпус корабля на поверхности
        # Основной корпус
        pygame.draw.polygon(ship_surface, self.color, [
            (self.width, self.height - self.height//2),
            (self.width - self.width//2, self.height + self.height//2),
            (self.width + self.width//2, self.height + self.height//2)
        ])
        
        # Кабина
        pygame.draw.circle(ship_surface, (173, 216, 230), (self.width, self.height - 5), 8)
        
        # Крылья
        pygame.draw.polygon(ship_surface, self.color, [
            (self.width - self.width//2, self.height + 5),
            (self.width - self.width, self.height + 15),
            (self.width - self.width//2, self.height + 15)
        ])
        pygame.draw.polygon(ship_surface, self.color, [
            (self.width + self.width//2, self.height + 5),
            (self.width + self.width, self.height + 15),
            (self.width + self.width//2, self.height + 15)
        ])
        
        # Анимация выхлопа двигателя
        self.engine_animation = (self.engine_animation + 0.3) % (2 * math.pi)
        engine_length = 15 + math.sin(self.engine_animation) * 5
        pygame.draw.polygon(ship_surface, YELLOW, [
            (self.width - 5, self.height + self.height//2),
            (self.width + 5, self.height + self.height//2),
            (self.width, self.height + self.height//2 + engine_length)
        ])
        pygame.draw.polygon(ship_surface, RED, [
            (self.width - 3, self.height + self.height//2),
            (self.width + 3, self.height + self.height//2),
            (self.width, self.height + self.height//2 + engine_length - 5)
        ])
        
        # Поворачиваем поверхность корабля
        rotated_ship = pygame.transform.rotate(ship_surface, -(ship_angle + self.image_rotation_offset))
        ship_rect = rotated_ship.get_rect(center=(self.x, self.y))
        
        # Рисуем повернутый корабль
        screen.blit(rotated_ship, ship_rect.topleft)
        
        # Рисуем здоровье игрока под кораблем
        try:
            font = pygame.font.SysFont(None, 24)
            health_text = font.render(f"{self.health}", True, GREEN)
            screen.blit(health_text, (self.x - health_text.get_width() // 2, self.y + self.height))
        except:
            pass  # Если создание шрифта не удалось, пропускаем отображение здоровья
        
    def move(self, left, right, up, down, target_x, target_y):
        # Сохраняем предыдущую позицию для вычисления угла
        prev_x, prev_y = self.x, self.y
        
        # Двигаемся на основе нажатых клавиш
        if left:
            self.x -= self.speed
        if right:
            self.x += self.speed
        if up:
            self.y -= self.speed
        if down:
            self.y += self.speed
            
        # Держим игрока на экране
        self.x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, self.x))
        self.y = max(self.height//2, min(SCREEN_HEIGHT - self.height//2, self.y))
        
        # Обновляем визуальный угол корабля, чтобы он всегда был направлен на врага (нос направлен на врага)
        if target_x is not None and target_y is not None:
            dx_to_target = target_x - self.x
            dy_to_target = target_y - self.y
            if dx_to_target != 0 or dy_to_target != 0:
                # Вычисляем угол от корабля к цели
                target_angle = math.degrees(math.atan2(dy_to_target, dx_to_target))
                self.angle = target_angle
                # Корабль будет стрелять туда, куда направлен его нос (self.angle)
        
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Обновляем пули
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0 or bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
                
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

# Класс пули
class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 4
        self.color = YELLOW
        self.trail = []  # Для эффекта следа пули
        
    def move(self):
        # Добавляем текущую позицию в след
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
    def draw(self):
        # Рисуем след пули
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            radius = int(self.radius * (i / len(self.trail)))
            pygame.draw.circle(screen, (255, 255, 0, alpha), (int(pos[0]), int(pos[1])), max(1, radius))
        
        # Рисуем основную пулю
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 2)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

# Класс врага (большое существо)
class Enemy:
    def __init__(self, level=1):
        self.width = 200
        self.height = 150
        self.x = SCREEN_WIDTH // 2
        self.y = 100
        self.speed = 2
        self.direction = 1
        self.color = RED
        self.health = 1000  # Гораздо больше здоровья
        self.max_health = 1000
        self.attack_cooldown = 0
        self.bullets = []
        self.animation_counter = 0
        self.pulse = 0
        self.damage_flash = 0
        # Для предсказания движения
        self.velocity_x = self.speed * self.direction
        self.velocity_y = 0
        # Для поворота корабля
        self.angle = 0
        self.image_rotation_offset = 0
        # Свойства, зависящие от уровня
        self.level = level
        # Увеличиваем сложность с каждым уровнем
        self.health = 1000 + (level - 1) * 500
        self.max_health = self.health
        self.speed = 2 + (level - 1) * 0.5
        self.attack_cooldown_max = max(20, 60 - (level - 1) * 8)  # Увеличенная скорость атаки
        # Для отслеживания позиции игрока
        self.target_x = 0
        self.target_y = 0
        # Броня для снижения урона
        self.armor = (level - 1) * 2  # Увеличиваем броню с уровнем
        
    def draw(self):
        # Мигание при получении урона
        if self.damage_flash > 0:
            self.damage_flash -= 1
            flash_color = (min(255, self.color[0] + 100), 
                          min(255, self.color[1] + 100), 
                          min(255, self.color[2] + 100))
        else:
            flash_color = self.color
            
        # Анимация пульсации
        self.pulse = math.sin(self.animation_counter * 0.1) * 5
        
        # Рисуем детальное вражеское существо
        # Основной корпус с градиентным эффектом
        body_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.ellipse(screen, flash_color, body_rect)
        
        # Рисуем сегменты корпуса для более сложного вида
        for i in range(5):
            segment_width = self.width - i * 10
            segment_height = self.height - i * 5
            segment_x = self.x - segment_width // 2
            segment_y = self.y - self.height//2 + i * 8
            pygame.draw.ellipse(screen, (max(0, flash_color[0]-i*10), max(0, flash_color[1]-i*10), max(0, flash_color[2]-i*10)), 
                              (segment_x, segment_y, segment_width, segment_height), 2)
        
        # Детализированные глаза с динамическими зрачками
        eye_offset = math.sin(self.animation_counter * 0.2) * 3
        # Левый глаз
        pygame.draw.ellipse(screen, (100, 100, 255), (self.x - self.width//3 - 10, self.y - 15, 30, 35))
        pygame.draw.ellipse(screen, YELLOW, (self.x - self.width//3 - 5, self.y - 10, 20, 25))
        pygame.draw.circle(screen, BLACK, (int(self.x - self.width//3 + 5 + eye_offset), int(self.y)), 8)
        pygame.draw.circle(screen, WHITE, (int(self.x - self.width//3 + 7 + eye_offset), int(self.y - 2)), 3)
        # Правый глаз
        pygame.draw.ellipse(screen, (100, 100, 255), (self.x + self.width//3 - 20, self.y - 15, 30, 35))
        pygame.draw.ellipse(screen, YELLOW, (self.x + self.width//3 - 15, self.y - 10, 20, 25))
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width//3 - 5 - eye_offset), int(self.y)), 8)
        pygame.draw.circle(screen, WHITE, (int(self.x + self.width//3 - 3 - eye_offset), int(self.y - 2)), 3)
        
        # Многослойные щупальца
        for i in range(7):
            angle = self.animation_counter * 0.07 + i * 0.9
            tentacle_x = self.x - self.width//2 + 10 + i * (self.width/7)
            tentacle_y = self.y + self.height//2 - 10
            
            # Основной сегмент щупальца
            point1 = (tentacle_x, tentacle_y)
            point2 = (tentacle_x + math.sin(angle) * 25, tentacle_y + 25 + math.cos(angle) * 15)
            point3 = (tentacle_x + math.sin(angle*1.3) * 35, tentacle_y + 50 + math.cos(angle*1.3) * 20)
            point4 = (tentacle_x + math.sin(angle*1.7) * 40, tentacle_y + 75 + math.cos(angle*1.7) * 25)
            
            pygame.draw.line(screen, flash_color, point1, point2, 6)
            pygame.draw.line(screen, flash_color, point2, point3, 5)
            pygame.draw.line(screen, flash_color, point3, point4, 4)
            
            # Присоски на щупальцах
            for j in range(4):
                sucker_pos = (
                    point1[0] + (point4[0] - point1[0]) * j/4,
                    point1[1] + (point4[1] - point1[1]) * j/4
                )
                pygame.draw.circle(screen, (150, 0, 0), (int(sucker_pos[0]), int(sucker_pos[1])), 3)
            
            # Кончик щупальца
            pygame.draw.circle(screen, (180, 0, 0), (int(point4[0]), int(point4[1])), 6)
        
        # Сложный рот с анимированными клыками
        mouth_y = self.y + self.height//4 + math.sin(self.animation_counter * 0.15) * 8
        pygame.draw.arc(screen, BLACK, (self.x - self.width//3, mouth_y, self.width*2//3, self.height//3), 0, math.pi, 4)
        
        # Клыки
        mandible_angle = math.sin(self.animation_counter * 0.2) * 0.5
        pygame.draw.polygon(screen, flash_color, [
            (self.x - self.width//4, mouth_y + 10),
            (self.x - self.width//4 - 20 - self.pulse, mouth_y + 15 + mandible_angle * 10),
            (self.x - self.width//4 - 10, mouth_y + 25)
        ])
        pygame.draw.polygon(screen, flash_color, [
            (self.x + self.width//4, mouth_y + 10),
            (self.x + self.width//4 + 20 + self.pulse, mouth_y + 15 + mandible_angle * 10),
            (self.x + self.width//4 + 10, mouth_y + 25)
        ])
        
        # Ряды зубов
        for row in range(2):
            for i in range(6):
                tooth_x = self.x - self.width//3 + 10 + i * (self.width*2/3/7)
                tooth_y = mouth_y + 5 + row * 8
                pygame.draw.polygon(screen, WHITE, [
                    (tooth_x, tooth_y),
                    (tooth_x - 3, tooth_y + 12),
                    (tooth_x + 3, tooth_y + 12)
                ])
        
        # Шипы на голове
        for i in range(5):
            spike_x = self.x - self.width//3 + i * (self.width*2/3/4)
            spike_height = 25 + math.sin(self.animation_counter * 0.3 + i) * 5
            pygame.draw.polygon(screen, (180, 0, 0), [
                (spike_x, self.y - self.height//2),
                (spike_x - 5, self.y - self.height//2 - spike_height),
                (spike_x + 5, self.y - self.height//2 - spike_height)
            ])
        
        # Пульсирующее энергетическое ядро
        core_radius = 12 + self.pulse
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y - self.height//4)), int(core_radius))
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y - self.height//4)), int(core_radius * 0.7))
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y - self.height//4)), int(core_radius * 0.4))
        
        # Пятна/узоры на корпусе
        for i in range(8):
            spot_x = self.x - self.width//2 + 20 + (i % 4) * (self.width - 40) / 3
            spot_y = self.y - self.height//4 + (i // 4) * (self.height//2)
            pygame.draw.circle(screen, (150, 0, 0), (int(spot_x), int(spot_y)), 5)
        
        # Рисуем здоровье врага над кораблем
        try:
            font = pygame.font.SysFont(None, 24)
            health_text = font.render(f"{self.health}", True, RED)
            screen.blit(health_text, (self.x - health_text.get_width() // 2, self.y - self.height - 20))
        except:
            pass  # Если создание шрифта не удалось, пропускаем отображение здоровья
        
    def move(self, target_x, target_y):
        # Отслеживаем позицию игрока для прицельных атак
        self.target_x = target_x
        self.target_y = target_y
        
        self.x += self.speed * self.direction
        self.velocity_x = self.speed * self.direction
        self.animation_counter += 1
        
        # Меняем направление при достижении края
        if self.x < self.width//2 or self.x > SCREEN_WIDTH - self.width//2:
            self.direction *= -1
            self.velocity_x = self.speed * self.direction
            
        # Небольшое вертикальное движение
        prev_y = self.y
        self.y = 100 + math.sin(pygame.time.get_ticks() / 1000) * 20
        self.velocity_y = self.y - prev_y
        
        # Поворачиваем вражеский корабль в сторону игрока
        if target_x is not None and target_y is not None:
            dx_to_target = target_x - self.x
            dy_to_target = target_y - self.y
            if dx_to_target != 0 or dy_to_target != 0:
                # Вычисляем угол от врага к цели
                target_angle = math.degrees(math.atan2(dy_to_target, dx_to_target))
                self.angle = target_angle
        
    def attack(self):
        if self.attack_cooldown <= 0:
            # Уровень 1: Базовая 8-направленная стрельба
            angles = [0, 45, 90, 135, 180, 225, 270, 315]
            for angle in angles:
                rad = math.radians(angle)
                dx = math.cos(rad) * 4
                dy = math.sin(rad) * 4
                bullet = EnemyBullet(self.x, self.y, dx, dy)
                self.bullets.append(bullet)
                    
            self.attack_cooldown = self.attack_cooldown_max  # Задержка атаки, зависящая от уровня
            
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Обновляем вражеские пули
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
                
    def take_damage(self, amount):
        # Применяем снижение урона от брони
        actual_damage = max(1, amount - self.armor)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
            
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

# Класс вражеской пули
class EnemyBullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 6
        self.color = PURPLE
        self.trail = []
        
    def move(self):
        # Добавляем текущую позицию в след
        self.trail.append((self.x, self.y))
        if len(self.trail) > 7:
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
    def draw(self):
        # Рисуем след пули
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            radius = int(self.radius * (i / len(self.trail)))
            pygame.draw.circle(screen, (128, 0, 128, alpha), (int(pos[0]), int(pos[1])), max(1, radius))
        
        # Рисуем основную пулю
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (200, 0, 200), (int(self.x), int(self.y)), self.radius - 2)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

# Класс кнопки для меню
class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=CYAN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.SysFont(None, 36)
        
    def draw(self):
        # Рисуем тень для лучшей видимости
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=12)
        
        # Рисуем основную кнопку с более толстой обводкой
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 4, border_radius=10)
        
        # Рисуем текст с тенью для лучшей читаемости
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        screen.blit(text_surf, text_rect)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
            
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                return True
        return False

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    FPS = 60
    
    # Состояние игры
    game_state = MENU
    current_level = 1
    max_levels = 5
    game_mode = "solo"  # Always solo mode
    
    # Создаем кнопки меню
    start_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50, "Начать игру", BLUE, CYAN)
    quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50, "Выход", BLUE, CYAN)
    
    # Создаем кнопки для режима игры
    menu_button = Button(SCREEN_WIDTH - 160, 20, 140, 50, "Меню", (60, 100, 200), (60, 150, 255))
    
    # Создаем игровые объекты
    player1 = None  # Первый игрок
    enemy = None
    particles = []
    explosions = []
    
    # Состояние игры
    score = 0
    
    # Шрифты для текста
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    
    # Основной игровой цикл
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Управление игроком 1 (WASD + ПРОБЕЛ)
                if event.key == pygame.K_SPACE and game_state == PLAYING and player1:
                    player1.shoot()
                elif event.key == pygame.K_r and (game_state == GAME_OVER or game_state == VICTORY):
                    # Сброс игры
                    game_state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    if game_state == PLAYING:
                        game_state = MENU
                elif event.key == pygame.K_b and game_state == PLAYING:  # Клавиша B для магазина
                    pass  # Магазин отключен в браузерной версии
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка нажатий кнопок меню
                if game_state == MENU:
                    if start_button.is_clicked(mouse_pos, event):
                        game_state = PLAYING
                        player1 = Player(1)  # Первый игрок
                        enemy = Enemy(current_level)  # Создаем врага для текущего уровня
                        particles = []
                        explosions = []
                        score = 0
                    elif quit_button.is_clicked(mouse_pos, event):
                        running = False
                elif game_state == PLAYING:
                    # Обработка нажатий кнопок в режиме игры
                    if menu_button.is_clicked(mouse_pos, event):
                        game_state = MENU
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Рисуем звездный фон
        for star in stars:
            x, y, size, speed, brightness = star
            # Обновляем положение звезды для эффекта параллакса
            star[1] = (y + speed) % SCREEN_HEIGHT
            pygame.draw.circle(screen, (brightness, brightness, brightness), (int(x), int(star[1])), size)
        
        if game_state == MENU:
            # Обновляем состояние наведения кнопок
            start_button.is_hovered(mouse_pos)
            quit_button.is_hovered(mouse_pos)
            
            # Рисуем меню
            # Добавляем название игры
            title_font = pygame.font.SysFont(None, 96)
            title_text = title_font.render("CHIPPY", True, YELLOW)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
            
            # Добавляем инструкции
            instructions = [
                "УПРАВЛЕНИЕ:",
                "WASD или стрелки - движение",
                "ПРОБЕЛ - выстрел",
                "ESC - выход в меню",
                "",
                "ЦЕЛЬ: Уничтожьте вражеские корабли!",
                "Избегайте столкновений и вражеских выстрелов."
            ]
            
            instruction_font = pygame.font.SysFont(None, 36)
            for i, line in enumerate(instructions):
                instruction_text = instruction_font.render(line, True, WHITE)
                screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 200 + i * 40))
            
            start_button.draw()
            quit_button.draw()
            
        elif (game_state == PLAYING or game_state == GAME_OVER) and player1 and enemy:
            # Рисуем игровые объекты
            player1.draw()
            enemy.draw()
            
            # Рисуем пули
            for bullet in player1.bullets:
                bullet.draw()
            for bullet in enemy.bullets:
                bullet.draw()
                
            # Рисуем счет и уровень
            score_text = font_small.render(f"Счет: {score}", True, YELLOW)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))
            
            level_text = font_small.render(f"Уровень: {current_level}/{max_levels}", True, CYAN)
            screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 40))
            
            # Рисуем подсказки управления
            controls_text1 = font_small.render("Игрок: WASD для движения, ПРОБЕЛ для стрельбы", True, BLUE)
            screen.blit(controls_text1, (10, SCREEN_HEIGHT - 60))
            
            # Рисуем подсказку магазина
            shop_text = font_small.render("ESC для меню", True, LIGHT_GRAY)
            screen.blit(shop_text, (SCREEN_WIDTH // 2 - shop_text.get_width() // 2, SCREEN_HEIGHT - 30))
            
            # Обновляем состояние наведения кнопок в режиме игры
            mouse_pos = pygame.mouse.get_pos()
            menu_button.is_hovered(mouse_pos)
            
            # Обрабатываем непрерывные нажатия клавиш для более естественного движения
            keys = pygame.key.get_pressed()
            
            # Игрок использует схему управления (WASD)
            left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            up = keys[pygame.K_UP] or keys[pygame.K_w]
            down = keys[pygame.K_DOWN] or keys[pygame.K_s]
                
            # Двигаем игрока с прямым управлением
            if player1 and enemy:
                player1.move(left, right, up, down, enemy.x, enemy.y)
            
            # Стрельба пробелом для игрока
            if keys[pygame.K_SPACE]:
                if player1 and player1.shoot_cooldown <= 0:
                    player1.shoot()
            
            # Обрабатываем регулировку поворота изображения
            if keys[pygame.K_q]:
                if player1:
                    player1.image_rotation_offset -= 1
            if keys[pygame.K_e]:
                if player1:
                    player1.image_rotation_offset += 1
            
            # Обновляем игровые объекты
            if player1:
                player1.update()
            # Враг нацеливается на игрока
            if enemy and player1:
                enemy.move(player1.x, player1.y)
                enemy.attack()
                enemy.update()
            
            # Проверяем столкновения между пулями игрока и врагом
            if player1 and enemy:
                for bullet in player1.bullets[:]:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        player1.bullets.remove(bullet)
                        enemy.take_damage(player1.damage)  # Используем атрибут урона игрока
                        score += player1.damage  # Очки начисляются только при попадании
                    if enemy.health <= 0:
                        if current_level >= max_levels:
                            game_state = VICTORY  # Игра завершена
                        else:
                            # Переходим на следующий уровень
                            current_level += 1
                            enemy = Enemy(current_level)  # Создаем врага для следующего уровня
            
            # Проверяем столкновения между вражескими пулями и игроком
            if enemy and player1:
                for bullet in enemy.bullets[:]:
                    # Проверяем столкновение с игроком
                    if bullet.get_rect().colliderect(player1.get_rect()):
                        enemy.bullets.remove(bullet)
                        player1.health -= 5  # Меньше урона за попадание
                        # Одиночный режим - игра окончена, когда умирает игрок
                        if player1.health <= 0:
                            game_state = GAME_OVER
            
            # Проверяем столкновение между игроком и врагом
            if player1 and enemy and hasattr(player1, 'get_rect') and hasattr(enemy, 'get_rect') and player1.get_rect().colliderect(enemy.get_rect()):
                player1.health -= 1
                # Одиночный режим - игра окончена, когда умирает игрок
                if player1.health <= 0:
                    game_state = GAME_OVER
            
            # Рисуем кнопки в режиме игры (поверх всех элементов)
            # Рисуем полупрозрачный фон для кнопок
            button_bg = pygame.Surface((150, 70), pygame.SRCALPHA)
            button_bg.fill((0, 0, 0, 180))  # Полупрозрачный черный
            screen.blit(button_bg, (SCREEN_WIDTH - 165, 15))
            
            # Рисуем кнопки поверх фона
            menu_button.draw()
            
        elif game_state == GAME_OVER:
            # Рисуем экран окончания игры
            game_over_text = font_large.render("ИГРА ОКОНЧЕНА", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            
            score_text = font_medium.render(f"Финальный счет: {score}", True, YELLOW)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            
            restart_text = font_small.render("Нажмите R для перезапуска или ESC для выхода в меню", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
            
        elif game_state == VICTORY:
            # Рисуем экран победы
            victory_text = font_large.render("ПОБЕДА!", True, GREEN)
            screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            
            score_text = font_medium.render(f"Финальный счет: {score}", True, YELLOW)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            
            restart_text = font_small.render("Нажмите R для перезапуска или ESC для выхода в меню", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    # For browser compatibility, don't call pygame.quit() and sys.exit()
    # pygame.quit()
    # sys.exit()

if __name__ == "__main__":
    main()