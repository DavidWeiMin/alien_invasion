import time
import math
class Settings():
    '''存储《外星人入侵》的所有设置的类
    
    包括屏幕，飞船，子弹，外星人，道具，计分等设置
    '''

    def __init__(self):
        '''初始化静态设置
        
        静态设置是游戏过程中不发生改变的设置
        '''
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 666
        self.bg_color = (230,230,230)

        # 飞船的设置
        self.ship_limit = 1

        # 子弹设置
        self.ship_bullet_height = 15
        self.alien_bullet_height = 15
        self.alien_bullet_width = 3
        self.ship_bullet_color = 255,127,0
        self.alien_bullet_color = 60,60,60

        # 加快游戏节奏
        self.speedup_scale = 1.05
        # 击中外星人得分的提高速度
        self.score_scale = 1.03
        # 每击杀外星人 10 个给予道具奖励
        self.award_base = 20
        self.level_base = 15

        # 无敌时间
        self.unstoppable_time = 3

        # 游戏数据文件保存地址
        self.filename = 'game_data.csv'

        # 背景音乐播放设置
        self.play_list = range(11)

        # 外星人射击时间间隔
        self.fire_interval = 8
        # 外星人产生时间间隔
        self.generate_interval = 1

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''初始化动态设置
        
        随游戏进行而发生变化的设置
        '''
        self.ship_bullet_width = 3
        self.ship_bullets_allowed = 10
        self.alien_bullets_allowed = 3
        self.ship_speed = 0.75
        self.ship_bullet_speed = 1.25
        self.alien_bullet_speed = 1.2
        self.alien_speed = 0.5
        self.item_speed = 0.5
        self.alien_drop_speed = 0.4
        self.item_drop_speed = 0.4
        self.bullet_energy = True
        self.item_list = range(7)
        self.timekeep = {i:[] for i in self.item_list}
        self.effect_time = 10

        # 1 表示向右移，为 -1 表示向左移
        self.alien_direction = 1
        self.item_direction = 1

        # 计分
        self.alien_points = 1

    def increase_speed(self):
        '''提高游戏等级'''
        self.ship_speed *= self.speedup_scale 
        self.ship_bullet_speed *= self.speedup_scale
        self.alien_bullet_speed *= math.sqrt(self.speedup_scale)
        self.alien_speed *= self.speedup_scale
        self.alien_drop_speed *= self.speedup_scale
        self.item_drop_speed *= self.speedup_scale
        self.alien_points = self.score_scale * self.alien_points
        self.fire_interval /= self.speedup_scale

