import pygame
import sys
from random import choice
from pygame.locals import *

import enemy
import bullet


def add_small_enemies(group1, group2, num, ai_settings):
    for i in range(num):
        e1 = enemy.SmallEnemy(ai_settings)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num, ai_settings):
    for i in range(num):
        e2 = enemy.MidEnemy(ai_settings)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num, ai_settings):
    for i in range(num):
        e3 = enemy.BigEnemy(ai_settings)
        group1.add(e3)
        group2.add(e3)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def add_enemies(ai_settings, small_enemies, mid_enemies, big_enemies, enemies):
    """生成敌方飞机，并加入编组"""
    # 生成敌方小型飞机
    add_small_enemies(small_enemies, enemies, 15, ai_settings)
    # 生成敌方中型飞机
    add_mid_enemies(mid_enemies, enemies, 4, ai_settings)
    # 生成敌方大型飞机
    add_big_enemies(big_enemies, enemies, 2, ai_settings)


def check_mouse_button_down_events(event, stats, timer, button):
    """响应按键事件"""
    if event.button == 1 and button.paused_rect.collidepoint(event.pos):
        stats.paused = not stats.paused
        if stats.paused:
            pygame.time.set_timer(timer.SUPPLY_TIME, 0)
            pygame.mixer.music.pause()
            pygame.mixer.pause()
        else:
            pygame.time.set_timer(timer.SUPPLY_TIME, 30 * 1000)
            pygame.mixer.music.unpause()
            pygame.mixer.unpause()


def check_mouse_motion_events(event, stats, button):
    """响应鼠标滑过事件"""
    if button.paused_rect.collidepoint(event.pos):
        if stats.paused:
            button.paused_image = button.resume_pressed_image
        else:
            button.paused_image = button.pause_pressed_image
    else:
        if stats.paused:
            button.paused_image = button.resume_nor_image
        else:
            button.paused_image = button.pause_nor_image


def check_key_down_events(event, bomb_supply, game_sound, enemies):
    """检查按键事件"""
    # 按空格键发射全屏炸弹
    if event.key == pygame.K_SPACE:
        if bomb_supply.bomb_num:
            bomb_supply.bomb_num -= 1
            game_sound.bomb_sound.play()
            for each in enemies:
                if each.rect.bottom > 0:
                    each.active = False
    # 按'q'退出游戏
    if event.key == pygame.K_q:
        pygame.quit()
        sys.exit()


def control_plane(me):
    """控制飞机"""
    # 检测用户的键盘操作
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w] or key_pressed[K_UP]:
        me.move_up()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        me.move_down()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        me.move_left()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        me.move_right()


def check_supply_events(game_sound, bomb_supply, bullet_supply):
    """检查补给事件"""
    game_sound.supply_sound.play()
    if choice([True, False]):
        bomb_supply.reset()
    else:
        bullet_supply.reset()


def check_events(ai_settings, me, stats, bomb_supply, bullet_supply, game_sound, timer, button, enemies):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_button_down_events(event, stats, timer, button)
        elif event.type == pygame.MOUSEMOTION:
            check_mouse_motion_events(event, stats, button)
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, bomb_supply, game_sound, enemies)
        elif event.type == timer.SUPPLY_TIME:
            check_supply_events(game_sound, bomb_supply, bullet_supply)
        elif event.type == timer.DOUBLE_BULLET_TIME:
            ai_settings.is_double_bullet = False
            pygame.time.set_timer(timer.DOUBLE_BULLET_TIME, 0)
        elif event.type == timer.INVINCIBLE_TIME:
            me.invincible = False
            pygame.time.set_timer(timer.INVINCIBLE_TIME, 0)


def record_score(ai_settings, stats):
    """存档最高得分"""
    # 如果没有存档过
    if not ai_settings.recorded:
        # 且玩家得分高于历史最高得分，则存档
        if stats.score > stats.record_score:
            with open("record.txt", "w") as f:
                f.write(str(stats.score))
    ai_settings.recorded = not ai_settings.recorded


