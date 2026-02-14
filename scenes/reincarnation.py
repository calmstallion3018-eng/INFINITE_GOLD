import pygame
import sys
import settings

FULL_W = settings.Display.WIDTH
FULL_H = settings.Display.HEIGHT

MINE_W = settings.Display.MINE_W
MINE_H = settings.Display.MINE_H
RIGHT_H = settings.Display.RIGHT_H

HEADLINE_SIZE = MINE_H // 8
BUTTON_SIZE_W = MINE_W // 2
BUTTON_SIZE_H = (MINE_H - HEADLINE_SIZE) // 2
TEXT_SIZE = BUTTON_SIZE_H // 12

button_quantity = settings.bottom_button_quantity

ADJUST = 20

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
LIGHTGREEN = settings.Color.LIGHTGREEN
YELLOW = settings.Color.YELLOW
GRAY = settings.Color.GRAY
RED = settings.Color.RED

class Main():
    def __init__(self) -> None:
        # 文字フォント
        self.font_path = "msgothic"
        
        # 転生するrect
        self.headline_font = pygame.font.SysFont(self.font_path, HEADLINE_SIZE // 2)
        if settings.have_exp < 1e9:
            self.headline_disp = self.headline_font.render(f"採掘をやり直す 経験値: {settings.have_exp:,}", True, BLACK)
        else:
            self.headline_disp = self.headline_font.render(f"採掘をやり直す 経験値: {settings.have_exp:.2E}".replace("+", ""), True, BLACK)
        self.headline_rect_real = pygame.Rect(0,0,MINE_W, HEADLINE_SIZE)
        self.headline_rect = self.headline_disp.get_rect(center=self.headline_rect_real.center)
        
        # 転生ボタン（[縦, 横, 獲得鉱石数, 転生経験値]）
        self.reinc_font = pygame.font.SysFont(self.font_path, TEXT_SIZE)
        self.reinc_button = [None] * 4
        self.reinc_button_color = [GRAY] * 4
        self.reinc_disp_name = [None] * 4
        self.reinc_disp_now = [None] * 4
        self.reinc_disp_after = [None] * 4
        self.reinc_disp_need_exp = [None] * 4
        self.reinc_rect_name = [None] * 4
        self.reinc_rect_now = [None] * 4
        self.reinc_rect_after = [None] * 4
        self.reinc_rect_need_exp = [None] * 4
        for i in range(4):
            self.reinc_button[i] = pygame.Rect((i%2)*BUTTON_SIZE_W + ADJUST, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + ADJUST, BUTTON_SIZE_W - 2*ADJUST, BUTTON_SIZE_H - 2*ADJUST)
            self.reinc_disp_name[i] = self.reinc_font.render(f"{settings.reinc_name[i]}", True, BLACK)
            self.reinc_disp_now[i] = self.reinc_font.render(f"現在：LEVEL {settings.calc_reinc_level(i, "now")}  {settings.calc_reinc_value(i, settings.calc_reinc_level(i, "now"))}{settings.reinc_unit[i]}", True, BLACK)
            self.reinc_disp_after[i] = self.reinc_font.render(f"転生後：LEVEL {settings.calc_reinc_level(i, "after")}  {settings.calc_reinc_value(i, settings.calc_reinc_level(i, "after"))}{settings.reinc_unit[i]}", True, BLACK)
            self.reinc_disp_need_exp[i] = self.reinc_font.render(f"経験値：{settings.experience[i] - 2**settings.calc_reinc_level(i, "now") + 1} + {settings.have_exp} / {2**settings.calc_reinc_level(i, "now")}", True, BLACK)
            self.reinc_rect_name[i] = self.reinc_disp_name[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H // 4))
            self.reinc_rect_now[i] = self.reinc_disp_now[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H * 5//12))
            self.reinc_rect_after[i] = self.reinc_disp_after[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H * 7//12))
            self.reinc_rect_need_exp[i] = self.reinc_disp_need_exp[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H * 3//4))
        
        # キーボード操作時にどのボタンを選択しているか
        self.reinc_button_which = None
        
        # 転生時に強化する要素
        self.reinc_num = None
        
        # 転生選択画面の表示
        self.reinc_select = False
        
        # ×マークrect
        self.cannot_font = pygame.font.SysFont(self.font_path, BUTTON_SIZE_H * 6//5)
        self.cannot_reinc_disp = self.cannot_font.render("X", True, RED)
        self.cannot_reinc_rect = None
        
        # ×マーク表示
        self.is_cannot = False
        
        # 小窓の設定
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.permit_font_1 = pygame.font.SysFont(self.font_path, FULL_H // 18)
        self.permit_font_2 = pygame.font.SysFont(self.font_path, FULL_H // 36)
        self.permit_font = [self.permit_font_1] * 2 + [self.permit_font_2] * 2
        
        self.permit_color = [BLACK] * 2 + [RED] * 2
        
        self.y_n_adjust = 30
        self.y_n_font = pygame.font.SysFont(self.font_path, FULL_H // 18)
        self.y_n_color = [GRAY] * 2
        self.y_n_text = ["はい", "いいえ"]
        self.y_n_button = []
        self.y_n_disp = []
        self.y_n_rect = []
        for i in range(2):
            self.y_n_button.append(pygame.Rect((i+1)*FULL_W // 4 + self.y_n_adjust, FULL_H * 2//3 - self.y_n_adjust, FULL_W // 4 - 2*self.y_n_adjust, FULL_H // 12))
            self.y_n_disp.append(self.y_n_font.render(f"{self.y_n_text[i]}", True, BLACK))
            self.y_n_rect.append(self.y_n_disp[i].get_rect(center=self.y_n_button[i].center))
        
        # キーボード操作時にはいいいえのどちらを選択しているか(y=0, n=1)
        self.y_n_which = None
        
    # 転生時の処理
    def reinc_change(self):
        value = settings.calc_reinc_value(self.reinc_num, settings.calc_reinc_level(self.reinc_num, "after"))
        if self.reinc_num == 0:
            settings.mining_size_y = value
        elif self.reinc_num == 1:
            settings.mining_size_x = value
        elif self.reinc_num == 2:
            settings.reinc_ore_get_ratio = value
        elif self.reinc_num == 3:
            settings.reinc_exp_ratio = value
        settings.experience[self.reinc_num] += settings.have_exp
        settings.record_list[18] += 1
        settings.record_list[19] = settings.mining_size_x * settings.mining_size_y
        
        # 転生変数以外の変数（プレイ時間除く）をリセット
        settings.stage_num = 1

        settings.player_x = settings.Display.BLOCK_SIZE * 3/2
        settings.player_y = settings.Display.BLOCK_SIZE * 3/2

        settings.character_x = []
        settings.character_y = []
        
        settings.character_move_time = []

        settings.ore_exist = [[-1]*settings.mining_size_x for _ in range(settings.mining_size_y)]

        settings.money = 0

        settings.ore_possession_list = [0] * len(settings.ore_list)

        settings.mining_durability = [[None]*settings.mining_size_x for _ in range(settings.mining_size_y)]

        settings.mining_degree = [[0]*settings.mining_size_x for _ in range(settings.mining_size_y)]

        settings.mining_power = [1]

        settings.lucky_flower_level = 0

        settings.pickaxe_level = [[] for _ in range(6)]
        settings.pickaxe_level[0].append(0) 

        settings.use_pickaxe_type , settings.use_pickaxe_num = [0], [0]

        settings.character_speed = []
        
        settings.have_exp = 0

    # ページ内変数のアップデート
    def update_page(self):
        # 取得経験値の変更
        settings.have_exp = int(((settings.stage_num - 1) ** 2 / 10000 + settings.lucky_flower_level ** 3 / 100) * settings.reinc_exp_ratio)
        
        if settings.have_exp < 1e9:
            self.headline_disp = self.headline_font.render(f"採掘をやり直す 経験値: {settings.have_exp:,}", True, BLACK)
        else:
            self.headline_disp = self.headline_font.render(f"採掘をやり直す 経験値: {settings.have_exp:.2E}".replace("+", ""), True, BLACK)
        self.headline_rect = self.headline_disp.get_rect(center=self.headline_rect_real.center)
        
        for i in range(4):
            self.reinc_disp_now[i] = self.reinc_font.render(f"現在：LEVEL {settings.calc_reinc_level(i, "now")}  {settings.calc_reinc_value(i, settings.calc_reinc_level(i, "now"))}{settings.reinc_unit[i]}", True, BLACK)
            self.reinc_disp_after[i] = self.reinc_font.render(f"転生後：LEVEL {settings.calc_reinc_level(i, "after")}  {settings.calc_reinc_value(i, settings.calc_reinc_level(i, "after"))}{settings.reinc_unit[i]}", True, BLACK)
            self.reinc_disp_need_exp[i] = self.reinc_font.render(f"経験値：{settings.experience[i] - 2**settings.calc_reinc_level(i, "now") + 1} + {settings.have_exp} / {2**settings.calc_reinc_level(i, "now")}", True, BLACK)
            self.reinc_rect_now[i] = self.reinc_disp_now[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H * 5//12))
            self.reinc_rect_after[i] = self.reinc_disp_after[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H * 7//12))
            self.reinc_rect_need_exp[i] = self.reinc_disp_need_exp[i].get_rect(center=((i%2)*BUTTON_SIZE_W + BUTTON_SIZE_W // 2, HEADLINE_SIZE + (i//2)*BUTTON_SIZE_H + BUTTON_SIZE_H * 3//4))
    
    # 描画処理
    def draw(self, canvas):
        canvas.fill(WHITE)
        # 見出しの描画
        canvas.blit(self.headline_disp, self.headline_rect)
        pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE), (MINE_W, HEADLINE_SIZE), 1)
        # 転生ボタンの描画
        for i in range(4):
            pygame.draw.rect(canvas, self.reinc_button_color[i], self.reinc_button[i])
            pygame.draw.rect(canvas, BLACK, self.reinc_button[i], width=3)
            canvas.blit(self.reinc_disp_name[i], self.reinc_rect_name[i])
            canvas.blit(self.reinc_disp_now[i], self.reinc_rect_now[i])
            canvas.blit(self.reinc_disp_after[i], self.reinc_rect_after[i])
            canvas.blit(self.reinc_disp_need_exp[i], self.reinc_rect_need_exp[i])
    
    # 転生確認画面
    def reinc_select_draw(self, canvas):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        self.permit_text = [f"{settings.reinc_name[self.reinc_num][:-1]}{"し" if self.reinc_num == 2 else ""}て", "最初からやり直しますか？", "※所持しているお金、鉱石、幸運の花、ツルハシと", "雇用している鉱夫は全て失われます"]
        self.permit_disp = []
        self.permit_rect = []
        for i in range(len(self.permit_text)):
            self.permit_disp.append(self.permit_font[i].render(f"{self.permit_text[i]}", True, self.permit_color[i]))
            if i < 2:
                self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+4)*FULL_H // 12)))
            else:
                self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+10)*FULL_H // 24)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])
        
    # 転生できないときに×を出す
    def cannot_reinc_draw(self, canvas):
        self.cannot_reinc_rect = self.cannot_reinc_disp.get_rect(center=self.reinc_button[self.reinc_num].center)
        canvas.blit(self.cannot_reinc_disp, self.cannot_reinc_rect)