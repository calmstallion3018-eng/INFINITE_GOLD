import pygame
from pygame.locals import *
import sys
import settings
from scenes import title, savedata, basescene, stage, exchange, luck, forge, employee, reincarnation, achievement

# pygameの初期化
pygame.init()
 
# 更新スピードの設定
fps = 60
fpsClock = pygame.time.Clock()

# 画面サイズの設定
LOGICAL_W, LOGICAL_H = settings.Display.WIDTH, settings.Display.HEIGHT
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
real_w, real_h = screen.get_size()

canvas = pygame.Surface((LOGICAL_W, LOGICAL_H))

# 画面サイズ調整関数
def screen_to_logical(x):
    if isinstance(x, tuple):
        xx, yy = x
        return (xx * LOGICAL_W / real_w, yy * LOGICAL_H / real_h)
    else:
        return x * LOGICAL_W / real_w

# ウィンドウタイトルの設定
pygame.display.set_caption("infinite gold")

running = True
tracking = False # 画面移動追跡

# ゲームプレイ時間の計測
play_start_time = 0
play_now_time = 0

# xマーク表示時間計測用
cannot_start_time = dict()

# xマーク表示関数
def draw_cannot(is_cannot, start, draw_f, canvas, limit_ms=2000):
    if not is_cannot:
        return False, 0
    now = pygame.time.get_ticks()
    if now - start <= limit_ms:
        draw_f(canvas)
        return True, start
    else:
        return False, 0

# 画面変数
gamen_title = title.Main("start")
gamen_title2 = title.Main("continue")
gamen_savedata = savedata.Main()
gamen_base = basescene.Basescene()
gamen_mine_list = [None] * (settings.bottom_button_quantity-1)

# 鉱山系画面のリセット
def gamen_liset(mine_list):
    mine_list[0] = stage.Main()
    mine_list[1] = exchange.Main()
    mine_list[2] = luck.Main()
    mine_list[3] = forge.Main()
    mine_list[4] = employee.Main()
    mine_list[5] = reincarnation.Main()
    mine_list[6] = achievement.Main()

# 下部ボタンによる画面移動
def bottom_button_move(gamen, pos, num, mine_list, savedata, base):
    new_i = None
    for i in range(len(mine_list)):
        if base.button[i].collidepoint(pos):
            if i != num:
                new_i = i
    if new_i is not None:
        mine_list[new_i].update_page()
        return mine_list[new_i], new_i
    elif base.button[-1].collidepoint(pos):
        savedata.gamen_type = "stage"
        return savedata, None
    return gamen, None

# キーボード操作でstage画面に戻る
def back_stage(gamen):
    if event.key == K_x or event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_ESCAPE:
        gamen_mine_list[0].update_page()
        gamen_base.change_page(0)
        return gamen_mine_list[0]
    return gamen

# タイトル画面の操作
def title_choice(gamen, event, pos, title_num, gamen_0, mine_list=None, gamen_2=None):
    which = gamen.which
    new_gamen = gamen
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        if gamen.button[0].collidepoint(pos):
            which = None
            new_gamen = gamen_0
            if title_num == 2:
                new_gamen.gamen_type = "title"
        elif gamen.button[1].collidepoint(pos):
            if title_num == 1:
                return which, new_gamen, True
            elif title_num == 2:
                which = None
                gamen_liset(mine_list)
                new_gamen = mine_list[0]
        elif title_num == 2 and gamen.button[2].collidepoint(pos):
            which = None
            new_gamen = gamen_2
    elif event.type == KEYDOWN:
        if event.key == K_x or event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_ESCAPE:
            if title_num == 1:
                return which, new_gamen, True
            elif title_num == 2:
                new_gamen = gamen_2
        elif which == 0 and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            which = None
            new_gamen = gamen_0
            if title_num == 2:
                new_gamen.gamen_type = "title"
        elif which == 1 and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            if title_num == 1:
                return which, new_gamen, True
            elif title_num == 2:
                which = None
                gamen_liset(mine_list)
                new_gamen = mine_list[0]
        elif which is not None and (event.key == K_w or event.key == K_UP or event.key == K_s or event.key == K_DOWN):
            which = 1 - which
        elif which is None:
            if event.key == K_w or event.key == K_UP:
                which = 0
            elif event.key == K_s or event.key == K_DOWN:
                which = 1
    return which, new_gamen, False