def draw_game_over_surface(ai_settings, screen, font, stats, button):
    # 绘制结束界面
    record_score_text = font.score_font.render("Best : %d" % stats.record_score, True, ai_settings.WHITE)
    screen.blit(record_score_text, (50, 50))

    gameover_text1 = font.gameover_font.render("Your Score", True, ai_settings.WHITE)
    gameover_text1_rect = gameover_text1.get_rect()
    gameover_text1_rect.left = int((ai_settings.bg_width - gameover_text1_rect.width) / 2)
    gameover_text1_rect.top = int(ai_settings.bg_height - 500)
    screen.blit(gameover_text1, gameover_text1_rect)

    gameover_text2 = font.gameover_font.render(str(stats.score), True, ai_settings.WHITE)
    gameover_text2_rect = gameover_text2.get_rect()
    gameover_text2_rect.left = int((ai_settings.bg_width - gameover_text2_rect.width) / 2)
    gameover_text2_rect.top = gameover_text1_rect.bottom + 10
    screen.blit(gameover_text2, gameover_text2_rect)

    button.again_rect.left = int((ai_settings.bg_width - button.again_rect.width) / 2)
    button.again_rect.top = gameover_text2_rect.bottom + 50
    screen.blit(button.again_image, button.again_rect)

    button.gameover_rect.left = int((ai_settings.bg_width - button.again_rect.width) / 2)
    button.gameover_rect.top = button.again_rect.bottom + 10
    screen.blit(button.gameover_image, button.gameover_rect)


def start_upgrade(ai_settings, sound, small_enemies, mid_enemies, big_enemies, enemies):
    """玩家等级1升2"""
    sound.upgrade_sound.play()
    # 增加3架小型敌机、2架中型敌机和1架大型敌机
    add_small_enemies(small_enemies, enemies, 3, ai_settings)
    add_mid_enemies(mid_enemies, enemies, 2, ai_settings)
    add_big_enemies(big_enemies, enemies, 1, ai_settings)
    # 提升小型敌机的速度
    inc_speed(small_enemies, 1)


def continue_upgrade(ai_settings, sound, small_enemies, mid_enemies, big_enemies, enemies):
    """玩家等级2升3、3升4、4升5"""
    sound.upgrade_sound.play()
    # 增加3架小型敌机、2架中型敌机和1架大型敌机
    add_small_enemies(small_enemies, enemies, 5, ai_settings)
    add_mid_enemies(mid_enemies, enemies, 3, ai_settings)
    add_big_enemies(big_enemies, enemies, 2, ai_settings)
    # 提升小型敌机的速度
    inc_speed(small_enemies, 1)
    inc_speed(mid_enemies, 1)


def level_up(ai_settings, stats, sound, small_enemies, mid_enemies, big_enemies, enemies):
    """根据用户的得分增加难度"""
    if stats.level == 1 and stats.score > 50000:
        stats.level += 1
        start_upgrade(ai_settings, sound, small_enemies, mid_enemies, big_enemies, enemies)
    elif stats.level == 2 and stats.score > 300000:
        stats.level += 1
        continue_upgrade(ai_settings, sound, small_enemies, mid_enemies, big_enemies, enemies)
    elif stats.level == 3 and stats.score > 600000:
        stats.level += 1
        continue_upgrade(ai_settings, sound, small_enemies, mid_enemies, big_enemies, enemies)
    elif stats.level == 4 and stats.score > 1000000:
        stats.level += 1
        continue_upgrade(ai_settings, sound, small_enemies, mid_enemies, big_enemies, enemies)


def check_bomb_supply(screen, sound, me, bomb_supply):
    """绘制全屏炸弹补给并检测是否获得"""
    if bomb_supply.active:
        bomb_supply.move()
        screen.blit(bomb_supply.image, bomb_supply.rect)
        if pygame.sprite.collide_mask(bomb_supply, me):
            sound.get_bomb_sound.play()
            if bomb_supply.bomb_num < 3:
                bomb_supply.bomb_num += 1
            bomb_supply.active = False


def check_bullet_supply(ai_settings, screen, sound, me, timer, bullet_supply):
    """绘制超级子弹补给并检测是否获得"""
    if bullet_supply.active:
        bullet_supply.move()
        screen.blit(bullet_supply.image, bullet_supply.rect)
        if pygame.sprite.collide_mask(bullet_supply, me):
            sound.get_bullet_sound.play()
            ai_settings.is_double_bullet = True
            pygame.time.set_timer(timer.DOUBLE_BULLET_TIME, 18 * 1000)
            bullet_supply.active = False


def check_hit_enemies(screen, bullets, mid_enemies, big_enemies, enemies):
    """检测子弹是否击中敌机"""
    for b in bullets:
        if b.active:
            b.move()
            screen.blit(b.image, b.rect)
            enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
            if enemy_hit:
                b.active = False
                for e in enemy_hit:
                    if e in mid_enemies or e in big_enemies:
                        e.hit = True
                        e.energy -= 1
                        if e.energy == 0:
                            e.active = False
                    else:
                        e.active = False


def create_normal_bullets(ai_settings, me, bullet1):
    """生成普通子弹"""
    for i in range(ai_settings.BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))


