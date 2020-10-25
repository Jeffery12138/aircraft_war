class Stats():
    """游戏状态的类"""
    def __init__(self, ai_settings):
        """初始化"""
        self.ai_settings = ai_settings
        # 游戏暂停标志
        self.paused = False
        # 统计得分
        self.score = 0
        self.record_score = self.get_record_score()
        # 设置难度级别
        self.level = 1

    def get_record_score(self):
        if not self.ai_settings.recorded:
            self.ai_settings.recorded = True
            try:
                # 读取历史最高得分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
            except FileNotFoundError:
                record_score = 0
        return record_score

