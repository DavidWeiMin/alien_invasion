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
        self.ship_limit = 1

        # 子弹设置
        self.bullet_height = 15
        self.alien_bullet_width = 3
        self.ship_bullet_color = 255,127,0
        self.alien_bullet_color = 60,60,60

        # 加快游戏节奏
        self.speedup_scale = 1.05
        # 击中外星人得分的提高速度
        self.score_scale = 1.1
        # 每击杀外星人 10 个给予道具奖励
        self.award_base = 3
        self.level_base = 10

        # 无敌时间
        self.unstoppable_time = 3

        # 游戏数据文件保存地址
        self.filename = 'game_data.csv'

        # 背景音乐播放设置
        self.play_list = range(11)

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的动态设置'''
        self.ship_bullet_width = 3
        self.ship_bullets_allowed = 10
        self.alien_bullets_allowed = 3
        self.ship_speed_factor = 0.75
        self.bullet_speed_factor = 1.25#todo 使飞船子弹与外星人子弹速度独立
        self.alien_speed_factor = 0.5
        self.floating_drop_speed = 0.4
        self.energy_bullet = True
        self.timekeep = {i:[] for i in range(1,8)}
        self.effect_time = 10

        # 1 表示向右移，为 -1 表示向左移
        self.alien_direction = 1
        self.item_direction = 1

        # 计分
        self.alien_points = 10

    def increase_speed(self):
        '''提高速度设置和得分设置'''
        self.ship_speed_factor *= self.speedup_scale #todo设置飞船最大速度
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.floating_drop_speed *= self.speedup_scale
        self.alien_points = self.score_scale * self.alien_points

