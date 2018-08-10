from time import time
from time import localtime
from time import strftime
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
        self.create_alien_time = 0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0
        self.item_1 = 0
        self.item_1_cum = 0
        self.item_2 = 0
        self.item_2_cum = 0
        self.item_3 = 0
        self.item_3_cum = 0
        self.item_4 = 0
        self.item_4_cum = 0
        self.item_5 = 0
        self.item_5_cum = 0
        self.item_6 = 0
        self.killed_number = 0
        self.generate_alien_number = 0
        self.generate_bullet_number = 0
        self.bullet_killed_number = 0
        self.die_time = [time()]
        self.player_name = 'dwm'
        self.game_start_time = time()
        self.game_over_time = 0
        self.which = 1
    
    def check_highest_score(self):
        '''检测是否诞生了新的最高得分'''
        if self.score > self.highest_score:
            self.highest_score = self.score

    def stats_analysis(self):
        '''计算分析游戏数据'''
        self.game_time = self.game_over_time - self.game_start_time
        self.killed_ratio = self.killed_number / self.generate_alien_number
        self.get_item_number = self.item_1_cum + self.item_2_cum + self.item_3_cum + self.item_4_cum + self.item_5_cum + self.item_6
        self.generate_item_number = self.killed_number // self.ai_settings.award_base
        if self.generate_item_number:
            self.get_item_ratio = self.get_item_number / self.generate_item_number
        else:
            self.get_item_ratio = 0

        if self.generate_bullet_number:
            self.hit_ratio = self.bullet_killed_number / self.generate_bullet_number
        else:
            self.hit_ratio = 0
        
        self.die_time.pop(0)
    
    def save_stats(self):
        '''保存用户的游戏数据'''
        self.stats_analysis()
        with open(self.ai_settings.filename,'a') as f:
            # f.write('玩家,开始时间,结束时间,持续时间,得分,等级,击杀数,击杀率,道具产生,道具获取,道具拾取率,道具1,道具2,道具3,道具4,道具5,道具6,发射子弹,子弹击中,击中率,')
            # for i in range(len(self.die_time)):
            #     f.write('第 ' + str(i + 1) + ' 次死亡')
            #     if i + 1 < len(self.die_time):
            #         f.write(',')
            #     else:
            #         f.write('\n')
            f.write(str(self.player_name) + ',')
            f.write(strftime('%Y-%m-%d %H:%M:%S',localtime(self.game_start_time)) + ',')
            f.write(strftime('%Y-%m-%d %H:%M:%S',localtime(self.game_over_time)) + ',')
            f.write(strftime('%M:%S',localtime(self.game_time)) + ',')
            f.write(str(round(self.score)) + ',')
            f.write(str(self.level) + ',')
            f.write(str(self.killed_number) + ',')
            f.write('%.2f%%' % (self.killed_ratio * 100) + ',')
            f.write(str(self.generate_item_number) + ',')
            f.write(str(self.get_item_number) + ',')
            f.write('%.2f%%' % (self.get_item_ratio * 100) + ',')
            f.write(str(self.item_1_cum) + ',')
            f.write(str(self.item_2_cum) + ',')
            f.write(str(self.item_3_cum) + ',')
            f.write(str(self.item_4_cum) + ',')
            f.write(str(self.item_5_cum) + ',')
            f.write(str(self.item_6) + ',')
            f.write(str(self.generate_bullet_number) + ',')
            f.write(str(self.bullet_killed_number) + ',')
            f.write('%.2f%%' % (self.hit_ratio * 100) + ',')
            for i in range(len(self.die_time)):
                f.write(strftime('%Y-%m-%d %H:%M:%S',localtime(self.die_time[i])))
                if i + 1 < len(self.die_time):
                    f.write(',')
                else:
                    f.write('\n')
    # add 敲击键盘总次数，上下左右射击次数，

