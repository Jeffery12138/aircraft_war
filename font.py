import pygame


class Font():
    """游戏字体类"""
    def __init__(self):
        """初始化"""
        # 分数字体
        self.score_font = pygame.font.Font("font/font.ttf", 36)
        # 炸弹字体
        self.bomb_font = pygame.font.Font("font/font.ttf", 48)
        # GameOver字体
        self.gameover_font = pygame.font.Font("font/font.ttf", 48)