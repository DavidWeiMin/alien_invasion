import time
class Settings():
    '''存储《外星人入侵》的所有设置的类'''

    def __init__(self):
        '''初始化游戏的静态设置'''
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 666
        self.bg_color = (230,230,230)

        # 飞船的设置
        self.ship_limit = 2

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 8

        # 加快游戏节奏
        self.speedup_scale = 1.05
        # 击中外星人得分的提高速度
        self.score_scale = 1.1
        # 每击杀外星人 10 个给予道具奖励
        self.award_base = 25
        self.level_base = 10
        self.effect_time = 10

        # 无敌时间
        self.unstoppable_time = 3

        # 游戏数据文件保存地址
        self.filename = 'game_data.csv'

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的动态设置'''
        self.ship_speed_factor = 0.75
        self.bullet_speed_factor = 1.25
        self.alien_speed_factor = 0.5
        self.floating_drop_speed = 0.4
        self.energy_bullet = True
        self.timekeep = {i:[] for i in range(1,7)}

        # 1 表示向右移，为 -1 表示向左移
        self.alien_direction = 1
        self.item_direction = 1

        # 计分
        self.alien_points = 10

    def increase_speed(self):
        '''提高速度设置和得分设置'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.floating_drop_speed *= self.speedup_scale
        self.alien_points = self.score_scale * self.alien_points