# 小窓画面でのはいorいいえの選択
def y_n_window(event, y_n_button, pos, select, which, y_f, n_f=None, y_gamen=None, mine_list=None, n_gamen=None):
    new_gamen = n_gamen
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        if y_n_button[0].collidepoint(pos):
            y_f()
            if isinstance(n_gamen, savedata.Main):
                if n_gamen.gamen_type == "title":
                    n_gamen.load_savedata(n_gamen.save_or_load())
                    gamen_liset(mine_list)
                    y_gamen = mine_list[0]
                    n_gamen.play_start_time = pygame.time.get_ticks()
                elif n_gamen.gamen_type == "stage":
                    play_now_time = pygame.time.get_ticks()
                    n_gamen.save_time(play_now_time)
                    n_gamen.play_start_time = play_now_time
                    n_gamen.save_or_load()
                    y_gamen = mine_list[0]
                    y_gamen.update_page()
            elif isinstance(n_gamen, reincarnation.Main):
                gamen_liset(mine_list)
                y_gamen = mine_list[0]
            elif mine_list is not None:
                mine_list[0] = stage.Main()
                y_gamen = mine_list[0]
            new_gamen = y_gamen
            select = False
        elif y_n_button[1].collidepoint(pos):
            if n_f is not None:
                n_f()
            select = False
    elif event.type == KEYDOWN:
        if (which is None or which == 0) and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
            which = None
            y_f()
            if isinstance(n_gamen, savedata.Main):
                if n_gamen.gamen_type == "title":
                    n_gamen.load_savedata(n_gamen.save_or_load())
                    gamen_liset(mine_list)
                    y_gamen = mine_list[0]
                    n_gamen.play_start_time = pygame.time.get_ticks()
                elif n_gamen.gamen_type == "stage":
                    play_now_time = pygame.time.get_ticks()
                    n_gamen.save_time(play_now_time)
                    n_gamen.play_start_time = play_now_time
                    n_gamen.save_or_load()
                    y_gamen = mine_list[0]
                    y_gamen.update_page()
            elif isinstance(n_gamen, reincarnation.Main):
                gamen_liset(mine_list)
                y_gamen = mine_list[0]
            if mine_list is not None:
                mine_list[0] = stage.Main()
                y_gamen = mine_list[0]
            new_gamen = y_gamen
            select = False
        elif (which == 1 and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN)) or (event.key == K_x or event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_ESCAPE):
            which = None
            if n_f is not None:
                n_f()
            select = False
        elif which is None:
            if event.key == K_a or event.key == K_LEFT:
                which = 0
            elif event.key == K_d or event.key == K_RIGHT:
                which = 1
        elif which is not None:
            if event.key == K_a or event.key == K_LEFT or event.key == K_d or event.key == K_RIGHT:
                which = 1 - which
    return select, which, new_gamen

# キーボードで2*2のボタンを選択する
def two_times_two_keyboard(event, which):
    if which is None:
        if event.key == K_w or event.key == K_UP or event.key == K_a or event.key == K_LEFT:
            return 0
        elif event.key == K_d or event.key == K_RIGHT:
            return 1
        elif event.key == K_s or event.key == K_DOWN:
            return 2
    elif which == 0:
        if event.key == K_w or event.key == K_UP or event.key == K_s or event.key == K_DOWN:
            return 2
        elif event.key == K_a or event.key == K_LEFT or event.key == K_d or event.key == K_RIGHT:
            return 1
    elif which == 1:
        if event.key == K_w or event.key == K_UP or event.key == K_s or event.key == K_DOWN:
            return 3
        elif event.key == K_a or event.key == K_LEFT or event.key == K_d or event.key == K_RIGHT:
            return 0
    elif which == 2:
        if event.key == K_w or event.key == K_UP or event.key == K_s or event.key == K_DOWN:
            return 0
        elif event.key == K_a or event.key == K_LEFT or event.key == K_d or event.key == K_RIGHT:
            return 3
    elif which == 3:
        if event.key == K_w or event.key == K_UP or event.key == K_s or event.key == K_DOWN:
            return 1
        elif event.key == K_a or event.key == K_LEFT or event.key == K_d or event.key == K_RIGHT:
            return 2

# 画面のスクロール判定
def mousewheel_scroll(gamen, event, pos, is_pickaxe=False, is_record=False):
    if event.type == MOUSEWHEEL:
        if gamen.scroll_screen.collidepoint(pos):
            gamen.update_camera(event.y)
            gamen.update_scrollbar()
            if is_pickaxe:
                gamen.update_pickaxe()
            if is_record:
                gamen.update_record()
            
# スクロールバーを掴む
def grab_scrollbar(gamen, pos):
    if gamen.scroll_bar_rect.collidepoint(pos):
        gamen.scroll_bar_color = ASH
        gamen.scroll_dragging = True
        gamen.drag_offset_y = pos[1] - gamen.scroll_bar_rect.y
        
# スクロールバーを動かす
def move_scrollbar(gamen, event, pos, camera_y, is_pickaxe=False, is_record=False):
    if event.type == MOUSEMOTION and gamen.scroll_dragging:
        gamen.update_scrollbar()
        new_bar_y = pos[1] - gamen.drag_offset_y
        min_y = gamen.scroll_screen.y
        max_y = gamen.scroll_screen.y + gamen.scroll_view_h - gamen.scroll_bar_rect.height
        new_bar_y = max(min_y, min(new_bar_y, max_y))
        ratio = (new_bar_y - min_y) / (max_y - min_y) if max_y - min_y > 0 else 0
        if is_pickaxe:
            gamen.update_pickaxe()
        if is_record:
            gamen.update_record()
        return ratio * (gamen.scroll_content_h - gamen.scroll_view_h)
    return camera_y

# スクロールバーを離す
def release_scrollbar(gamen, event):
    if event.type == MOUSEBUTTONUP and event.button == 1:
        gamen.scroll_bar_color = DARK_GRAY
        gamen.scroll_dragging = False

