import pygame
import sys
import settings

FULL_W = settings.Display.WIDTH
FULL_H = settings.Display.HEIGHT

MINE_W = settings.Display.MINE_W
MINE_H = settings.Display.MINE_H
RIGHT_H = settings.Display.RIGHT_H

HEADLINE_SIZE = MINE_H // 8
TAB_H = MINE_H // 8
TERMS_TEXT_SIZE = MINE_H // 36
PRICE_H = MINE_H // 18
PRICE_SIZE = PRICE_H - 1

button_quantity = settings.bottom_button_quantity

ADJUST = 5

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
LIGHTGREEN = settings.Color.LIGHTGREEN
YELLOW = settings.Color.YELLOW
GRAY = settings.Color.GRAY
DARK_GRAY = settings.Color.DARK_GRAY
RED = settings.Color.RED
PURPLE = settings.Color.PURPLE

class Main():
    def __init__(self) -> None:
        # 文字フォント
        self.font_path = "msgothic"
        
        # 画像ダウンロード
        self.ore_image_default = []
        self.ore_image = []
        for i, IMAGE in enumerate(settings.ORE_IMAGE):
            self.ore_image_default.append(pygame.image.load(IMAGE).convert_alpha())
            self.ore_image.append(pygame.transform.scale(self.ore_image_default[i], (PRICE_H, PRICE_H)))
        
        # 実績解除で鉱石の値段が上昇！rect
        self.headline_font = pygame.font.SysFont(self.font_path, HEADLINE_SIZE // 2)
        self.headline_disp = self.headline_font.render("実績解除で鉱石の値段が上昇！", True, BLACK)
        self.headline_rect_real = pygame.Rect(0,0,MINE_W, HEADLINE_SIZE)
        self.headline_rect = self.headline_disp.get_rect(center=self.headline_rect_real.center)
        
        # スクロール用カメラ補正
        self.camera_y = 0
        
        # スクロールする画面の範囲
        self.scroll_screen = pygame.Rect(MINE_W // 20, HEADLINE_SIZE, MINE_W // 2, MINE_H - HEADLINE_SIZE)
        self.bar_w = 20
        
        # 実績rect
        self.record_terms_text = []
        for i, name in enumerate(settings.ore_name_list):
            if i < settings.ore_limit(settings.ore_prop_list):
                self.record_terms_text.append(f"{name}を累計{settings.record_terms_num[i][settings.record_completes[i]]}個採掘する")
            else:
                self.record_terms_text.append("????????????????????")
        self.record_terms_text.append(f"幸運の花LEVELが{settings.record_terms_num[13][settings.record_completes[13]]}に到達する")
        self.record_terms_text.append(f"ツルハシを累計{settings.record_terms_num[14][settings.record_completes[14]]}回鋳造する")
        self.record_terms_text.append(f"鍛錬して +{settings.record_terms_num[15][settings.record_completes[15]]}のツルハシを作る")
        self.record_terms_text.append(f"{settings.record_terms_num[16][settings.record_completes[16]]}人目の鉱夫を雇う")
        self.record_terms_text.append(f"鉱夫の移動速度が{settings.record_terms_num[17][settings.record_completes[17]]}に到達する")
        self.record_terms_text.append(f"{settings.record_terms_num[18][settings.record_completes[18]]}回転生する")
        self.record_terms_text.append(f"1層に鉱石が{settings.record_terms_num[19][settings.record_completes[19]]}個出現するようになる")
        self.record_terms_text.append(f"実績を{settings.record_terms_num[20][settings.record_completes[20]]}個達成する(この実績は除く)")
        self.record_bar_w = MINE_W // 4
        self.record_bar_h = 10
        self.reward_text = []
        for i, name in enumerate(settings.ore_name_list):
            if i < settings.ore_limit(settings.ore_prop_list):
                self.reward_text.append(f"{name}の価格 +{int(settings.reward_ratio[i][settings.record_completes[i]] * 100)}%")
            else:
                self.reward_text.append("????????????????????")
        for i in range(len(settings.ore_name_list), len(settings.record_list)):
            self.reward_text.append(f"全ての鉱石の価格 +{int(settings.reward_ratio[i][settings.record_completes[i]] * 100)}%")
        
        self.record_font = pygame.font.SysFont(self.font_path, TERMS_TEXT_SIZE)
        self.record_color = []
        self.record_rect = []
        self.record_terms_disp = []
        self.record_terms_rect = []
        self.record_full_bar = []
        self.record_progress_bar = []
        self.record_progress_disp = []
        self.record_progress_rect = []
        self.reward_disp = []
        self.reward_rect = []
        for i, num in enumerate(settings.record_list):
            self.record_color.append(PURPLE)
            self.record_rect.append(pygame.Rect(self.scroll_screen.left, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y, MINE_W // 2, TAB_H))
            self.record_terms_disp.append(self.record_font.render(self.record_terms_text[i], True, BLACK))
            self.record_terms_rect.append(self.record_terms_disp[i].get_rect(midleft=(self.scroll_screen.left + ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 6)))
            self.record_full_bar.append(pygame.Rect(self.scroll_screen.left + ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 2 - self.record_bar_h // 2, self.record_bar_w, self.record_bar_h))
            self.record_progress_bar.append(pygame.Rect(self.scroll_screen.left + ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 2 - self.record_bar_h // 2, min(1, num / settings.record_terms_num[i][settings.record_completes[i]])*self.record_bar_w, self.record_bar_h))
            self.record_progress_disp.append(self.record_font.render(f"{num} / {settings.record_terms_num[i][settings.record_completes[i]]}", True, BLACK))
            self.record_progress_rect.append(self.record_progress_disp[i].get_rect(midright=(self.scroll_screen.right - ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 2)))
            self.reward_disp.append(self.record_font.render(f"報酬: {self.reward_text[i]}", True, BLACK))
            self.reward_rect.append(self.reward_disp[i].get_rect(midright=(self.scroll_screen.right - ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H * 5//6)))
        
        # スクロールバーrect
        self.scroll_view_h = self.scroll_screen.height
        self.scroll_content_h = self.record_rect[-1].bottom - HEADLINE_SIZE
        self.bar_h = max(20, self.scroll_view_h ** 2 // self.scroll_content_h)
        self.scroll_ratio = self.camera_y / (self.scroll_content_h - self.scroll_view_h)
        self.bar_y = self.scroll_screen.y + self.scroll_ratio * (self.scroll_view_h - self.bar_h)
        self.scroll_bar_rect = pygame.Rect(self.scroll_screen.right + 1, self.bar_y, self.bar_w - 2, self.bar_h)
        self.scroll_rail_rect = pygame.Rect(self.scroll_screen.right, self.scroll_screen.y, self.bar_w, self.scroll_view_h)
        self.scroll_bar_color = DARK_GRAY
        
        # スクロールバーを掴んでいるか
        self.scroll_dragging = False
        self.drag_offset_y = 0
        
        # 鉱石価格倍率rect
        self.price_ratio_whole_rect = pygame.Rect(MINE_W * 3//5, HEADLINE_SIZE, MINE_W - MINE_W * 3//5, PRICE_H * (len(settings.ore_list)+1))
        
        self.price_font = pygame.font.SysFont(self.font_path, PRICE_SIZE)
        self.price_small_font = pygame.font.SysFont(self.font_path, PRICE_SIZE // 2 - 1)
        self.price_name_disp = [None] * len(settings.ore_list)
        self.price_name_rect = [None] * len(settings.ore_list)
        self.price_ratio_disp = []
        self.price_ratio_rect = []
        for i, name in enumerate(settings.ore_name_list):
            if len(name) <= 2:
                self.price_name_disp[i] = self.price_font.render(name, True, BLACK)
                self.price_name_rect[i] = self.price_name_disp[i].get_rect(midleft=(self.price_ratio_whole_rect.left + PRICE_H, HEADLINE_SIZE + i*PRICE_H + PRICE_H // 2))
            elif len(name) <= 6:
                self.price_name_disp[i] = self.price_small_font.render(name, True, BLACK)
                self.price_name_rect[i] = self.price_name_disp[i].get_rect(midleft=(self.price_ratio_whole_rect.left + PRICE_H, HEADLINE_SIZE + i*PRICE_H + PRICE_H // 2))
            else:
                self.price_name_disp[i] = [None] * 2
                self.price_name_rect[i] = [None] * 2
                if name == "アレキサンドライト":
                    self.price_name_disp[i][0] = self.price_small_font.render(name[:6], True, BLACK)
                    self.price_name_disp[i][1] = self.price_small_font.render(" "+name[6:], True, BLACK)
                elif name == "パライバトルマリン":
                    self.price_name_disp[i][0] = self.price_small_font.render(name[:4], True, BLACK)
                    self.price_name_disp[i][1] = self.price_small_font.render(" "+name[4:], True, BLACK)
                elif name == "パパラチアサファイア":
                    self.price_name_disp[i][0] = self.price_small_font.render(name[:5], True, BLACK)
                    self.price_name_disp[i][1] = self.price_small_font.render(" "+name[5:], True, BLACK)
                self.price_name_rect[i][0] = self.price_name_disp[i][0].get_rect(bottomleft=(self.price_ratio_whole_rect.left + PRICE_H, HEADLINE_SIZE + i*PRICE_H + PRICE_H // 2))
                self.price_name_rect[i][1] = self.price_name_disp[i][1].get_rect(topleft=(self.price_ratio_whole_rect.left + PRICE_H, HEADLINE_SIZE + i*PRICE_H + PRICE_H // 2))
            self.price_ratio_disp.append(self.price_font.render(f"×{settings.ore_price_ratio[i]}", True, BLACK))
            self.price_ratio_rect.append(self.price_ratio_disp[i].get_rect(midright=(MINE_W - ADJUST, HEADLINE_SIZE + i*PRICE_H + PRICE_H // 2)))
        
        self.price_caution_disp = [self.price_small_font.render("※鉱石価格の端数は", True, BLACK),
                                   self.price_small_font.render("　　切り捨てされます", True, BLACK)]
        self.price_caution_rect = [self.price_caution_disp[0].get_rect(bottomleft=(self.price_ratio_whole_rect.left + ADJUST, HEADLINE_SIZE + (len(settings.ore_name_list))*PRICE_H + PRICE_H // 2)),
                                   self.price_caution_disp[1].get_rect(topleft=(self.price_ratio_whole_rect.left + ADJUST, HEADLINE_SIZE + (len(settings.ore_name_list))*PRICE_H + PRICE_H // 2))]
        
        # ×マークrect
        self.cannot_font = pygame.font.SysFont(self.font_path, TAB_H * 6//5)
        self.cannot_reward_disp = self.cannot_font.render("X", True, RED)
        self.cannot_reward_rect = None
        
        # ×マーク表示
        self.is_cannot = False
        self.cannot_num = -1
        
    # 実績達成時の処理
    def get_reward(self, i):
        if i <= 12:
            settings.ore_price_ratio[i] += settings.reward_ratio[i][settings.record_completes[i]]
        else:
            for j in range(len(settings.ore_price_ratio)):
                settings.ore_price_ratio[j] += settings.reward_ratio[i][settings.record_completes[i]]
        settings.record_completes[i] += 1
        settings.record_list[20] = sum(settings.record_completes[:-1])
        self.update_page()
    
    # ページ内変数のアップデート
    def update_page(self):
        self.record_terms_text = []
        for i, name in enumerate(settings.ore_name_list):
            if i < settings.ore_limit(settings.ore_prop_list):
                self.record_terms_text.append(f"{name}を累計{settings.record_terms_num[i][settings.record_completes[i]]}個採掘する")
            else:
                self.record_terms_text.append("????????????????????")
        self.record_terms_text.append(f"幸運の花LEVELが{settings.record_terms_num[13][settings.record_completes[13]]}に到達する")
        self.record_terms_text.append(f"ツルハシを累計{settings.record_terms_num[14][settings.record_completes[14]]}回鋳造する")
        self.record_terms_text.append(f"鍛錬して +{settings.record_terms_num[15][settings.record_completes[15]]}のツルハシを作る")
        self.record_terms_text.append(f"{settings.record_terms_num[16][settings.record_completes[16]]}人目の鉱夫を雇う")
        self.record_terms_text.append(f"鉱夫の移動速度が{settings.record_terms_num[17][settings.record_completes[17]]}に到達する")
        self.record_terms_text.append(f"{settings.record_terms_num[18][settings.record_completes[18]]}回転生する")
        self.record_terms_text.append(f"1層に鉱石が{settings.record_terms_num[19][settings.record_completes[19]]}個出現するようになる")
        self.record_terms_text.append(f"実績を{settings.record_terms_num[20][settings.record_completes[20]]}個達成する(この実績は除く)")
        self.reward_text = []
        for i, name in enumerate(settings.ore_name_list):
            if i < settings.ore_limit(settings.ore_prop_list):
                self.reward_text.append(f"{name}の価格 +{int(settings.reward_ratio[i][settings.record_completes[i]] * 100)}%")
            else:
                self.reward_text.append("????????????????????")
        for i in range(len(settings.ore_name_list), len(settings.record_list)):
            self.reward_text.append(f"全ての鉱石の価格 +{int(settings.reward_ratio[i][settings.record_completes[i]] * 100)}%")
        
        self.update_record()
        
        self.price_ratio_disp = []
        self.price_ratio_rect = []
        for i, name in enumerate(settings.ore_name_list):
            self.price_ratio_disp.append(self.price_font.render(f"×{settings.ore_price_ratio[i]}", True, BLACK))
            self.price_ratio_rect.append(self.price_ratio_disp[i].get_rect(midright=(MINE_W - ADJUST, HEADLINE_SIZE + i*PRICE_H + PRICE_H // 2)))
    
    # カメラ移動
    def update_camera(self, y):
        CAMERA_SPEED = 20
        self.camera_y -= y * CAMERA_SPEED
        self.camera_y = max(0, min(self.camera_y, self.scroll_content_h - self.scroll_view_h))
        
    # スクロールバー移動
    def update_scrollbar(self):
        self.scroll_ratio = self.camera_y / (self.scroll_content_h - self.scroll_view_h)
        self.bar_y = self.scroll_screen.y + self.scroll_ratio * (self.scroll_view_h - self.bar_h)
        self.scroll_bar_rect = pygame.Rect(self.scroll_screen.right + 1, self.bar_y, self.bar_w - 2, self.bar_h)
    
    # 実績rectを動かす
    def update_record(self):
        self.record_rect = []
        self.record_terms_disp = []
        self.record_terms_rect = []
        self.record_full_bar = []
        self.record_progress_bar = []
        self.record_progress_disp = []
        self.record_progress_rect = []
        self.reward_disp = []
        self.reward_rect = []
        for i, num in enumerate(settings.record_list):
            self.record_rect.append(pygame.Rect(self.scroll_screen.left, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y, MINE_W // 2, TAB_H))
            self.record_terms_disp.append(self.record_font.render(self.record_terms_text[i], True, BLACK))
            self.record_terms_rect.append(self.record_terms_disp[i].get_rect(midleft=(self.scroll_screen.left + ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 6)))
            self.record_full_bar.append(pygame.Rect(self.scroll_screen.left + ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 2 - self.record_bar_h // 2, self.record_bar_w, self.record_bar_h))
            self.record_progress_bar.append(pygame.Rect(self.scroll_screen.left + ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 2 - self.record_bar_h // 2, min(1, num / settings.record_terms_num[i][settings.record_completes[i]])*self.record_bar_w, self.record_bar_h))
            self.record_progress_disp.append(self.record_font.render(f"{num} / {settings.record_terms_num[i][settings.record_completes[i]]}", True, BLACK))
            self.record_progress_rect.append(self.record_progress_disp[i].get_rect(midright=(self.scroll_screen.right - ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H // 2)))
            self.reward_disp.append(self.record_font.render(f"報酬: {self.reward_text[i]}", True, BLACK))
            self.reward_rect.append(self.reward_disp[i].get_rect(midright=(self.scroll_screen.right - ADJUST, HEADLINE_SIZE + i*(TAB_H + ADJUST) - self.camera_y + TAB_H * 5//6)))
    
    # 描画処理
    def draw(self, canvas):
        canvas.fill(WHITE)
        # 見出しの描画
        canvas.blit(self.headline_disp, self.headline_rect)
        pygame.draw.line(canvas, BLACK, (0, HEADLINE_SIZE), (MINE_W, HEADLINE_SIZE), 1)
        # 描画範囲の制限
        old_clip = canvas.get_clip()
        canvas.set_clip(self.scroll_screen)
        # 実績の描画
        for i in range(len(settings.record_list)):
            pygame.draw.rect(canvas, self.record_color[i], self.record_rect[i])
            pygame.draw.rect(canvas, BLACK, self.record_rect[i], width=2)
            canvas.blit(self.record_terms_disp[i], self.record_terms_rect[i])
            pygame.draw.rect(canvas, WHITE, self.record_full_bar[i])
            pygame.draw.rect(canvas, BLACK, self.record_full_bar[i], width=1)
            pygame.draw.rect(canvas, YELLOW, self.record_progress_bar[i])
            pygame.draw.rect(canvas, BLACK, self.record_progress_bar[i], width=1)
            canvas.blit(self.record_progress_disp[i], self.record_progress_rect[i])
            canvas.blit(self.reward_disp[i], self.reward_rect[i])
        # 描画制限の解除
        canvas.set_clip(old_clip)
        pygame.draw.rect(canvas, GRAY, self.scroll_rail_rect)
        pygame.draw.rect(canvas, BLACK, self.scroll_rail_rect, width=1)
        pygame.draw.rect(canvas, self.scroll_bar_color, self.scroll_bar_rect)
        pygame.draw.rect(canvas, BLACK, self.scroll_bar_rect, width=1)
        # 鉱石価格倍率の表示
        for i in range(len(settings.ore_name_list)):
            canvas.blit(self.ore_image[i], (self.price_ratio_whole_rect.left, HEADLINE_SIZE + i*PRICE_H))
            if len(settings.ore_name_list[i]) <= 6:
                canvas.blit(self.price_name_disp[i], self.price_name_rect[i])
            else:
                canvas.blit(self.price_name_disp[i][0], self.price_name_rect[i][0])
                canvas.blit(self.price_name_disp[i][1], self.price_name_rect[i][1])
            canvas.blit(self.price_ratio_disp[i], self.price_ratio_rect[i])
            pygame.draw.line(canvas, BLACK, (self.price_ratio_whole_rect.left, HEADLINE_SIZE + (i+1)*PRICE_H), (self.price_ratio_whole_rect.right, HEADLINE_SIZE + (i+1)*PRICE_H), 1)
        canvas.blit(self.price_caution_disp[0], self.price_caution_rect[0])
        canvas.blit(self.price_caution_disp[1], self.price_caution_rect[1])
        pygame.draw.rect(canvas, BLACK, self.price_ratio_whole_rect, width=2)
    
    # 転生できないときに×を出す
    def cannot_reward_draw(self, canvas):
        old_clip = canvas.get_clip()
        canvas.set_clip(self.scroll_screen)
        self.cannot_reward_rect = self.cannot_reward_disp.get_rect(center=self.record_rect[self.cannot_num].center)
        canvas.blit(self.cannot_reward_disp, self.cannot_reward_rect)
        canvas.set_clip(old_clip)