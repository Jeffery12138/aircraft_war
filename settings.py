import pygame


class Settings():
    """游戏的所有设置类"""
    def __init__(self):
        """初始化"""
        # 背景设置
        self.bg_width = 480
        self.bg_height = 700
        # 颜色设置
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)

        # 子弹设置
        # 标志是否使用超级子弹
        self.is_double_bullet = False
        # 普通子弹设置
        self.bullet1_index = 0
        self.BULLET1_NUM = 4
        # 超级子弹设置
        self.bullet2_index = 0
        self.BULLET2_NUM = 8

        # 标志是否已经记录最高得分
        self.recorded = False
        # 用于延迟
        self.delay = 100
        # 用于切换图片
        self.switch_image = True
        # 中弹图片索引
        self.e1_destroy_index = 0
        self.e2_destroy_index = 0
        self.e3_destroy_index = 0
        self.me_destroy_index = 0