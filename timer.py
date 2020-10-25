from pygame.locals import *


class Timer():
    """计时器的类"""
    def __init__(self):
        """初始化"""
        self.SUPPLY_TIME = USEREVENT
        # 超级子弹定时器
        self.DOUBLE_BULLET_TIME = USEREVENT + 1
        # 解除我方无敌状态定时器
        self.INVINCIBLE_TIME = USEREVENT + 2