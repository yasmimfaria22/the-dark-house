import os
import math
import random
from collections import deque
from datetime import datetime

import pygame

pygame.init()
pygame.mixer.init()

# ==================================================
# PATHS / SCREEN
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Dark House")
clock = pygame.time.Clock()

# ==================================================
# COLORS / FONTS
# ==================================================

BACKGROUND_COLOR = (10, 8, 8)
TEXT_COLOR = (235, 235, 235)
SECONDARY_TEXT_COLOR = (155, 155, 155)
OBJECTIVE_COLOR = (245, 210, 90)
ROOM_COLOR = (185, 185, 185)
HEALTH_BACKGROUND = (60, 20, 20)
HEALTH_COLOR = (160, 35, 35)
GAME_OVER_COLOR = (190, 25, 25)
WIN_COLOR = (120, 220, 140)
MENU_TITLE_COLOR = (170, 30, 30)
BUTTON_COLOR = (28, 25, 25)
BUTTON_HOVER_COLOR = (75, 30, 30)
BUTTON_BORDER_COLOR = (150, 55, 55)
NOTE_COLOR = (215, 205, 165)

GRASS_COLOR = (20, 32, 23)
GRASS_DETAIL = (31, 49, 34)
DIRT_COLOR = (60, 48, 39)
DIRT_EDGE = (43, 35, 29)
FENCE_COLOR = (83, 61, 42)
FENCE_LIGHT = (108, 77, 50)
FENCE_DARK = (42, 31, 24)
TREE_TRUNK = (66, 43, 29)
TREE_TRUNK_LIGHT = (91, 57, 35)
TREE_LEAVES = (18, 39, 23)
TREE_LEAVES_LIGHT = (27, 55, 32)
STONE_COLOR = (70, 72, 68)
STONE_DARK = (45, 47, 44)
POWER_OFF_COLOR = (170, 40, 35)
POWER_ON_COLOR = (55, 190, 70)
FUSE_COLOR = (205, 180, 75)
MEDKIT_BODY = (205, 205, 195)
MEDKIT_BORDER = (80, 80, 75)
MEDKIT_RED = (175, 35, 35)

font = pygame.font.SysFont("arial", 23)
small_font = pygame.font.SysFont("arial", 18)
tiny_font = pygame.font.SysFont("arial", 15)
big_font = pygame.font.SysFont("arial", 55)
title_font = pygame.font.SysFont("arial", 72, bold=True)
button_font = pygame.font.SysFont("arial", 30, bold=True)
room_font = pygame.font.SysFont("arial", 19, bold=True)
chapter_font = pygame.font.SysFont("arial", 60, bold=True)

# ==================================================
# IMAGE HELPERS
# ==================================================


def load_sprite(filename, size):
    image = pygame.image.load(asset_path(filename)).convert_alpha()
    bounds = image.get_bounding_rect()
    if bounds.width > 0 and bounds.height > 0:
        image = image.subsurface(bounds).copy()
    return pygame.transform.scale(image, size)


def load_texture(filename, size):
    image = pygame.image.load(asset_path(filename)).convert()
    return pygame.transform.scale(image, size)


# ==================================================
# IMAGES
# ==================================================

PLAYER_SIZE = (48, 60)

player_sprites = {
    "down": {
        "idle": load_sprite("player_down_idle.png", PLAYER_SIZE),
        "walk": [
            load_sprite("player_down_1.png", PLAYER_SIZE),
            load_sprite("player_down_2.png", PLAYER_SIZE),
        ],
    },
    "up": {
        "idle": load_sprite("player_up_idle.png", PLAYER_SIZE),
        "walk": [
            load_sprite("player_up_1.png", PLAYER_SIZE),
            load_sprite("player_up_2.png", PLAYER_SIZE),
        ],
    },
    "left": {
        "idle": load_sprite("player_left_idle.png", PLAYER_SIZE),
        "walk": [
            load_sprite("player_left_1.png", PLAYER_SIZE),
            load_sprite("player_left_2.png", PLAYER_SIZE),
        ],
    },
    "right": {
        "idle": load_sprite("player_right_idle.png", PLAYER_SIZE),
        "walk": [
            load_sprite("player_right_1.png", PLAYER_SIZE),
            load_sprite("player_right_2.png", PLAYER_SIZE),
        ],
    },
}

key_image = load_sprite("key.png", (30, 30))
flashlight_image = load_sprite("flashlight.png", (42, 42))
door_image = load_sprite("door.png", (60, 110))
monster_image = load_sprite("monster.png", (85, 85))
floor_texture = load_texture("floor.png", (180, 180))
wall_texture = load_texture("wall.png", (100, 100))

bed_image = load_sprite("bed.png", (145, 90))
nightstand_image = load_sprite("nightstand.png", (55, 65))
table_image = load_sprite("table.png", (100, 70))
bookshelf_image = load_sprite("bookshelf.png", (60, 125))
wardrobe_image = load_sprite("wardrobe.png", (100, 115))
storage_table_image = load_sprite("storage_table.png", (85, 65))

# ==================================================
# SOUNDS
# ==================================================

key_sound = pygame.mixer.Sound(asset_path("key.wav"))
flashlight_sound = pygame.mixer.Sound(asset_path("flashlight.wav"))
door_sound = pygame.mixer.Sound(asset_path("door.wav"))
attack_sound = pygame.mixer.Sound(asset_path("attack.wav"))

key_sound.set_volume(0.55)
flashlight_sound.set_volume(0.65)
door_sound.set_volume(0.65)
attack_sound.set_volume(0.75)

pygame.mixer.music.load(asset_path("ambience.wav"))
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

# ==================================================
# CHAPTER 1 MAP
# ==================================================

LIVING_ROOM = pygame.Rect(110, 110, 290, 430)
HALLWAY = pygame.Rect(430, 110, 130, 430)
BEDROOM = pygame.Rect(590, 110, 300, 210)
STORAGE = pygame.Rect(590, 350, 300, 190)

chapter1_walls = [
    pygame.Rect(80, 80, 840, 30),
    pygame.Rect(80, 540, 840, 30),
    pygame.Rect(80, 80, 30, 490),
    pygame.Rect(890, 80, 30, 105),
    pygame.Rect(890, 265, 30, 305),
    pygame.Rect(400, 110, 30, 140),
    pygame.Rect(400, 350, 30, 190),
    pygame.Rect(560, 110, 30, 60),
    pygame.Rect(560, 245, 30, 155),
    pygame.Rect(560, 475, 30, 65),
    pygame.Rect(590, 320, 300, 30),
]

hallway_door = pygame.Rect(395, 250, 40, 100)
hallway_door_open = False

house_exit_door = pygame.Rect(885, 185, 40, 80)

first_key = pygame.Rect(315, 455, 30, 30)
key_collected = False
has_key = False

flashlight = pygame.Rect(475, 185, 40, 40)
flashlight_collected = False
has_flashlight = False

note = pygame.Rect(820, 180, 22, 16)
note_read = False
note_open = False

has_exit_key = False
wardrobe_searched = False

chapter1_medkit = pygame.Rect(675, 260, 34, 28)
chapter1_medkit_collected = False

# Visual centers stay fixed even though the hitboxes are smaller.
BOOKSHELF_CENTER = (152, 190)
LIVING_TABLE_CENTER = (280, 197)
BED_CENTER = (707, 165)
NIGHTSTAND_CENTER = (830, 180)
WARDROBE_CENTER = (812, 452)
STORAGE_TABLE_CENTER = (667, 447)

