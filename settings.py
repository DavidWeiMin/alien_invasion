class Settings():
    '''存储《外星人入侵》的所有设置的类'''

    def __init__(self):
        '''初始化游戏的静态设置'''
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 666
        self.bg_color = (230,230,230)

        # 飞船的设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 6

        # 加快游戏节奏
        self.speedup_scale = 1.05
        # 击中外星人得分的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的动态设置'''
        self.ship_speed_factor = 0.75
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 0.3

        # fleet_direction 为 1 表示向右移，为 -1 表示向左移
        self.fleet_direction = 1

        # 计分
        self.alien_points = 10

    def increase_speed(self):
        '''提高速度设置和得分设置'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)