# ボタンの色更新関数
def update_hover_color(rect, mouse_pos, default_color, hover_color):
    return hover_color if rect.collidepoint(mouse_pos) else default_color

# ボタンリストの色更新用関数
def update_hover_colors(rects, mouse_pos, default_color, hover_color, colors, scroll_screen=None, skip_num=None, can_push=None):
    for i in range(len(rects)):
        if skip_num is not None and i == skip_num:
            continue
        if can_push is not None and not can_push[i]:
            continue
        if scroll_screen is not None and not scroll_screen.collidepoint(mouse_pos):
            colors[i] = default_color
            continue
        colors[i] = hover_color if rects[i].collidepoint(mouse_pos) else default_color

# ボタンリストinリストの色更新用関数
def update_hover_colorss(rectss, mouse_pos, default_color, hover_color, colorss, scroll_screen=None):
    for i in range(len(rectss)):
        for j in range(len(rectss[i])):
            if rectss[i][j] is None:
                continue
            if scroll_screen is not None and not scroll_screen.collidepoint(mouse_pos):
                colorss[i][j] = default_color
                continue
            colorss[i][j] = hover_color if rectss[i][j].collidepoint(mouse_pos) else default_color

# マウス操作時にキーボードの選択を解除する
def delete_which(rects, mouse_pos, which, skip_num=None):
    for i in range(len(rects)):
        if skip_num is not None and i == skip_num:
            continue
        if rects[i].collidepoint(mouse_pos):
            return None
    return which

# キーボードで選択中のボタンの色変更
def update_which_color(which, colors, assign_color):
    if which is not None:
        colors[which] = assign_color

GRAY = settings.Color.GRAY
DARK_GRAY = settings.Color.DARK_GRAY
ASH = settings.Color.ASH
PURPLE = settings.Color.PURPLE
DARK_PURPLE = settings.Color.DARK_PURPLE