# Smaller, more natural collision boxes.
bookshelf_hitbox = pygame.Rect(138, 160, 28, 78)
living_table_hitbox = pygame.Rect(245, 188, 70, 27)
bed_hitbox = pygame.Rect(642, 150, 130, 47)
bedside_table_hitbox = pygame.Rect(813, 170, 34, 30)
wardrobe_hitbox = pygame.Rect(784, 426, 57, 64)
storage_table_hitbox = pygame.Rect(642, 437, 52, 27)

furniture_obstacles = [
    bookshelf_hitbox,
    living_table_hitbox,
    bed_hitbox,
    bedside_table_hitbox,
    wardrobe_hitbox,
    storage_table_hitbox,
]

# ==================================================
# CHAPTER 2 - THE YARD
# ==================================================

YARD_AREA = pygame.Rect(105, 105, 790, 440)

yard_fences = [
    pygame.Rect(80, 80, 840, 25),
    pygame.Rect(80, 550, 840, 25),
    pygame.Rect(80, 80, 25, 495),
    pygame.Rect(895, 80, 25, 190),
    pygame.Rect(895, 370, 25, 205),
]

yard_gate = pygame.Rect(890, 270, 35, 100)
gate_checked = False
gate_open = False

house_back = pygame.Rect(110, 410, 245, 130)

# (center_x, center_y, canopy_radius)
yard_trees = [
    (190, 190, 38),
    (420, 195, 42),
    (525, 355, 39),
    (665, 190, 38),
    (690, 455, 42),
    (820, 470, 36),
]

# Collision is only around the trunks, not the full canopy.
tree_hitboxes = [
    pygame.Rect(cx - 13, cy + 5, 26, 36)
    for cx, cy, _ in yard_trees
]

yard_fuse = pygame.Rect(275, 280, 28, 18)
yard_fuse_collected = False
has_yard_fuse = False

fuse_box = pygame.Rect(790, 455, 48, 58)
yard_power_on = False

yard_medkit_1 = pygame.Rect(335, 365, 34, 28)
yard_medkit_2 = pygame.Rect(775, 305, 34, 28)
yard_medkit_1_collected = False
yard_medkit_2_collected = False

# Fixed decoration positions so the scene does not randomly change every frame.
yard_stones = [
    (140, 305, 8),
    (245, 235, 6),
    (350, 145, 7),
    (475, 270, 8),
    (590, 500, 6),
    (750, 250, 7),
    (850, 420, 8),
]

yard_bushes = [
    (135, 150, 18),
    (295, 510, 17),
    (580, 155, 16),
    (745, 520, 17),
    (850, 170, 18),
]

yard_grass_tufts = [
    (135, 255), (165, 365), (225, 480), (310, 175), (365, 295),
    (455, 125), (500, 500), (560, 245), (620, 300), (735, 145),
    (755, 420), (845, 245), (860, 510), (450, 430), (325, 330),
]

# ==================================================
# PLAYER / HEALTH
# ==================================================

player = pygame.Rect(175, 350, 40, 40)
player_speed = 5
player_direction = "right"
player_moving = False
animation_frame = 0
last_animation_update = 0
animation_delay = 170

health = 100
max_health = 100
chapter2_start_health = 100

last_damage_time = 0
damage_cooldown = 1000

# ==================================================
# MONSTER
# ==================================================

monster = pygame.Rect(655, 455, 45, 45)
monster_active = False
monster_state = "inactive"
MONSTER_SEARCH_DURATION = 3500
last_seen_position = None
last_seen_time = 0

GRID_SIZE = 20
monster_path = []
monster_path_index = 0
last_path_update = 0
PATH_UPDATE_DELAY = 260
patrol_index = 0

# ==================================================
# GAME STATE / UI
# ==================================================

scene = "menu"
chapter = 1
message = "Find the key."

play_button = pygame.Rect(SCREEN_WIDTH // 2 - 140, 310, 280, 60)
how_to_play_button = pygame.Rect(SCREEN_WIDTH // 2 - 140, 390, 280, 60)
quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 140, 470, 280, 60)
back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 525, 200, 50)

darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
NO_FLASHLIGHT_DARKNESS = 185
FLASHLIGHT_DARKNESS = 172
flashlight_flickering = False
flashlight_flicker_end = 0
next_flashlight_flicker = 0
flashlight_flicker_strength = 0

# ==================================================
# MAP HELPERS
# ==================================================


def get_walk_area():
    if chapter == 1:
        return pygame.Rect(110, 110, 780, 430)
    return YARD_AREA


def get_chapter1_obstacles():
    obstacles = chapter1_walls.copy() + furniture_obstacles.copy()
    if not hallway_door_open:
        obstacles.append(hallway_door)
    obstacles.append(house_exit_door)
    return obstacles


def get_chapter2_obstacles():
    obstacles = yard_fences.copy() + tree_hitboxes.copy()
    obstacles.append(house_back)
    obstacles.append(fuse_box)
    if not gate_open:
        obstacles.append(yard_gate)
    return obstacles


def get_solid_obstacles():
    return get_chapter1_obstacles() if chapter == 1 else get_chapter2_obstacles()


def get_patrol_points():
    if chapter == 1:
        return [
            pygame.Vector2(680, 450),
            pygame.Vector2(500, 440),
            pygame.Vector2(500, 210),
            pygame.Vector2(700, 245),
            pygame.Vector2(500, 300),
        ]

    return [
        pygame.Vector2(570, 170),
        pygame.Vector2(790, 205),
        pygame.Vector2(760, 385),
        pygame.Vector2(470, 485),
        pygame.Vector2(300, 330),
    ]


def get_monster_patrol_speed():
    return 1 if chapter == 1 else 2


def get_monster_search_speed():
    return 2 if chapter == 1 else 3


def get_monster_chase_speed():
    return 3 if chapter == 1 else 4


def get_current_area():
    if chapter == 2:
        if yard_gate.inflate(150, 160).collidepoint(player.center):
            return "OLD GATE"
        if fuse_box.inflate(130, 130).collidepoint(player.center):
            return "POWER BOX"
        return "THE YARD"

    center = player.center
    if LIVING_ROOM.collidepoint(center):
        return "LIVING ROOM"
    if HALLWAY.collidepoint(center):
        return "HALLWAY"
    if BEDROOM.collidepoint(center):
        return "BEDROOM"
    if STORAGE.collidepoint(center):
        return "STORAGE"
    return "HOUSE"


def get_objective():
    if chapter == 1:
        if not key_collected:
            return "Find the key"
        if not hallway_door_open:
            return "Unlock the hallway door"
        if not flashlight_collected:
            return "Find the flashlight"
        if not note_read:
            return "Find and read the note in the bedroom"
        if not has_exit_key:
            return "Search the wardrobe in storage"
        return "Leave the house"

    if not gate_checked:
        return "Find the main gate"
    if not yard_fuse_collected:
        return "Find the missing fuse"
    if not yard_power_on:
        return "Restore power at the fuse box"
    return "Open the main gate"


def get_objective_target():
    if chapter == 1:
        if not key_collected:
            return first_key.center
        if not hallway_door_open:
            return hallway_door.center
        if not flashlight_collected:
            return flashlight.center
        if not note_read:
            return note.center
        if not has_exit_key:
            return WARDROBE_CENTER
        return house_exit_door.center

    if not gate_checked:
        return yard_gate.center
    if not yard_fuse_collected:
        return yard_fuse.center
    if not yard_power_on:
        return fuse_box.center
    return yard_gate.center

