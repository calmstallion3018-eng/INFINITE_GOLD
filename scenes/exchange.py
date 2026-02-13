import pygame
import sys
import settings

FULL_W = settings.Display.WIDTH
FULL_H = settings.Display.HEIGHT

MINE_W = settings.Display.MINE_W
MINE_H = settings.Display.MINE_H
RIGHT_H = settings.Display.RIGHT_H

HEADLINE_SIZE = MINE_H // 8
TEXT_SIZE = MINE_H // 24
LEFT_H = TEXT_SIZE * 3

button_quantity = settings.bottom_button_quantity

ADJUST = 2

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
        
        # 画像ダウンロード
        self.ore_image_default = []
        self.ore_image = []
        for i, IMAGE in enumerate(settings.ORE_IMAGE):
            self.ore_image_default.append(pygame.image.load(IMAGE).convert_alpha())
            self.ore_image.append(pygame.transform.scale(self.ore_image_default[i], (2*TEXT_SIZE, 2*TEXT_SIZE)))
        
        # 鉱石買取rect
        self.headline_font = pygame.font.SysFont(self.font_path, HEADLINE_SIZE // 2)
        self.headline_disp = self.headline_font.render("鉱石買取", True, BLACK)
        self.headline_rect_real = pygame.Rect(0,0,MINE_W, HEADLINE_SIZE)
        self.headline_rect = self.headline_disp.get_rect(center=self.headline_rect_real.center)
        
        # 鉱石の名前と売値と売却ボタンrect
        self.price_font = pygame.font.SysFont(self.font_path, TEXT_SIZE)
        self.sell_button_font = pygame.font.SysFont(self.font_path ,TEXT_SIZE // 2)
        
        self.sell_ore_rect_real = [None] * len(settings.ore_list)
        self.price_rect_real = [None] * len(settings.ore_list)
        self.sell_button = [[None] * 4 for _ in range(len(settings.ore_list))]
        
        self.sell_ore_name_disp = [None] * len(settings.ore_list)
        self.price_disp = [None] * len(settings.ore_list)
        self.sell_button_disp = [None] * 3
        for j in range(3):
            self.sell_button_disp[j] = self.sell_button_font.render(f"x {10**j:,}", True, BLACK)
        self.sell_button_disp.append(self.sell_button_font.render("x MAX", True, BLACK))
        
        self.sell_ore_name_rect = [None] * len(settings.ore_list)
        self.price_rect = [None] * len(settings.ore_list)
        self.sell_button_rect = [[None] * 4 for _ in range(len(settings.ore_list))]
        for i in range(len(settings.ore_list)):
            if i % 2 == 0:
                self.sell_ore_rect_real[i] = pygame.Rect(2*TEXT_SIZE, HEADLINE_SIZE + (i//2)*LEFT_H, MINE_W // 2 - 2*TEXT_SIZE, TEXT_SIZE)
                self.price_rect_real[i] = pygame.Rect(0, HEADLINE_SIZE + (i//2)*LEFT_H + TEXT_SIZE, MINE_W // 2, TEXT_SIZE)
                for j in range(4):
                    self.sell_button[i][j] = pygame.Rect(MINE_W * j//8 + ADJUST, HEADLINE_SIZE + (i//2)*LEFT_H + 2*TEXT_SIZE + ADJUST, MINE_W // 8 - 2*ADJUST, TEXT_SIZE - 2*ADJUST)
            else:
                self.sell_ore_rect_real[i] = pygame.Rect(MINE_W // 2 + 2*TEXT_SIZE, HEADLINE_SIZE + (i//2)*LEFT_H, MINE_W // 2 - 2*TEXT_SIZE, TEXT_SIZE)
                self.price_rect_real[i] = pygame.Rect(MINE_W // 2, HEADLINE_SIZE + (i//2)*LEFT_H + TEXT_SIZE, MINE_W // 2, TEXT_SIZE)
                for j in range(4):
                    self.sell_button[i][j] = pygame.Rect(MINE_W * (4+j)//8 + ADJUST, HEADLINE_SIZE + (i//2)*LEFT_H + 2*TEXT_SIZE + ADJUST, MINE_W // 8 - 2*ADJUST, TEXT_SIZE - 2*ADJUST)
            self.sell_ore_name_disp[i] = self.price_font.render(settings.ore_name_list[i], True, BLACK)
            self.price_disp[i] = self.price_font.render(f"￥{int(settings.ore_price_list[i] * settings.ore_price_ratio[i]):,} / 個", True, BLACK)
            self.sell_ore_name_rect[i] = self.sell_ore_name_disp[i].get_rect(midleft=self.sell_ore_rect_real[i].midleft)
            self.price_rect[i] = self.price_disp[i].get_rect(midright=self.price_rect_real[i].midright)
            for j in range(4):
                self.sell_button_rect[i][j] = self.sell_button_disp[j].get_rect(center=self.sell_button[i][j].center)
        
        self.sell_button_color = [[GRAY] * 4 for _ in range(len(settings.ore_list))]
        
        # 売却選択画面の表示
        self.can_select = False
        self.sell_ore_num, self.sell_quantity = -1, -1
        
        # ×マークrect
        self.cannot_font = pygame.font.SysFont(self.font_path, LEFT_H // 2)
        self.cannot_disp = self.cannot_font.render("X", True, RED)
        self.cannot_rect = None
        
        # ×マーク表示位置
        self.is_cannot = False
        self.cannot_ore_num, self.cannot_quantity = -1, -1
        
        # 小窓の設定
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.permit_font = pygame.font.SysFont(self.font_path, FULL_H // 12)
        
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
    
    # 鉱石売却
    def sell_ore(self):
        if self.sell_quantity != 3:
            settings.money += int(settings.ore_price_list[self.sell_ore_num] * settings.ore_price_ratio[self.sell_ore_num]) * 10**self.sell_quantity
            settings.ore_possession_list[self.sell_ore_num] -= 10**self.sell_quantity
        else:
            settings.money += int(settings.ore_price_list[self.sell_ore_num] * settings.ore_price_ratio[self.sell_ore_num]) * settings.ore_possession_list[self.sell_ore_num]
            settings.ore_possession_list[self.sell_ore_num] = 0
        self.sell_ore_num, self.sell_quantity = -1, -1
        self.update_page()
    
    # ページ内変数のアップデート
    def update_page(self):
        for i in range(len(settings.ore_list)):
            self.price_disp[i] = self.price_font.render(f"￥{int(settings.ore_price_list[i] * settings.ore_price_ratio[i]):,} / 個", True, BLACK)
            self.price_rect[i] = self.price_disp[i].get_rect(midright=self.price_rect_real[i].midright)
    
    def draw(self, canvas):
        canvas.fill(WHITE)
        # 見出しの描画
        canvas.blit(self.headline_disp, self.headline_rect)
        # 鉱石売却画面の描画
        for i in range(settings.ore_limit(settings.ore_prop_list)):
            if i % 2 == 0:
                canvas.blit(self.ore_image[i], (0, HEADLINE_SIZE + (i//2)*LEFT_H))
                pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE + (i//2+1)*LEFT_H), (MINE_W // 2, HEADLINE_SIZE + (i//2+1)*LEFT_H), 1)
            else:
                canvas.blit(self.ore_image[i], (MINE_W // 2, HEADLINE_SIZE + (i//2)*LEFT_H))
                pygame.draw.line(canvas, BLACK, (MINE_W // 2, HEADLINE_SIZE + (i//2+1)*LEFT_H), (MINE_W, HEADLINE_SIZE + (i//2+1)*LEFT_H), 1)
            canvas.blit(self.sell_ore_name_disp[i], self.sell_ore_name_rect[i])
            canvas.blit(self.price_disp[i], self.price_rect[i])
            for j in range(4):
                pygame.draw.rect(canvas, self.sell_button_color[i][j], self.sell_button[i][j])
                pygame.draw.rect(canvas, BLACK, self.sell_button[i][j], 2)
                canvas.blit(self.sell_button_disp[j], self.sell_button_rect[i][j])
        pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE), (MINE_W, HEADLINE_SIZE), 1)
        pygame.draw.line(canvas, BLACK, (MINE_W // 2, HEADLINE_SIZE), (MINE_W // 2, HEADLINE_SIZE + LEFT_H * ((settings.ore_limit(settings.ore_prop_list)+1)//2)), 1)
    
    # 売却確認画面
    def sell_select_draw(self, canvas):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        self.permit_text = []
        if self.sell_quantity != 3:
            self.permit_text.append(f"{settings.ore_name_list[self.sell_ore_num]} {10**self.sell_quantity:,}個")
        else:
            self.permit_text.append(f"{settings.ore_name_list[self.sell_ore_num]} {settings.ore_possession_list[self.sell_ore_num]:,}個")
        self.permit_text.append("売却しますか？")
        
        self.permit_disp = []
        self.permit_rect = []
        for i in range(len(self.permit_text)):
            self.permit_disp.append(self.permit_font.render(f"{self.permit_text[i]}", True, BLACK))
            self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])
    
    # 所持数以上の鉱石を売却しようとしたときに×を出す
    def cannot_sell_draw(self, canvas):
        self.cannot_rect = self.cannot_disp.get_rect(center=self.sell_button[self.cannot_ore_num][self.cannot_quantity].center)
        canvas.blit(self.cannot_disp, self.cannot_rect)