# タイトル画面の表示
gamen = gamen_title
while running:
    mouse = screen_to_logical(pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        # 終了イベント
        if event.type == pygame.QUIT:
            running = False
        
        if (event.type == MOUSEBUTTONDOWN and event.button == 1) or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
            event_pos = screen_to_logical(event.pos)
        else:
            event_pos = (-1, -1)
        
        if gamen == gamen_title:
            gamen.which, gamen, is_quit = title_choice(gamen, event, event_pos, 1, gamen_title2)
            if is_quit:
                running = False
        
        elif gamen == gamen_title2:
            gamen.which, gamen, _ = title_choice(gamen, event, event_pos, 2, gamen_savedata, mine_list=gamen_mine_list, gamen_2=gamen_title)
        
        elif gamen == gamen_savedata:
            if gamen.can_select:
                gamen.can_select, gamen.y_n_which, gamen = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_select, gamen.y_n_which, gamen_base.change_page, mine_list=gamen_mine_list, n_gamen=gamen)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # ロード確認画面へ移動（マウス）
                    for i in range(4):
                        if gamen.save_button[i].collidepoint(event_pos):
                            gamen.savedata_slot = i
                            gamen.can_select = True
                            break
                    # 前の画面に戻る（マウス）
                    if gamen.back_button.collidepoint(event_pos):
                        if gamen.gamen_type == "title":
                            gamen = gamen_title2
                        elif gamen.gamen_type == "stage":
                            gamen = gamen_mine_list[0]
                            gamen_base.change_page(0)
                elif event.type == KEYDOWN:
                    # ロード確認画面へ移動（キーボード）
                    if gamen.savedata_which is not None and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
                        gamen.savedata_slot = gamen.savedata_which
                        gamen.savedata_which = None
                        gamen.can_select = True
                    # 前の画面に戻る（キーボード）
                    elif event.key == K_x or event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_ESCAPE:
                        gamen.savedata_which = None
                        if gamen.gamen_type == "title":
                            gamen = gamen_title2
                        elif gamen.gamen_type == "stage":
                            gamen = gamen_mine_list[0]
                            gamen.update_page()
                            gamen_base.change_page(0)
                    # ボタン選択（キーボードのみ）
                    else:
                        gamen.savedata_which = two_times_two_keyboard(event, gamen.savedata_which)
            
        elif gamen is gamen_mine_list[0]:
            if gamen.next_stage_select:
                gamen.next_stage_select, gamen.y_n_which, gamen = y_n_window(event, gamen.y_n_button, event_pos, gamen.next_stage_select, gamen.y_n_which, gamen.settings_liset, n_f=gamen.move_or_mining(-1,0), mine_list=gamen_mine_list, n_gamen=gamen)
            elif gamen.end_game_select:
                gamen.end_game_select, gamen.y_n_which, gamen = y_n_window(event, gamen.y_n_button, event_pos, gamen.end_game_select, gamen.y_n_which, gamen_title.settings_liset, y_gamen=gamen_title, n_gamen=gamen)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # 鉱山のカメラ移動（マウスのみ）
                    if gamen.mining_rect.collidepoint(event_pos):
                        tracking = True
                        gamen.update_cursor("before", event_pos)
                    # 下部ボタンによる画面移動（マウスのみ）
                    gamen, move_num = bottom_button_move(gamen, event_pos, 0, gamen_mine_list, gamen_savedata, gamen_base)
                    if move_num is not None:
                        gamen_base.change_page(move_num)
                elif event.type == KEYDOWN:
                    # プレイヤーの移動・採掘（キーボードのみ）
                    if event.key == K_LEFT or event.key == K_a:
                        gamen.move_or_mining(-1,0)
                    if event.key == K_RIGHT or event.key == K_d:
                        gamen.move_or_mining(1,0)
                    if event.key == K_UP or event.key == K_w:
                        gamen.move_or_mining(0,-1)
                    if event.key == K_DOWN or event.key == K_s:
                        gamen.move_or_mining(0,1)
                    # ゲーム終了選択画面（キーボードのみ）
                    if event.key == K_x or event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_ESCAPE:
                        gamen.end_game_select = True
        
        elif gamen is gamen_mine_list[1]:
            if gamen.can_select:
                gamen.can_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_select, gamen.y_n_which, gamen.sell_ore)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # 売却確認画面（マウスのみ）
                    for i in range(len(settings.ore_list)):
                        for j in range(4):
                            if gamen.sell_button[i][j].collidepoint(event_pos):
                                if j != 3 and settings.ore_possession_list[i] >= 10**j:
                                        gamen.can_select = True
                                        gamen.sell_ore_num, gamen.sell_quantity = i, j
                                elif j == 3 and settings.ore_possession_list[i] >= 1:
                                        gamen.can_select = True
                                        gamen.sell_ore_num, gamen.sell_quantity = i, j
                                else:
                                    # Xマークの表示（マウスのみ）
                                    cannot_start_time["sell"] = pygame.time.get_ticks()
                                    gamen.is_cannot = True
                                    gamen.cannot_ore_num, gamen.cannot_quantity = i, j
                    # 下部ボタンによる画面移動（マウスのみ）
                    gamen, move_num = bottom_button_move(gamen, event_pos, 1, gamen_mine_list, gamen_savedata, gamen_base)
                    if move_num is not None:
                        gamen_base.change_page(move_num)
                # stage画面に戻る（キーボードのみ）
                elif event.type == KEYDOWN:
                    gamen = back_stage(gamen)
            
        elif gamen is gamen_mine_list[2]:
            if gamen.can_select:
                gamen.can_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_select, gamen.y_n_which, gamen.flower_levelup)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # レベルアップ確認画面（マウス）
                    if gamen.button_levelup.collidepoint(event_pos):
                        if settings.money >= int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level):
                            gamen.can_select = True
                        else:
                            # Xマークの表示（マウスのみ）
                            cannot_start_time["flower"] = pygame.time.get_ticks()
                            gamen.is_cannot = True
                    # 下部ボタンによる画面移動（マウスのみ）
                    gamen, move_num = bottom_button_move(gamen, event_pos, 2, gamen_mine_list, gamen_savedata, gamen_base)
                    if move_num is not None:
                        gamen_base.change_page(move_num)
                elif event.type == KEYDOWN:
                    # レベルアップ確認画面（キーボード）
                    if event.key == K_z or event.key == K_SPACE or event.key == K_RETURN:
                        if settings.money >= int(settings.flower_levelup_money_zero * settings.flower_levelup_money_ratio**settings.lucky_flower_level):
                            gamen.can_select = True
                    # stage画面に戻る（キーボードのみ）
                    gamen = back_stage(gamen)
            
        elif gamen is gamen_mine_list[3]:
            if gamen.can_cast_select:
                gamen.can_cast_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_cast_select, gamen.y_n_which, gamen.cast_pickaxe)
            elif gamen.can_training_select:
                gamen.can_training_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_training_select, gamen.y_n_which, gamen.training_pickaxe)
            elif gamen.can_set_select:
                gamen.can_set_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_set_select, gamen.y_n_which, gamen.set_pickaxe)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if gamen.scroll_screen.collidepoint(event_pos):
                        for i in range(len(settings.pickaxe_type)):
                            # 鋳造確認画面（マウスのみ）
                            if gamen.cast_button[i].collidepoint(event_pos):
                                gamen.can_cast_select = True
                                # ×マーク表示（マウスのみ）
                                for ore_id, quantity in settings.materials_require[i]:
                                    if settings.ore_possession_list[ore_id] < quantity:
                                        cannot_start_time["cast"] = pygame.time.get_ticks()
                                        gamen.is_cannot_cast = True
                                        gamen.cannot_cast_type = i
                                        gamen.can_cast_select = False
                                if gamen.can_cast_select:
                                    gamen.cast_type = i
                            else:
                                for j in range(len(settings.pickaxe_level[i])):
                                    # 鍛錬確認画面（マウスのみ）
                                    if gamen.training_button[i][j].collidepoint(event_pos):
                                        if 0 in (settings.pickaxe_level[i][:j] + settings.pickaxe_level[i][(j+1):]):
                                            gamen.can_training_select = True
                                            gamen.training_type, gamen.training_num = i, j
                                        else:
                                            # Xマーク表示（マウスのみ）
                                            cannot_start_time["training"] = pygame.time.get_ticks()
                                            gamen.is_cannot_training = True
                                            gamen.cannot_training_type, gamen.cannot_training_num = i, j
                                    # 装備確認画面（マウスのみ）
                                    if gamen.set_button[i][j] != None and gamen.set_button[i][j].collidepoint(event_pos):
                                        gamen.can_set_select = True
                                        gamen.set_type, gamen.set_num = i, j
                                        break
                    # スクロールバーを掴む（マウスのみ）
                    grab_scrollbar(gamen, event_pos)
                    # 下部ボタンによる画面移動（マウスのみ）
                    gamen, move_num = bottom_button_move(gamen, event_pos, 3, gamen_mine_list, gamen_savedata, gamen_base)
                    if move_num is not None:
                        gamen_base.change_page(move_num)
                # stage画面に戻る（キーボードのみ）
                elif event.type == KEYDOWN:
                    gamen = back_stage(gamen)
                else:
                    # 掴んだスクロールバーを動かす
                    gamen.camera_y = move_scrollbar(gamen, event, event_pos, gamen.camera_y, is_pickaxe=True)
                    # 掴んだスクロールバーを離す
                    release_scrollbar(gamen, event)
                    # ツルハシ画面のマウスホイール
                    mousewheel_scroll(gamen, event, mouse, is_pickaxe=True)
            
        elif gamen is gamen_mine_list[4]:
            if gamen.can_employ_select:
                gamen.can_employ_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_employ_select, gamen.y_n_which, gamen.new_character_employ)
            elif gamen.can_levelup_select:
                gamen.can_levelup_select, gamen.y_n_which, _ = y_n_window(event, gamen.y_n_button, event_pos, gamen.can_levelup_select, gamen.y_n_which, gamen.character_levelup)
            elif gamen.change_pickaxe_select:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # ツルハシ選択（マウス）
                    if gamen.scroll_screen.collidepoint(event_pos):
                        for i in range(len(gamen.pickaxes_button)):
                            if gamen.pickaxes_button_can_push[i] and gamen.pickaxes_button[i].collidepoint(event_pos):
                                gamen.pickaxes_which = i
                                gamen.change_pickaxe()
                                gamen.change_pickaxe_select = False
                                gamen.pickaxes_which = None
                    # 雇用画面に戻る（マウス）
                    if gamen.back_button.collidepoint(event_pos):
                        gamen.change_pickaxe_select = False
                        gamen.pickaxes_which = None
                    # スクロールバーを掴む（マウスのみ）
                    grab_scrollbar(gamen, event_pos)
                elif event.type == KEYDOWN:
                    # ツルハシ選択（キーボード）
                    if gamen.pickaxes_which != None and gamen.pickaxes_button_can_push[gamen.pickaxes_which] and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
                        gamen.change_pickaxe()
                        gamen.change_pickaxe_select = False
                        gamen.pickaxes_which = None
                    # 雇用画面に戻る（キーボード）
                    elif event.key == K_x or event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_ESCAPE:
                        gamen.change_pickaxe_select = False
                        gamen.pickaxes_which = None
                    else:
                        # ボタン選択（キーボードのみ）
                        if gamen.pickaxes_which == None:
                            if event.key == K_w or event.key == K_UP or event.key == K_s or event.key == K_DOWN:
                                gamen.pickaxes_which = 0
                                while True:
                                    if gamen.pickaxes_button_can_push[gamen.pickaxes_which]:
                                        break
                                    if gamen.pickaxes_which == len(gamen.pickaxes_button) - 1:
                                        gamen.pickaxes_which = 0
                                        break
                                    gamen.pickaxes_which += 1
                        if gamen.pickaxes_which != None:
                            if event.key == K_w or event.key == K_UP:
                                while True:
                                    if gamen.pickaxes_which != 0:
                                        gamen.pickaxes_which -= 1
                                    elif gamen.pickaxes_which == 0:
                                        gamen.pickaxes_which = len(gamen.pickaxes_button) - 1
                                    if gamen.pickaxes_button_can_push[gamen.pickaxes_which]:
                                        break
                            elif event.key == K_s or event.key == K_DOWN:
                                while True:
                                    if gamen.pickaxes_which != len(gamen.pickaxes_button) - 1:
                                        gamen.pickaxes_which += 1
                                    elif gamen.pickaxes_which == len(gamen.pickaxes_button) - 1:
                                        gamen.pickaxes_which = 0
                                    if gamen.pickaxes_button_can_push[gamen.pickaxes_which]:
                                        break
                            # 選択しているボタンが画面外にある時に映るようにする
                            if (gamen.pickaxes_which+1) * gamen.change_pickaxes_size - gamen.pickaxe_camera_y > gamen.scroll_screen.bottom - gamen.scroll_screen.top:
                                gamen.pickaxe_camera_y = (gamen.pickaxes_which+1) * gamen.change_pickaxes_size - (gamen.scroll_screen.bottom - gamen.scroll_screen.top)
                            elif gamen.pickaxes_which * gamen.change_pickaxes_size - gamen.pickaxe_camera_y < 0:
                                gamen.pickaxe_camera_y = gamen.pickaxes_which * gamen.change_pickaxes_size
                else:
                    # 掴んだスクロールバーを動かす
                    gamen.pickaxe_camera_y = move_scrollbar(gamen, event, event_pos, gamen.pickaxe_camera_y)
                    # 掴んだスクロールバーを離す
                    release_scrollbar(gamen, event)
                    # ツルハシ画面のマウスホイール
                    mousewheel_scroll(gamen, event, mouse)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # 採用選択画面（マウスのみ）
                    if gamen.new_character_button != None and gamen.new_character_button.collidepoint(event_pos):
                        if settings.money >= settings.employ_money_zero * settings.employ_money_ratio**len(settings.character_speed):
                            gamen.can_employ_select = True
                        else:
                            cannot_start_time["employ"] = pygame.time.get_ticks()
                            gamen.is_cannot_employ = True
                    # ツルハシ選択画面（マウスのみ）
                    for i in range(len(gamen.change_pickaxe_button)):
                        if gamen.change_pickaxe_button[i].collidepoint(event_pos):
                            gamen.change_pickaxe_select = True
                            gamen.change_pickaxe_character_num = i + gamen.what_character_num
                    # 昇給選択画面（マウスのみ）
                    for i in range(len(gamen.character_levelup_button)):
                        if gamen.character_levelup_button[i].collidepoint(event_pos):
                            if settings.money >= int(settings.employ_money_zero * settings.employ_money_ratio**(i+gamen.what_character_num) * settings.raise_money_ratio(i+gamen.what_character_num)**(settings.character_speed[i+gamen.what_character_num])):
                                gamen.can_levelup_select = True
                                gamen.character_levelup_num = i + gamen.what_character_num
                            else:
                                cannot_start_time["levelup"] = pygame.time.get_ticks()
                                gamen.is_cannot_levelup = True
                                gamen.cannot_levelup_num = i
                    # 雇用画面の移動（マウス）
                    if gamen.what_character_num > 0 and gamen.arrow_button[0].collidepoint(event_pos):
                        gamen.what_character_num -= 1
                        gamen.update_page()
                    elif len(settings.character_speed) >= 3 and gamen.what_character_num <= len(settings.character_speed) - 3 and gamen.arrow_button[1].collidepoint(event_pos):
                        gamen.what_character_num += 1
                        gamen.update_page()
                    # 下部ボタンによる画面移動（マウスのみ）
                    gamen, move_num = bottom_button_move(gamen, event_pos, 4, gamen_mine_list, gamen_savedata, gamen_base)
                    if move_num is not None:
                        gamen_base.change_page(move_num)
                elif event.type == KEYDOWN:
                    # 雇用画面の移動（キーボード）
                    if gamen.what_character_num > 0 and (event.key == K_a or event.key == K_LEFT):
                        gamen.what_character_num -= 1
                        gamen.update_page()
                    elif len(settings.character_speed) >= 3 and gamen.what_character_num <= len(settings.character_speed) - 3 and (event.key == K_d or event.key == K_RIGHT):
                        gamen.what_character_num += 1
                        gamen.update_page()
                    # stage画面に戻る（キーボードのみ）
                    gamen = back_stage(gamen)
        
        elif gamen is gamen_mine_list[5]:
            if gamen.reinc_select:
                gamen.reinc_select, gamen.y_n_which, gamen = y_n_window(event, gamen.y_n_button, event_pos, gamen.reinc_select, gamen.y_n_which, gamen.reinc_change, mine_list=gamen_mine_list, n_gamen=gamen)
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # 転生選択画面（マウス）
                    for i in range(4):
                        if gamen.reinc_button[i].collidepoint(event_pos):
                            gamen.reinc_num = i
                            if settings.have_exp >= 1:
                                gamen.reinc_select = True
                            else:
                                cannot_start_time["reinc"] = pygame.time.get_ticks()
                                gamen.is_cannot = True
                    # 下部ボタンによる画面移動（マウスのみ）
                    gamen, move_num = bottom_button_move(gamen, event_pos, 5, gamen_mine_list, gamen_savedata, gamen_base)
                    if move_num is not None:
                        gamen_base.change_page(move_num)
                elif event.type == KEYDOWN:
                    # 転生選択画面（キーボード）
                    if gamen.reinc_button_which != None and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN):
                        gamen.reinc_num = gamen.reinc_button_which
                        gamen.reinc_button_which = None
                        gamen.reinc_select = True
                    # ボタン選択（キーボードのみ）
                    else:
                        gamen.reinc_button_which = two_times_two_keyboard(event, gamen.reinc_button_which)
                    # stage画面に戻る（キーボードのみ）
                    gamen = back_stage(gamen)
            
        elif gamen is gamen_mine_list[6]:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # 実績達成（マウスのみ）
                if gamen.scroll_screen.collidepoint(event_pos):
                    for i in range(len(settings.record_list)):
                        if gamen.record_rect[i].collidepoint(event_pos):
                            if settings.record_list[i] >= settings.record_terms_num[i][settings.record_completes[i]]:
                                gamen.get_reward(i)
                            else:
                                cannot_start_time["reward"] = pygame.time.get_ticks()
                                gamen.is_cannot = True
                                gamen.cannot_num = i
                # スクロールバーを掴む（マウスのみ）
                grab_scrollbar(gamen, event_pos)
                # 下部ボタンによる画面移動（マウスのみ）
                gamen, move_num = bottom_button_move(gamen, event_pos, 6, gamen_mine_list, gamen_savedata, gamen_base)
                if move_num is not None:
                    gamen_base.change_page(move_num)
            elif event.type == KEYDOWN:
                # stage画面に戻る（キーボードのみ）
                gamen = back_stage(gamen)
            else:
                # 掴んだスクロールバーを動かす
                gamen.camera_y = move_scrollbar(gamen, event, event_pos, gamen.camera_y, is_record=True)
                # 掴んだスクロールバーを離す
                release_scrollbar(gamen, event)
                # ツルハシ画面のマウスホイール
                mousewheel_scroll(gamen, event, mouse, is_record=True)
    
    # マウスが合っている場合に色を変える
    if isinstance(gamen, title.Main):
        update_hover_colors(gamen.button, mouse, GRAY, DARK_GRAY, gamen.button_color)
        gamen.which = delete_which(gamen.button, mouse, gamen.which, skip_num=2)
        update_which_color(gamen.which, gamen.button_color, DARK_GRAY)
    
    elif gamen is gamen_savedata:
        if not gamen.can_select:
            update_hover_colors(gamen.save_button, mouse, ASH, DARK_GRAY, gamen.save_button_color)
            gamen.back_color = update_hover_color(gamen.back_button, mouse, ASH, DARK_GRAY)
            gamen.savedata_which = delete_which(gamen.save_button, mouse, gamen.savedata_which)
            update_which_color(gamen.savedata_which, gamen.save_button_color, DARK_GRAY)

    elif gamen is gamen_mine_list[0]:
        if not gamen.next_stage_select and not gamen.end_game_select:
            update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=0)
            
            # 鉱夫の移動
            for i in range(len(settings.character_speed)):
                if settings.character_move_time[i] == None:
                    settings.character_move_time[i] = 0
                else:
                    settings.character_move_time[i] += settings.character_speed[i]
                    if settings.character_move_time[i] >= 100: # 移動間隔
                        gamen.character_move_or_mining(i)
                        settings.character_move_time[i] -= 100
                
        # 鉱山の画面移動
        if tracking == True:
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                gamen.update_cursor("after", mouse)
                gamen.update_camera("update")
            else:
                gamen.update_cursor("before", (0,0))
                gamen.update_cursor("after", (0,0))
                gamen.update_camera("save")
                tracking = False

    elif gamen is gamen_mine_list[1]:
        if not gamen.can_select:
            update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=1)
            update_hover_colorss(gamen.sell_button, mouse, GRAY, DARK_GRAY, gamen.sell_button_color)
    
    elif gamen is gamen_mine_list[2]:
        if not gamen.can_select:
            update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=2)
            gamen.button_levelup_color = update_hover_color(gamen.button_levelup, mouse, GRAY, DARK_GRAY)
    
    elif gamen is gamen_mine_list[3]:
        if not gamen.can_cast_select and not gamen.can_training_select and not gamen.can_set_select:
            update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=3)
            update_hover_colors(gamen.cast_button, mouse, GRAY, DARK_GRAY, gamen.cast_button_color, gamen.scroll_screen)
            update_hover_colorss(gamen.training_button, mouse, GRAY, DARK_GRAY, gamen.training_button_color, gamen.scroll_screen)
            update_hover_colorss(gamen.set_button, mouse, GRAY, DARK_GRAY, gamen.set_button_color, gamen.scroll_screen)
    
    elif gamen is gamen_mine_list[4]:
        if not gamen.can_employ_select and not gamen.can_levelup_select and not gamen.change_pickaxe_select:
            update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=4)
            if gamen.new_character_button is not None:
                gamen.new_character_color = update_hover_color(gamen.new_character_button, mouse, GRAY, DARK_GRAY)
            update_hover_colors(gamen.change_pickaxe_button, mouse, GRAY, DARK_GRAY, gamen.change_pickaxe_button_color)
            update_hover_colors(gamen.character_levelup_button, mouse, GRAY, DARK_GRAY, gamen.character_levelup_button_color)    
            update_hover_colors(gamen.arrow_button, mouse, GRAY, DARK_GRAY, gamen.arrow_color)
        
        elif gamen.change_pickaxe_select:
            gamen.update_pickaxes_page()
            gamen.back_button_color = update_hover_color(gamen.back_button, mouse, GRAY, DARK_GRAY)
            update_hover_colors(gamen.pickaxes_button, mouse, GRAY, DARK_GRAY, gamen.pickaxes_button_color, gamen.scroll_screen, can_push=gamen.pickaxes_button_can_push)
            gamen.pickaxes_which = delete_which(gamen.pickaxes_button, mouse, gamen.pickaxes_which)
            update_which_color(gamen.pickaxes_which, gamen.pickaxes_button_color, DARK_GRAY)
        
    elif gamen is gamen_mine_list[5]:
        if not gamen.reinc_select:
            update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=5)
            update_hover_colors(gamen.reinc_button, mouse, GRAY, DARK_GRAY, gamen.reinc_button_color)
            gamen.reinc_button_which = delete_which(gamen.reinc_button, mouse, gamen.reinc_button_which)
            update_which_color(gamen.reinc_button_which, gamen.reinc_button_color, DARK_GRAY)
    
    elif gamen is gamen_mine_list[6]:
        update_hover_colors(gamen_base.button, mouse, GRAY, DARK_GRAY, gamen_base.button_color, skip_num=6)
        update_hover_colors(gamen.record_rect, mouse, PURPLE, DARK_PURPLE, gamen.record_color, gamen.scroll_screen)
        
    # 基本画面描画
    gamen.draw(canvas)
    if gamen in gamen_mine_list:
        gamen_base.update_page()
        gamen_base.draw_base(canvas)
    
    # はいいいえの選択をする画面かどうか
    is_y_n = True
    # セーブorロード選択画面
    if gamen is gamen_savedata and gamen.can_select:
        gamen.save_or_load_select_draw(canvas)
    elif gamen is gamen_mine_list[0]:
        # ゲーム終了選択画面
        if gamen.end_game_select:
            gamen.select_draw(canvas, "end_game")
        # 次のステージへの選択画面
        elif gamen.player_rect.colliderect(gamen.next_stage_rect):
            gamen.next_stage_select = True
            gamen.select_draw(canvas, "next_stage")
    # 売却選択画面
    elif gamen is gamen_mine_list[1] and gamen.can_select:
        gamen.sell_select_draw(canvas)
    # 幸運の花レベルアップ選択画面
    elif gamen is gamen_mine_list[2] and gamen.can_select:
        gamen.levelup_select_draw(canvas)
    elif gamen is gamen_mine_list[3]:
        # 鋳造選択画面
        if gamen.can_cast_select:
            gamen.select_draw(canvas, "cast")
        # 修練選択画面
        elif gamen.can_training_select:
            gamen.select_draw(canvas, "training")
        # 設定選択画面
        elif gamen.can_set_select:
            gamen.select_draw(canvas, "set")
    elif gamen is gamen_mine_list[4]:
        # 雇用選択画面
        if gamen.can_employ_select:
            gamen.select_draw(canvas, "employ")
        # 鉱夫レベルアップ選択画面
        elif gamen.can_levelup_select:
            gamen.select_draw(canvas, "levelup")
    # 転生選択画面
    elif gamen is gamen_mine_list[5] and gamen.reinc_select:
        gamen.reinc_select_draw(canvas)
    else:
        is_y_n = False
    if is_y_n:
        update_hover_colors(gamen.y_n_button, mouse, GRAY, DARK_GRAY, gamen.y_n_color)
        gamen.y_n_which = delete_which(gamen.y_n_button, mouse, gamen.y_n_which)
        update_which_color(gamen.y_n_which, gamen.y_n_color, DARK_GRAY)
    
    # 装備変更画面
    if gamen is gamen_mine_list[4] and gamen.change_pickaxe_select:
        gamen.change_pickaxe_select_draw(canvas)
    
    # 売却不可能時の×マークの描画
    if gamen is gamen_mine_list[1]:
        gamen.is_cannot, cannot_start_time["sell"] = draw_cannot(gamen.is_cannot, cannot_start_time.get("sell", 0), gamen.cannot_sell_draw, canvas)
    # 幸運の花レベルアップ不可能時の×マークの描画
    elif gamen is gamen_mine_list[2]:
        gamen.is_cannot, cannot_start_time["flower"] = draw_cannot(gamen.is_cannot, cannot_start_time.get("flower", 0), gamen.cannot_levelup_draw, canvas)
    elif gamen is gamen_mine_list[3]:
        # 鋳造不可能時の×マークの描画
        gamen.is_cannot_cast, cannot_start_time["cast"] = draw_cannot(gamen.is_cannot_cast, cannot_start_time.get("cast", 0), gamen.cannot_cast_draw, canvas)
        # 鍛錬不可能時の×マークの描画
        gamen.is_cannot_training, cannot_start_time["training"] = draw_cannot(gamen.is_cannot_training, cannot_start_time.get("training", 0), gamen.cannot_training_draw, canvas)
    elif gamen is gamen_mine_list[4]:
        # 採用不可能時の×マークの描画
        gamen.is_cannot_employ, cannot_start_time["employ"] = draw_cannot(gamen.is_cannot_employ, cannot_start_time.get("employ", 0), gamen.cannot_employ_draw, canvas)
        # 昇給不可能時の×マークの描画
        gamen.is_cannot_levelup, cannot_start_time["levelup"] = draw_cannot(gamen.is_cannot_levelup, cannot_start_time.get("levelup", 0), gamen.cannot_levelup_draw, canvas)
    # 転生不可能時の×マークの描画
    elif gamen is gamen_mine_list[5]:
        gamen.is_cannot, cannot_start_time["reinc"] = draw_cannot(gamen.is_cannot, cannot_start_time.get("reinc", 0), gamen.cannot_reinc_draw, canvas)
    # 実績未達時のxマークの描画
    elif gamen is gamen_mine_list[6]:
        gamen.is_cannot, cannot_start_time["reward"] = draw_cannot(gamen.is_cannot, cannot_start_time.get("reward", 0), gamen.cannot_reward_draw, canvas)

    scaled = pygame.transform.smoothscale(canvas, (real_w, real_h))
    screen.blit(scaled, (0,0))
    pygame.display.update()
    fpsClock.tick(fps)

pygame.quit()
sys.exit()