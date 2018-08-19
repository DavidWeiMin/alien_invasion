''' 本书配套资源网站：https/www.ituring.cn/book/1861'''

'''改进余地
加入向上飞行效果
设计自动射击，无限子弹模式
设计不同类型的外星人，不同的外星人得分不同
双人模式
'''
#refactor根据代码规范完善代码格式

import pygame
from settings import Settings
from ship import Ship
from game_stats import Game_Stats
from button import Button
from scoreboard import Scoreboard
from item import Item
from time import time
import game_functions as gf
import cProfile
import pstats
import os
import memory_profiler


def run_game():
    '''运行游戏'''

    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height)) # 屏幕显示大小
    pygame.display.set_caption = ('Alien Invasion')

    # 创建 Play 按钮
    play_button = Button(ai_settings,screen,'Play')                     

    # 创建一艘飞船
    ship = Ship(ai_settings,screen)
    # 创建一个用于储存子弹的编组
    ship.bullets = pygame.sprite.Group()
    # 创建一个外星人编组
    aliens = pygame.sprite.Group()
    # 创建一组道具
    items = pygame.sprite.Group()

    # 创建一个用于储存游戏统计信息的对象
    stats = Game_Stats(ai_settings)

    # 创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)

    # 创建外星人群
    stats.create_alien_time = time()
    gf.create_alien(ai_settings,screen,stats,aliens)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,ship,aliens,items)

        if stats.game_active:
            # 更新状态
            gf.update(ai_settings,screen,stats,ship,aliens,items)
            # 检测碰撞
            gf.check_collisions(ai_settings,screen,stats,ship,aliens,items)
            
        gf.display(ai_settings,screen,stats,ship,aliens,items,sb,play_button) 

# run_game()
cProfile.run('run_game()',filename='result.prof')
p = pstats.Stats('result.prof')
p.sort_stats('time').print_stats()
os.chdir('d:\\Documents\\GitHub\\alien_invasion')
# memory_profiler.os.system('run alien_invasion.py')
# os.system('mprof run alien_invasion.py')
# os.system('mprof plot')
os.popen('python E:\Anaconda\Lib\site-packages\gprof2dot.py -f pstats result.prof | dot -Tpng -o result.png')