# ==================================================
# MOVEMENT / PLAYER
# ==================================================


def move_object(object_rect, move_x, move_y, obstacles):
    object_rect.x += move_x

    for obstacle in obstacles:
        if object_rect.colliderect(obstacle):
            if move_x > 0:
                object_rect.right = obstacle.left
            elif move_x < 0:
                object_rect.left = obstacle.right

    object_rect.y += move_y

    for obstacle in obstacles:
        if object_rect.colliderect(obstacle):
            if move_y > 0:
                object_rect.bottom = obstacle.top
            elif move_y < 0:
                object_rect.top = obstacle.bottom


def update_player_animation():
    global animation_frame, last_animation_update

    if not player_moving:
        animation_frame = 0
        return

    current_time = pygame.time.get_ticks()
    if current_time - last_animation_update >= animation_delay:
        animation_frame = (animation_frame + 1) % 2
        last_animation_update = current_time


def draw_player():
    if player_moving:
        current_image = player_sprites[player_direction]["walk"][animation_frame]
    else:
        current_image = player_sprites[player_direction]["idle"]

    screen.blit(current_image, current_image.get_rect(center=player.center))

# ==================================================
# TEXTURES / CHAPTER 1 VISUALS
# ==================================================


def draw_tiled_texture(texture, rect):
    old_clip = screen.get_clip()
    screen.set_clip(rect)

    texture_width = texture.get_width()
    texture_height = texture.get_height()

    y = rect.top
    while y < rect.bottom:
        x = rect.left
        while x < rect.right:
            screen.blit(texture, (x, y))
            x += texture_width
        y += texture_height

    screen.set_clip(old_clip)


def draw_chapter1_floor():
    draw_tiled_texture(floor_texture, LIVING_ROOM)
    draw_tiled_texture(floor_texture, HALLWAY)
    draw_tiled_texture(floor_texture, BEDROOM)
    draw_tiled_texture(floor_texture, STORAGE)


def draw_chapter1_walls():
    for wall in chapter1_walls:
        draw_tiled_texture(wall_texture, wall)


def draw_sprite_at(image, center):
    screen.blit(image, image.get_rect(center=center))


def draw_chapter1_furniture():
    draw_sprite_at(bookshelf_image, BOOKSHELF_CENTER)
    draw_sprite_at(table_image, LIVING_TABLE_CENTER)
    draw_sprite_at(bed_image, BED_CENTER)
    draw_sprite_at(nightstand_image, NIGHTSTAND_CENTER)
    draw_sprite_at(wardrobe_image, WARDROBE_CENTER)
    draw_sprite_at(storage_table_image, STORAGE_TABLE_CENTER)

    pygame.draw.rect(screen, NOTE_COLOR, note)
    pygame.draw.line(
        screen,
        (90, 75, 55),
        (note.left + 3, note.top + 5),
        (note.right - 3, note.top + 5),
        1,
    )


def draw_floor_crack(x, y):
    color = (42, 38, 36)
    points = [(x, y), (x + 8, y + 5), (x + 3, y + 12), (x + 13, y + 18), (x + 9, y + 27)]
    pygame.draw.lines(screen, color, False, points, 1)
    pygame.draw.line(screen, color, (x + 4, y + 11), (x - 4, y + 17), 1)
    pygame.draw.line(screen, color, (x + 12, y + 18), (x + 20, y + 14), 1)


