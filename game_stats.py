from time import time
from time import localtime
from time import strftime
import math
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
        self.adjust_highest_score = 0
        self.create_alien_time = 0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.score = 0
        self.adjust_score = 0
        self.level = 0
        self.item_ = {i:0 for i in self.ai_settings.item_list}
        self.item_[0] = self.ai_settings.ship_limit
        self.item_cum = {i:0 for i in self.ai_settings.item_list}
        self.killed_number = 0
        self.generate_alien_number = 0
        self.generate_bullet_number = 0
        self.bullet_killed_number = 0
        self.die_time = [time()]
        self.player_name = 'wyt'
        self.game_start_time = time()
        self.game_over_time = 0
        self.which = 1
        self.key = 0
        self.key_down = 0
        self.key_up = 0
        self.key_left = 0
        self.key_right = 0
        self.play_music = True
        self.new_record = False
    
    def check_highest_score(self):
        '''检测是否诞生了新的最高得分'''
        if self.adjust_score > self.adjust_highest_score:
            self.adjust_highest_score = self.adjust_score
            self.new_record = True
        elif self.new_record:
            self.adjust_highest_score = self.adjust_score

    def stats_analysis(self):
        '''计算分析游戏数据'''
        self.game_time = self.game_over_time - self.game_start_time

        if self.generate_alien_number:
            self.killed_ratio = self.killed_number / self.generate_alien_number
        else:
            self.killed_ratio = 0

        self.get_item_number = sum(self.item_cum.values())
        self.generate_item_number = self.killed_number // self.ai_settings.award_base

        if self.generate_item_number:
            self.get_item_ratio = self.get_item_number / self.generate_item_number
        else:
            self.get_item_ratio = 0

        if self.generate_bullet_number:
            self.hit_ratio = self.bullet_killed_number / self.generate_bullet_number
        else:
            self.hit_ratio = 0

        self.adjust_score = self.score * math.pow(math.e,2.75 + self.hit_ratio + self.killed_ratio / 6) / 2

    def save_stats(self):
        '''保存用户的游戏数据'''
        self.stats_analysis()
        self.die_time.pop(0)
        if self.game_time >= 6:
            with open(self.ai_settings.filename,'a') as f:
                # f.write('玩家,开始时间,结束时间,持续时间,得分,等级,击杀数,击杀率,道具产生,道具获取,道具拾取率,道具1,道具2,道具3,道具4,道具5,道具6,道具7,发射子弹,子弹击中,击中率,')
                # f.write('player,start,end,duration,score,level,kill,kill ratio,generate item,get item,get item ratio,item 1,item 2,item 3,item 4,item 5,item 6,fire,hit,hit ratio,key,up,down,left,right,die 1,die 2,die 3,die 4,die 5,die 6,die 7,die 8,die 9\n')
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
                [f.write(str(self.item_cum[i]) + ',') for i in self.ai_settings.item_list]
                f.write(str(self.generate_bullet_number) + ',')
                f.write(str(self.bullet_killed_number) + ',')
                f.write('%.2f%%' % (self.hit_ratio * 100) + ',')
                f.write(str(self.key) + ',')
                f.write(str(self.key_up) + ',')
                f.write(str(self.key_down) + ',')
                f.write(str(self.key_left) + ',')
                f.write(str(self.key_right) + ',')
                for i in range(len(self.die_time)):
                    f.write(strftime('%Y-%m-%d %H:%M:%S',localtime(self.die_time[i])))
                    if i + 1 < len(self.die_time):
                        f.write(',')
                    else:
                        f.write('\n')
