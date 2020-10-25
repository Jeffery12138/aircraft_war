import pygame
import traceback
from pygame.sprite import Group


import myplane
import supply
from sound import Sound
from settings import Settings
from timer import Timer
import game_functions as gf
from stats import Stats
from button import Button
from font import Font


def main():
    pygame.init()
    pygame.mixer.init()

    # 创建设置实例
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.bg_width, ai_settings.bg_height))
    background = pygame.image.load("images/background.png").convert()
    pygame.display.set_caption("飞机大战 -- 代码重构版")

    # 创建音乐、音效实例
    sound = Sound()
    pygame.mixer.music.play(-1)

    # 创建游戏状态实例
    stats = Stats(ai_settings)
    # 创建计时器实例
    timer = Timer()
    # 创建button实例
    button = Button(ai_settings)
    # 创建字体实例
    font = Font()

    # 生成我方飞机
    me = myplane.MyPlane(ai_settings)
    # 生成地方飞机
    enemies = Group()
    small_enemies = Group()
    mid_enemies = Group()
    big_enemies = Group()
    gf.add_enemies(ai_settings, small_enemies, mid_enemies, big_enemies, enemies)

    # 生成子弹
    bullet1 = []
    bullet2 = []
    gf.create_bullets(ai_settings, me, bullet1, bullet2)

    clock = pygame.time.Clock()

    # 每30秒发放一个补给包
    bullet_supply = supply.BulletSupply(ai_settings)
    bomb_supply = supply.BombSupply(ai_settings)
    pygame.time.set_timer(timer.SUPPLY_TIME, 30 * 1000)

    running = True
    while running:
        # 响应鼠标和键盘事件
        gf.check_events(ai_settings, me, stats, bomb_supply, bullet_supply, sound, timer, button, enemies)
        # 根据用户的得分增加难度
        gf.level_up(ai_settings, stats, sound, small_enemies, mid_enemies, big_enemies, enemies)

        # 背景图像先绘制，防止通过暂停作弊
        screen.blit(background, (0, 0))
        if me.life_num:
            # 绘制暂停按钮
            screen.blit(button.paused_image, button.paused_rect)
        if me.life_num and not stats.paused:
            # 控制飞机
            gf.control_plane(me)
            # 绘制全屏炸弹补给并检测是否获得
            gf.check_bomb_supply(screen, sound, me, bomb_supply)
            # 绘制超级子弹补给并检测是否获得
            gf.check_bullet_supply(ai_settings, screen, sound, me, timer, bullet_supply)
            # 发射子弹
            if not (ai_settings.delay % 10):
                bullets = gf.fire_bullets(ai_settings, sound, me, bullet1, bullet2)
            # 检测子弹是否击中敌机
            gf.check_hit_enemies(screen, bullets, mid_enemies, big_enemies, enemies)
            # 绘制敌机
            gf.create_enemies(ai_settings, screen, sound, stats, big_enemies, mid_enemies, small_enemies)
            # 绘制我方飞机
            gf.create_my_plane(ai_settings, screen, sound, me, timer)
            # 检测我方飞机是否被撞
            gf.check_my_plane_hit(me, enemies)
            # 更新游戏界面
            gf.update_play_screen(ai_settings, screen, font, button, stats, me, bomb_supply)
        # 绘制游戏结束画面
        elif me.life_num == 0:
            gf.update_end_screen(ai_settings, screen, font, button, stats, timer, main)

        # 切换我方飞机图片
        gf.switch_image(ai_settings)
        gf.change_delay(ai_settings)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    else:
        traceback.print_exc()
        pygame.quit()
        input()