import pygame
import sys
import settings
import os, pickle

FULL_W = settings.Display.WIDTH
FULL_H = settings.Display.HEIGHT

ADJUST = 40
BACK_ADJUST = 10

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
GRAY = settings.Color.GRAY
ASH = settings.Color.ASH

class Main():
    def __init__(self) -> None:
        # 文字フォント
        self.font_path = "msgothic"
        
        # セーブデータのディレクトリを作成
        self.SAVE_DIR = "save_data"
        os.makedirs(self.SAVE_DIR, exist_ok=True)
        
        # セーブデータボタン
        self.save_button_color = [ASH] * 4
        self.save_button = [None] * 4
        self.save_headline_font = pygame.font.SysFont(self.font_path, FULL_H // 16)
        self.save_headline_disp = [None] * 4
        self.save_headline_rect_real = [None] * 4
        self.save_headline_rect = [None] * 4
        
        self.save_text_font = pygame.font.SysFont(self.font_path, FULL_H // 24)
        self.save_text_rect_real = [[] for _ in range(4)]
        self.save_text_disp = [[] for _ in range(4)]
        self.save_text_rect = [[] for _ in range(4)]
        
        self.save_text_time_disp = [None] * 4
        self.save_text_time_rect_real = [None] * 4
        self.save_text_time_rect = [None] * 4
        
        for i in range(4):
            self.save_button[i] = pygame.Rect(ADJUST + (i%2)*FULL_W//2, (2-i//2)*ADJUST + (i//2)*FULL_H//2, FULL_W // 2 - 2*ADJUST, FULL_H // 2 - 2*ADJUST)
            self.save_headline_disp[i] = self.save_headline_font.render(f"セーブデータ {i+1}", True, WHITE)
            self.save_headline_rect_real[i] = pygame.Rect((i%2)*FULL_W//2 + ADJUST + 5,(i//2)*FULL_H//2 + (2-i//2)*ADJUST, FULL_W // 2 - 2*ADJUST - 10, FULL_H // 12)
            self.save_headline_rect[i] = self.save_headline_disp[i].get_rect(midleft=self.save_headline_rect_real[i].midleft)
            
            for j in range(4):
                self.save_text_rect_real[i].append(pygame.Rect((i%2)*FULL_W//2 + ADJUST + 5, (i//2)*FULL_H//2 + (2-i//2)*ADJUST + FULL_H // 12 + j*FULL_H // 18, FULL_W // 2 - 2*ADJUST - 10, FULL_H // 18))
            
            self.save_text_time_rect_real[i] = pygame.Rect((i%2)*FULL_W//2 + ADJUST + 5, (i//2+1)*FULL_H//2 - (i//2)*ADJUST - FULL_H // 18, FULL_W // 2 - 2*ADJUST - 10, FULL_H // 18)
            
            path = f"{self.SAVE_DIR}/slot{i+1}.dat"
            if not os.path.exists(path):
                self.save_text_disp[i].append(self.save_text_font.render("なし", True, WHITE))
                self.save_text_rect[i].append(self.save_text_disp[i][0].get_rect(midleft=self.save_text_rect_real[i][0].midleft))
            else:
                with open(path, "rb") as f:
                    data = pickle.load(f)
                self.save_text_disp[i].append(self.save_text_font.render(f"第{data["stage_num"]}層", True, WHITE))
                self.save_text_disp[i].append(self.save_text_font.render(f"幸運の花 LEVEL {data["lucky_flower_level"]}", True, WHITE))
                self.save_text_disp[i].append(self.save_text_font.render(f"雇用人数 {len(data["character_speed"])}人", True, WHITE))
                self.save_text_disp[i].append(self.save_text_font.render(f"転生回数 {data["record_list"][18]}回", True, WHITE))
                for j in range(4):
                    self.save_text_rect[i].append(self.save_text_disp[i][j].get_rect(midleft=self.save_text_rect_real[i][j].midleft))
                
                sec = data["playing_time"]
                min, sec = sec // 60, sec % 60
                hour, min = min // 60, min % 60
                day, hour = hour // 24, hour % 24
                self.save_text_time_disp[i] = self.save_text_font.render(f"{day}:{hour:02d}:{min:02d}:{sec:02d}", True, WHITE)
                self.save_text_time_rect[i] = self.save_text_time_disp[i].get_rect(midright=self.save_text_time_rect_real[i].midright)
        
        # 戻るボタン
        self.back_color = ASH
        self.back_font = pygame.font.SysFont(self.font_path, FULL_H // 24)
        self.back_button = pygame.Rect(BACK_ADJUST, BACK_ADJUST, FULL_W // 10, FULL_H // 18)
        self.back_button_disp = self.back_font.render("戻る", True, WHITE)
        self.back_button_rect = self.back_button_disp.get_rect(center=self.back_button.center)
        
        # プレイ開始時間の計測
        self.play_start_time = 0
        
        # セーブorロード選択画面の表示状態
        self.can_select = False
        self.savedata_slot = -1
        
        # この画面にする前の画面タイプ、title -> savedata -> load -> stage, stage -> savedata -> save -> stage
        self.gamen_type = None
        
        # キーボード操作時にどのデータを選択しているか（0,1,2,3）
        self.savedata_which = None
        
        # セーブorロード画面
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.permit_font_1 = pygame.font.SysFont(self.font_path, FULL_H // 12)
        self.permit_font_2 = pygame.font.SysFont(self.font_path, FULL_H // 15)
        self.permit_font = [self.permit_font_1, self.permit_font_2]
        
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
        
        # キーボード操作時にはいいいえのどちらを選択しているか（0or1）
        self.y_n_which = None
        
    # 総プレイ時間の変更
    def save_time(self, now_time):
        settings.playing_time += (now_time - self.play_start_time) // 1000
    
    # セーブ・ロード関数本体
    def save_or_load(self):
        path = f"{self.SAVE_DIR}/slot{self.savedata_slot+1}.dat"
        if self.gamen_type == "stage":
            self.game_data = {
                "stage_num": settings.stage_num,
                "player_x": settings.player_x,
                "player_y": settings.player_y,
                "character_x": settings.character_x,
                "character_y": settings.character_y,
                "character_move_time": settings.character_move_time,
                "mining_size_x": settings.mining_size_x,
                "mining_size_y": settings.mining_size_y,
                "ore_exist": settings.ore_exist,
                "money": settings.money,
                "ore_possession_list": settings.ore_possession_list,
                "mining_durability": settings.mining_durability,
                "mining_degree": settings.mining_degree,
                "mining_power": settings.mining_power,
                "ore_prop_list": settings.ore_prop_list,
                "lucky_flower_level": settings.lucky_flower_level,
                "pickaxe_level": settings.pickaxe_level,
                "use_pickaxe_type": settings.use_pickaxe_type,
                "use_pickaxe_num": settings.use_pickaxe_num,
                "character_speed": settings.character_speed,
                "experience": settings.experience,
                "reinc_ore_get_ratio": settings.reinc_ore_get_ratio,
                "have_exp": settings.have_exp,
                "reinc_exp_ratio": settings.reinc_exp_ratio,
                "record_list": settings.record_list,
                "ore_price_ratio": settings.ore_price_ratio,
                "record_completes": settings.record_completes,
                "playing_time": settings.playing_time
            }
            with open(path, "wb") as f:
                pickle.dump(self.game_data, f)
            
            sec = settings.playing_time
            min, sec = sec // 60, sec % 60
            hour, min = min // 60, min % 60
            day, hour = hour // 24, hour % 24
            
            self.save_text_disp[self.savedata_slot] = []
            self.save_text_disp[self.savedata_slot].append(self.save_text_font.render(f"第{settings.stage_num}層", True, WHITE))
            self.save_text_disp[self.savedata_slot].append(self.save_text_font.render(f"幸運の花 LEVEL {settings.lucky_flower_level}", True, WHITE))
            self.save_text_disp[self.savedata_slot].append(self.save_text_font.render(f"雇用人数 {len(settings.character_speed)}人", True, WHITE))
            self.save_text_disp[self.savedata_slot].append(self.save_text_font.render(f"転生回数 {settings.record_list[18]}回", True, WHITE))
            for j in range(4):
                self.save_text_rect[self.savedata_slot][j] = self.save_text_disp[self.savedata_slot][j].get_rect(midleft=self.save_text_rect_real[self.savedata_slot][j].midleft)
            
            self.save_text_time_disp[self.savedata_slot] = self.save_text_font.render(f"{day}:{hour:02d}:{min:02d}:{sec:02d}", True, WHITE)
            self.save_text_time_rect[self.savedata_slot] = self.save_text_time_disp[self.savedata_slot].get_rect(midright=self.save_text_time_rect_real[self.savedata_slot].midright)
            
        elif self.gamen_type == "title":
            if not os.path.exists(path):
                return None
            with open(path, "rb") as f:
                return pickle.load(f)
    
    # セーブデータのロード
    def load_savedata(self, data):
        if data is not None:
            settings.stage_num = data["stage_num"]
            settings.player_x = data["player_x"]
            settings.player_y = data["player_y"]
            settings.character_x = data["character_x"]
            settings.character_y = data["character_y"]
            settings.character_move_time = data["character_move_time"]
            settings.mining_size_x = data["mining_size_x"]
            settings.mining_size_y = data["mining_size_y"]
            settings.ore_exist = data["ore_exist"]
            settings.money = data["money"]
            settings.ore_possession_list = data["ore_possession_list"]
            settings.mining_durability = data["mining_durability"]
            settings.mining_degree = data["mining_degree"]
            settings.mining_power = data["mining_power"]
            settings.ore_prop_list = data["ore_prop_list"]
            settings.lucky_flower_level = data["lucky_flower_level"]
            settings.pickaxe_level = data["pickaxe_level"]
            settings.use_pickaxe_type = data["use_pickaxe_type"]
            settings.use_pickaxe_num = data["use_pickaxe_num"]
            settings.character_speed = data["character_speed"]
            settings.experience = data["experience"]
            settings.reinc_ore_get_ratio = data["reinc_ore_get_ratio"]
            settings.have_exp = data["have_exp"]
            settings.reinc_exp_ratio = data["reinc_exp_ratio"]
            settings.record_list = data["record_list"]
            settings.ore_price_ratio = data["ore_price_ratio"]
            settings.record_completes = data["record_completes"]
            settings.playing_time = data["playing_time"]
    
    def draw(self, canvas):
        canvas.fill(BLACK)
        # セーブデータの描画
        for i in range(4):
            pygame.draw.rect(canvas, self.save_button_color[i], self.save_button[i])
            pygame.draw.rect(canvas, WHITE, self.save_button[i], width=4)
            canvas.blit(self.save_headline_disp[i], self.save_headline_rect[i])
            for j in range(len(self.save_text_disp[i])):
                canvas.blit(self.save_text_disp[i][j], self.save_text_rect[i][j])
            if self.save_text_time_disp[i] is not None:
                canvas.blit(self.save_text_time_disp[i], self.save_text_time_rect[i])
        # 戻るボタンの描画
        pygame.draw.rect(canvas, self.back_color, self.back_button)
        pygame.draw.rect(canvas, WHITE, self.back_button, width=2)
        canvas.blit(self.back_button_disp, self.back_button_rect)
        
    # セーブorロード選択画面の描画    
    def save_or_load_select_draw(self, canvas):
        self.light_surface = pygame.Surface((FULL_W, FULL_H))
        self.light_surface.set_alpha(150)
        self.light_surface.fill(WHITE)
        canvas.blit(self.light_surface, (0,0))
        
        self.permit_text = [f"セーブデータ {self.savedata_slot+1}"]
        if self.gamen_type == "title":
            self.permit_text.append("をロードしますか？")
        elif self.gamen_type == "stage":
            self.permit_text.append("にセーブしますか？")
        self.permit_disp = []
        self.permit_rect = []
        for i in range(len(self.permit_text)):
            self.permit_disp.append(self.permit_font[i].render(f"{self.permit_text[i]}", True, BLACK))
            self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])