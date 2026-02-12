import pygame
import sys
import settings

FULL_W = settings.Display.WIDTH
FULL_H = settings.Display.HEIGHT

MINE_W = settings.Display.MINE_W
MINE_H = settings.Display.MINE_H
RIGHT_H = settings.Display.RIGHT_H

button_quantity = settings.bottom_button_quantity

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
LIGHTGREEN = settings.Color.LIGHTGREEN
YELLOW = settings.Color.YELLOW
GRAY = settings.Color.GRAY
DARK_GRAY = settings.Color.DARK_GRAY

class Basescene:
    def __init__(self) -> None:
        # 文字フォント
        self.font_path = "msgothic"
        
        # 右側鉱石画像ダウンロード
        self.ore_image_default = []
        self.right_ore_image = []
        for i, IMAGE in enumerate(settings.ORE_IMAGE):
            self.ore_image_default.append(pygame.image.load(IMAGE).convert_alpha())
            self.right_ore_image.append(pygame.transform.scale(self.ore_image_default[i], (RIGHT_H, RIGHT_H)))
        
        # 右側画面
        self.right_rect = pygame.Rect(MINE_W, 0, FULL_W - MINE_W, MINE_H)
        self.right_font = pygame.font.SysFont(self.font_path, RIGHT_H)
        
        # 現在のステージrect
        self.stage_num_disp = self.right_font.render(f"-第{settings.stage_num:,}層-", True, BLACK)
        self.stage_num_rect_real = pygame.Rect(MINE_W, 0, FULL_W - MINE_W, RIGHT_H)
        self.stage_num_rect = self.stage_num_disp.get_rect(center=self.stage_num_rect_real.center)
                
        # 所持金rect
        if settings.money < 1e9:
            self.money_disp = self.right_font.render(f"￥{settings.money:,}", True, BLACK)
        else:
            self.money_disp = self.right_font.render(f"￥{settings.money:.2E}".replace("+", ""), True, BLACK)
        self.money_rect_real = pygame.Rect(MINE_W, RIGHT_H, FULL_W - MINE_W, RIGHT_H)
        self.money_rect = self.money_disp.get_rect(midright=(FULL_W - 5, RIGHT_H * 3//2))
        
        # 鉱石の名前rect
        self.ore_font = pygame.font.SysFont(self.font_path, RIGHT_H)
        self.ore_small_font = pygame.font.SysFont(self.font_path, RIGHT_H // 2 - 1)
        self.ore_rect = [None] * len(settings.ore_list)
        self.ore_name_disp = [None] * len(settings.ore_list)
        self.ore_name_rect = [None] * len(settings.ore_list)
        for i in range(len(settings.ore_list)):
            self.ore_rect[i] = pygame.Rect(MINE_W + RIGHT_H, (2+i)*RIGHT_H, FULL_W - (MINE_W + RIGHT_H), RIGHT_H)
            if len(settings.ore_name_list[i]) <= 2:
                self.ore_name_disp[i] = self.ore_font.render(settings.ore_name_list[i], True, BLACK)
                self.ore_name_rect[i] = self.ore_name_disp[i].get_rect(midleft=self.ore_rect[i].midleft)
            elif len(settings.ore_name_list[i]) <= 6:
                self.ore_name_disp[i] = self.ore_small_font.render(settings.ore_name_list[i], True, BLACK)
                self.ore_name_rect[i] = self.ore_name_disp[i].get_rect(midleft=self.ore_rect[i].midleft)
            else:
                self.ore_name_disp[i] = [None] * 2
                self.ore_name_rect[i] = [None] * 2
                if settings.ore_list[i] == "alexandrite":
                    self.ore_name_disp[i][0] = self.ore_small_font.render(settings.ore_name_list[i][:6], True, BLACK)
                    self.ore_name_disp[i][1] = self.ore_small_font.render(" "+settings.ore_name_list[i][6:], True, BLACK)
                elif settings.ore_list[i] == "paraiba_tourmaline":
                    self.ore_name_disp[i][0] = self.ore_small_font.render(settings.ore_name_list[i][:4], True, BLACK)
                    self.ore_name_disp[i][1] = self.ore_small_font.render(" "+settings.ore_name_list[i][4:], True, BLACK)
                elif settings.ore_list[i] == "padparadscha_sapphire":
                    self.ore_name_disp[i][0] = self.ore_small_font.render(settings.ore_name_list[i][:5], True, BLACK)
                    self.ore_name_disp[i][1] = self.ore_small_font.render(" "+settings.ore_name_list[i][5:], True, BLACK)
                self.ore_name_rect[i][0] = self.ore_name_disp[i][0].get_rect(bottomleft=self.ore_rect[i].midleft)
                self.ore_name_rect[i][1] = self.ore_name_disp[i][1].get_rect(topleft=self.ore_rect[i].midleft)
        
        # 鉱石の所持数rect
        self.ore_possession_disp = [None] * len(settings.ore_list)
        self.ore_possession_rect = [None] * len(settings.ore_list)
        for i in range(len(settings.ore_list)):
            self.ore_possession_disp[i] = self.ore_font.render(f"{settings.ore_possession_list[i]:,}個", True, BLACK)
            self.ore_possession_rect[i] = self.ore_possession_disp[i].get_rect(midright=self.ore_rect[i].midright)
        
        # 下部ボタン
        self.buttons_rect = pygame.Rect(0, MINE_H, FULL_W, FULL_H - MINE_H)
        self.button_font = pygame.font.SysFont(self.font_path, settings.bottom_button_font_size)
        self.button_color = [GRAY] * button_quantity
        self.button_color[0] = DARK_GRAY
        self.button = []
        self.button_text = []
        self.button_text_rect = []
        for i in range(button_quantity):
            self.button.append(pygame.Rect(i * FULL_W // button_quantity, MINE_H, FULL_W // button_quantity, FULL_H - MINE_H))
            self.button_text.append(self.button_font.render(f"{settings.bottom_button_name[i]}", True, BLACK))
            self.button_text_rect.append(self.button_text[i].get_rect(center=self.button[i].center))
    
    # 画面移動
    def change_page(self, num=0):
        self.button_color = [GRAY] * button_quantity
        self.button_color[num] = DARK_GRAY
        
        if num == 0:
            self.stage_num_disp = self.right_font.render(f"-第{settings.stage_num:,}層-", True, BLACK)
        else:
            self.stage_num_disp = self.right_font.render(f"-{settings.bottom_button_name[num]}-", True, BLACK)
        self.stage_num_rect = self.stage_num_disp.get_rect(center=self.stage_num_rect_real.center)
    
    # 変数のアップデート
    def update_page(self):
        self.stage_num_disp = self.right_font.render(f"-第{settings.stage_num:,}層-", True, BLACK)
        self.stage_num_rect = self.stage_num_disp.get_rect(center=self.stage_num_rect_real.center)
        
        if settings.money < 1e9:
            self.money_disp = self.right_font.render(f"￥{settings.money:,}", True, BLACK)
        else:
            self.money_disp = self.right_font.render(f"￥{settings.money:.2E}".replace("+", ""), True, BLACK)
        self.money_rect = self.money_disp.get_rect(midright=(FULL_W - 5, RIGHT_H * 3//2))
        
        for i in range(len(settings.ore_list)):
            self.ore_possession_disp[i] = self.ore_font.render(f"{settings.ore_possession_list[i]:,}個", True, BLACK)
            self.ore_possession_rect[i] = self.ore_possession_disp[i].get_rect(midright=self.ore_rect[i].midright)
    
    def draw_base(self, canvas):
        # 右側画面の描画
        pygame.draw.rect(canvas, LIGHTGREEN, self.right_rect)
        # ステージ番号の描画
        pygame.draw.rect(canvas, WHITE, self.stage_num_rect_real)
        pygame.draw.rect(canvas, BLACK, self.stage_num_rect_real, 1)
        canvas.blit(self.stage_num_disp, self.stage_num_rect)
        # 金額の描画
        pygame.draw.rect(canvas, YELLOW, self.money_rect_real)
        pygame.draw.rect(canvas, BLACK, self.money_rect_real, 1)
        canvas.blit(self.money_disp, self.money_rect)
        # 鉱石の所持数の描画
        for i in range(settings.ore_limit(settings.ore_prop_list)):
            canvas.blit(self.right_ore_image[i], (MINE_W, (2+i)*RIGHT_H))
            if len(settings.ore_name_list[i]) <= 6:
                canvas.blit(self.ore_name_disp[i], self.ore_name_rect[i])
            else:
                canvas.blit(self.ore_name_disp[i][0], self.ore_name_rect[i][0])
                canvas.blit(self.ore_name_disp[i][1], self.ore_name_rect[i][1])
            canvas.blit(self.ore_possession_disp[i], self.ore_possession_rect[i])
            pygame.draw.line(canvas, BLACK, (MINE_W, (3+i)*RIGHT_H), (FULL_W, (3+i)*RIGHT_H), 2)
        pygame.draw.line(canvas, BLACK, (MINE_W, 2*RIGHT_H), (FULL_W, 2*RIGHT_H), 1)
        # 右側画面の枠線
        pygame.draw.line(canvas, BLACK, (MINE_W, 0), (MINE_W, MINE_H), 2)
        # 下部ボタンの描画
        pygame.draw.rect(canvas, BLACK, self.buttons_rect)
        for i in range(len(self.button)):
            pygame.draw.rect(canvas, self.button_color[i], self.button[i])
            pygame.draw.rect(canvas, BLACK, self.button[i], width=2)
            if self.button_text[i] is not None:
                canvas.blit(self.button_text[i], self.button_text_rect[i])