def draw_dark_stain(x, y, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (45, 26, 22, 95), (0, height // 4, width, height // 2))
    pygame.draw.ellipse(surface, (55, 30, 24, 60), (width // 4, 0, width // 2, height))
    screen.blit(surface, (x, y))


def draw_bloodstain(x, y):
    pygame.draw.circle(screen, (72, 12, 12), (x, y), 11)
    pygame.draw.circle(screen, (45, 8, 8), (x + 8, y + 5), 6)
    pygame.draw.circle(screen, (72, 12, 12), (x - 11, y + 8), 4)
    pygame.draw.line(screen, (72, 12, 12), (x + 4, y + 7), (x + 25, y + 22), 4)


def draw_old_papers(x, y):
    color = (150, 138, 110)
    dark = (85, 76, 62)
    rects = [
        pygame.Rect(x, y, 20, 15),
        pygame.Rect(x + 13, y + 11, 22, 16),
        pygame.Rect(x - 8, y + 17, 18, 13),
    ]
    for rect in rects:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.line(screen, dark, (rect.left + 4, rect.top + 5), (rect.right - 4, rect.top + 5), 1)


def draw_scratch_marks(x, y):
    for offset in range(0, 24, 6):
        pygame.draw.line(screen, (100, 88, 78), (x + offset, y), (x + offset - 7, y + 25), 2)


def draw_chapter1_decorations():
    draw_floor_crack(190, 285)
    draw_dark_stain(300, 310, 55, 32)
    draw_old_papers(145, 430)
    draw_floor_crack(485, 365)
    draw_scratch_marks(520, 280)
    draw_dark_stain(720, 255, 45, 25)
    draw_floor_crack(610, 265)
    draw_bloodstain(735, 455)
    draw_old_papers(605, 375)

# ==================================================
# MEDKIT
# ==================================================


def draw_medkit(rect):
    shadow_rect = rect.move(3, 4)
    pygame.draw.rect(screen, (20, 20, 20), shadow_rect, border_radius=4)
    pygame.draw.rect(screen, MEDKIT_BODY, rect, border_radius=4)
    pygame.draw.rect(screen, MEDKIT_BORDER, rect, 2, border_radius=4)

    pygame.draw.rect(screen, MEDKIT_RED, (rect.centerx - 3, rect.centery - 9, 6, 18))
    pygame.draw.rect(screen, MEDKIT_RED, (rect.centerx - 9, rect.centery - 3, 18, 6))


def use_medkit():
    global health, message

    old_health = health
    health = min(max_health, health + 20)
    restored = health - old_health
    message = f"You used a medkit. +{restored} Health"

# ==================================================
# CHAPTER 2 VISUALS
# ==================================================


def draw_grass():
    pygame.draw.rect(screen, GRASS_COLOR, YARD_AREA)

    for x, y in yard_grass_tufts:
        pygame.draw.line(screen, GRASS_DETAIL, (x, y), (x + 3, y - 8), 2)
        pygame.draw.line(screen, GRASS_DETAIL, (x + 4, y), (x + 8, y - 6), 1)
        pygame.draw.line(screen, GRASS_DETAIL, (x - 3, y), (x - 6, y - 5), 1)


def draw_yard_path():
    # Main dirt path from the house to the gate.
    main_path = [
        (330, 505),
        (390, 520),
        (470, 490),
        (550, 450),
        (640, 415),
        (725, 375),
        (820, 345),
        (895, 340),
        (895, 295),
        (810, 305),
        (710, 335),
        (620, 375),
        (530, 415),
        (450, 455),
        (375, 475),
        (330, 470),
    ]

    pygame.draw.polygon(screen, DIRT_EDGE, main_path)

    inner_path = [
        (340, 495),
        (395, 505),
        (470, 478),
        (555, 438),
        (645, 403),
        (730, 365),
        (820, 335),
        (895, 330),
        (895, 307),
        (815, 315),
        (715, 345),
        (625, 385),
        (540, 425),
        (455, 465),
        (390, 486),
        (340, 480),
    ]

    pygame.draw.polygon(screen, DIRT_COLOR, inner_path)

    # Branch to the power box.
    pygame.draw.polygon(
        screen,
        DIRT_EDGE,
        [(650, 405), (695, 420), (760, 455), (812, 500), (830, 480), (780, 435), (710, 395), (665, 380)],
    )
    pygame.draw.polygon(
        screen,
        DIRT_COLOR,
        [(665, 400), (705, 414), (765, 448), (811, 487), (819, 478), (773, 440), (713, 405), (672, 390)],
    )

    # Small worn patches.
    for x, y in [(435, 485), (540, 430), (665, 380), (790, 330), (735, 430)]:
        pygame.draw.ellipse(screen, (73, 57, 44), (x, y, 18, 8))


def draw_yard_stones_and_bushes():
    for x, y, radius in yard_stones:
        pygame.draw.ellipse(screen, STONE_DARK, (x - radius, y - radius // 2, radius * 2, radius))
        pygame.draw.ellipse(screen, STONE_COLOR, (x - radius + 1, y - radius // 2 - 1, radius * 2 - 2, radius - 1))

    for x, y, radius in yard_bushes:
        pygame.draw.circle(screen, (14, 29, 17), (x, y), radius)
        pygame.draw.circle(screen, (24, 47, 27), (x - 7, y - 5), max(5, radius - 7))
        pygame.draw.circle(screen, (20, 40, 23), (x + 8, y + 3), max(4, radius - 9))


def draw_fence_rect(rect):
    pygame.draw.rect(screen, FENCE_DARK, rect)
    pygame.draw.rect(screen, FENCE_COLOR, rect, 3)

    # Add repeating boards / posts.
    if rect.width > rect.height:
        for x in range(rect.left + 12, rect.right, 34):
            pygame.draw.line(screen, FENCE_LIGHT, (x, rect.top + 3), (x, rect.bottom - 3), 3)
    else:
        for y in range(rect.top + 12, rect.bottom, 34):
            pygame.draw.line(screen, FENCE_LIGHT, (rect.left + 3, y), (rect.right - 3, y), 3)


def draw_tree(center_x, center_y, canopy_radius):
    # Shadow.
    shadow = pygame.Surface((canopy_radius * 2 + 30, canopy_radius + 30), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
    screen.blit(shadow, (center_x - canopy_radius - 15, center_y + 18))

    # Trunk.
    pygame.draw.rect(screen, TREE_TRUNK, (center_x - 9, center_y + 5, 18, 38))
    pygame.draw.rect(screen, TREE_TRUNK_LIGHT, (center_x - 5, center_y + 8, 5, 30))

    # Layered canopy.
    pygame.draw.circle(screen, TREE_LEAVES, (center_x, center_y), canopy_radius)
    pygame.draw.circle(screen, TREE_LEAVES_LIGHT, (center_x - canopy_radius // 3, center_y - canopy_radius // 3), canopy_radius // 2)
    pygame.draw.circle(screen, (14, 32, 19), (center_x + canopy_radius // 3, center_y + 4), canopy_radius // 2)


def draw_yard_gate():
    # Gate frame.
    pygame.draw.rect(screen, FENCE_DARK, yard_gate)
    pygame.draw.rect(screen, FENCE_LIGHT, yard_gate, 4)

    # Iron bars.
    for x in range(yard_gate.left + 7, yard_gate.right - 2, 8):
        pygame.draw.line(screen, (95, 83, 69), (x, yard_gate.top + 6), (x, yard_gate.bottom - 6), 2)

    pygame.draw.line(
        screen,
        (95, 83, 69),
        (yard_gate.left + 4, yard_gate.centery),
        (yard_gate.right - 4, yard_gate.centery),
        3,
    )

    light_color = POWER_ON_COLOR if yard_power_on else POWER_OFF_COLOR
    pygame.draw.circle(screen, (20, 20, 20), (yard_gate.left - 9, yard_gate.centery), 8)
    pygame.draw.circle(screen, light_color, (yard_gate.left - 9, yard_gate.centery), 5)


def draw_house_back():
    # House shadow.
    pygame.draw.rect(screen, (18, 14, 14), house_back.move(6, 8))

    # House body.
    pygame.draw.rect(screen, (40, 31, 29), house_back)
    pygame.draw.rect(screen, (87, 61, 47), house_back, 4)

    # Roof.
    roof_points = [
        (house_back.left - 12, house_back.top + 5),
        (house_back.centerx, house_back.top - 52),
        (house_back.right + 12, house_back.top + 5),
    ]
    pygame.draw.polygon(screen, (25, 20, 20), roof_points)
    pygame.draw.lines(screen, (70, 50, 42), False, roof_points, 4)

    # Back door.
    door_rect = pygame.Rect(house_back.right - 78, house_back.top + 48, 45, 82)
    pygame.draw.rect(screen, (48, 34, 29), door_rect)
    pygame.draw.rect(screen, (94, 66, 48), door_rect, 3)
    pygame.draw.circle(screen, (160, 130, 75), (door_rect.right - 8, door_rect.centery), 3)

    # Window.
    window = pygame.Rect(house_back.left + 34, house_back.top + 38, 52, 40)
    pygame.draw.rect(screen, (14, 20, 24), window)
    pygame.draw.rect(screen, (78, 72, 62), window, 3)
    pygame.draw.line(screen, (78, 72, 62), (window.centerx, window.top), (window.centerx, window.bottom), 2)
    pygame.draw.line(screen, (78, 72, 62), (window.left, window.centery), (window.right, window.centery), 2)

    label = tiny_font.render("THE HOUSE", True, SECONDARY_TEXT_COLOR)
    screen.blit(label, (house_back.left + 72, house_back.top + 88))


def draw_fuse():
    if yard_fuse_collected:
        return

    pygame.draw.rect(screen, (35, 30, 20), yard_fuse.move(2, 3), border_radius=3)
    pygame.draw.rect(screen, FUSE_COLOR, yard_fuse, border_radius=3)
    pygame.draw.rect(screen, (90, 80, 45), yard_fuse, 2, border_radius=3)
    pygame.draw.line(
        screen,
        (230, 220, 150),
        (yard_fuse.left + 5, yard_fuse.centery),
        (yard_fuse.right - 5, yard_fuse.centery),
        2,
    )


def draw_fuse_box():
    box_color = (55, 90, 55) if yard_power_on else (52, 52, 50)
    light_color = POWER_ON_COLOR if yard_power_on else POWER_OFF_COLOR

    # Concrete base.
    pygame.draw.rect(screen, (55, 55, 52), (fuse_box.x - 7, fuse_box.bottom - 4, fuse_box.width + 14, 12))

    # Box.
    pygame.draw.rect(screen, (20, 20, 20), fuse_box.move(4, 5))
    pygame.draw.rect(screen, box_color, fuse_box)
    pygame.draw.rect(screen, (120, 120, 110), fuse_box, 3)

    # Small warning symbol.
    pygame.draw.polygon(
        screen,
        (170, 145, 65),
        [
            (fuse_box.centerx, fuse_box.top + 16),
            (fuse_box.centerx - 8, fuse_box.top + 32),
            (fuse_box.centerx + 8, fuse_box.top + 32),
        ],
        2,
    )

    pygame.draw.circle(screen, (20, 20, 20), (fuse_box.centerx, fuse_box.top + 9), 7)
    pygame.draw.circle(screen, light_color, (fuse_box.centerx, fuse_box.top + 9), 4)

    # Cable to the gate.
    pygame.draw.line(
        screen,
        (26, 24, 23),
        (fuse_box.centerx, fuse_box.top),
        (860, 360),
        3,
    )


def draw_yard_fog():
    fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    t = pygame.time.get_ticks() * 0.02

    fog_specs = [
        (220 + math.sin(t * 0.7) * 25, 250, 210, 45, 18),
        (560 + math.sin(t * 0.5 + 1.2) * 30, 300, 250, 55, 16),
        (760 + math.sin(t * 0.6 + 2.1) * 20, 500, 190, 40, 14),
    ]

    for x, y, width, height, alpha in fog_specs:
        pygame.draw.ellipse(fog, (180, 190, 185, alpha), (int(x), y, width, height))

    screen.blit(fog, (0, 0))


def draw_chapter2():
    screen.fill(BACKGROUND_COLOR)
    draw_grass()
    draw_yard_path()
    draw_yard_stones_and_bushes()

    for fence in yard_fences:
        draw_fence_rect(fence)

    draw_house_back()

    for center_x, center_y, canopy_radius in yard_trees:
        draw_tree(center_x, center_y, canopy_radius)

    draw_yard_gate()
    draw_fuse()
    draw_fuse_box()

    if not yard_medkit_1_collected:
        draw_medkit(yard_medkit_1)

    if not yard_medkit_2_collected:
        draw_medkit(yard_medkit_2)

    draw_yard_fog()

# ==================================================
# FLASHLIGHT
# ==================================================


def get_flashlight_angle():
    if player_direction == "right":
        return 0
    if player_direction == "down":
        return math.pi / 2
    if player_direction == "left":
        return math.pi
    return -math.pi / 2


def light_hits_obstacle(point, obstacles):
    x = int(point.x)
    y = int(point.y)

    for obstacle in obstacles:
        if obstacle.collidepoint(x, y):
            return True
    return False


def cast_light_ray(origin, angle, max_distance, obstacles):
    direction = pygame.Vector2(math.cos(angle), math.sin(angle))
    last_safe_point = pygame.Vector2(origin)

    for distance in range(4, max_distance + 1, 4):
        point = origin + direction * distance
        if light_hits_obstacle(point, obstacles):
            return last_safe_point
        last_safe_point = point

    return last_safe_point


def update_flashlight_flicker():
    global flashlight_flickering
    global flashlight_flicker_end
    global next_flashlight_flicker
    global flashlight_flicker_strength

    if not has_flashlight:
        flashlight_flickering = False
        flashlight_flicker_strength = 0
        next_flashlight_flicker = 0
        return

    current_time = pygame.time.get_ticks()

    if next_flashlight_flicker == 0:
        next_flashlight_flicker = current_time + random.randint(2500, 6000)

    if flashlight_flickering:
        if current_time >= flashlight_flicker_end:
            flashlight_flickering = False
            flashlight_flicker_strength = 0
            next_flashlight_flicker = current_time + random.randint(2500, 6500)
    elif current_time >= next_flashlight_flicker:
        flashlight_flickering = True
        flashlight_flicker_strength = random.randint(25, 50)
        flashlight_flicker_end = current_time + random.randint(70, 180)


def draw_darkness():
    if not has_flashlight:
        darkness.fill((0, 0, 0, NO_FLASHLIGHT_DARKNESS))
        pygame.draw.circle(darkness, (0, 0, 0, 0), player.center, 125)
        screen.blit(darkness, (0, 0))
        return

    ambient_alpha = min(245, FLASHLIGHT_DARKNESS + flashlight_flicker_strength)
    darkness.fill((0, 0, 0, ambient_alpha))

    origin = pygame.Vector2(player.center)
    obstacles = get_solid_obstacles()
    center_angle = get_flashlight_angle()

    if flashlight_flickering:
        beam_length = 295
        half_angle = math.radians(29)
        beam_alpha = 45
        glow_radius = 40
    else:
        beam_length = 365
        half_angle = math.radians(35)
        beam_alpha = 0
        glow_radius = 58

    ray_count = 75
    beam_points = [(int(origin.x), int(origin.y))]

    for ray_number in range(ray_count):
        percentage = ray_number / (ray_count - 1)
        angle = center_angle - half_angle + percentage * half_angle * 2
        ray_end = cast_light_ray(origin, angle, beam_length, obstacles)
        beam_points.append((int(ray_end.x), int(ray_end.y)))

    pygame.draw.polygon(darkness, (0, 0, 0, beam_alpha), beam_points)
    pygame.draw.circle(darkness, (0, 0, 0, beam_alpha), player.center, glow_radius)
    screen.blit(darkness, (0, 0))

# ==================================================
# HEALTH / MONSTER AI
# ==================================================


def draw_health():
    bar_width = 180
    bar_height = 20

    pygame.draw.rect(screen, HEALTH_BACKGROUND, (795, 25, bar_width, bar_height))
    current_width = int(bar_width * health / max_health)
    pygame.draw.rect(screen, HEALTH_COLOR, (795, 25, current_width, bar_height))

    health_text = tiny_font.render(f"Health: {health}", True, TEXT_COLOR)
    screen.blit(health_text, (795, 50))


def has_line_of_sight(start, end, obstacles):
    start = pygame.Vector2(start)
    end = pygame.Vector2(end)
    direction = end - start
    distance = direction.length()

    if distance == 0:
        return True

    direction = direction.normalize()
    travelled = 7

    while travelled < distance:
        point = start + direction * travelled
        for obstacle in obstacles:
            if obstacle.collidepoint(int(point.x), int(point.y)):
                return False
        travelled += 7

    return True


def monster_can_see_player(obstacles):
    distance = pygame.Vector2(player.center).distance_to(monster.center)
    vision_distance = 320 if chapter == 1 else 370

    if distance > vision_distance:
        return False

    return has_line_of_sight(monster.center, player.center, obstacles)


def point_to_cell(point):
    area = get_walk_area()
    column = int((point[0] - area.left) // GRID_SIZE)
    row = int((point[1] - area.top) // GRID_SIZE)
    return column, row


def cell_to_center(cell):
    area = get_walk_area()
    column, row = cell
    return pygame.Vector2(
        area.left + column * GRID_SIZE + GRID_SIZE // 2,
        area.top + row * GRID_SIZE + GRID_SIZE // 2,
    )


def cell_is_walkable(cell, obstacles):
    area = get_walk_area()
    columns = area.width // GRID_SIZE
    rows = area.height // GRID_SIZE

    if cell[0] < 0 or cell[1] < 0 or cell[0] >= columns or cell[1] >= rows:
        return False

    center = cell_to_center(cell)
    test_rect = pygame.Rect(0, 0, monster.width, monster.height)
    test_rect.center = (round(center.x), round(center.y))

    for obstacle in obstacles:
        if test_rect.colliderect(obstacle):
            return False

    return True


def nearest_walkable_cell(point, obstacles):
    base_cell = point_to_cell(point)

    if cell_is_walkable(base_cell, obstacles):
        return base_cell

    for radius in range(1, 9):
        candidates = []

        for x_offset in range(-radius, radius + 1):
            for y_offset in range(-radius, radius + 1):
                cell = (base_cell[0] + x_offset, base_cell[1] + y_offset)
                if cell_is_walkable(cell, obstacles):
                    candidates.append(cell)

        if candidates:
            candidates.sort(key=lambda candidate: cell_to_center(candidate).distance_to(point))
            return candidates[0]

    return None


def find_path(start_point, target_point, obstacles):
    start_cell = nearest_walkable_cell(start_point, obstacles)
    target_cell = nearest_walkable_cell(target_point, obstacles)

    if start_cell is None or target_cell is None:
        return []

    queue = deque([start_cell])
    came_from = {start_cell: None}
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        current = queue.popleft()

        if current == target_cell:
            break

        for direction in directions:
            neighbour = (current[0] + direction[0], current[1] + direction[1])

            if neighbour in came_from:
                continue
            if not cell_is_walkable(neighbour, obstacles):
                continue

            came_from[neighbour] = current
            queue.append(neighbour)

    if target_cell not in came_from:
        return []

    cells = []
    current = target_cell

    while current is not None:
        cells.append(current)
        current = came_from[current]

    cells.reverse()
    return [cell_to_center(cell) for cell in cells[1:]]


def create_monster_path(target, obstacles):
    global monster_path, monster_path_index, last_path_update

    monster_path = find_path(monster.center, target, obstacles)
    monster_path_index = 0
    last_path_update = pygame.time.get_ticks()


def move_monster_toward(target, obstacles, speed):
    direction = pygame.Vector2(target) - pygame.Vector2(monster.center)

    if direction.length() == 0:
        return

    direction = direction.normalize() * speed
    move_object(monster, round(direction.x), round(direction.y), obstacles)


def follow_monster_path(obstacles, speed):
    global monster_path_index

    if not monster_path or monster_path_index >= len(monster_path):
        return

    target = monster_path[monster_path_index]

    if pygame.Vector2(monster.center).distance_to(target) < 13:
        monster_path_index += 1
        if monster_path_index >= len(monster_path):
            return
        target = monster_path[monster_path_index]

    move_monster_toward(target, obstacles, speed)


def update_monster_ai():
    global monster_state
    global last_seen_position
    global last_seen_time
    global patrol_index
    global monster_path
    global monster_path_index
    global last_path_update

    if not monster_active:
        return

    current_time = pygame.time.get_ticks()
    obstacles = get_solid_obstacles()
    sees_player = monster_can_see_player(obstacles)

    if sees_player:
        monster_state = "chase"
        last_seen_position = pygame.Vector2(player.center)
        last_seen_time = current_time

        if current_time - last_path_update >= PATH_UPDATE_DELAY:
            create_monster_path(player.center, obstacles)

        if monster_path:
            follow_monster_path(obstacles, get_monster_chase_speed())
        else:
            move_monster_toward(player.center, obstacles, get_monster_chase_speed())
        return

    if monster_state == "chase":
        monster_state = "search"
        if last_seen_position is not None:
            create_monster_path(last_seen_position, obstacles)

    if monster_state == "search":
        if current_time - last_seen_time > MONSTER_SEARCH_DURATION:
            monster_state = "patrol"
            monster_path = []
            monster_path_index = 0
        else:
            follow_monster_path(obstacles, get_monster_search_speed())
            return

    if monster_state in ("patrol", "inactive"):
        monster_state = "patrol"
        patrol_points = get_patrol_points()

        if patrol_index >= len(patrol_points):
            patrol_index = 0

        target = patrol_points[patrol_index]
        distance = pygame.Vector2(monster.center).distance_to(target)

        if distance < 30:
            patrol_index = (patrol_index + 1) % len(patrol_points)
            target = patrol_points[patrol_index]
            create_monster_path(target, obstacles)

        if current_time - last_path_update >= 700:
            create_monster_path(target, obstacles)

        follow_monster_path(obstacles, get_monster_patrol_speed())

# ==================================================
# OBJECTIVE / LABELS / NOTE
# ==================================================


def draw_objective_marker():
    target = get_objective_target()
    pulse = 9 + int(3 * abs(math.sin(pygame.time.get_ticks() * 0.005)))

    pygame.draw.circle(screen, OBJECTIVE_COLOR, target, pulse, 2)
    marker_text = room_font.render("!", True, OBJECTIVE_COLOR)
    screen.blit(marker_text, marker_text.get_rect(center=(target[0], target[1] - 22)))


def draw_chapter1_labels():
    labels = [
        ("LIVING ROOM", (255, 500)),
        ("HALLWAY", (495, 505)),
        ("BEDROOM", (735, 285)),
        ("STORAGE", (735, 505)),
    ]

    for text, position in labels:
        label = tiny_font.render(text, True, (165, 165, 165))
        label.set_alpha(155)
        screen.blit(label, label.get_rect(center=position))


def draw_note_overlay():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 215))
    screen.blit(overlay, (0, 0))

    paper = pygame.Rect(225, 125, 550, 400)
    pygame.draw.rect(screen, (210, 200, 170), paper, border_radius=7)
    pygame.draw.rect(screen, (70, 55, 40), paper, 4, border_radius=7)

    title = font.render("June 14", True, (45, 35, 30))
    screen.blit(title, (275, 170))

    lines = [
        "I hid the spare exit key in the old wardrobe.",
        "The wardrobe is in the storage room.",
        "That thing is still walking through the house.",
        "If it sees you, break its line of sight.",
        "Do not stay in the hallway.",
    ]

    y = 225
    for line in lines:
        text = small_font.render(line, True, (45, 35, 30))
        screen.blit(text, (275, y))
        y += 42

    close_text = small_font.render("Press E or ESC to close", True, (65, 50, 40))
    screen.blit(close_text, close_text.get_rect(center=(SCREEN_WIDTH // 2, 485)))

# ==================================================
# MENU / HOW TO PLAY / TRANSITIONS
# ==================================================


def draw_button(button_rect, text):
    hovering = button_rect.collidepoint(pygame.mouse.get_pos())
    color = BUTTON_HOVER_COLOR if hovering else BUTTON_COLOR

    pygame.draw.rect(screen, color, button_rect, border_radius=8)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 2, border_radius=8)

    surface = button_font.render(text, True, TEXT_COLOR)
    screen.blit(surface, surface.get_rect(center=button_rect.center))


def draw_menu():
    draw_tiled_texture(floor_texture, screen.get_rect())

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    screen.blit(overlay, (0, 0))

    shadow = title_font.render("THE DARK HOUSE", True, (40, 0, 0))
    screen.blit(shadow, shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 178)))

    title = title_font.render("THE DARK HOUSE", True, MENU_TITLE_COLOR)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 174)))

    subtitle = small_font.render("Some doors should never be opened.", True, SECONDARY_TEXT_COLOR)
    screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 235)))

    draw_button(play_button, "PLAY")
    draw_button(how_to_play_button, "HOW TO PLAY")
    draw_button(quit_button, "QUIT")

    creator_text = tiny_font.render(
        "A game by Yasmim Faria",
        True,
        SECONDARY_TEXT_COLOR
    )
    screen.blit(
        creator_text,
        creator_text.get_rect(
            center=(SCREEN_WIDTH // 2, 585)
        )
    )


def draw_how_to_play():
    screen.fill((12, 10, 10))

    title = big_font.render("HOW TO PLAY", True, MENU_TITLE_COLOR)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 65)))

    sections = [
        ("CONTROLS", ["WASD  - Move", "E     - Interact", "ESC   - Menu / Close"]),
        ("OBJECTIVE", ["Follow the objective at the top of the screen.", "The yellow ! marks the next important location."]),
        ("MEDKITS", ["Walk over a medkit to use it automatically.", "Each medkit restores up to 20 Health."]),
        ("FLASHLIGHT", ["The flashlight illuminates the direction you are facing.", "Its light may fail for a moment."]),
        ("MONSTER", ["Break its line of sight using walls, furniture and trees.", "The creature is faster in Chapter 2."]),
        ("HEALTH", ["Your remaining Health carries from Chapter 1 into Chapter 2."]),
    ]

    y = 105
    for section_title, lines in sections:
        heading = room_font.render(section_title, True, OBJECTIVE_COLOR)
        screen.blit(heading, (165, y))
        y += 26

        for line in lines:
            text = small_font.render(line, True, TEXT_COLOR)
            screen.blit(text, (195, y))
            y += 22

        y += 8

    draw_button(back_button, "BACK")


def draw_chapter_transition():
    screen.fill((5, 5, 5))

    complete = small_font.render("CHAPTER 1 COMPLETE", True, SECONDARY_TEXT_COLOR)
    screen.blit(complete, complete.get_rect(center=(SCREEN_WIDTH // 2, 200)))

    title = chapter_font.render("CHAPTER 2", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 275)))

    subtitle = big_font.render("THE YARD", True, MENU_TITLE_COLOR)
    screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 345)))

    health_text = small_font.render(f"Health remaining: {health}", True, HEALTH_COLOR)
    screen.blit(health_text, health_text.get_rect(center=(SCREEN_WIDTH // 2, 405)))

    story = small_font.render("You made it outside. The gate is still locked.", True, SECONDARY_TEXT_COLOR)
    screen.blit(story, story.get_rect(center=(SCREEN_WIDTH // 2, 445)))

    continue_text = small_font.render("Press ENTER to continue", True, OBJECTIVE_COLOR)
    screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, 505)))

# ==================================================
# RESET / CHAPTER SETUP
# ==================================================


def reset_monster_ai():
    global monster_state
    global last_seen_position
    global last_seen_time
    global monster_path
    global monster_path_index
    global last_path_update
    global patrol_index

    monster_state = "inactive"
    last_seen_position = None
    last_seen_time = 0
    monster_path = []
    monster_path_index = 0
    last_path_update = 0
    patrol_index = 0


def reset_flashlight_flicker():
    global flashlight_flickering
    global flashlight_flicker_end
    global next_flashlight_flicker
    global flashlight_flicker_strength

    flashlight_flickering = False
    flashlight_flicker_end = 0
    next_flashlight_flicker = 0
    flashlight_flicker_strength = 0


def reset_chapter1():
    global chapter
    global health
    global chapter2_start_health
    global last_damage_time
    global hallway_door_open
    global key_collected
    global has_key
    global flashlight_collected
    global has_flashlight
    global note_read
    global note_open
    global has_exit_key
    global wardrobe_searched
    global chapter1_medkit_collected
    global monster_active
    global player_direction
    global player_moving
    global animation_frame
    global last_animation_update
    global message

    chapter = 1

    player.x = 175
    player.y = 350
    player_direction = "right"
    player_moving = False
    animation_frame = 0
    last_animation_update = 0

    health = 100
    chapter2_start_health = 100
    last_damage_time = 0

    hallway_door_open = False
    key_collected = False
    has_key = False
    flashlight_collected = False
    has_flashlight = False
    note_read = False
    note_open = False
    has_exit_key = False
    wardrobe_searched = False
    chapter1_medkit_collected = False

    monster.x = 655
    monster.y = 455
    monster_active = False

    reset_monster_ai()
    reset_flashlight_flicker()

    message = "Find the key."


def setup_chapter2(preserve_health=True):
    global chapter
    global health
    global chapter2_start_health
    global last_damage_time
    global gate_checked
    global gate_open
    global yard_fuse_collected
    global has_yard_fuse
    global yard_power_on
    global yard_medkit_1_collected
    global yard_medkit_2_collected
    global monster_active
    global player_direction
    global player_moving
    global animation_frame
    global last_animation_update
    global message

    chapter = 2

    if preserve_health:
        chapter2_start_health = health
    else:
        health = chapter2_start_health

    player.x = 390
    player.y = 475
    player_direction = "right"
    player_moving = False
    animation_frame = 0
    last_animation_update = 0
    last_damage_time = 0

    gate_checked = False
    gate_open = False
    yard_fuse_collected = False
    has_yard_fuse = False
    yard_power_on = False
    yard_medkit_1_collected = False
    yard_medkit_2_collected = False

    monster.x = 565
    monster.y = 245
    monster_active = False

    reset_monster_ai()
    reset_flashlight_flicker()

    message = "Find a way out of the yard."


def restart_current_chapter():
    if chapter == 1:
        reset_chapter1()
    else:
        setup_chapter2(preserve_health=False)

# ==================================================
# HUD / DRAW GAME
# ==================================================


def draw_hud():
    controls_text = tiny_font.render("WASD = Move    E = Interact    ESC = Menu", True, TEXT_COLOR)
    screen.blit(controls_text, (20, 18))

    objective_text = small_font.render("OBJECTIVE: " + get_objective(), True, OBJECTIVE_COLOR)
    screen.blit(objective_text, (250, 18))

    area_text = small_font.render("AREA: " + get_current_area(), True, ROOM_COLOR)
    screen.blit(area_text, (250, 47))

    if chapter == 1:
        inventory = (
            "Key: " + ("YES" if has_key else "NO")
            + "   Flashlight: " + ("YES" if has_flashlight else "NO")
            + "   Exit Key: " + ("YES" if has_exit_key else "NO")
        )
    else:
        inventory = (
            "Flashlight: YES"
            + "   Fuse: " + ("YES" if has_yard_fuse else "NO")
            + "   Power: " + ("ON" if yard_power_on else "OFF")
        )

    inventory_text = tiny_font.render(inventory, True, TEXT_COLOR)
    screen.blit(inventory_text, (20, 75))

    draw_health()

    message_text = small_font.render(message, True, TEXT_COLOR)
    screen.blit(message_text, (20, 615))


def draw_game():
    screen.fill(BACKGROUND_COLOR)

    if chapter == 1:
        draw_chapter1_floor()
        draw_chapter1_decorations()
        draw_chapter1_walls()
        draw_chapter1_furniture()

        if not chapter1_medkit_collected:
            draw_medkit(chapter1_medkit)

        if not key_collected:
            screen.blit(key_image, key_image.get_rect(center=first_key.center))

        if not flashlight_collected:
            screen.blit(flashlight_image, flashlight_image.get_rect(center=flashlight.center))

        if not hallway_door_open:
            screen.blit(door_image, door_image.get_rect(center=hallway_door.center))

        screen.blit(door_image, door_image.get_rect(center=house_exit_door.center))

    else:
        draw_chapter2()

    if monster_active:
        screen.blit(monster_image, monster_image.get_rect(center=monster.center))

    draw_player()
    draw_darkness()

    if chapter == 1:
        draw_chapter1_labels()

    draw_objective_marker()
    draw_hud()

    if note_open:
        draw_note_overlay()


def draw_end_screen(title_text, title_color, subtitle_text):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 215))
    screen.blit(overlay, (0, 0))

    title = big_font.render(title_text, True, title_color)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 265)))

    subtitle = font.render(subtitle_text, True, TEXT_COLOR)
    screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 330)))

    restart_label = "Press R to restart this chapter" if scene == "game_over" else "Press R to play again"
    restart_text = font.render(restart_label, True, TEXT_COLOR)
    screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, 390)))

    menu_text = small_font.render("Press M to return to the menu", True, SECONDARY_TEXT_COLOR)
    screen.blit(menu_text, menu_text.get_rect(center=(SCREEN_WIDTH // 2, 430)))

    if scene == "escaped":
        creator_label = small_font.render(
            "Created and programmed by",
            True,
            SECONDARY_TEXT_COLOR
        )
        screen.blit(
            creator_label,
            creator_label.get_rect(
                center=(SCREEN_WIDTH // 2, 490)
            )
        )

        creator_name = font.render(
            "Yasmim Faria",
            True,
            OBJECTIVE_COLOR
        )
        screen.blit(
            creator_name,
            creator_name.get_rect(
                center=(SCREEN_WIDTH // 2, 522)
            )
        )

# ==================================================
# MAIN LOOP
# ==================================================

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ==================================================
        # SCREENSHOT - F12
        # ==================================================

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
            screenshots_dir = os.path.join(BASE_DIR, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            filename = datetime.now().strftime(
                "screenshot_%Y%m%d_%H%M%S.png"
            )

            screenshot_path = os.path.join(
                screenshots_dir,
                filename
            )

            pygame.image.save(
                screen,
                screenshot_path
            )

            print(
                "Screenshot saved:",
                screenshot_path
            )

        if scene == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_chapter1()
                    scene = "playing"
                elif event.key == pygame.K_h:
                    scene = "how_to_play"
                elif event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    reset_chapter1()
                    scene = "playing"
                elif how_to_play_button.collidepoint(event.pos):
                    scene = "how_to_play"
                elif quit_button.collidepoint(event.pos):
                    running = False

        elif scene == "how_to_play":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_BACKSPACE):
                    scene = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    scene = "menu"

        elif scene == "chapter_transition":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    setup_chapter2(preserve_health=True)
                    scene = "playing"
                elif event.key == pygame.K_ESCAPE:
                    scene = "menu"

        elif scene == "playing":
            if event.type == pygame.KEYDOWN:
                if note_open:
                    if event.key in (pygame.K_e, pygame.K_ESCAPE):
                        note_open = False
                        message = "The wardrobe is in the storage room."
                else:
                    if event.key == pygame.K_ESCAPE:
                        scene = "menu"

                    elif event.key == pygame.K_e:
                        if chapter == 1:
                            door_area = hallway_door.inflate(70, 70)
                            exit_area = house_exit_door.inflate(55, 55)
                            note_area = note.inflate(45, 45)
                            wardrobe_area = pygame.Rect(WARDROBE_CENTER[0] - 50, WARDROBE_CENTER[1] - 55, 100, 110).inflate(50, 50)

                            if has_exit_key and player.colliderect(exit_area):
                                door_sound.play()
                                scene = "chapter_transition"

                            elif player.colliderect(note_area):
                                if not note_read:
                                    note_read = True
                                    message = "You found a note."
                                else:
                                    message = "You read the note again."
                                note_open = True

                            elif player.colliderect(wardrobe_area):
                                if wardrobe_searched:
                                    message = "The wardrobe is empty."
                                elif not note_read:
                                    message = "Just old clothes and dust."
                                else:
                                    wardrobe_searched = True
                                    has_exit_key = True
                                    key_sound.play()
                                    message = "You found the EXIT KEY!"

                            elif player.colliderect(door_area):
                                if hallway_door_open:
                                    message = "The hallway door is already open."
                                elif has_key:
                                    hallway_door_open = True
                                    has_key = False
                                    door_sound.play()
                                    message = "The hallway door is open."
                                else:
                                    message = "The door is locked. Find the key."

                            elif player.colliderect(exit_area):
                                message = "The exit is locked."

                        else:
                            gate_area = yard_gate.inflate(90, 90)
                            box_area = fuse_box.inflate(90, 90)

                            if player.colliderect(gate_area):
                                if yard_power_on:
                                    gate_open = True
                                    door_sound.play()
                                    scene = "escaped"
                                else:
                                    gate_checked = True
                                    message = "The gate has no power. Find a fuse."

                            elif player.colliderect(box_area):
                                if yard_power_on:
                                    message = "The power is already on."
                                elif has_yard_fuse:
                                    has_yard_fuse = False
                                    yard_power_on = True

                                    monster.x = 565
                                    monster.y = 245
                                    reset_monster_ai()
                                    monster_active = True
                                    monster_state = "patrol"

                                    message = "Power restored... Something is moving again."
                                else:
                                    message = "The fuse box is missing a fuse."

        elif scene in ("game_over", "escaped"):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if scene == "escaped":
                        reset_chapter1()
                    else:
                        restart_current_chapter()
                    scene = "playing"
                elif event.key == pygame.K_m:
                    scene = "menu"

    # ==================================================
    # GAMEPLAY UPDATE
    # ==================================================

    if scene == "playing" and not note_open:
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(0, 0)
        player_moving = False

        if keys[pygame.K_w]:
            movement.y -= 1
            player_direction = "up"
            player_moving = True

        if keys[pygame.K_s]:
            movement.y += 1
            player_direction = "down"
            player_moving = True

        if keys[pygame.K_a]:
            movement.x -= 1
            player_direction = "left"
            player_moving = True

        if keys[pygame.K_d]:
            movement.x += 1
            player_direction = "right"
            player_moving = True

        if movement.length() > 0:
            movement = movement.normalize() * player_speed

        move_object(
            player,
            round(movement.x),
            round(movement.y),
            get_solid_obstacles(),
        )

        update_player_animation()

        if chapter == 1:
            if not key_collected and player.colliderect(first_key):
                key_collected = True
                has_key = True
                key_sound.play()
                message = "You found the key. Go to the hallway door."

            if not flashlight_collected and player.colliderect(flashlight):
                flashlight_collected = True
                has_flashlight = True
                monster_active = True
                monster_state = "patrol"
                flashlight_sound.play()
                message = "You found the flashlight... Something woke up."

            if (
                not chapter1_medkit_collected
                and health < max_health
                and player.colliderect(chapter1_medkit)
            ):
                chapter1_medkit_collected = True
                use_medkit()

        else:
            if not yard_fuse_collected and player.colliderect(yard_fuse):
                yard_fuse_collected = True
                has_yard_fuse = True
                key_sound.play()

                if gate_checked:
                    message = "You found the fuse. Take it to the power box."
                else:
                    message = "You found an old fuse."

            if (
                not yard_medkit_1_collected
                and health < max_health
                and player.colliderect(yard_medkit_1)
            ):
                yard_medkit_1_collected = True
                use_medkit()

            if (
                not yard_medkit_2_collected
                and health < max_health
                and player.colliderect(yard_medkit_2)
            ):
                yard_medkit_2_collected = True
                use_medkit()

        update_flashlight_flicker()
        update_monster_ai()

        if monster_active and player.colliderect(monster):
            current_time = pygame.time.get_ticks()

            if current_time - last_damage_time >= damage_cooldown:
                health -= 20
                attack_sound.play()
                last_damage_time = current_time
                message = "The creature attacked you!"

                if health <= 0:
                    health = 0
                    player_moving = False
                    scene = "game_over"

    else:
        player_moving = False

    # ==================================================
    # DRAW
    # ==================================================

    if scene == "menu":
        draw_menu()
    elif scene == "how_to_play":
        draw_how_to_play()
    elif scene == "chapter_transition":
        draw_chapter_transition()
    elif scene == "playing":
        draw_game()
    elif scene == "game_over":
        draw_game()
        draw_end_screen("GAME OVER", GAME_OVER_COLOR, "The creature found you.")
    elif scene == "escaped":
        draw_game()
        draw_end_screen("YOU ESCAPED", WIN_COLOR, "You survived The Dark House.")

    pygame.display.update()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
