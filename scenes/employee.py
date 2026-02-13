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
ARROW_W = MINE_W // 21
CHARACTER_SIZE = (MINE_W - 2*ARROW_W) // 3

button_quantity = settings.bottom_button_quantity

ADJUST = 2

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
LIGHTGREEN = settings.Color.LIGHTGREEN
YELLOW = settings.Color.YELLOW
GRAY = settings.Color.GRAY
DARK_GRAY = settings.Color.DARK_GRAY
RED = settings.Color.RED

class Main():
    def __init__(self) -> None:
        # 文字フォント
        self.font_path = "msgothic"
        
        # ツルハシ変更画面の行サイズ
        self.change_pickaxes_size = TEXT_SIZE * 3//2
        
        # 新たな鉱夫を採用するrect
        self.headline_font = pygame.font.SysFont(self.font_path, HEADLINE_SIZE // 2)
        self.headline_disp = self.headline_font.render(f"鉱夫を採用する　現在雇用人数: {len(settings.character_speed)}人", True, BLACK)
        self.headline_rect_real = pygame.Rect(0,0,MINE_W, HEADLINE_SIZE)
        self.headline_rect = self.headline_disp.get_rect(center=self.headline_rect_real.center)
        
        # 新鉱夫ダウンロード
        self.image_character = pygame.image.load(settings.CHARACTER_IMAGE).convert_alpha()
        self.image_character = pygame.transform.scale(self.image_character, (CHARACTER_SIZE, CHARACTER_SIZE))
        
        # ツルハシのダウンロード（石、鉄、銅、銀、金、ダイヤモンド）
        self.image_pickaxe_default = [None] * len(settings.pickaxe_type)
        self.image_pickaxe = [None] * len(settings.pickaxe_type)
        self.image_change_pickaxe = [None] * len(settings.pickaxe_type)
        for i in range(len(settings.pickaxe_type)):
            self.image_pickaxe_default[i] = pygame.image.load(settings.PICKAXE_IMAGE[i]).convert_alpha()
            self.image_pickaxe[i] = pygame.transform.scale(self.image_pickaxe_default[i], (TEXT_SIZE, TEXT_SIZE))
            self.image_change_pickaxe[i] = pygame.transform.scale(self.image_pickaxe_default[i], (self.change_pickaxes_size, self.change_pickaxes_size))
        
        # 何人目の鉱夫を表示しているか（3人ずつしか表示できないため、0 -> 0~2人目、0~len(settings.character_speed)-2）
        self.what_character_num = 0
        
        # 鉱夫採用rect
        self.profile_font = pygame.font.SysFont(self.font_path, TEXT_SIZE)
        self.button_font = pygame.font.SysFont(self.font_path, TEXT_SIZE * 2//3)
        self.character_all_rect = []
        self.character_name_disp = []
        self.character_name_rect = []
        self.move_speed_disp = []
        self.move_speed_rect = []
        self.set_pickaxe_disp1 = []
        self.set_pickaxe_disp2 = []
        self.set_pickaxe_rect1 = []
        self.set_pickaxe_rect2 = []
        self.change_pickaxe_button_color = []
        self.change_pickaxe_button = []
        self.change_pickaxe_disp = self.button_font.render("装備の変更", True, BLACK)
        self.change_pickaxe_rect = []
        self.character_levelup_button_color = []
        self.character_levelup_button = []
        self.character_levelup_disp = self.button_font.render("昇給", True, BLACK)
        self.character_levelup_rect = []
        self.levelup_money_disp = []
        self.levelup_money_rect = []
        self.employ_money_disp = None
        self.employ_money_rect = None
        self.new_character_color = GRAY
        self.new_character_button = None
        self.new_character_disp = self.button_font.render("採用する", True, BLACK)
        self.new_character_rect = None
        for i in range(min(len(settings.character_speed)+1, 3)): # 3人までしか表示できない
            self.character_all_rect.append(pygame.Rect(ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE, CHARACTER_SIZE, MINE_H - HEADLINE_SIZE))
            self.character_name_disp.append(self.profile_font.render(f"{i+1+self.what_character_num}人目", True, BLACK))
            self.character_name_rect.append(self.character_name_disp[i].get_rect(center=(ARROW_W + (2*i+1)*CHARACTER_SIZE // 2, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE // 2)))
            if i != len(settings.character_speed) - self.what_character_num:
                self.move_speed_disp.append(self.profile_font.render(f"移動速度: {settings.character_speed[i+self.what_character_num]}", True, BLACK))
                self.move_speed_rect.append(self.move_speed_disp[i].get_rect(midleft=(ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 3//2)))
                if settings.use_pickaxe_type[i+1+self.what_character_num] is not None:
                    self.set_pickaxe_disp1.append(self.profile_font.render(f"{settings.pickaxe_type[settings.use_pickaxe_type[i+1+self.what_character_num]]}のツルハシ", True, BLACK))
                    self.set_pickaxe_disp2.append(self.profile_font.render(f"+{settings.pickaxe_level[settings.use_pickaxe_type[i+1+self.what_character_num]][settings.use_pickaxe_num[i+1+self.what_character_num]]} を使用中"))
                else:
                    self.set_pickaxe_disp1.append(self.profile_font.render("ツルハシを装備", True, BLACK))
                    self.set_pickaxe_disp2.append(self.profile_font.render("していません", True, BLACK))
                self.set_pickaxe_rect1.append(self.set_pickaxe_disp1[i].get_rect(midleft=(ARROW_W + i*CHARACTER_SIZE + TEXT_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 5//2)))
                self.set_pickaxe_rect2.append(self.set_pickaxe_disp2[i].get_rect(midright=(ARROW_W + (i+1)*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 7//2)))
                self.change_pickaxe_button_color.append(GRAY)
                self.change_pickaxe_button.append(pygame.Rect(ARROW_W + (6*i+1)*CHARACTER_SIZE // 6, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 9//2, CHARACTER_SIZE * 2//3, TEXT_SIZE))
                self.change_pickaxe_rect.append(self.change_pickaxe_disp.get_rect(center=self.change_pickaxe_button[i].center))
                self.character_levelup_button_color.append(GRAY)
                self.character_levelup_button.append(pygame.Rect(ARROW_W + (6*i+1)*CHARACTER_SIZE // 6, HEADLINE_SIZE + CHARACTER_SIZE + 6*TEXT_SIZE, CHARACTER_SIZE * 2//3, TEXT_SIZE))
                self.character_levelup_rect.append(self.character_levelup_disp.get_rect(center=self.character_levelup_button[i].center))
                if int(settings.employ_money_zero * settings.employ_money_ratio**(i+self.what_character_num) * settings.raise_money_ratio(i+self.what_character_num)**(settings.character_speed[i+self.what_character_num])) < 1e6:
                    self.levelup_money_disp.append(self.profile_font.render(f"経費: ￥{int(settings.employ_money_zero * settings.employ_money_ratio**(i+self.what_character_num) * settings.raise_money_ratio(i+self.what_character_num)**(settings.character_speed[i+self.what_character_num])):,}", True, BLACK))
                else:
                    self.levelup_money_disp.append(self.profile_font.render(f"経費: ￥{int(settings.employ_money_zero * settings.employ_money_ratio**(i+self.what_character_num) * settings.raise_money_ratio(i+self.what_character_num)**(settings.character_speed[i+self.what_character_num])):.2E}", True, BLACK))
                self.levelup_money_rect.append(self.levelup_money_disp[i].get_rect(midright=(ARROW_W + (i+1)*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 8*TEXT_SIZE)))
            else:
                if settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed) < 1e9:
                    self.employ_money_disp = self.profile_font.render(f"￥{settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed):,}", True, BLACK)
                else:
                    self.employ_money_disp = self.profile_font.render(f"￥{settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed):.2E}", True, BLACK)
                self.employ_money_rect = self.employ_money_disp.get_rect(midright=(ARROW_W + (i+1)*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 3//2))
                self.new_character_button = pygame.Rect(ARROW_W + (6*i+1)*CHARACTER_SIZE // 6, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 5//2, CHARACTER_SIZE * 2//3, TEXT_SIZE)
                self.new_character_rect = self.new_character_disp.get_rect(center=self.new_character_button.center)
        
        # 左右矢印ボタン
        self.arrow_font = pygame.font.SysFont(self.font_path, 2*TEXT_SIZE)
        self.arrow_color = [GRAY] * 2
        self.arrow_button = []
        self.arrow_button.append(pygame.Rect(0, HEADLINE_SIZE, ARROW_W, MINE_H - HEADLINE_SIZE))
        self.arrow_button.append(pygame.Rect(MINE_W - ARROW_W, HEADLINE_SIZE, ARROW_W, MINE_H - HEADLINE_SIZE))
        self.arrow_text = ["<", ">"]
        self.arrow_disp = []
        self.arrow_rect = []
        for i in range(len(self.arrow_button)):
            self.arrow_disp.append(self.arrow_font.render(f"{self.arrow_text[i]}", True, BLACK))
            self.arrow_rect.append(self.arrow_disp[i].get_rect(center=self.arrow_button[i].center))
        
        # 採用選択画面の表示
        self.can_employ_select = False
                
        # 昇給選択画面の表示
        self.can_levelup_select = False
        
        # 昇給する人の番号(0~)
        self.character_levelup_num = -1
        
        # 装備選択画面の表示
        self.change_pickaxe_select = False
        
        # 装備する人の番号
        self.change_pickaxe_character_num = -1
        
        # 装備変更画面のスクロール用カメラ補正
        self.pickaxe_camera_y = 0
        
        # 表示できる（スクロールできる）画面の範囲
        self.scroll_screen = pygame.Rect(FULL_W // 4, FULL_H // 4 + self.change_pickaxes_size, FULL_W // 2, FULL_H // 2 - self.change_pickaxes_size)
        self.bar_w = 20
    
        # 装備変更画面rect
        self.pickaxes_font = pygame.font.SysFont(self.font_path, TEXT_SIZE)
        self.change_pickaxe_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        self.change_pickaxe_screen_border = pygame.Rect(FULL_W // 4 - ADJUST, FULL_H // 4 - ADJUST, FULL_W // 2 + 2*ADJUST, FULL_H // 2 + 2*ADJUST)
        if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is None:
            self.mini_headline_disp = self.pickaxes_font.render("ツルハシを装備していません", True, BLACK)
        else:
            self.mini_headline_disp = self.pickaxes_font.render(f"{settings.pickaxe_type[settings.use_pickaxe_type[self.change_pickaxe_character_num+1]]}のツルハシ +{settings.pickaxe_level[settings.use_pickaxe_type[self.change_pickaxe_character_num+1]][settings.use_pickaxe_num[self.change_pickaxe_character_num+1]]} を装備中", True, BLACK)
        self.mini_headline_rect = self.mini_headline_disp.get_rect(midleft=(FULL_W // 4 + self.change_pickaxes_size, FULL_H // 4 + self.change_pickaxes_size // 2))
        self.pickaxes_button_color = []
        self.pickaxes_button_can_push = []
        self.pickaxes_button = []
        self.pickaxes_button_disp = []
        self.pickaxes_button_rect = []
        self.sum_pickaxes = 0
        if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is not None:
            self.pickaxes_button_color.append(GRAY)
            self.pickaxes_button_can_push.append(True)
            self.pickaxes_button.append(pygame.Rect(FULL_W // 4, FULL_H // 4 + self.change_pickaxes_size + self.pickaxe_camera_y, FULL_W // 2 - self.bar_w, self.change_pickaxes_size))
            self.pickaxes_button_disp.append(self.pickaxes_font.render("装備中のツルハシを外す", True, BLACK))
            self.pickaxes_button_rect.append(self.pickaxes_button_disp[0].get_rect(midleft=self.pickaxes_button[0].midleft))
            self.sum_pickaxes += 1
        for i in range(len(settings.pickaxe_level)):
            for j in range(len(settings.pickaxe_level[i])):
                color_append = False
                for k in range(len(settings.use_pickaxe_type)):
                    if i == settings.use_pickaxe_type[k] and j == settings.use_pickaxe_num[k]:
                        if k == self.change_pickaxe_character_num + 1:
                            self.pickaxes_button_color.append(RED)
                        else:
                            self.pickaxes_button_color.append(WHITE)
                        self.pickaxes_button_can_push.append(False)
                        color_append = True
                        break
                if not color_append:
                    self.pickaxes_button_color.append(GRAY)
                    self.pickaxes_button_can_push.append(True)
                self.pickaxes_button.append(pygame.Rect(FULL_W // 4, FULL_H // 4 + (self.sum_pickaxes+1)*self.change_pickaxes_size + self.pickaxe_camera_y, FULL_W // 2 - self.bar_w, self.change_pickaxes_size))
                self.pickaxes_button_disp.append(self.pickaxes_font.render(f"{settings.pickaxe_type[i]}のツルハシ +{settings.pickaxe_level[i][j]}", True, BLACK))
                self.pickaxes_button_rect.append(self.pickaxes_button_disp[self.sum_pickaxes].get_rect(midleft=(FULL_W // 4 + self.change_pickaxes_size, FULL_H // 4 + (2*self.sum_pickaxes+3)*self.change_pickaxes_size // 2 - self.pickaxe_camera_y)))
                self.sum_pickaxes += 1
        
        # 装備変更画面の戻るボタン
        self.back_button = pygame.Rect(FULL_W // 4 + FULL_W * 5//12, FULL_H // 4, FULL_W // 12, self.change_pickaxes_size)
        self.back_button_color = GRAY
        self.back_button_disp = self.pickaxes_font.render("戻る", True, BLACK)
        self.back_button_rect = self.back_button_disp.get_rect(center=self.back_button.center)
        
        # キーボード操作時にどのツルハシを選択しているか(0~sum_pickaxes-1)
        self.pickaxes_which = None
        
        # スクロールバーrect
        self.scroll_view_h = FULL_H // 2 - self.change_pickaxes_size
        self.scroll_content_h = self.sum_pickaxes*self.change_pickaxes_size
        self.bar_h = max(20, self.scroll_view_h ** 2 // self.scroll_content_h)
        self.scroll_ratio = self.pickaxe_camera_y / (self.scroll_content_h - self.scroll_view_h)
        self.bar_y = self.scroll_screen.y + self.scroll_ratio * (self.scroll_view_h - self.bar_h)
        self.scroll_bar_rect = pygame.Rect(self.scroll_screen.right - (self.bar_w - 1), self.bar_y, self.bar_w - 2, self.bar_h)
        self.scroll_rail_rect = pygame.Rect(self.scroll_screen.right - self.bar_w, self.scroll_screen.y, self.bar_w, self.scroll_view_h)
        self.scroll_bar_color = DARK_GRAY
        
        # スクロールバーを掴んでいるか
        self.scroll_dragging = False
        self.drag_offset_y = 0
        
        # ×マークrect
        self.cannot_font = pygame.font.SysFont(self.font_path, TEXT_SIZE * 3//2)
        self.cannot_disp = self.cannot_font.render("X", True, RED)
        self.cannot_employ_rect = None
        if self.new_character_button is not None:
            self.cannot_employ_rect = self.cannot_disp.get_rect(center=self.new_character_button.center)
        
        self.cannot_levelup_rect = None
        self.cannot_levelup_num = -1
        
        # ×マーク表示
        self.is_cannot_employ = False
        self.is_cannot_levelup = False
        
        # 小窓の設定
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.employ_permit_font = pygame.font.SysFont(self.font_path, FULL_H // 12)
        self.levelup_permit_font = pygame.font.SysFont(self.font_path, FULL_H // 18)
        
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
    
    # 採用時の処理
    def new_character_employ(self):
        settings.money -= settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed)
        settings.mining_power.append(0)
        settings.use_pickaxe_type.append(None)
        settings.use_pickaxe_num.append(None)
        settings.character_speed.append(1)
        settings.character_move_time.append(None)
        settings.character_x.append(settings.Display.BLOCK_SIZE * 3//2)
        settings.character_y.append(settings.Display.BLOCK_SIZE * 3//2)
        settings.record_list[16] = max(len(settings.character_speed), settings.record_list[16])
        settings.record_list[17] = max(1, settings.record_list[17])
        self.update_page()
    
    # ツルハシ選択時の処理
    def change_pickaxe(self):
        # ツルハシの番号を逆算
        real_num = 1 if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is not None else 0
        if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is not None and self.pickaxes_which == 0:
            settings.use_pickaxe_type[self.change_pickaxe_character_num+1] = None
            settings.use_pickaxe_num[self.change_pickaxe_character_num+1] = None
            settings.mining_power[self.change_pickaxe_character_num+1] = 0
        else:
            ii, jj = -1, -1
            for i in range(len(settings.pickaxe_level)):
                for j in range(len(settings.pickaxe_level[i])):
                    if real_num == self.pickaxes_which:
                        ii, jj = i, j
                    real_num += 1
            settings.use_pickaxe_type[self.change_pickaxe_character_num+1], settings.use_pickaxe_num[self.change_pickaxe_character_num+1] = ii, jj
            settings.mining_power[self.change_pickaxe_character_num+1] = settings.pickaxe_power[ii] * (1+jj*settings.pickaxe_power_ratio)
        self.update_page()
    
    # 昇給時の処理
    def character_levelup(self):
        settings.money -= int(settings.employ_money_zero * settings.employ_money_ratio**self.character_levelup_num * settings.raise_money_ratio(self.character_levelup_num)**(settings.character_speed[self.character_levelup_num]))
        settings.character_speed[self.character_levelup_num] += 1
        settings.record_list[17] = max(settings.character_speed[self.character_levelup_num], settings.record_list[17])
        self.update_page()

    # ページ内変数のアップデート
    def update_page(self):
        self.headline_disp = self.headline_font.render(f"鉱夫を採用する　現在雇用人数: {len(settings.character_speed)}人", True, BLACK)
        self.headline_rect = self.headline_disp.get_rect(center=self.headline_rect_real.center)
        
        self.character_all_rect = []
        self.character_name_disp = []
        self.character_name_rect = []
        self.move_speed_disp = []
        self.move_speed_rect = []
        self.set_pickaxe_disp1 = []
        self.set_pickaxe_disp2 = []
        self.set_pickaxe_rect1 = []
        self.set_pickaxe_rect2 = []
        self.change_pickaxe_button_color = []
        self.change_pickaxe_button = []
        self.change_pickaxe_rect = []
        self.character_levelup_button_color = []
        self.character_levelup_button = []
        self.character_levelup_rect = []
        self.levelup_money_disp = []
        self.levelup_money_rect = []
        self.employ_money_disp = None
        self.employ_money_rect = None
        self.new_character_button = None
        self.new_character_rect = None
        for i in range(min(len(settings.character_speed)+1, 3)): # 3人までしか表示できない
            self.character_all_rect.append(pygame.Rect(ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE, CHARACTER_SIZE, MINE_H - HEADLINE_SIZE))
            self.character_name_disp.append(self.profile_font.render(f"{i+1+self.what_character_num}人目", True, BLACK))
            self.character_name_rect.append(self.character_name_disp[i].get_rect(center=(ARROW_W + (2*i+1)*CHARACTER_SIZE // 2, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE // 2)))
            if i != len(settings.character_speed) - self.what_character_num:
                self.move_speed_disp.append(self.profile_font.render(f"移動速度: {settings.character_speed[i+self.what_character_num]}", True, BLACK))
                self.move_speed_rect.append(self.move_speed_disp[i].get_rect(midleft=(ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 3//2)))
                if settings.use_pickaxe_type[i+1+self.what_character_num] is not None:
                    self.set_pickaxe_disp1.append(self.profile_font.render(f"{settings.pickaxe_type[settings.use_pickaxe_type[i+1+self.what_character_num]]}のツルハシ", True, BLACK))
                    self.set_pickaxe_disp2.append(self.profile_font.render(f"+{settings.pickaxe_level[settings.use_pickaxe_type[i+1+self.what_character_num]][settings.use_pickaxe_num[i+1+self.what_character_num]]} を使用中", True, BLACK))
                else:
                    self.set_pickaxe_disp1.append(self.profile_font.render("ツルハシを装備", True, BLACK))
                    self.set_pickaxe_disp2.append(self.profile_font.render("していません", True, BLACK))
                self.set_pickaxe_rect1.append(self.set_pickaxe_disp1[i].get_rect(midleft=(ARROW_W + i*CHARACTER_SIZE + TEXT_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 5//2)))
                self.set_pickaxe_rect2.append(self.set_pickaxe_disp2[i].get_rect(midright=(ARROW_W + (i+1)*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 7//2)))
                self.change_pickaxe_button_color.append(GRAY)
                self.change_pickaxe_button.append(pygame.Rect(ARROW_W + (6*i+1)*CHARACTER_SIZE // 6, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 9//2, CHARACTER_SIZE * 2//3, TEXT_SIZE))
                self.change_pickaxe_rect.append(self.change_pickaxe_disp.get_rect(center=self.change_pickaxe_button[i].center))
                self.character_levelup_button_color.append(GRAY)
                self.character_levelup_button.append(pygame.Rect(ARROW_W + (6*i+1)*CHARACTER_SIZE // 6, HEADLINE_SIZE + CHARACTER_SIZE + 6*TEXT_SIZE, CHARACTER_SIZE * 2//3, TEXT_SIZE))
                self.character_levelup_rect.append(self.character_levelup_disp.get_rect(center=self.character_levelup_button[i].center))
                if int(settings.employ_money_zero * settings.employ_money_ratio**(i+self.what_character_num) * settings.raise_money_ratio(i+self.what_character_num)**(settings.character_speed[i+self.what_character_num])) < 1e6:
                    self.levelup_money_disp.append(self.profile_font.render(f"経費: ￥{int(settings.employ_money_zero * settings.employ_money_ratio**(i+self.what_character_num) * settings.raise_money_ratio(i+self.what_character_num)**(settings.character_speed[i+self.what_character_num])):,}", True, BLACK))
                else:
                    self.levelup_money_disp.append(self.profile_font.render(f"経費: ￥{int(settings.employ_money_zero * settings.employ_money_ratio**(i+self.what_character_num) * settings.raise_money_ratio(i+self.what_character_num)**(settings.character_speed[i+self.what_character_num])):.2E}", True, BLACK))
                self.levelup_money_rect.append(self.levelup_money_disp[i].get_rect(midright=(ARROW_W + (i+1)*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 8*TEXT_SIZE)))
            else:
                if settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed) < 1e9:
                    self.employ_money_disp = self.profile_font.render(f"￥{settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed):,}", True, BLACK)
                else:
                    self.employ_money_disp = self.profile_font.render(f"￥{settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed):.2E}", True, BLACK)
                self.employ_money_rect = self.employ_money_disp.get_rect(midright=(ARROW_W + (i+1)*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 3//2))
                self.new_character_button = pygame.Rect(ARROW_W + (6*i+1)*CHARACTER_SIZE // 6, HEADLINE_SIZE + CHARACTER_SIZE + TEXT_SIZE * 5//2, CHARACTER_SIZE * 2//3, TEXT_SIZE)
                self.new_character_rect = self.new_character_disp.get_rect(center=self.new_character_button.center)
        
        self.cannot_employ_rect = None
        if self.new_character_button is not None:
            self.cannot_employ_rect = self.cannot_disp.get_rect(center=self.new_character_button.center)
    
    # 装備変更画面をマウスホイールもしくはキーボードで移動
    def update_camera(self, y):
        CAMERA_SPEED = 20
        self.pickaxe_camera_y -= y * CAMERA_SPEED
        self.pickaxe_camera_y = max(0, min(self.pickaxe_camera_y, (self.sum_pickaxes+1)*self.change_pickaxes_size - FULL_H // 2))
    
    # 装備変更画面をスクロールバーで移動
    def update_scrollbar(self):
        self.scroll_content_h = self.sum_pickaxes*self.change_pickaxes_size
        
        if self.scroll_content_h <= self.scroll_view_h:
            self.scroll_bar_rect.height = self.scroll_view_h
            self.scroll_bar_rect.y = self.scroll_screen.y
            return
        
        self.bar_h = max(20, self.scroll_view_h ** 2 // self.scroll_content_h)
        self.scroll_ratio = self.pickaxe_camera_y / (self.scroll_content_h - self.scroll_view_h)
        self.bar_y = self.scroll_screen.y + self.scroll_ratio * (self.scroll_view_h - self.bar_h)
        self.scroll_bar_rect = pygame.Rect(self.scroll_screen.right - (self.bar_w - 1), self.bar_y, self.bar_w - 2, self.bar_h)
    
    # 装備変更画面の更新
    def update_pickaxes_page(self):
        if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is None:
            self.mini_headline_disp = self.pickaxes_font.render("ツルハシを装備していません", True, BLACK)
        else:
            self.mini_headline_disp = self.pickaxes_font.render(f"{settings.pickaxe_type[settings.use_pickaxe_type[self.change_pickaxe_character_num+1]]}のツルハシ +{settings.pickaxe_level[settings.use_pickaxe_type[self.change_pickaxe_character_num+1]][settings.use_pickaxe_num[self.change_pickaxe_character_num+1]]} を装備中", True, BLACK)
        self.mini_headline_rect = self.mini_headline_disp.get_rect(midleft=(FULL_W // 4 + self.change_pickaxes_size, FULL_H // 4 + self.change_pickaxes_size // 2))
        self.pickaxes_button_color = []
        self.pickaxes_button_can_push = []
        self.pickaxes_button = []
        self.pickaxes_button_disp = []
        self.pickaxes_button_rect = []
        self.sum_pickaxes = 0
        if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is not None:
            self.pickaxes_button_color.append(GRAY)
            self.pickaxes_button_can_push.append(True)
            self.pickaxes_button.append(pygame.Rect(FULL_W // 4, FULL_H // 4 + self.change_pickaxes_size - self.pickaxe_camera_y, FULL_W // 2 - self.bar_w, self.change_pickaxes_size))
            self.pickaxes_button_disp.append(self.pickaxes_font.render("装備中のツルハシを外す", True, BLACK))
            self.pickaxes_button_rect.append(self.pickaxes_button_disp[0].get_rect(midleft=self.pickaxes_button[0].midleft))
            self.sum_pickaxes += 1
        for i in range(len(settings.pickaxe_level)):
            for j in range(len(settings.pickaxe_level[i])):
                color_append = False
                for k in range(len(settings.use_pickaxe_type)):
                    if i == settings.use_pickaxe_type[k] and j == settings.use_pickaxe_num[k]:
                        if k == self.change_pickaxe_character_num + 1:
                            self.pickaxes_button_color.append(RED)
                        else:
                            self.pickaxes_button_color.append(WHITE)
                        self.pickaxes_button_can_push.append(False)
                        color_append = True
                        break
                if not color_append:
                    self.pickaxes_button_color.append(GRAY)
                    self.pickaxes_button_can_push.append(True)
                self.pickaxes_button.append(pygame.Rect(FULL_W // 4, FULL_H // 4 + (self.sum_pickaxes+1)*self.change_pickaxes_size - self.pickaxe_camera_y, FULL_W // 2 - self.bar_w, self.change_pickaxes_size))
                self.pickaxes_button_disp.append(self.pickaxes_font.render(f"{settings.pickaxe_type[i]}のツルハシ +{settings.pickaxe_level[i][j]}", True, BLACK))
                self.pickaxes_button_rect.append(self.pickaxes_button_disp[self.sum_pickaxes].get_rect(midleft=(FULL_W // 4 + self.change_pickaxes_size, FULL_H // 4 + (2*self.sum_pickaxes+3)*self.change_pickaxes_size // 2 - self.pickaxe_camera_y)))
                self.sum_pickaxes += 1
        self.update_scrollbar()
    
    # 描画処理
    def draw(self, canvas):
        canvas.fill(WHITE)
        # 見出し描画
        canvas.blit(self.headline_disp, self.headline_rect)
        pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE), (MINE_W, HEADLINE_SIZE), 1)
        # 左右移動ボタンの描画
        if self.what_character_num > 0:
            pygame.draw.rect(canvas, self.arrow_color[0], self.arrow_button[0])
            pygame.draw.rect(canvas, BLACK, self.arrow_button[0], width=1)
            canvas.blit(self.arrow_disp[0], self.arrow_rect[0])
        if len(settings.character_speed) >= 3 and self.what_character_num < len(settings.character_speed) - 2:
            pygame.draw.rect(canvas, self.arrow_color[1], self.arrow_button[1])
            pygame.draw.rect(canvas, BLACK, self.arrow_button[1], width=1)
            canvas.blit(self.arrow_disp[1], self.arrow_rect[1])
        # 鉱夫の描画
        for i in range(min(len(settings.character_speed)+1, 3)): # 3人までしか表示できない
            canvas.blit(self.image_character, (ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE))
            canvas.blit(self.character_name_disp[i], self.character_name_rect[i])
            if i != len(settings.character_speed) - self.what_character_num:
                canvas.blit(self.move_speed_disp[i], self.move_speed_rect[i])
                if settings.use_pickaxe_type[i+1+self.what_character_num] is not None:
                    canvas.blit(self.image_pickaxe[settings.use_pickaxe_type[i+1+self.what_character_num]], (ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 2*TEXT_SIZE))
                else:
                    pygame.draw.line(canvas, BLACK, (ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 2*TEXT_SIZE), (ARROW_W + i*CHARACTER_SIZE + TEXT_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 3*TEXT_SIZE), 1)
                    pygame.draw.line(canvas, BLACK, (ARROW_W + i*CHARACTER_SIZE + TEXT_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 2*TEXT_SIZE), (ARROW_W + i*CHARACTER_SIZE, HEADLINE_SIZE + CHARACTER_SIZE + 3*TEXT_SIZE), 1)
                canvas.blit(self.set_pickaxe_disp1[i], self.set_pickaxe_rect1[i])
                canvas.blit(self.set_pickaxe_disp2[i], self.set_pickaxe_rect2[i])
                pygame.draw.rect(canvas, self.change_pickaxe_button_color[i], self.change_pickaxe_button[i])
                pygame.draw.rect(canvas, BLACK, self.change_pickaxe_button[i], width=1)
                canvas.blit(self.change_pickaxe_disp, self.change_pickaxe_rect[i])
                pygame.draw.rect(canvas, self.character_levelup_button_color[i], self.character_levelup_button[i])
                pygame.draw.rect(canvas, BLACK, self.character_levelup_button[i], width=1)
                canvas.blit(self.character_levelup_disp, self.character_levelup_rect[i])
                canvas.blit(self.levelup_money_disp[i], self.levelup_money_rect[i])
            else:
                canvas.blit(self.employ_money_disp, self.employ_money_rect)
                pygame.draw.rect(canvas, self.new_character_color, self.new_character_button)
                pygame.draw.rect(canvas, BLACK, self.new_character_button, width=1)
                canvas.blit(self.new_character_disp, self.new_character_rect)
            pygame.draw.rect(canvas, BLACK, self.character_all_rect[i], width=1)
    
    # 確認画面（type==employ -> 採用, type==levelup -> 昇給）
    def select_draw(self, canvas, type):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        self.permit_disp = []
        self.permit_rect = []
        if type == "employ":
            self.permit_text = [f"{len(settings.character_speed)+1}人目の鉱夫を", "採用しますか？"]
            for i in range(len(self.permit_text)):
                self.permit_disp.append(self.employ_permit_font.render(f"{self.permit_text[i]}", True, BLACK))
        elif type == "levelup":
            self.permit_text = [f"{self.character_levelup_num+1}人目の鉱夫を昇給して", "移動速度を上げますか？"]
            for i in range(len(self.permit_text)):
                self.permit_disp.append(self.levelup_permit_font.render(f"{self.permit_text[i]}", True, BLACK))
        for i in range(len(self.permit_text)):
            self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])

    # ツルハシ変更画面描画
    def change_pickaxe_select_draw(self, canvas):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        # ボタンの色変更
        if self.pickaxes_which is not None:
            self.pickaxes_button_color[self.pickaxes_which] = DARK_GRAY
        
        pygame.draw.rect(canvas, WHITE, self.change_pickaxe_screen)
        if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is None:
            pygame.draw.line(canvas, BLACK, (FULL_W // 4, FULL_H // 4), (FULL_W // 4 + self.change_pickaxes_size, FULL_H // 4 + self.change_pickaxes_size), 1)
            pygame.draw.line(canvas, BLACK, (FULL_W // 4, FULL_H // 4 + self.change_pickaxes_size), (FULL_W // 4 + self.change_pickaxes_size, FULL_H // 4), 1)
        else:
            canvas.blit(self.image_change_pickaxe[settings.use_pickaxe_type[self.change_pickaxe_character_num+1]], (FULL_W // 4, FULL_H // 4))
        canvas.blit(self.mini_headline_disp, self.mini_headline_rect)
        pygame.draw.rect(canvas, self.back_button_color, self.back_button)
        pygame.draw.rect(canvas, BLACK, self.back_button, width=3)
        canvas.blit(self.back_button_disp, self.back_button_rect)
        # 描画範囲の制限
        old_clip = canvas.get_clip()
        canvas.set_clip(self.scroll_screen)
        for i in range(self.sum_pickaxes):
            pygame.draw.rect(canvas, self.pickaxes_button_color[i], self.pickaxes_button[i])
            if i == 0 and settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is not None:
                pass
            else:
                sum_i = 1 if settings.use_pickaxe_type[self.change_pickaxe_character_num+1] is not None else 0
                for j in range(len(settings.pickaxe_level)):
                    for _ in range(len(settings.pickaxe_level[j])):
                        if i == sum_i:
                            canvas.blit(self.image_change_pickaxe[j], self.pickaxes_button[i].topleft)
                        sum_i += 1
            canvas.blit(self.pickaxes_button_disp[i], self.pickaxes_button_rect[i])
            pygame.draw.rect(canvas, BLACK, self.pickaxes_button[i], width=1)
        pygame.draw.rect(canvas, GRAY, self.scroll_rail_rect)
        pygame.draw.rect(canvas, BLACK, self.scroll_rail_rect, width=1)
        pygame.draw.rect(canvas, self.scroll_bar_color, self.scroll_bar_rect)
        pygame.draw.rect(canvas, BLACK, self.scroll_bar_rect, width=1)
        # 描画制限の解除
        canvas.set_clip(old_clip)
        pygame.draw.line(canvas, BLACK, (FULL_W // 4, FULL_H // 4 + self.change_pickaxes_size), (FULL_W // 4 + FULL_W // 2, FULL_H // 4 + self.change_pickaxes_size), 3)
        pygame.draw.rect(canvas, BLACK, self.change_pickaxe_screen_border, width=5)
        
    # 採用できないときに×を出す
    def cannot_employ_draw(self, canvas):
        if self.cannot_employ_rect is not None:
            canvas.blit(self.cannot_disp, self.cannot_employ_rect)
    
    # 昇給できないときに×を出す
    def cannot_levelup_draw(self, canvas):
        self.cannot_levelup_rect = self.cannot_disp.get_rect(center=self.character_levelup_button[self.cannot_levelup_num].center)
        canvas.blit(self.cannot_disp, self.cannot_levelup_rect)