def create_supply_bullets(ai_settings, me, bullet2):
    """生成超级子弹"""
    for i in range(int(ai_settings.BULLET2_NUM / 2)):
        bullet2.append(bullet.Bullet2(((me.rect.centerx - 33), me.rect.centery)))
        bullet2.append(bullet.Bullet2(((me.rect.centerx + 30), me.rect.centery)))


def create_bullets(ai_settings, me, bullet1, bullet2):
    """生成子弹"""
    create_normal_bullets(ai_settings, me, bullet1)
    create_supply_bullets(ai_settings, me, bullet2)


def fire_bullets(ai_settings, sound, me, bullet1, bullet2):
    """发射子弹"""
    sound.bullet_sound.play()
    if ai_settings.is_double_bullet:
        bullets = bullet2
        bullets[ai_settings.bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
        bullets[ai_settings.bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
        ai_settings.bullet2_index = (ai_settings.bullet2_index + 2) % ai_settings.BULLET2_NUM
    else:
        bullets = bullet1
        bullets[ai_settings.bullet1_index].reset(me.rect.midtop)
        ai_settings.bullet1_index = (ai_settings.bullet1_index + 1) % ai_settings.BULLET1_NUM
    return bullets


def create_big_enemies(ai_settings, screen, sound, stats, big_enemies):
    """绘制大型敌机"""
    for each in big_enemies:
        if each.active:
            each.move()
            if each.hit:
                # 绘制被打到的特效
                screen.blit(each.image_hit, each.rect)
                each.hit = False
            else:
                if ai_settings.switch_image:
                    screen.blit(each.image1, each.rect)
                else:
                    screen.blit(each.image2, each.rect)

            # 绘制血槽
            pygame.draw.line(screen, ai_settings.BLACK, (each.rect.left, each.rect.top - 5),
                             (each.rect.right, each.rect.top - 5), 2)
            # 当生命大于20%显示绿色，否则显示红色
            energy_remain = each.energy / enemy.BigEnemy.energy
            if energy_remain > 0.2:
                energy_color = ai_settings.GREEN
            else:
                energy_color = ai_settings.RED
            pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                             (each.rect.left + int(each.rect.width * energy_remain), each.rect.top - 5), 2)

            # 即将出现在画面中，播放音效
            if each.rect.bottom == -50:
                sound.enemy3_fly_sound.play(-1)
        else:
            # 毁灭
            if not(ai_settings.delay % 3):
                if ai_settings.e3_destroy_index == 0:
                    sound.enemy3_down_sound.play()
                screen.blit(each.destroy_images[ai_settings.e3_destroy_index], each.rect)
                ai_settings.e3_destroy_index = (ai_settings.e3_destroy_index + 1) % 6
                if ai_settings.e3_destroy_index == 0:
                    sound.enemy3_fly_sound.stop()
                    stats.score += 10000
                    each.reset()


def create_mid_enemies(ai_settings, screen, sound, stats, mid_enemies):
    """绘制中型敌机"""
    for each in mid_enemies:
        if each.active:
            each.move()
            if each.hit:
                screen.blit(each.image_hit, each.rect)
                each.hit = False
            else:
                screen.blit(each.image, each.rect)

            # 绘制血槽
            pygame.draw.line(screen, ai_settings.BLACK, (each.rect.left, each.rect.top - 5),
                             (each.rect.right, each.rect.top - 5), 2)
            # 当生命大于20%显示绿色，否则显示红色
            energy_remain = each.energy / enemy.MidEnemy.energy
            if energy_remain > 0.2:
                energy_color = ai_settings.GREEN
            else:
                energy_color = ai_settings.RED
            pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                             (each.rect.left + int(each.rect.width * energy_remain), each.rect.top - 5), 2)

        else:
            # 毁灭
            if not (ai_settings.delay % 3):
                if ai_settings.e3_destroy_index == 0:
                    sound.enemy2_down_sound.play()
                screen.blit(each.destroy_images[ai_settings.e2_destroy_index], each.rect)
                ai_settings.e2_destroy_index = (ai_settings.e2_destroy_index + 1) % 4
                if ai_settings.e3_destroy_index == 0:
                    stats.score += 6000
                    each.reset()


def create_small_enemies(ai_settings, screen, sound, stats, small_enemies):
    """绘制小型敌机"""
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)
        else:
            # 毁灭
            if not (ai_settings.delay % 3):
                if ai_settings.e1_destroy_index == 0:
                    sound.enemy1_down_sound.play()
                screen.blit(each.destroy_images[ai_settings.e1_destroy_index], each.rect)
                ai_settings.e1_destroy_index = (ai_settings.e1_destroy_index + 1) % 4
                if ai_settings.e1_destroy_index == 0:
                    stats.score += 1000
                    each.reset()


