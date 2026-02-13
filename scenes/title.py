import pygame
import sys
import settings

WIDTH = settings.Display.WIDTH
HEIGHT = settings.Display.HEIGHT

ADJUST = 5
BACK_ADJUST = 10

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
GRAY = settings.Color.GRAY
DARK_GRAY = settings.Color.DARK_GRAY

class Main():
    def __init__(self, mode) -> None:
        # [START or 続きから, 終了 or 初めから, 戻る] の色
        self.button_color = [GRAY] * 3
        
        # 文字フォント
        self.font_path = "msgothic"
        
        # タイトルrect
        self.title_font = pygame.font.SysFont(self.font_path, HEIGHT // 6)
        self.title = self.title_font.render("INFINITE GOLD", True, BLACK)
        self.title_rect = self.title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # ボタンrect
        self.button = []
        self.button.append(pygame.Rect(WIDTH // 4, HEIGHT * 7//12 + ADJUST, WIDTH // 2, HEIGHT // 6 - 2*ADJUST))
        self.button.append(pygame.Rect(WIDTH // 4, HEIGHT * 3//4 + ADJUST, WIDTH // 2, HEIGHT // 6 - 2*ADJUST))
        
        self.text_font = pygame.font.SysFont(self.font_path, HEIGHT // 10)
        self.text = []
        if mode == "start":
            self.text.append(self.text_font.render("START", True, BLACK))
            self.text.append(self.text_font.render("終了", True, BLACK))
        elif mode == "continue":
            self.text.append(self.text_font.render("続きから", True, BLACK))
            self.text.append(self.text_font.render("初めから", True, BLACK))
            
            # mode==continueの時はstartに戻る用のボタンが必要
            self.button.append(pygame.Rect(BACK_ADJUST, BACK_ADJUST, WIDTH // 10, HEIGHT // 18))
            self.back_font = pygame.font.SysFont(self.font_path, HEIGHT // 24)
            self.text.append(self.back_font.render("戻る", True, BLACK))
        
        self.rect = []
        for i in range(len(self.button)):
            self.rect.append(self.text[i].get_rect(center=self.button[i].center))
        
        # キーボード操作時にどちらのボタンを選択しているか（0or1)
        self.which = None
    
    # プレイ画面からタイトル画面に戻ってきた後に初めからプレイするための全リセット
    def settings_liset(self):
        settings.stage_num = 1

        settings.player_x = settings.Display.BLOCK_SIZE * 3/2
        settings.player_y = settings.Display.BLOCK_SIZE * 3/2

        settings.character_x = []
        settings.character_y = []
        
        settings.character_move_time = []
        
        settings.mining_size_x = 10
        settings.mining_size_y = 10

        settings.ore_exist = [[-1]*settings.mining_size_x for _ in range(settings.mining_size_y)]

        settings.money = 0

        settings.ore_possession_list = [0] * len(settings.ore_list)

        settings.mining_durability = [[None]*settings.mining_size_x for _ in range(settings.mining_size_y)]

        settings.mining_degree = [[0]*settings.mining_size_x for _ in range(settings.mining_size_y)]

        settings.mining_power = [1]

        settings.ore_prop_list = [0.9, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        settings.lucky_flower_level = 0

        settings.pickaxe_level = [[] for _ in range(6)]
        settings.pickaxe_level[0].append(0) 

        settings.use_pickaxe_type , settings.use_pickaxe_num = [0], [0]

        settings.character_speed = []
        
        settings.experience = [0, 0, 0, 0]
        
        settings.reinc_ore_get_ratio = 1
        
        settings.have_exp = 0
        
        settings.reinc_exp_ratio = 1
        
        settings.reinc_times = 0
        
        settings.playing_time = 0
            
    # 描画処理
    def draw(self, canvas):
        canvas.fill(WHITE)
        canvas.blit(self.title, self.title_rect)
        for i in range(len(self.button)):
            pygame.draw.rect(canvas, self.button_color[i], self.button[i])
            pygame.draw.rect(canvas, BLACK, self.button[i], width=3)
            canvas.blit(self.text[i], self.rect[i])