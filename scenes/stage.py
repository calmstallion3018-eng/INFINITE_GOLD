import pygame
import random
from collections import deque
import sys
import settings

FULL_W = settings.Display.WIDTH
FULL_H = settings.Display.HEIGHT

BLOCK_SIZE = settings.Display.BLOCK_SIZE
MINE_W = settings.Display.MINE_W
MINE_H = settings.Display.MINE_H
RIGHT_H = settings.Display.RIGHT_H

button_quantity = settings.bottom_button_quantity

BLACK = settings.Color.BLACK
WHITE = settings.Color.WHITE
LIGHTGREEN = settings.Color.LIGHTGREEN
YELLOW = settings.Color.YELLOW
GRAY = settings.Color.GRAY
RED = settings.Color.RED

class Main():
    def __init__(self) -> None:
        # 採掘ウィンドウのrect
        self.mining_rect = pygame.Rect(0, 0, MINE_W, MINE_H)
        
        # 文字フォント
        self.font_path = "msgothic"
        
        # 採掘場所全体の大きさ
        self.MAX_MINE_W = BLOCK_SIZE * (settings.mining_size_x+4)
        self.MAX_MINE_H = BLOCK_SIZE * (settings.mining_size_y+2)

        # カメラ移動補正
        self.cursor_before_x = 0
        self.cursor_before_y = 0
        self.cursor_after_x = 0
        self.cursor_after_y = 0
        self.camera_x = 0
        self.camera_y = 0
        self.already_move_x = 0
        self.already_move_y = 0
        
        # 鉱石画像ダウンロード
        self.ore_image_default = []
        self.ore_image = []
        for i, IMAGE in enumerate(settings.ORE_IMAGE):
            self.ore_image_default.append(pygame.image.load(IMAGE).convert_alpha())
            self.ore_image.append(pygame.transform.scale(self.ore_image_default[i], (BLOCK_SIZE, BLOCK_SIZE)))
        
        # 背景の土
        self.image_ground = pygame.image.load(settings.GROUND_IMAGE).convert()
        self.image_ground = pygame.transform.scale(self.image_ground, (BLOCK_SIZE, BLOCK_SIZE))
        
        # 周りの壁の配置
        self.image_wall = pygame.image.load(settings.WALL_IMAGE).convert()
        self.image_wall = pygame.transform.scale(self.image_wall, (BLOCK_SIZE, BLOCK_SIZE))
        self.wall_posit = []
        for j in range(settings.mining_size_x+4):
            self.wall_posit.append((j*BLOCK_SIZE, 0))
        for i in range(settings.mining_size_y):
            self.wall_posit.append((0,(i+1)*BLOCK_SIZE))
            self.wall_posit.append(((settings.mining_size_x+3)*BLOCK_SIZE, (i+1)*BLOCK_SIZE))
        self.wall_posit = self.wall_posit[:-1]
        for j in range(settings.mining_size_x+4):
            self.wall_posit.append((j*BLOCK_SIZE, (settings.mining_size_y+1)*BLOCK_SIZE))
        self.wall_rect = []
        for x, y in self.wall_posit:
            self.wall_rect.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
        
        # この層の鉱石出現確率
        self.this_stage_ore_prop_list = settings.ore_prop_list
        
        # 鉱物の固有値(0-1)
        ok_random = True
        for i in range(settings.mining_size_y):
            for j in range(settings.mining_size_x):
                if ok_random and settings.ore_exist[i][j] != -1:
                    ok_random = False
        if ok_random:
            for i in range(settings.mining_size_y):
                for j in range(settings.mining_size_x):
                    settings.ore_exist[i][j] = random.random()
        
        # 鉱物の当たり判定
        self.ground = []
        for i in range(settings.mining_size_y):
            row = []
            for j in range(settings.mining_size_x):
                if settings.ore_exist[i][j] != -1:
                    row.append(pygame.Rect((2+j)*BLOCK_SIZE, (1+i)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    row.append(None)
            self.ground.append(row)
        
        # 採掘耐久値
        for i in range(settings.mining_size_y):
            for j in range(settings.mining_size_x):
                if settings.ore_exist[i][j] == -1:
                    continue
                for k in range(len(settings.ore_list)):
                    if settings.ore_exist[i][j] < sum(self.this_stage_ore_prop_list[:k+1]):
                        settings.mining_durability[i][j] = settings.ore_durability_list[k]
                        break
        
        # 鉱石のひび
        self.image_soil_crack = pygame.image.load(settings.SOIL_CRACK).convert_alpha()
        self.image_soil_crack = pygame.transform.scale(self.image_soil_crack, (BLOCK_SIZE, BLOCK_SIZE))
        
        self.image_stone_crack = pygame.image.load(settings.STONE_CRACK).convert_alpha()
        self.image_stone_crack = pygame.transform.scale(self.image_stone_crack, (BLOCK_SIZE, BLOCK_SIZE))
        
        self.image_ore_crack = pygame.image.load(settings.ORE_CRACK).convert_alpha()
        self.image_ore_crack = pygame.transform.scale(self.image_ore_crack, (BLOCK_SIZE, BLOCK_SIZE))
        
        # 次ステージへ向かうrect
        self.image_next_stage = pygame.image.load(settings.NEXT_STAGE).convert_alpha()
        self.image_next_stage = pygame.transform.scale(self.image_next_stage, (BLOCK_SIZE, BLOCK_SIZE))
        self.next_stage_rect = pygame.Rect((settings.mining_size_x+3)*BLOCK_SIZE, settings.mining_size_y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

        # プレイヤー画像と当たり判定
        self.image_miner = pygame.image.load(settings.MINER_IMAGE).convert_alpha()
        self.image_miner = pygame.transform.scale(self.image_miner, (BLOCK_SIZE, BLOCK_SIZE))
        self.player_rect = pygame.Rect(settings.player_x - BLOCK_SIZE / 2, settings.player_y - BLOCK_SIZE / 2, BLOCK_SIZE, BLOCK_SIZE)
        
        # 鉱夫画像と当たり判定
        self.image_character = pygame.image.load(settings.CHARACTER_IMAGE).convert_alpha()
        self.image_character = pygame.transform.scale(self.image_character, (BLOCK_SIZE, BLOCK_SIZE))
        self.character_rect = []
        for i in range(len(settings.character_speed)):
            self.character_rect.append(pygame.Rect(settings.character_x[i] - BLOCK_SIZE / 2, settings.character_y[i] - BLOCK_SIZE / 2, BLOCK_SIZE, BLOCK_SIZE))
        
        # 次ステージ選択画面の表示状態
        self.next_stage_select = False
        
        # ゲーム終了確認画面の表示状態
        self.end_game_select = False
        
        # 小窓の設定
        self.select_screen = pygame.Rect(FULL_W // 4, FULL_H // 4, FULL_W // 2, FULL_H // 2)
        
        self.next_stage_permit_font = pygame.font.SysFont(self.font_path, FULL_H // 12)
        self.end_game_permit_font_1 = pygame.font.SysFont(self.font_path, FULL_H // 18)
        self.end_game_permit_font_2 = pygame.font.SysFont(self.font_path, FULL_H // 24)
        self.end_game_permit_font = [self.end_game_permit_font_1, self.end_game_permit_font_2]
        
        self.end_game_permit_color = [BLACK, RED]
        
        self.next_stage_permit_text = ["次の階層へ", "進みますか？"]
        self.end_game_permit_text = ["タイトル画面に戻りますか？", "※セーブは自動ではされません"]
        
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
    
    # 新しい階層に行く時に位置と鉱石と採掘度をリセット
    def settings_liset(self):
        settings.stage_num += 1
        settings.player_x = BLOCK_SIZE * 3/2
        settings.player_y = BLOCK_SIZE * 3/2
        for i in range(len(settings.character_speed)):
            settings.character_x[i] = BLOCK_SIZE * 3/2
            settings.character_y[i] = BLOCK_SIZE * 3/2
            settings.character_move_time[i] = None
        settings.ore_exist = [[-1]*settings.mining_size_x for _ in range(settings.mining_size_y)]
        settings.mining_durability = [[None]*settings.mining_size_x for _ in range(settings.mining_size_y)]
        settings.mining_degree = [[0]*settings.mining_size_x for _ in range(settings.mining_size_y)]
    
    # プレイヤー位置変更
    def update_player(self, x, y):
        settings.player_x += x
        settings.player_y += y
        self.player_rect = pygame.Rect(settings.player_x - BLOCK_SIZE // 2, settings.player_y - BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE)
        
    #  鉱夫の位置変更
    def update_character(self, i, x, y): # x, y は 0 or 1 or -1
        settings.character_x[i] += x * settings.player_speed
        settings.character_y[i] += y * settings.player_speed
        self.character_rect[i] = pygame.Rect(settings.character_x[i] - BLOCK_SIZE // 2, settings.character_y[i] - BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE)
    
    # 所持鉱石変更
    def update_ore(self, ore_num, x):
        settings.ore_possession_list[ore_num] += x
        settings.record_list[ore_num] += x
    
    # カメラ用カーソル変数変更
    def update_cursor(self, time, pos):
        if time == "before":
            self.cursor_before_x, self.cursor_before_y = pos
        elif time == "after":
            self.cursor_after_x, self.cursor_after_y = pos
    
    # カメラ変数変更
    def update_camera(self, type):
        if type == "update":
            self.camera_x = self.already_move_x + (self.cursor_after_x - self.cursor_before_x)
            self.camera_y = self.already_move_y + (self.cursor_after_y - self.cursor_before_y)
        elif type == "save":
            if self.camera_x > 0:
                self.camera_x = 0
            if self.camera_y > 0:
                self.camera_y = 0
            if self.camera_x < MINE_W - self.MAX_MINE_W:
                self.camera_x = MINE_W - self.MAX_MINE_W
            if self.camera_y < MINE_H - self.MAX_MINE_H:
                self.camera_y = MINE_H - self.MAX_MINE_H
            self.already_move_x = self.camera_x
            self.already_move_y = self.camera_y
    
    # ページ内変数のアップデート
    def update_page(self):
        # 鉱物の当たり判定
        for i in range(settings.mining_size_y):
            for j in range(settings.mining_size_x):
                if settings.ore_exist[i][j] == -1:
                    self.ground[i][j] = None
            
        # プレイヤーの当たり判定
        self.player_rect = pygame.Rect(settings.player_x - BLOCK_SIZE / 2, settings.player_y - BLOCK_SIZE / 2, BLOCK_SIZE, BLOCK_SIZE)
        
        # 鉱夫の当たり判定
        self.character_rect = []
        for i in range(len(settings.character_speed)):
            self.character_rect.append(pygame.Rect(settings.character_x[i] - BLOCK_SIZE // 2, settings.character_y[i] - BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE))
    
    # 移動または採掘関数
    def move_or_mining(self, x, y): # x, yは0,1,-1のいずれか
        self.update_player(x * settings.player_speed, y * settings.player_speed)
        # 壁判定
        for rect in self.wall_rect:
            if self.player_rect.colliderect(rect):
                self.update_player(-x * settings.player_speed, -y * settings.player_speed)
                break
        # 採掘判定
        mining = False
        ii, jj = 0, 0 # 採掘位置
        for i in range(settings.mining_size_y):
            for j in range(settings.mining_size_x):
                if self.ground[i][j] is not None and self.player_rect.colliderect(self.ground[i][j]):
                    self.update_player(-x * settings.player_speed, -y * settings.player_speed)
                    ii, jj = i, j
                    mining = True
                    break
            if mining:
                break
        if mining:
            # 採掘度の上昇
            settings.mining_degree[ii][jj] += settings.mining_power[0]
            # 採掘完了時の動作
            if settings.mining_degree[ii][jj] >= settings.mining_durability[ii][jj]:
                self.ground[ii][jj] = None
                for k in range(len(settings.ore_list)):
                    if settings.ore_exist[ii][jj] < sum(self.this_stage_ore_prop_list[:k+1]):
                        self.update_ore(k, settings.reinc_ore_get_ratio)
                        settings.ore_exist[ii][jj] = -1
                        break
        # プレイヤーがカメラ外の時の画面移動
        if (settings.player_x - BLOCK_SIZE / 2) + self.camera_x <= 0:
            self.camera_x = BLOCK_SIZE * 3/2 - settings.player_x
        elif (settings.player_x - BLOCK_SIZE / 2) + self.camera_x >= MINE_W - BLOCK_SIZE:
            self.camera_x = MINE_W - BLOCK_SIZE * 3/2 - settings.player_x
        if (settings.player_y - BLOCK_SIZE / 2) + self.camera_y <= 0:
            self.camera_y = BLOCK_SIZE * 3/2 - settings.player_y
        elif (settings.player_y - BLOCK_SIZE / 2) + self.camera_y >= MINE_H - BLOCK_SIZE:
            self.camera_y = MINE_H - BLOCK_SIZE * 3/2 - settings.player_y
        self.update_camera("save")
    
    # 自動で動かす鉱夫が残っている鉱石に近づく
    def character_approaching(self, x, y):
        gx = int(x // settings.player_speed) - 2
        gy = int(y // settings.player_speed) - 1
        
        visited = set()
        q = deque()
        
        q.append((gx, gy, 0, (0, 0))) # (現在xy座標, 距離, 方向)
        visited.add((gx, gy))

        best = None # (距離, 点数, 方向)
        
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] # 右下左上の順
        
        while q:
            x, y, distance, first_dir = q.popleft()
            
            # 遠い距離の探索は不要
            if best and distance > best[0]:
                break
            
            # 隣に鉱石があったら鉱石のレアリティが最も高い方向を返す
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) in visited:
                    continue
                visited.add((nx, ny))
                
                ndir = first_dir if distance > 0 else (dx, dy)
                
                # 近くの鉱石を探索
                if 0 <= nx < settings.mining_size_x and 0 <= ny < settings.mining_size_y and self.ground[ny][nx] is not None:
                    ore = settings.ore_exist[ny][nx]
                    candidate = (distance+1, -ore, ndir)
                    if best is None or candidate < best:
                        best = candidate
                    continue
                
                q.append((nx, ny, distance+1, ndir))
        
        if best:
            return best
        
        for dx, dy in directions:
            nx, ny = gx + dx, gy + dy
            if 0 <= nx < settings.mining_size_x and 0 <= ny < settings.mining_size_y:
                if self.ground[ny][nx] is None:
                    return float("inf"), 0, (dx, dy)
        
        return float("inf"), 0, (0, 0)
    
    # 鉱夫の移動・採掘関数
    def character_move_or_mining(self, character_num):
        # 採掘できる鉱石がない時
        mineable = False
        for i in range(settings.mining_size_y):
            for j in range(settings.mining_size_x):
                if settings.ore_exist[i][j] != -1:
                    mineable = True
                    break
            if mineable:
                break
        if not mineable:
            return
        
        #鉱石があるときに近づく
        gx = int(settings.character_x[character_num] // settings.player_speed - 2)
        gy = int(settings.character_y[character_num] // settings.player_speed - 1)
        _, _, direct = self.character_approaching(settings.character_x[character_num], settings.character_y[character_num])
        dx, dy = direct
        # 指定した方向に鉱石がある時
        if 0 <= gx + dx < settings.mining_size_x and 0 <= gy + dy < settings.mining_size_y and self.ground[gy + dy][gx + dx] != None:
            # 採掘度の上昇
            settings.mining_degree[gy + dy][gx + dx] += settings.mining_power[character_num+1]
            # 採掘完了時の動作
            if settings.mining_degree[gy + dy][gx + dx] >= settings.mining_durability[gy + dy][gx + dx]:
                self.ground[gy + dy][gx + dx] = None
                for k in range(len(settings.ore_list)):
                    if settings.ore_exist[gy + dy][gx + dx] < sum(self.this_stage_ore_prop_list[:k+1]):
                        self.update_ore(k, settings.reinc_ore_get_ratio)
                        settings.ore_exist[gy + dy][gx + dx] = -1
                        break
            return
        else:
            self.update_character(character_num, dx, dy)
            
    # 描画処理
    def draw(self, canvas):
        # 背景：黒
        canvas.fill(BLACK)
        # 地面の描画
        for x in range(settings.mining_size_x+4):
            for y in range(settings.mining_size_y+2):
                canvas.blit(self.image_ground, (x*BLOCK_SIZE + self.camera_x, y*BLOCK_SIZE + self.camera_y))
        # 壁の描画
        for x, y in self.wall_posit:
            canvas.blit(self.image_wall, (x + self.camera_x, y + self.camera_y))
        pygame.draw.line(canvas, BLACK, (BLOCK_SIZE + self.camera_x, BLOCK_SIZE + self.camera_y), ((settings.mining_size_x+3)*BLOCK_SIZE + self.camera_x, BLOCK_SIZE + self.camera_y), 2)
        pygame.draw.line(canvas, BLACK, (BLOCK_SIZE + self.camera_x, BLOCK_SIZE + self.camera_y), (BLOCK_SIZE + self.camera_x, (settings.mining_size_y+1)*BLOCK_SIZE + self.camera_y), 2)
        pygame.draw.line(canvas, BLACK, ((settings.mining_size_x+3)*BLOCK_SIZE + self.camera_x, BLOCK_SIZE + self.camera_y), ((settings.mining_size_x+3)*BLOCK_SIZE + self.camera_x, settings.mining_size_y*BLOCK_SIZE + self.camera_y), 2)
        pygame.draw.line(canvas, BLACK, (BLOCK_SIZE + self.camera_x, (settings.mining_size_y+1)*BLOCK_SIZE + self.camera_y), ((settings.mining_size_x+4)*BLOCK_SIZE + self.camera_x, (settings.mining_size_y+1)*BLOCK_SIZE + self.camera_y), 2)
        pygame.draw.line(canvas, BLACK, ((settings.mining_size_x+3)*BLOCK_SIZE + self.camera_x, settings.mining_size_y*BLOCK_SIZE + self.camera_y), ((settings.mining_size_x+4)*BLOCK_SIZE + self.camera_x, settings.mining_size_y*BLOCK_SIZE + self.camera_y), 2)
        # 鉱物の描画
        for i in range(settings.mining_size_y):
            for j in range(settings.mining_size_x):
                if settings.ore_exist[i][j] != -1:
                    for k in range(len(settings.ore_list)):
                        if settings.ore_exist[i][j] < sum(self.this_stage_ore_prop_list[:k+1]):
                            canvas.blit(self.ore_image[k], ((2+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y))
                            if k == 0:
                                pygame.draw.line(canvas, BLACK, ((2+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y), ((3+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y))
                                pygame.draw.line(canvas, BLACK, ((2+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y), ((2+j)*BLOCK_SIZE + self.camera_x, (2+i)*BLOCK_SIZE + self.camera_y))
                                pygame.draw.line(canvas, BLACK, ((3+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y), ((3+j)*BLOCK_SIZE + self.camera_x, (2+i)*BLOCK_SIZE + self.camera_y))
                                pygame.draw.line(canvas, BLACK, ((2+j)*BLOCK_SIZE + self.camera_x, (2+i)*BLOCK_SIZE + self.camera_y), ((3+j)*BLOCK_SIZE + self.camera_x, (2+i)*BLOCK_SIZE + self.camera_y))
                                self.image_soil_crack.set_alpha(min(255, int(255*settings.mining_degree[i][j] / (settings.mining_durability[i][j] - 1))))
                                canvas.blit(self.image_soil_crack, ((2+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y))
                            elif k == 1:
                                self.image_stone_crack.set_alpha(min(255, int(255*settings.mining_degree[i][j] / (settings.mining_durability[i][j] - 1))))
                                canvas.blit(self.image_stone_crack, ((2+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y))
                            else:
                                self.image_ore_crack.set_alpha(min(255, int(255*settings.mining_degree[i][j] / (settings.mining_durability[i][j] - 1))))
                                canvas.blit(self.image_ore_crack, ((2+j)*BLOCK_SIZE + self.camera_x, (1+i)*BLOCK_SIZE + self.camera_y))
                            break
                        
        # 次ステージへ進む看板の描画
        canvas.blit(self.image_next_stage, ((settings.mining_size_x+3)*BLOCK_SIZE + self.camera_x, (settings.mining_size_y-3/4)*BLOCK_SIZE + self.camera_y))
        # プレイヤーの描画
        canvas.blit(self.image_miner, ((settings.player_x - BLOCK_SIZE / 2) + self.camera_x, (settings.player_y - BLOCK_SIZE / 2) + self.camera_y))
        # 鉱夫の描画
        mis = 2 # 鉱夫をちょっとズラす
        for i in range(len(settings.character_speed)):
            canvas.blit(self.image_character, ((settings.character_x[i] - BLOCK_SIZE / 2) + mis*i + self.camera_x, (settings.character_y[i] - BLOCK_SIZE / 2) + self.camera_y))
                
    # 選択画面の描画（type==next_stage -> 次ステージ, type==end_game -> ゲーム終了）
    def select_draw(self, canvas, type):
        self.dark_surface = pygame.Surface((FULL_W, FULL_H))
        self.dark_surface.set_alpha(150)
        self.dark_surface.fill(BLACK)
        canvas.blit(self.dark_surface, (0,0))
        
        self.permit_disp = []
        self.permit_rect = []
        if type == "next_stage":
            for i in range(len(self.next_stage_permit_text)):
                self.permit_disp.append(self.next_stage_permit_font.render(f"{self.next_stage_permit_text[i]}", True, BLACK))
                self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        elif type == "end_game":
            for i in range(len(self.end_game_permit_text)):
                self.permit_disp.append(self.end_game_permit_font[i].render(f"{self.end_game_permit_text[i]}", True, self.end_game_permit_color[i]))
                self.permit_rect.append(self.permit_disp[i].get_rect(center=(FULL_W // 2, (i+3)*FULL_H // 8)))
        
        pygame.draw.rect(canvas, WHITE, self.select_screen)
        pygame.draw.rect(canvas, BLACK, self.select_screen, width=5)
        for i in range(len(self.permit_disp)):
            canvas.blit(self.permit_disp[i], self.permit_rect[i])
        for i in range(len(self.y_n_button)):
            pygame.draw.rect(canvas, self.y_n_color[i], self.y_n_button[i])
            pygame.draw.rect(canvas, BLACK, self.y_n_button[i], width=2)
            canvas.blit(self.y_n_disp[i], self.y_n_rect[i])