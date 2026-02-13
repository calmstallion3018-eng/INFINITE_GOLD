import pygame
import os
import math

# 画面定数
class Display:
    WIDTH = 900
    HEIGHT  = 600
    
    # 一ブロックごとのサイズ
    BLOCK_SIZE = 45
    MINE_W = BLOCK_SIZE * 14
    MINE_H = BLOCK_SIZE * 12 # == 540 == FULL_H * 9/10
    
    # 右側画面の1列の高さ
    RIGHT_H = MINE_H // 15

def init():
    info = pygame.display.Info()
    Display.WIDTH = info.current_w
    Display.HEIGHT = info.current_h

# 色定数
class Color:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    LIGHTGREEN = (154,196,50)
    YELLOW = (255,215,0)
    GRAY = (200,200,200)
    DARK_GRAY = (150,150,150)
    ASH = (100,100,100)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (170,120,210)
    DARK_PURPLE = (120,70,160)

# 下部ボタンの文字サイズ
bottom_button_font_size = Display.HEIGHT // 20

# 下部ボタンの名前
bottom_button_name = ["鉱山", "交易所", "幸運", "鍛冶屋", "雇用", "転生", "実績", "セーブ"]
    
# 下部ボタンの数
bottom_button_quantity = len(bottom_button_name)
    
# 表示する鉱石を制限
def ore_limit(ore_prop_list):
    ore = len(ore_prop_list)
    while True:
        if ore_prop_list[ore-1] != 0:
            break
        ore -= 1
    return ore

# 階層番号（変数）
stage_num = 1

# プレイヤーの位置（変数）
player_x = Display.BLOCK_SIZE * 3/2
player_y = Display.BLOCK_SIZE * 3/2

# 鉱夫の位置（変数）
character_x = []
character_y = []

# プレイヤーの速度
player_speed = Display.BLOCK_SIZE

# 鉱夫の移動間隔計算用（変数）
character_move_time = []

# 採掘場所のサイズ（転生変数）
mining_size_x = 10
mining_size_y = 10

# 鉱物の有無のリスト（二次元）（変数） -1 -> nonexist, 0~1 -> 鉱物の固有値
ore_exist = [[-1]*mining_size_x for _ in range(mining_size_y)]

# お金（変数）
money = 0

# 鉱石の種類リスト
ore_list = ["soil", "stone", "iron", "copper", "silver", "gold", "diamond", "ruby", "sapphire", "emerald", "alexandrite", "paraiba_tourmaline", "padparadscha_sapphire"]

# 鉱石の名前リスト
ore_name_list = ["土", "石", "鉄", "銅", "銀", "金", "ダイヤモンド", "ルビー", "サファイア", "エメラルド", "アレキサンドライト", "パライバトルマリン", "パパラチアサファイア"]

# 鉱石の所持数リスト（変数）
ore_possession_list = [0] * len(ore_list)

# 鉱石の耐久値リスト
ore_durability_list = [2, 5, 20, 100, 300, 700, 1500, 1500, 1500, 1500, 2500, 2500, 2500]

# 画像ダウンロード
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
ORES_DIR = os.path.join(IMAGES_DIR, "ores")
ORE_IMAGE = []
for name in ore_list:
    ORE_IMAGE.append(os.path.join(ORES_DIR, name+".png"))

GROUNDS_DIR = os.path.join(IMAGES_DIR, "grounds")
GROUND_IMAGE = os.path.join(GROUNDS_DIR, "ground.png")
WALL_IMAGE = os.path.join(GROUNDS_DIR, "wall.png")

CRACKS_DIR = os.path.join(IMAGES_DIR, "cracks")
SOIL_CRACK = os.path.join(CRACKS_DIR, "soil_crack.png")
STONE_CRACK = os.path.join(CRACKS_DIR, "stone_crack.png")
ORE_CRACK = os.path.join(CRACKS_DIR, "ore_crack.png")

PEOPLE_DIR = os.path.join(IMAGES_DIR, "people")
MINER_IMAGE = os.path.join(PEOPLE_DIR, "miner.png")
CHARACTER_IMAGE = os.path.join(PEOPLE_DIR, "character.png")

OTHERS_DIR = os.path.join(IMAGES_DIR, "others")
NEXT_STAGE = os.path.join(OTHERS_DIR, "next_stage.png")
FLOWER_IMAGE = os.path.join(OTHERS_DIR, "lucky_flower.png")

PICKAXES_DIR = os.path.join(IMAGES_DIR, "pickaxes")
PICKAXE_IMAGE = []
for name in ore_list[1:7]:
    PICKAXE_IMAGE.append(os.path.join(PICKAXES_DIR, name+"_pickaxe.png"))

# 採掘耐久値（変数）
mining_durability = [[None]*mining_size_x for _ in range(mining_size_y)]

