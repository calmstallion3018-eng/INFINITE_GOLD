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
            
        # ツルハシのダウンロード（石、鉄、銅、銀、金、ダイヤモンド）
        self.image_pickaxe = [None] * len(settings.pickaxe_type)
        self.image_pickaxe_headline = [None] * len(settings.pickaxe_type)
        self.image_pickaxe_sample = [None] * len(settings.pickaxe_type)
        self.image_pickaxe_belong = [None] * len(settings.pickaxe_type)
        for i in range(len(settings.pickaxe_type)):
            self.image_pickaxe[i] = pygame.image.load(settings.PICKAXE_IMAGE[i]).convert_alpha()
            self.image_pickaxe_headline[i] = pygame.transform.scale(self.image_pickaxe[i], (HEADLINE_SIZE - 2*ADJUST, HEADLINE_SIZE - 2*ADJUST))
            self.image_pickaxe_sample[i] = pygame.transform.scale(self.image_pickaxe[i], (2*TEXT_SIZE, 2*TEXT_SIZE))
            self.image_pickaxe_belong[i] = pygame.transform.scale(self.image_pickaxe[i], (TEXT_SIZE, TEXT_SIZE))
        
        # 使用中のツルハシrect
        self.pickaxe_font = pygame.font.SysFont(self.font_path, HEADLINE_SIZE // 2)
        self.pickaxe_disp = self.pickaxe_font.render(f"{settings.pickaxe_type[settings.use_pickaxe_type[0]]}のツルハシ +{settings.pickaxe_level[settings.use_pickaxe_type[0]][settings.use_pickaxe_num[0]]} を使用中", True, BLACK)
        self.pickaxe_rect_real = pygame.Rect(HEADLINE_SIZE, 0, MINE_W - HEADLINE_SIZE, HEADLINE_SIZE)
        self.pickaxe_rect = self.pickaxe_disp.get_rect(center=self.pickaxe_rect_real.center)
        
        # スクロール用カメラ補正
        self.camera_y = 0
        
        # スクロールする画面の範囲
        self.scroll_screen = pygame.Rect(MINE_W // 4, HEADLINE_SIZE, MINE_W // 2, MINE_H - HEADLINE_SIZE)
        self.bar_w = 20
        
        # ツルハシの鋳造・鍛錬・セットrect
        self.forge_text_font = pygame.font.SysFont(self.font_path, TEXT_SIZE * 3//4)
        self.cast_button_color = [GRAY] * len(settings.pickaxe_type)
        self.cast_button = [None] * len(settings.pickaxe_type)
        self.sample_name_disp = [None] * len(settings.pickaxe_type)
        self.sample_name_rect_real = [None] * len(settings.pickaxe_type)
        self.sample_name_rect = [None] * len(settings.pickaxe_type)
        self.material_disp = [None] * len(settings.pickaxe_type)
        self.material_rect_real = [None] * len(settings.pickaxe_type)
        self.material_rect = [None] * len(settings.pickaxe_type)
        
        self.pickaxe_point = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_enclose = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_disp = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_rect_real = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_rect = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_button_color = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_button = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_disp = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_rect = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_button_color = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_button = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_disp = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_rect = [[] for _ in range(len(settings.pickaxe_type))]
        
        MAX_H = HEADLINE_SIZE - self.camera_y # ツルハシの種類ごとの高さ
        for i in range(len(settings.pickaxe_type)):
            self.cast_button[i] = pygame.Rect(MINE_W // 4, MAX_H, MINE_W // 2, 2*TEXT_SIZE)
            self.sample_name_disp[i] = self.forge_text_font.render(f"{settings.pickaxe_type[i]}のツルハシ", True, BLACK)
            self.sample_name_rect_real[i] = pygame.Rect(MINE_W // 4 + 2*TEXT_SIZE, MAX_H, MINE_W // 2 - 2*TEXT_SIZE, TEXT_SIZE)
            self.sample_name_rect[i] = self.sample_name_disp[i].get_rect(midleft=self.sample_name_rect_real[i].midleft)
            material_text = "、".join([f"{settings.ore_name_list[ore_id]} x {quantity}個" for ore_id, quantity in settings.materials_require[i]])
            self.material_disp[i] = self.forge_text_font.render(f"{material_text}", True, BLACK)
            self.material_rect_real[i] = pygame.Rect(MINE_W // 4 + 2*TEXT_SIZE, MAX_H + TEXT_SIZE, MINE_W // 2 - 2*TEXT_SIZE, TEXT_SIZE)
            self.material_rect[i] = self.material_disp[i].get_rect(midleft=self.material_rect_real[i].midleft)
            for j in range(len(settings.pickaxe_level[i])):
                self.pickaxe_point[i].append((MINE_W // 4, MAX_H + (2+j)*TEXT_SIZE))
                self.belongs_disp[i].append(self.forge_text_font.render(f"{settings.pickaxe_type[i]}のツルハシ +{settings.pickaxe_level[i][j]}", True, BLACK))
                self.belongs_enclose[i].append(pygame.Rect(MINE_W // 4, MAX_H + (2+j)*TEXT_SIZE, MINE_W // 2, TEXT_SIZE))
                self.belongs_rect_real[i].append(pygame.Rect(MINE_W // 4 + TEXT_SIZE, MAX_H + (2+j)*TEXT_SIZE, MINE_W // 2 - TEXT_SIZE, TEXT_SIZE))
                self.belongs_rect[i].append(self.belongs_disp[i][j].get_rect(midleft=self.belongs_rect_real[i][j].midleft))
                self.training_button_color[i].append(GRAY)
                self.training_button[i].append(pygame.Rect(MINE_W // 4 + MINE_W // 3, MAX_H + (2+j)*TEXT_SIZE + ADJUST, MINE_W // 12 - ADJUST, TEXT_SIZE - 2*ADJUST))
                self.training_disp[i].append(self.forge_text_font.render("鍛錬", True, BLACK))
                self.training_rect[i].append(self.training_disp[i][j].get_rect(center=self.training_button[i][j].center))
                self.set_button_color[i].append(GRAY)
                self.set_button[i].append(pygame.Rect(MINE_W // 4 + MINE_W // 3 + MINE_W // 12, MAX_H + (2+j)*TEXT_SIZE + ADJUST, MINE_W // 12 - ADJUST, TEXT_SIZE - 2*ADJUST))
                self.set_disp[i].append(self.forge_text_font.render("装備", True, BLACK))
                self.set_rect[i].append(self.set_disp[i][j].get_rect(center=self.set_button[i][j].center))
            # 行の高さを変更
            try:
                MAX_H = self.belongs_rect[i][-1].bottom
            except IndexError:
                MAX_H = self.cast_button[i].bottom
        
        # 装備中のツルハシのみ装備中と表示する
        for i in range(len(settings.use_pickaxe_type)):
            if settings.use_pickaxe_type[i] is None:
                continue
            self.set_button[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]] = None
            if i == 0:
                self.set_disp[settings.use_pickaxe_type[0]][settings.use_pickaxe_num[0]] = self.forge_text_font.render("装備中", True, RED)
            else:
                self.set_disp[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]] = self.forge_text_font.render("装備中", True, BLACK)
            self.set_rect[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]] = self.set_disp[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]].get_rect(midright=self.belongs_rect_real[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]].midright)

        # 装備による採掘力の変更
        settings.mining_power[0] = settings.pickaxe_power[settings.use_pickaxe_type[0]] * (1 + settings.pickaxe_power_ratio * settings.pickaxe_level[settings.use_pickaxe_type[0]][settings.use_pickaxe_num[0]])
        
        # スクロールバーrect
        self.scroll_view_h = self.scroll_screen.height
        try:
            self.scroll_content_h = self.belongs_rect[-1][-1].bottom - self.cast_button[0].top
        except IndexError:
            self.scroll_content_h = self.cast_button[-1].bottom - self.cast_button[0].top
        self.bar_h = max(20, self.scroll_view_h ** 2 // self.scroll_content_h)
        self.scroll_ratio = self.camera_y / (self.scroll_content_h - self.scroll_view_h)
        self.bar_y = self.scroll_screen.y + self.scroll_ratio * (self.scroll_view_h - self.bar_h)
        self.scroll_bar_rect = pygame.Rect(self.scroll_screen.right + 1, self.bar_y, self.bar_w - 2, self.bar_h)
        self.scroll_rail_rect = pygame.Rect(self.scroll_screen.right, self.scroll_screen.y, self.bar_w, self.scroll_view_h)
        self.scroll_bar_color = DARK_GRAY
        
        # スクロールバーを掴んでいるか
        self.scroll_dragging = False
        self.drag_offset_y = 0
        
        # 選択画面の表示
        self.can_cast_select = False
        self.can_training_select = False
        self.can_set_select = False
        
        # 鋳造するツルハシのpickaxe_type番号
        self.cast_type = -1
        
        # 鍛錬するツルハシのpickaxe_type番号と何番目のツルハシか
        self.training_type, self.training_num = -1, -1
        
        # 装備するツルハシのpickaxe_type番号と何番目のツルハシか
        self.set_type, self.set_num = -1, -1
        
        # ×マークrect
        self.cannot_cast_font = pygame.font.SysFont(self.font_path, 2*TEXT_SIZE)
        self.cannot_cast_disp = self.cannot_cast_font.render("X", True, RED)
        self.cannot_cast_rect = None
        
        self.cannot_training_font = pygame.font.SysFont(self.font_path, TEXT_SIZE * 3//2)
        self.cannot_training_disp = self.cannot_training_font.render("X", True, RED)
        self.cannot_training_rect = None
        
        # ×マーク表示位置
        self.is_cannot_cast = False
        self.cannot_cast_type = -1
        self.is_cannot_training = False
        self.cannot_training_type, self.cannot_training_num = -1, -1
        
        # 小窓の設定
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.cast_permit_font = pygame.font.SysFont(self.font_path, FULL_H // 15)
        self.training_permit_font_1 = pygame.font.SysFont(self.font_path, FULL_H // 18)
        self.training_permit_font_2 = pygame.font.SysFont(self.font_path, FULL_H // 36)
        self.training_permit_font = [self.training_permit_font_1] * 3 + [self.training_permit_font_2]
        self.set_permit_font = pygame.font.SysFont(self.font_path, FULL_H // 15)
        
        self.training_permit_color = [BLACK] * 3 + [RED]
        
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
    
    # 鋳造時の処理
    def cast_pickaxe(self):
        settings.pickaxe_level[self.cast_type].append(0)
        for ore_id, quantity in settings.materials_require[self.cast_type]:
            settings.ore_possession_list[ore_id] -= quantity
        settings.record_list[14] += 1
        self.update_page()
    
    # 鍛錬時の処理
    def training_pickaxe(self):
        settings.pickaxe_level[self.training_type][self.training_num] += 1
        settings.pickaxe_level[self.training_type].remove(0)
        settings.record_list[15] = max(settings.pickaxe_level[self.training_type][self.training_num], settings.record_list[15])
        self.update_page()
    
    # 装備時の処理
    def set_pickaxe(self):
        settings.use_pickaxe_type[0], settings.use_pickaxe_num[0] = self.set_type, self.set_num
        self.update_page()

    # ページ内変数のアップデート
    def update_page(self):
        self.pickaxe_disp = self.pickaxe_font.render(f"{settings.pickaxe_type[settings.use_pickaxe_type[0]]}のツルハシ +{settings.pickaxe_level[settings.use_pickaxe_type[0]][settings.use_pickaxe_num[0]]} を使用中", True, BLACK)
        self.pickaxe_rect = self.pickaxe_disp.get_rect(center=self.pickaxe_rect_real.center)
        
        self.update_scrollbar()
        self.update_pickaxe()
        
        settings.mining_power[0] = settings.pickaxe_power[settings.use_pickaxe_type[0]] * (1 + settings.pickaxe_power_ratio * settings.pickaxe_level[settings.use_pickaxe_type[0]][settings.use_pickaxe_num[0]])
    
    # カメラ移動
    def update_camera(self, y):
        CAMERA_SPEED = 20
        self.camera_y -= y * CAMERA_SPEED
        self.camera_y = max(0, min(self.camera_y, self.scroll_content_h - self.scroll_view_h))
        
    # スクロールバー移動
    def update_scrollbar(self):
        try:
            self.scroll_content_h = self.belongs_rect[-1][-1].bottom - self.cast_button[0].top
        except IndexError:
            self.scroll_content_h = self.cast_button[-1].bottom - self.cast_button[0].top
        
        if self.scroll_content_h <= self.scroll_view_h:
            self.scroll_bar_rect.height = self.scroll_view_h
            self.scroll_bar_rect.y = self.scroll_screen.y
            return
            
        self.bar_h = max(20, self.scroll_view_h ** 2 // self.scroll_content_h)
        self.scroll_ratio = self.camera_y / (self.scroll_content_h - self.scroll_view_h)
        self.bar_y = self.scroll_screen.y + self.scroll_ratio * (self.scroll_view_h - self.bar_h)
        self.scroll_bar_rect = pygame.Rect(self.scroll_screen.right + 1, self.bar_y, self.bar_w - 2, self.bar_h)
    
    # ツルハシ画面の移動
    def update_pickaxe(self):
        self.pickaxe_point = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_enclose = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_disp = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_rect_real = [[] for _ in range(len(settings.pickaxe_type))]
        self.belongs_rect = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_button_color = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_button = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_disp = [[] for _ in range(len(settings.pickaxe_type))]
        self.training_rect = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_button_color = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_button = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_disp = [[] for _ in range(len(settings.pickaxe_type))]
        self.set_rect = [[] for _ in range(len(settings.pickaxe_type))]
        
        MAX_H = HEADLINE_SIZE - self.camera_y
        for i in range(len(settings.pickaxe_type)):
            self.cast_button[i] = pygame.Rect(MINE_W // 4, MAX_H, MINE_W // 2, 2*TEXT_SIZE)
            self.sample_name_rect_real[i] = pygame.Rect(MINE_W // 4 + 2*TEXT_SIZE, MAX_H, MINE_W // 2 - 2*TEXT_SIZE, TEXT_SIZE)
            self.sample_name_rect[i] = self.sample_name_disp[i].get_rect(midleft=self.sample_name_rect_real[i].midleft)
            self.material_rect_real[i] = pygame.Rect(MINE_W // 4 + 2*TEXT_SIZE, MAX_H + TEXT_SIZE, MINE_W // 2 - 2*TEXT_SIZE, TEXT_SIZE)
            self.material_rect[i] = self.material_disp[i].get_rect(midleft=self.material_rect_real[i].midleft)
            for j in range(len(settings.pickaxe_level[i])):
                self.pickaxe_point[i].append((MINE_W // 4, MAX_H + (2+j)*TEXT_SIZE))
                self.belongs_disp[i].append(self.forge_text_font.render(f"{settings.pickaxe_type[i]}のツルハシ +{settings.pickaxe_level[i][j]}", True, BLACK))
                self.belongs_enclose[i].append(pygame.Rect(MINE_W // 4, MAX_H + (2+j)*TEXT_SIZE, MINE_W // 2, TEXT_SIZE))
                self.belongs_rect_real[i].append(pygame.Rect(MINE_W // 4 + TEXT_SIZE, MAX_H + (2+j)*TEXT_SIZE, MINE_W // 2 - TEXT_SIZE, TEXT_SIZE))
                self.belongs_rect[i].append(self.belongs_disp[i][j].get_rect(midleft=self.belongs_rect_real[i][j].midleft))
                self.training_button_color[i].append(GRAY)
                self.training_button[i].append(pygame.Rect(MINE_W // 4 + MINE_W // 3, MAX_H + (2+j)*TEXT_SIZE + ADJUST, MINE_W // 12 - ADJUST, TEXT_SIZE - 2*ADJUST))
                self.training_disp[i].append(self.forge_text_font.render("鍛錬", True, BLACK))
                self.training_rect[i].append(self.training_disp[i][j].get_rect(center=self.training_button[i][j].center))
                self.set_button_color[i].append(GRAY)
                self.set_button[i].append(pygame.Rect(MINE_W // 4 + MINE_W // 3 + MINE_W // 12, MAX_H + (2+j)*TEXT_SIZE + ADJUST, MINE_W // 12 - ADJUST, TEXT_SIZE - 2*ADJUST))
                self.set_disp[i].append(self.forge_text_font.render("装備", True, BLACK))
                self.set_rect[i].append(self.set_disp[i][j].get_rect(center=self.set_button[i][j].center))
            # 行の高さを変更
            try:
                MAX_H = self.belongs_rect[i][-1].bottom
            except IndexError:
                MAX_H = self.cast_button[i].bottom
        
        for i in range(len(settings.use_pickaxe_type)):
            if settings.use_pickaxe_type[i] is None:
                continue
            self.set_button[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]] = None
            if i == 0:
                self.set_disp[settings.use_pickaxe_type[0]][settings.use_pickaxe_num[0]] = self.forge_text_font.render("装備中", True, RED)
            else:
                self.set_disp[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]] = self.forge_text_font.render("装備中", True, BLACK)
            self.set_rect[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]] = self.set_disp[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]].get_rect(midright=self.belongs_rect_real[settings.use_pickaxe_type[i]][settings.use_pickaxe_num[i]].midright)
        
    # 描画処理
    def draw(self, canvas):
        canvas.fill(WHITE)
        # 使用中のツルハシの描画
        canvas.blit(self.image_pickaxe_headline[settings.use_pickaxe_type[0]], (ADJUST, ADJUST))
        canvas.blit(self.pickaxe_disp, self.pickaxe_rect)
        pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE), (MINE_W, HEADLINE_SIZE), 2)
        # 描画範囲の制限
        old_clip = canvas.get_clip()
        canvas.set_clip(self.scroll_screen)
        # ツルハシの鋳造・鍛錬・セット画面の描画
        for i in range(min(settings.ore_limit(settings.ore_prop_list)-1, len(settings.pickaxe_type))):
            pygame.draw.rect(canvas, self.cast_button_color[i], self.cast_button[i])
            canvas.blit(self.image_pickaxe_sample[i], self.cast_button[i].topleft)
            canvas.blit(self.sample_name_disp[i], self.sample_name_rect[i])
            canvas.blit(self.material_disp[i], self.material_rect[i])
            pygame.draw.rect(canvas, BLACK, self.cast_button[i], width=2)
            for j in range(len(settings.pickaxe_level[i])):
                canvas.blit(self.image_pickaxe_belong[i], self.pickaxe_point[i][j])
                canvas.blit(self.belongs_disp[i][j], self.belongs_rect[i][j])
                pygame.draw.rect(canvas, self.training_button_color[i][j], self.training_button[i][j])
                pygame.draw.rect(canvas, BLACK, self.training_button[i][j], width=1)
                canvas.blit(self.training_disp[i][j], self.training_rect[i][j])
                if self.set_button[i][j] is not None:
                    pygame.draw.rect(canvas, self.set_button_color[i][j], self.set_button[i][j])
                    pygame.draw.rect(canvas, BLACK, self.set_button[i][j], width=1)
                canvas.blit(self.set_disp[i][j], self.set_rect[i][j])
                pygame.draw.rect(canvas, BLACK, self.belongs_enclose[i][j], width=1)
        # 描画制限の解除
        canvas.set_clip(old_clip)
        pygame.draw.rect(canvas, GRAY, self.scroll_rail_rect)
        pygame.draw.rect(canvas, BLACK, self.scroll_rail_rect, width=1)
        pygame.draw.rect(canvas, self.scroll_bar_color, self.scroll_bar_rect)
        pygame.draw.rect(canvas, BLACK, self.scroll_bar_rect, width=1)
        
    # 確認画面（type==cast -> 鋳造, type==training -> 鍛錬, type==set -> 装備）
    def select_draw(self, canvas, type):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        self.permit_disp = []
        self.permit_rect = []
        if type == "cast":
            self.permit_text = [f"{settings.pickaxe_type[self.cast_type]}のツルハシを", "鋳造しますか？"]
            for i in range(len(self.permit_text)):
                self.permit_disp.append(self.cast_permit_font.render(f"{self.permit_text[i]}", True, BLACK))
                self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        elif type == "training":
            self.permit_text = [f"{settings.pickaxe_type[self.training_type]}のツルハシ +{settings.pickaxe_level[self.training_type][self.training_num]} に", f"+0 の{settings.pickaxe_type[self.training_type]}のツルハシを", "合成しますか？", "※合成に使用したツルハシは失われます"]
            for i in range(len(self.permit_text)):
                self.permit_disp.append(self.training_permit_font[i].render(f"{self.permit_text[i]}", True, self.training_permit_color[i]))
                if i < 3:
                    self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+4)*FULL_H // 12)))
                else:
                    self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+11)*FULL_H // 24)))
        elif type == "set":
            self.permit_text = [f"{settings.pickaxe_type[self.set_type]}のツルハシ +{settings.pickaxe_level[self.set_type][self.set_num]}を", "装備しますか？"]
            for i in range(len(self.permit_text)):
                self.permit_disp.append(self.set_permit_font.render(f"{self.permit_text[i]}", True, BLACK))
                self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])

    # 鋳造できないときに×を出す
    def cannot_cast_draw(self, canvas):
        old_clip = canvas.get_clip()
        canvas.set_clip(self.scroll_screen)
        self.cannot_cast_rect = self.cannot_cast_disp.get_rect(center=self.cast_button[self.cannot_cast_type].center)
        canvas.blit(self.cannot_cast_disp, self.cannot_cast_rect)
        canvas.set_clip(old_clip)
    
    # 鍛錬できないときに×を出す
    def cannot_training_draw(self, canvas):
        old_clip = canvas.get_clip()
        canvas.set_clip(self.scroll_screen)
        self.cannot_training_rect = self.cannot_training_disp.get_rect(center=self.training_button[self.cannot_training_type][self.cannot_training_num].center)
        canvas.blit(self.cannot_training_disp, self.cannot_training_rect)
        canvas.set_clip(old_clip)