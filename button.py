import pygame


class Button():
    """游戏中的所有按钮"""
    def __init__(self, ai_settings):
        """初始化"""
        # 暂停、恢复按钮
        self.pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
        self.pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
        self.resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
        self.resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
        self.paused_rect = self.pause_nor_image.get_rect()
        self.paused_rect.left, self.paused_rect.top = ai_settings.bg_width - self.paused_rect.width - 10, 10
        self.paused_image = self.pause_nor_image
        # 全屏炸弹
        self.bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
        self.bomb_rect = self.bomb_image.get_rect()
        # 生命数量
        self.life_image = pygame.image.load("images/life.png").convert_alpha()
        self.life_rect = self.life_image.get_rect()
        # 游戏结束画面
        self.again_image = pygame.image.load("images/again.png").convert_alpha()
        self.again_rect = self.again_image.get_rect()
        self.gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
        self.gameover_rect = self.gameover_image.get_rect()