# 採掘度（変数）
mining_degree = [[0]*mining_size_x for _ in range(mining_size_y)]

# 採掘力（変数）
mining_power = [1]

# 鉱物の出現確率リスト（変数）
ore_prop_list = [0.9, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 鉱物の出現確率の変更リストのリスト
ore_prop_change_list = []
ore_prop_change_list.append([-0.005, 0.005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # 0~9 -> [0.85, 0.15, 0...]
ore_prop_change_list.append([-0.01, 0.005, 0.005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # 10~29 -> [0.65, 0.25, 0.1, 0...]
ore_prop_change_list.append([-0.01, 0.005, 0.003, 0.002, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # 30~49 -> [0.45, 0.35, 0.16, 0.04, 0...]
ore_prop_change_list.append([-0.015, 0.01, 0.003, 0.001, 0.001, 0, 0, 0, 0, 0, 0, 0, 0]) # 50~59 -> [0.35, 0.45, 0.19, 0.05, 0.01, 0...]
ore_prop_change_list.append([-0.015, 0.005, 0.005, 0.003, 0.002, 0, 0, 0, 0, 0, 0, 0, 0]) # 60~79 -> [0, 0.55, 0.29, 0.11, 0.05, 0...]
ore_prop_change_list.append([0, -0.01, 0.003, 0.003, 0.002, 0.002, 0, 0, 0, 0, 0, 0, 0]) # 80~99 -> [0, 0.35, 0.35, 0.17, 0.09, 0.04, 0...]
ore_prop_change_list.append([0, -0.015, 0.005, 0.003, 0.003, 0.003, 0.001, 0, 0, 0, 0, 0, 0]) # 100~109 -> [0, 0.2, 0.4, 0.2, 0.12, 0.07, 0.01, 0...]
ore_prop_change_list.append([0, -0.005, 0, 0, 0.002, 0.002, 0.001, 0, 0, 0, 0, 0, 0]) # 110~129 -> [0, 0.1, 0.4, 0.2, 0.16, 0.11, 0.03, 0...]
ore_prop_change_list.append([0, -0.005, 0, 0, 0, 0, 0.002, 0.001, 0.001, 0.001, 0, 0, 0]) # 130~149 -> [0, 0, 0.4, 0.2, 0.16, 0.11, 0.07, 0.02, 0.02, 0.02, 0...]
ore_prop_change_list.append([0, 0, -0.002, -0.001, -0.001, 0, 0.001, 0.001, 0.001, 0.001, 0, 0, 0]) # 150~169 -> [0, 0, 0.36, 0.18, 0.14, 0.11, 0.09, 0.04, 0.04, 0.04, ...]
ore_prop_change_list.append([0, 0, -0.003, 0, 0, 0, 0, 0, 0, 0, 0.001, 0.001, 0.001]) # 170~199 -> [0, 0, 0.27, 0.18, 0.14, 0.11, 0.09, 0.04, 0.04, 0.04, 0.03, 0.03, 0.03]
ore_prop_change_list.append([0, 0, -0.02, -0.015, -0.01, 0, 0, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005]) # 200 -> [0, 0, 0.25, 0.165, 0.13, 0.11, 0.09, 0.05, 0.05, 0.05, 0.035, 0.035, 0.035]

# 出現確率変化値の変化場所リスト
prop_change_change_list = [9,29,49,59,79,99,109,129,149,169,199,200]

# 鉱物の売値リスト
ore_price_list = [1, 5, 200, 3000, 25000, 150000, 600000, 1000000, 1000000, 1000000, 10000000, 10000000, 10000000]

# 幸運の花レベル（変数）
lucky_flower_level = 0

# 幸運の花レベルアップ必要金額初期値
flower_levelup_money_zero = 100

# 幸運の花レベルアップ必要金額倍率補正
flower_levelup_money_ratio = 1.1

# ツルハシの素材
pickaxe_type = ["石", "鉄", "銅", "銀", "金", "ダイヤ"]

# ツルハシレベル（変数）
pickaxe_level = [[] for _ in range(6)]
pickaxe_level[0].append(0) # 初期装備

# ツルハシ（レベル0）の基礎採掘力
pickaxe_power = [1, 5, 20, 50, 120, 200]

# ツルハシのレベルごとの採掘力の上昇率 10%
pickaxe_power_ratio = 0.1

# 使用中のツルハシの素材(0-5)、何番目のツルハシか（変数）
use_pickaxe_type , use_pickaxe_num = [0], [0]

# ツルハシの鋳造に必要な素材 (必要鉱石のore_list番号, 必要個数)
materials_require = [[(1, 10)], [(1, 5), (2, 10)], [(2, 5), (3, 10)], [(2, 5), (4, 10)], [(2, 5), (5, 10)], [(2, 5), (6, 10)]]

# 鉱夫の移動速度（変数）
character_speed = []

# 雇用必要金額初期値（=昇給必要金額初期値）
employ_money_zero = 10000

# 雇用必要金額倍率補正
employ_money_ratio = 20

# 昇給必要金額倍率補正関数（xは何-1人目か）
def raise_money_ratio(x):
    return 1 + 1/math.exp(math.sqrt(x))

# 転生ボタンの名前
reinc_name = ["鉱山の縦の幅を広げる", "鉱山の奥行を広げる", "1回の獲得鉱石数を増やす", "転生経験値倍率を上げる"]

# 既に所持している転生経験値（[縦, 横, 獲得鉱石数, 転生経験値]）(変数)
experience = [0, 0, 0, 0]

# 転生前後のレベル計算関数
def calc_reinc_level(i, time):
    if time == "now":
        return int(math.log2(1+experience[i]))
    elif time == "after":
        return int(math.log2(1+experience[i]+have_exp)) # レベルをiから1上げるのに必要な経験値が2^i

# 鉱石獲得倍率（転生変数）
reinc_ore_get_ratio = 1

# 画面表示時の単位
reinc_unit = ["マス", "マス", "倍", "倍"]

# 取得経験値（変数）
have_exp = 0

# 取得経験値倍率（転生変数）（have_expを直接変更する）
reinc_exp_ratio = 1

# 転生レベルごとの広さ、倍率計算関数
def calc_reinc_value(i, level):
    if i == 0: # 横の奥行
        return 10 + level
    elif i == 1: # 縦の幅
        return 10 + level
    elif i == 2: # 鉱石獲得倍率
        return 1 + level
    elif i == 3: # 取得経験値倍率
        return 1 + level

# 実績達成度計算リスト（転生後もリセットされない変数）（[0~12:鉱石の累計採掘数13種類, 13:最大幸運の花レベル, 14:累計鋳造回数, 15:最大鍛錬レベル, 16:最高雇用人数, 17:鉱夫最高移動速度, 18:転生回数, 19:鉱山面積, 20:実績達成回数]）
record_list = [0] * 21
record_list[19] = mining_size_x * mining_size_y

# 実績の達成条件数リストリスト
record_terms_num = []
for _ in ore_list:
    record_terms_num.append([50, 100, 200, 300, 500, 750] + list(range(1000, 5000, 500)) + list(range(5000, 10001, 1000))) # 0~12
record_terms_num.append(list(range(10, 201, 10))) # 13
record_terms_num.append([5, 10, 20, 30] + list(range(50, 500, 50)) + list(range(500, 1001, 100))) # 14
record_terms_num.append(list(range(5, 101, 5))) # 15
record_terms_num.append(list(range(1, 21))) # 16
record_terms_num.append(list(range(5, 30, 5)) + list(range(30, 101, 10))) # 17
record_terms_num.append([1, 2, 3, 5, 7] + list(range(10, 50, 5)) + list(range(50, 101, 10))) # 18
record_terms_num.append(list(range(200, 500, 100)) + list(range(500, 1500, 250)) + list(range(1500, 5001, 500))) # 19
max_records = 0
for lst in record_terms_num:
    max_records += len(lst)
record_terms_num.append(list(range(5, 30, 5)) + list(range(30, 100, 10)) + list(range(100, max_records, 20)) + [max_records]) # 20

# 鉱物の売値の実績による倍率リスト（転生後もリセットされない変数）
ore_price_ratio = [1.0] * len(ore_list)

# 実績の報酬リストリスト
reward_ratio = []
for _ in ore_list:
    reward_ratio.append([1] * 6 + [2] * 8 + [3] * 6) # 0~12
reward_ratio.append([0.5] * 5 + [1] * 5 + [1.5] * 5 + [2] * 5) # 13
reward_ratio.append([0.5] * 4 + [1] * 5 + [1.5] * 4 + [2] * 6) # 14
reward_ratio.append([0.5] * 5 + [1] * 5 + [1.5] * 5 + [2] * 5) # 15
reward_ratio.append([1] * 5 + [2] * 5 + [3] * 5 + [4] * 5) # 16
reward_ratio.append([1] * 5 + [2] * 8) # 17
reward_ratio.append([0.5] * 5 + [1] * 5 + [1.5] * 5) # 18
reward_ratio.append([1] * 4 + [2] * 4 + [3] * 4 + [4] * 4) # 19
reward_ratio.append([1] * 5 + [2] * 7) # 20
count = 0
for _ in range((max_records-101) // 20 + 1):
    reward_ratio[-1].append(3 + count//5) # 20
    count += 1
reward_ratio[-1].append(10) # 20

# 達成した実績の数リスト（転生後もリセットされない変数）
record_completes = [0] * 21

# プレイ時間（変数）
playing_time = 0