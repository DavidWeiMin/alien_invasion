class Game_stats():
    '''跟踪游戏的统计信息'''

    def __init__(self,ai_settings):
        '''初始化统计信息'''
        self.ai_settings = ai_settings
        self.reset_stats()

        # 游戏刚启动时处于非活动状态
        self.game_active = False

        # 在任何情况下都不应重置的最高得分
        self.highest_score = 0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.item_1 = 0
        self.item_2 = 0
        self.item_3 = 0
        self.item_4 = 0
        self.hit_number = 0
    
    def check_highest_score(self):
        '''检测是否诞生了新的最高得分'''
        if self.score > self.highest_score:
            self.highest_score = self.score
        