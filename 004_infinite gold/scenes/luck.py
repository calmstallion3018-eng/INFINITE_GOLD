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

button_quantity = settings.bottom_button_quantity

ADJUST = 5

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
LIGHTGREEN = settings.Color.LIGHTGREEN
YELLOW = settings.Color.YELLOW
GRAY = settings.Color.GRAY
RED = settings.Color.RED
GREEN = settings.Color.GREEN

class Main():
    def __init__(self) -> None:
        # 文字フォント
        self.font_path = "msgothic"
        
        # 画像ダウンロード
        self.ore_image_default = []
        self.ore_image = []
        for i, IMAGE in enumerate(settings.ORE_IMAGE):
            self.ore_image_default.append(pygame.image.load(IMAGE).convert_alpha())
            self.ore_image.append(pygame.transform.scale(self.ore_image_default[i], (TEXT_SIZE, TEXT_SIZE)))
        
        # 幸運の花ダウンロード
        self.image_lucky_flower = pygame.image.load(settings.FLOWER_IMAGE).convert_alpha()
        self.image_lucky_flower = pygame.transform.scale(self.image_lucky_flower, (HEADLINE_SIZE - 2*ADJUST, HEADLINE_SIZE - 2*ADJUST))
        
        # 幸運の花rect
        self.lucky_flower_font = pygame.font.SysFont(self.font_path, HEADLINE_SIZE * 2//3)
        self.lucky_flower_disp = self.lucky_flower_font.render(f"幸運の花 現在：LEVEL {settings.lucky_flower_level}", True, BLACK)
        self.lucky_flower_rect_real = pygame.Rect(HEADLINE_SIZE, 0, MINE_W - HEADLINE_SIZE, HEADLINE_SIZE)
        self.lucky_flower_rect = self.lucky_flower_disp.get_rect(center=self.lucky_flower_rect_real.center)
        
        # レベル上昇rect
        self.level_font = pygame.font.SysFont(self.font_path, TEXT_SIZE * 3//2)
        self.levelup_before_disp = self.level_font.render(f"LEVEL {settings.lucky_flower_level}", True, BLACK)
        self.levelup_before_rect_real = pygame.Rect(0, HEADLINE_SIZE ,MINE_W // 2, 2*TEXT_SIZE)
        self.levelup_before_rect = self.levelup_before_disp.get_rect(center=self.levelup_before_rect_real.center)
        self.levelup_arrow_disp = self.level_font.render("→", True, BLACK)
        self.levelup_arrow_rect = self.levelup_arrow_disp.get_rect(center=(MINE_W // 2, HEADLINE_SIZE + TEXT_SIZE))
        self.levelup_after_disp = self.level_font.render(f"LEVEL {settings.lucky_flower_level+1}", True, BLACK)
        self.levelup_after_rect_real = pygame.Rect(MINE_W // 2, HEADLINE_SIZE ,MINE_W // 2, 2*TEXT_SIZE)
        self.levelup_after_rect = self.levelup_after_disp.get_rect(center=self.levelup_after_rect_real.center)
        
        self.levelup_font = pygame.font.SysFont(self.font_path, TEXT_SIZE)
        self.levelup_before_ore_name_disp = [None] * len(settings.ore_list)
        self.levelup_before_ore_prop_disp = [None] * len(settings.ore_list)
        self.levelup_before_ore_rect_real = [None] * len(settings.ore_list)
        self.levelup_before_ore_name_rect = [None] * len(settings.ore_list)
        self.levelup_before_ore_prop_rect = [None] * len(settings.ore_list)
        for i in range(len(settings.ore_list)):
            self.levelup_before_ore_name_disp[i] = self.levelup_font.render(settings.ore_name_list[i], True, BLACK)
            self.levelup_before_ore_prop_disp[i] = self.levelup_font.render(f"{settings.ore_prop_list[i]:.1%}", True, BLACK)
            self.levelup_before_ore_rect_real[i] = pygame.Rect(TEXT_SIZE, HEADLINE_SIZE + (i+2)*TEXT_SIZE, MINE_W // 2 - TEXT_SIZE - 1, TEXT_SIZE)
            self.levelup_before_ore_name_rect[i] = self.levelup_before_ore_name_disp[i].get_rect(midleft=self.levelup_before_ore_rect_real[i].midleft)
            self.levelup_before_ore_prop_rect[i] = self.levelup_before_ore_prop_disp[i].get_rect(midright=self.levelup_before_ore_rect_real[i].midright)
        
        self.levelup_updown_ore_prop_disp = [None] * len(settings.ore_list)
        self.levelup_after_ore_prop_disp = [None] * len(settings.ore_list)
        self.levelup_after_ore_rect_real = [None] * len(settings.ore_list)
        self.levelup_updown_ore_prop_rect = [None] * len(settings.ore_list)
        self.levelup_after_ore_prop_rect = [None] * len(settings.ore_list)
        for i in range(len(settings.ore_list)):
            for j in range(len(settings.prop_change_change_list)):
                if settings.lucky_flower_level <= settings.prop_change_change_list[j]:
                    if settings.ore_prop_change_list[j][i] < 0:
                        self.levelup_updown_ore_prop_disp[i] = self.levelup_font.render(f"{settings.ore_prop_change_list[j][i]:.1%}", True, RED)
                        self.levelup_after_ore_prop_disp[i] = self.levelup_font.render(f"{(settings.ore_prop_list[i] + settings.ore_prop_change_list[j][i]):.1%}", True, RED)
                    elif settings.ore_prop_change_list[j][i] == 0:
                        self.levelup_updown_ore_prop_disp[i] = self.levelup_font.render("+0.0%", True, BLACK)
                        self.levelup_after_ore_prop_disp[i] = self.levelup_font.render(f"{(settings.ore_prop_list[i] + settings.ore_prop_change_list[j][i]):.1%}", True, BLACK)
                    else:
                        self.levelup_updown_ore_prop_disp[i] = self.levelup_font.render(f"+{settings.ore_prop_change_list[j][i]:.1%}", True, GREEN)
                        self.levelup_after_ore_prop_disp[i] = self.levelup_font.render(f"{(settings.ore_prop_list[i] + settings.ore_prop_change_list[j][i]):.1%}", True, GREEN)
                    break
            self.levelup_after_ore_rect_real[i] = pygame.Rect(MINE_W // 2, HEADLINE_SIZE + (i+2)*TEXT_SIZE, MINE_W // 2 - 1, TEXT_SIZE)
            self.levelup_updown_ore_prop_rect[i] = self.levelup_updown_ore_prop_disp[i].get_rect(midleft=self.levelup_after_ore_rect_real[i].center)
            self.levelup_after_ore_prop_rect[i] = self.levelup_after_ore_prop_disp[i].get_rect(midright=self.levelup_after_ore_rect_real[i].midright)
        
        # レベルアップボタン
        self.button_levelup_color = GRAY
        self.button_levelup = pygame.Rect(MINE_W // 6, MINE_H * 4//5, MINE_W * 2//3, 3*TEXT_SIZE)
        self.button_levelup_font = pygame.font.SysFont(self.font_path, TEXT_SIZE * 2)
        if int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level) < 1e6:
            self.button_levelup_disp = self.button_levelup_font.render(f"LEVEL UP ￥{int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level):,}", True, BLACK)
        else:
            self.button_levelup_disp = self.button_levelup_font.render(f"LEVEL UP ￥{int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level):.2E}".replace("+", ""), True, BLACK)
        self.button_levelup_rect = self.button_levelup_disp.get_rect(center=self.button_levelup.center)
        
        # レベルアップ選択画面の表示
        self.can_select = False
        
        # ×マークrect
        self.cannot_font = pygame.font.SysFont(self.font_path, 3*TEXT_SIZE)
        self.cannot_disp = self.cannot_font.render("X", True, RED)
        self.cannot_rect = self.cannot_disp.get_rect(center=self.button_levelup.center)
        
        # ×マーク表示
        self.is_cannot = False
        
        # 小窓の設定
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.permit_font_1 = pygame.font.SysFont(self.font_path, FULL_H // 18)
        self.permit_font_2 = pygame.font.SysFont(self.font_path, FULL_H // 36)
        self.permit_font = [self.permit_font_1] * 2 + [self.permit_font_2]
        
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
    
    # 左側画面の鉱石を制限
    def left_ore_limit(self):
        ore = len(settings.ore_prop_list)
        for i in range(len(settings.prop_change_change_list)):
            if settings.lucky_flower_level <= settings.prop_change_change_list[i]:
                lst = list(map(lambda x, y: x+y, settings.ore_prop_list, settings.ore_prop_change_list[i]))
                break
        while True:
            if lst[ore-1] !=  0:
                break
            ore -= 1
        return ore
    
    # 幸運の花レベルアップ
    def flower_levelup(self):
        for i in range(len(settings.prop_change_change_list)):
            if settings.lucky_flower_level <= settings.prop_change_change_list[i]:
                settings.ore_prop_list = list(map(lambda x, y: x+y, settings.ore_prop_list, settings.ore_prop_change_list[i]))
                break
        settings.money -= int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level)
        settings.lucky_flower_level += 1
        settings.record_list[13] = max(settings.lucky_flower_level, settings.record_list[13])
        self.update_page()
    
    # ページ内変数のアップデート
    def update_page(self):
        self.lucky_flower_disp = self.lucky_flower_font.render(f"幸運の花 現在：LEVEL {settings.lucky_flower_level}", True, BLACK)
        self.lucky_flower_rect = self.lucky_flower_disp.get_rect(center=self.lucky_flower_rect_real.center)
        self.levelup_before_disp = self.level_font.render(f"LEVEL {settings.lucky_flower_level}", True, BLACK)
        self.levelup_before_rect = self.levelup_before_disp.get_rect(center=self.levelup_before_rect_real.center)
        for i in range(len(settings.ore_list)):
            self.levelup_before_ore_prop_disp[i] = self.levelup_font.render(f"{settings.ore_prop_list[i]:.1%}", True, BLACK)
            self.levelup_before_ore_prop_rect[i] = self.levelup_before_ore_prop_disp[i].get_rect(midright=self.levelup_before_ore_rect_real[i].midright)
        self.levelup_after_disp = self.level_font.render(f"LEVEL {settings.lucky_flower_level+1}", True, BLACK)
        self.levelup_after_rect = self.levelup_after_disp.get_rect(center=self.levelup_after_rect_real.center)
        for i in range(len(settings.ore_list)):
            for j in range(len(settings.prop_change_change_list)):
                if settings.lucky_flower_level <= settings.prop_change_change_list[j]:
                    if settings.ore_prop_change_list[j][i] < 0:
                        self.levelup_updown_ore_prop_disp[i] = self.levelup_font.render(f"{settings.ore_prop_change_list[j][i]:.1%}", True, RED)
                        self.levelup_after_ore_prop_disp[i] = self.levelup_font.render(f"{(settings.ore_prop_list[i] + settings.ore_prop_change_list[j][i]):.1%}", True, RED)
                    elif settings.ore_prop_change_list[j][i] == 0:
                        self.levelup_updown_ore_prop_disp[i] = self.levelup_font.render("+0.0%", True, BLACK)
                        self.levelup_after_ore_prop_disp[i] = self.levelup_font.render(f"{(settings.ore_prop_list[i] + settings.ore_prop_change_list[j][i]):.1%}", True, BLACK)
                    else:
                        self.levelup_updown_ore_prop_disp[i] = self.levelup_font.render(f"+{settings.ore_prop_change_list[j][i]:.1%}", True, GREEN)
                        self.levelup_after_ore_prop_disp[i] = self.levelup_font.render(f"{(settings.ore_prop_list[i] + settings.ore_prop_change_list[j][i]):.1%}", True, GREEN)
                    break
            self.levelup_updown_ore_prop_rect[i] = self.levelup_updown_ore_prop_disp[i].get_rect(midleft=self.levelup_after_ore_rect_real[i].center)
            self.levelup_after_ore_prop_rect[i] = self.levelup_after_ore_prop_disp[i].get_rect(midright=self.levelup_after_ore_rect_real[i].midright)
        if int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level) < 1e6:
            self.button_levelup_disp = self.button_levelup_font.render(f"LEVEL UP ￥{int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level):,}", True, BLACK)
        else:
            self.button_levelup_disp = self.button_levelup_font.render(f"LEVEL UP ￥{int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level):.2E}".replace("+", ""), True, BLACK)
        self.button_levelup_rect = self.button_levelup_disp.get_rect(center=self.button_levelup.center)

    # 描画処理
    def draw(self, canvas):
        canvas.fill(WHITE)
        # 幸運の花の描画
        canvas.blit(self.image_lucky_flower, (ADJUST, ADJUST))
        canvas.blit(self.lucky_flower_disp, self.lucky_flower_rect)
        pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE), (MINE_W, HEADLINE_SIZE), 2)
        # レベルアップ前後の確率の描画
        canvas.blit(self.levelup_before_disp, self.levelup_before_rect)
        canvas.blit(self.levelup_arrow_disp, self.levelup_arrow_rect)
        canvas.blit(self.levelup_after_disp, self.levelup_after_rect)
        for i in range(self.left_ore_limit()):
            canvas.blit(self.ore_image[i], (0, HEADLINE_SIZE + (i+2)*TEXT_SIZE))
            canvas.blit(self.levelup_before_ore_name_disp[i], self.levelup_before_ore_name_rect[i])
            canvas.blit(self.levelup_before_ore_prop_disp[i], self.levelup_before_ore_prop_rect[i])
            canvas.blit(self.levelup_updown_ore_prop_disp[i], self.levelup_updown_ore_prop_rect[i])
            canvas.blit(self.levelup_after_ore_prop_disp[i], self.levelup_after_ore_prop_rect[i])
        # レベルアップボタンの描画
        if settings.lucky_flower_level < 200:
            pygame.draw.rect(canvas, self.button_levelup_color, self.button_levelup)
            pygame.draw.rect(canvas, BLACK, self.button_levelup, width=2)
            canvas.blit(self.button_levelup_disp, self.button_levelup_rect)
    
    # レベルアップ確認画面
    def levelup_select_draw(self, canvas):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        self.permit_text = [f"幸運の花 LEVEL {settings.lucky_flower_level} → {settings.lucky_flower_level+1}", "LEVEL UPしますか？", "※鉱石の出現確率は次の層から適用されます"]
        self.permit_disp = []
        self.permit_rect = []
        for i in range(len(self.permit_text)):
            self.permit_disp.append(self.permit_font[i].render(f"{self.permit_text[i]}", True, BLACK))
            self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (2*i+9)*FULL_H // 24)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])

    # レベルアップ不可能時に×を出す
    def cannot_levelup_draw(self, canvas):
        canvas.blit(self.cannot_disp, self.cannot_rect)