def create_enemies(ai_settings, screen, sound, stats, big_enemies, mid_enemies, small_enemies):
    """绘制敌机"""
    # 绘制大型敌机
    create_big_enemies(ai_settings, screen, sound, stats, big_enemies)
    # 绘制中型敌机
    create_mid_enemies(ai_settings, screen, sound, stats, mid_enemies)
    # 绘制小型敌机
    create_small_enemies(ai_settings, screen, sound, stats, small_enemies)


def create_my_plane(ai_settings, screen, sound, me, timer):
    """绘制我方飞机"""
    if me.active:
        if ai_settings.switch_image:
            screen.blit(me.image1, me.rect)
        else:
            screen.blit(me.image2, me.rect)
    else:
        # 毁灭
        if not (ai_settings.delay % 3):
            if ai_settings.me_destroy_index == 0:
                sound.me_down_sound.play()
            screen.blit(me.destroy_images[ai_settings.me_destroy_index], me.rect)
            ai_settings.me_destroy_index = (ai_settings.me_destroy_index + 1) % 4
            if ai_settings.me_destroy_index == 0:
                me.life_num -= 1
                me.reset()
                pygame.time.set_timer(timer.INVINCIBLE_TIME, 3 * 1000)


def check_my_plane_hit(me, enemies):
    """检测我方飞机是否被撞"""
    enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
    if enemies_down and not me.invincible:
        me.active = False
        for e in enemies_down:
            e.active = False


def draw_bomb_left(ai_settings, screen, button, font, bomb_supply):
    """绘制剩余全屏炸弹数量"""
    bomb_text = font.bomb_font.render("× %d" % bomb_supply.bomb_num, True, ai_settings.WHITE)
    text_rect = bomb_text.get_rect()
    screen.blit(button.bomb_image, (10, ai_settings.bg_height - 10 - button.bomb_rect.height))
    screen.blit(bomb_text, (20 + button.bomb_rect.width, ai_settings.bg_height - 5 - text_rect.height))


def draw_my_plane_left(ai_settings, screen, button, me):
    """绘制剩余生命数量"""
    if me.life_num:
        for i in range(me.life_num):
            screen.blit(button.life_image,
                        ((ai_settings.bg_width - 10 - (i + 1) * button.life_rect.width), ai_settings.bg_height - 10 - button.life_rect.height))


def draw_score(ai_settings, screen, font, stats):
    """绘制得分"""
    score_text = font.score_font.render("Score : %s" % str(stats.score), True, ai_settings.WHITE)
    screen.blit(score_text, (10, 5))


def update_play_screen(ai_settings, screen, font, button, stats, me, bomb_supply):
    """更新游戏屏幕"""
    # 绘制剩余全屏炸弹数量
    draw_bomb_left(ai_settings, screen, button, font, bomb_supply)
    # 绘制剩余生命数量
    draw_my_plane_left(ai_settings, screen, button, me)
    # 绘制得分
    draw_score(ai_settings, screen, font, stats)


def check_end_mouse_events(button, main):
    """检测用户的鼠标操作"""
    # 如果用户按下鼠标左键
    if pygame.mouse.get_pressed()[0]:
        # 获取鼠标坐标
        pos = pygame.mouse.get_pos()
        # 如果用户点击“重新开始”
        if button.again_rect.left < pos[0] < button.again_rect.right and \
                button.again_rect.top < pos[1] < button.again_rect.bottom:
            # 调用main函数，重新开始游戏
            main()
        # 如果用户点击“结束游戏”
        elif button.gameover_rect.left < pos[0] < button.gameover_rect.right and \
                button.gameover_rect.top < pos[1] < button.gameover_rect.bottom:
            # 退出游戏
            pygame.quit()
            sys.exit()


def update_end_screen(ai_settings, screen, font, button, stats, timer, main):
    """更新结束屏幕"""
    # 背景音乐停止
    pygame.mixer.music.stop()
    # 停止全部音效
    pygame.mixer.stop()
    # 停止发放补给
    pygame.time.set_timer(timer.SUPPLY_TIME, 0)
    # 记录最高得分
    record_score(ai_settings, stats)
    # 绘制游戏结束界面
    draw_game_over_surface(ai_settings, screen, font, stats, button)
    # 检测用户的鼠标事件
    check_end_mouse_events(button, main)


def switch_image(ai_settings):
    """切换图片"""
    if not (ai_settings.delay % 5):
        ai_settings.switch_image = not ai_settings.switch_image


def change_delay(ai_settings):
    """delay变更"""
    ai_settings.delay -= 1
    if not ai_settings.delay:
        ai_settings.delay = 100

