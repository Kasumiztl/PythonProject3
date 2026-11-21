import pygame
import os
import sys
import math

pygame.init()
pygame.display.set_caption("REALITY.exe — Wifies' Adventure")

W, H = 1100, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
FPS = 60

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")

def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Verdana.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except Exception:
                pass
    for name in ("arial", "dejavusans", "notosans", "freesans"):
        path = pygame.font.match_font(name, bold=bold)
        if path:
            try:
                return pygame.font.Font(path, size)
            except Exception:
                pass
    return pygame.font.Font(None, size)

FONT = load_font(23)
SMALL = load_font(17)
TINY = load_font(14)
TITLE = load_font(38, True)
BIG = load_font(54, True)

def load_image(filename):
    path = os.path.join(ASSETS, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except Exception:
        return None

sprites = {
    "Wifies": load_image("wifies.png"),
    "Verity": load_image("verity.png"),
    "Moggity": load_image("moggity.png"),
    "Obesity": load_image("obesity.png"),
    "Squaredity": load_image("squaredity.png"),
}

def fit_image(image, size):
    if image is None:
        return None
    copy = image.copy()
    copy.thumbnail(size, pygame.transform.smoothscale)
    return copy

def blit_center(image, center, size):
    if image is None:
        pygame.draw.circle(screen, (240, 220, 120), center, size[0] // 2)
        return
    scaled = pygame.transform.smoothscale(image, size)
    rect = scaled.get_rect(center=center)
    screen.blit(scaled, rect)

def draw_text(text, font, color, pos, center=False):
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    screen.blit(surf, rect)
    return rect

def wrap_lines(text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = word if not line else line + " " + word
        if font.size(test)[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def draw_wrapped(text, font, color, x, y, width, line_gap=7):
    for line in wrap_lines(text, font, width):
        draw_text(line, font, color, (x, y))
        y += font.get_linesize() + line_gap
    return y

chapters = [
    {
        "title": "Глава 1. Помилка в реальності",
        "place": "Зламане селище",
        "npc": "Мешканець",
        "sprite": None,
        "desc": "Допоможи мешканцю з знайди перший фрагмент коду.",
        "task": "Поговори з мешканцем.",
        "lines": [
            "Мешканець: Нарешті хтось прийшов! В мене moggity забрав лице, будь ласка, допоможи, я тобі дам фрагмент!",
            "Wifies: Треба знайти джерело помилки.",
            "СИСТЕМА: Отримано фрагмент коду реальності."
        ],
        "question": "Що робити далі?",
        "choices": ["Піти шукати джерело", "Залишитись з мешканцем", "Сказати, що втомився"],
        "answer": 0,
        "reward": "Фрагмент коду №1",
        "bg": (20, 36, 48),
        "ground": (35, 76, 65),
    },
    {
        "title": "Глава 2. Бібліотека Verity",
        "place": "Архів нескінченних відповідей",
        "npc": "Verity",
        "sprite": "Verity",
        "desc": "Пройди контекстну вікторину. У Verity правильна відповідь залежить від обставин.",
        "task": "Поговори з Verity та доведи, що розумієш контекст.",
        "lines": [
            "Verity: Я знаю абсолютно все.",
            "Verity: Навіть де ти спиш.",
            "Wifies: бро..."
        ],
        "question": "Скільки яєць можна з'їсти натщесерце?",
        "choices": ["скільки поміститься в живіт", "1", "безліч"],
        "answer": 1,
        "reward": "Фрагмент коду №2",
        "bg": (30, 27, 55),
        "ground": (65, 48, 91),
    },
    {
        "title": "Глава 3. Територія Moggity",
        "place": "Площа дзеркал",
        "npc": "Moggity",
        "sprite": "Moggity",
        "desc": "Виграй луксмакс-батл: обери найкращу відповідь на провокацію Moggity.",
        "task": "Підійди до Moggity та кинь виклик у луксмакс-батлі.",
        "lines": [
            "Moggity: На жаль, сьогодні ти програєш.",
            "Wifies: Мог мог",
            "Moggity: Кого ти там моггаєщ."
        ],
        "question": "Moggity каже: «Я тебе моггаю».",
        "choices": ["Тобі труси миє мама", "...", "На жаль"],
        "answer": 0,
        "reward": "Фрагмент коду №3",
        "bg": (48, 25, 45),
        "ground": (94, 43, 75),
    },
    {
        "title": "Глава 4. Економіка Obesity",
        "place": "Ринок нескінченної комісії",
        "npc": "Obesity",
        "sprite": "Obesity",
        "desc": "Не дай економіці Obesity себе обдурити: обери найвигіднішу угоду.",
        "task": "Поговори з Obesity та спробуй повернути свої речі.",
        "lines": [
            "Obesity: Вітаю на ринку! Твій інвентар тепер належить мені. Викупити можна за невелику комісію.",
            "Wifies: Ти забрав мої речі й тепер продаєш їх мені?",
            "Obesity: Саме так. Це називається бізнес, дитинко."
        ],
        "question": "Obesity пропонує повернути 10 монет за 40. Що найрозумніше зробити?",
        "choices": ["Запропунувати йому не їсти мак", "Позичити ще 100 монет", "Купити негайно"],
        "answer": 0,
        "reward": "Фрагмент коду №4",
        "bg": (52, 38, 22),
        "ground": (103, 76, 39),
    },
    {
        "title": "Глава 5. Суд Squaredity",
        "place": "Зала абсолютного порядку",
        "npc": "Squaredity",
        "sprite": "Squaredity",
        "desc": "Знайди вихідний код і виріши долю світу.",
        "task": "Поговори із Squaredity та пройди останнє випробування.",
        "lines": [
            "Squaredity: Усі дії мають бути впорядковані. Навіть хаос повинен мати дозвіл.",
            "Wifies: Ми знайшли вихідний код. Одна помилка зламала все.",
            "Squaredity: Виправлення видалить усі досягнення, предмети та спогади.",
            "Wifies: Тоді рішення має бути нашим спільним."
        ],
        "question": "Що робити з помилкою в коді реальності?",
        "choices": ["Виправити рядок і почати спочатку", "Залишити світ таким, яким він став", "Змінити код так, щоб зберегти спогади"],
        "answer": 2,
        "reward": "Вихідний код реальності",
        "bg": (23, 31, 48),
        "ground": (48, 62, 87),
    },
]

class Game:
    def __init__(self):
        self.chapter = 0
        self.player_x, self.player_y = 235, 480
        self.speed = 4
        self.aura = 50
        self.coins = 0
        self.fragments = 0
        self.chaos = 0
        self.inventory = ["Старий компас"]
        self.dialogue = None
        self.dialogue_index = 0
        self.choice_mode = False
        self.finished_chapters = set()
        self.ending = None
        self.notice = "Знайди персонажа та натисни E, щоб поговорити."
        self.notice_timer = 240
        self.running = True

    def npc_position(self):
        return (820, 440)

    def npc_name(self):
        return chapters[self.chapter]["npc"]

    def start_dialogue(self):
        self.dialogue = list(chapters[self.chapter]["lines"])
        self.dialogue_index = 0
        self.choice_mode = False

    def next_dialogue(self):
        if self.dialogue is None:
            return
        if self.dialogue_index < len(self.dialogue) - 1:
            self.dialogue_index += 1
        else:
            self.dialogue = None
            self.choice_mode = True

    def choose(self, choice):
        ch = chapters[self.chapter]
        if choice < 0 or choice >= len(ch["choices"]):
            return
        if choice == ch["answer"]:
            self.fragments += 1
            self.aura += 10
            self.coins += 15
            self.inventory.append(ch["reward"])
            self.finished_chapters.add(self.chapter)
            self.notice = "Успіх! " + ch["reward"] + " отримано."
            self.chaos = max(0, self.chaos - 1)
            if self.chapter == 4:
                self.finish_game(choice)
            else:
                self.chapter += 1
                self.player_x, self.player_y = 235, 480
        else:
            self.chaos += 2
            self.aura = max(0, self.aura - 5)
            self.notice = "Світ став ще хаотичнішим."
        self.notice_timer = 240
        self.choice_mode = False

    def finish_game(self, choice):
        if self.chaos <= 1:
            self.ending = "Збережена реальність"
            self.ending_text = "Ти змінив код так, щоб зберегти спогади. Світ не став ідеальним, але тепер його мешканці самі вирішують, яким йому бути."
        elif self.chaos >= 5:
            self.ending = "Хаотична реальність"
            self.ending_text = "Світ залишився дивним і непередбачуваним."
        else:
            self.ending = "Новий початок"
            self.ending_text = "Реальність перезапустилася, але деякі спогади залишилися у фрагментах коду. Можливо, це не кінець."
        self.dialogue = None
        self.choice_mode = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif self.ending:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                    self.__init__()
            elif self.dialogue is not None:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e):
                    self.next_dialogue()
            elif self.choice_mode:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    self.choose(event.key - pygame.K_1)
            elif event.key == pygame.K_e:
                nx, ny = self.npc_position()
                if math.hypot(self.player_x - nx, self.player_y - ny) < 170:
                    self.start_dialogue()
                else:
                    self.notice = "Підійди ближче до персонажа."
                    self.notice_timer = 150

    def update(self, keys):
        if self.dialogue is not None or self.choice_mode or self.ending:
            return
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        self.player_x = max(70, min(W - 70, self.player_x + dx))
        self.player_y = max(270, min(H - 85, self.player_y + dy))
        if self.notice_timer > 0:
            self.notice_timer -= 1

    def draw_background(self):
        ch = chapters[self.chapter]
        screen.fill(ch["bg"])
        # distant stars / glitch particles
        for i in range(32):
            x = (i * 173 + 31) % W
            y = 100 + (i * 67) % 330
            pygame.draw.circle(screen, (100, 125, 155), (x, y), 2)
        pygame.draw.rect(screen, ch["ground"], (0, 245, W, H - 245))
        # path
        pygame.draw.ellipse(screen, (ch["ground"][0] + 12, ch["ground"][1] + 10, ch["ground"][2] + 8), (80, 360, 940, 260))
        # stylized glitch blocks
        for i in range(9):
            x = (i * 139 + 40) % W
            y = 280 + (i % 3) * 36
            pygame.draw.rect(screen, (ch["ground"][0] + 18, ch["ground"][1] + 16, ch["ground"][2] + 14), (x, y, 35, 18), border_radius=4)

    def draw_character(self, name, pos, size, fallback_color):
        image = sprites.get(name)
        if image:
            blit_center(image, pos, size)
        else:
            pygame.draw.circle(screen, fallback_color, pos, size[0] // 2)
        if name != "Мешканець":
            pygame.draw.ellipse(screen, (0, 0, 0, 70),
                                (pos[0] - size[0] // 3, pos[1] + size[1] // 3, size[0] * 2 // 3, 13))

    def draw_hud(self):
        pygame.draw.rect(screen, (9, 12, 23), (0, 0, W, 100))
        pygame.draw.line(screen, (87, 213, 220), (0, 99), (W, 99), 2)
        draw_text("REALITY.exe", TITLE, (104, 231, 229), (25, 14))
        draw_text(chapters[self.chapter]["title"], FONT, (245, 245, 255), (320, 25))
        draw_text(f"Аура: {self.aura}    Монети: {self.coins}    Фрагменти: {self.fragments}/5    Хаос: {self.chaos}", SMALL, (221, 224, 241), (27, 67))
        draw_text("Інвентар: " + ", ".join(self.inventory[-3:]), TINY, (221, 224, 241), (600, 70))

    def draw_dialogue(self):
        if self.dialogue is None and not self.choice_mode:
            return
        pygame.draw.rect(screen, (8, 11, 23), (35, 485, W - 70, 180), border_radius=18)
        pygame.draw.rect(screen, (91, 214, 220), (35, 485, W - 70, 180), 2, border_radius=18)
        if self.choice_mode:
            ch = chapters[self.chapter]
            draw_text("ВИПРОБУВАННЯ", SMALL, (106, 229, 224), (65, 505))
            y = draw_wrapped(ch["question"], FONT, (255, 255, 255), 65, 535, 950)
            for i, option in enumerate(ch["choices"]):
                draw_text(f"{i+1}. {option}", SMALL, (255, 225, 140), (75, y + 8 + i*30))
            draw_text("Натисни 1, 2 або 3", TINY, (170, 180, 200), (880, 630))
        else:
            line = self.dialogue[self.dialogue_index]
            draw_wrapped(line, FONT, (245, 245, 255), 65, 535, 950, 9)
            draw_text("SPACE / ENTER — далі", SMALL, (106, 229, 224), (825, 625))

    def draw_ending(self):
        screen.fill((8, 12, 25))
        draw_text("REALITY.exe", TITLE, (100, 230, 225), (W//2, 110), True)
        draw_text(self.ending, BIG, (255, 225, 130), (W//2, 220), True)
        draw_wrapped(self.ending_text, FONT, (240, 242, 250), 180, 310, 740, 12)
        draw_text(f"Фрагменти: {self.fragments}/5    Хаос: {self.chaos}    Аура: {self.aura}", SMALL, (170, 190, 215), (W//2, 470), True)
        draw_text("ENTER — зіграти знову     ESC — вийти", FONT, (100, 230, 225), (W//2, 570), True)

    def draw(self):
        if self.ending:
            self.draw_ending()
            pygame.display.flip()
            return
        self.draw_background()
        # NPC / player
        nx, ny = self.npc_position()
        npc = self.npc_name()
        npc_color = (230, 190, 110)
        self.draw_character(npc, (nx, ny - 35), (155, 155), npc_color)
        draw_text(npc, FONT, (255, 255, 255), (nx, ny + 55), True)
        self.draw_character("Wifies", (self.player_x, self.player_y - 25), (125, 150), (235, 220, 170))
        draw_text("Wifies", SMALL, (255, 255, 255), (self.player_x, self.player_y + 55), True)
        self.draw_hud()
        if not self.dialogue and not self.choice_mode:
            if math.hypot(self.player_x - nx, self.player_y - ny) < 170:
                draw_text("E — поговорити", SMALL, (255, 238, 155), (nx, ny + 92), True)
            if self.notice_timer > 0:
                pygame.draw.rect(screen, (10, 15, 28), (260, 620, 580, 42), border_radius=12)
                draw_text(self.notice, SMALL, (220, 235, 240), (W//2, 641), True)
        self.draw_dialogue()
        pygame.display.flip()

game = Game()
while game.running:
    for event in pygame.event.get():
        game.handle_event(event)
    game.update(pygame.key.get_pressed())
    game.draw()
    clock.tick(FPS)

pygame.quit()
sys.exit()
