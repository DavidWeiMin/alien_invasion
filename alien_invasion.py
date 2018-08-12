''' 本书配套资源网站：https/www.ituring.cn/book/1861'''

'''改进余地
加入向上飞行效果
保存最高分
加入设置按钮
设计自动射击，无限子弹模式
设计不同类型的外星人，不同的外星人得分不同
设计飞船护甲
双人模式
'''
#refactor根据代码规范完善代码格式
#refactor根据实际所属关系重构类，alien)bullet应该是alien的属性
#refactor简化函数参数调用，因为许多实例都含有其他实例

import pygame
from settings import Settings
from ship import Ship
from game_stats import Game_stats
from button import Button
from scoreboard import Scoreboard
from item import Item
from time import time
import game_functions as gf

def run_game():
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
    ship_bullets = pygame.sprite.Group()
    # 创建一个外星人编组
    aliens = pygame.sprite.Group()
    # 创建一组道具
    items = pygame.sprite.Group()

    # 创建一个用于储存游戏统计信息的对象
    stats = Game_stats(ai_settings)

    # 创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)

    # 创建外星人群
    stats.create_alien_time = time()
    gf.create_fleet(ai_settings,screen,stats,aliens)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,ship_bullets,items)

        if stats.game_active:
            # 更新状态
            ship.update()
            gf.update_ship_bullets(ai_settings,screen,stats,sb,ship,aliens,ship_bullets,items)
            gf.update_alien_bullets(ai_settings,stats,ship,aliens)
            gf.update_items(ai_settings,screen,stats,ship,items)
            gf.update_aliens(ai_settings,screen,stats,ship,aliens,ship_bullets)
            
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,ship_bullets,play_button,items) 

run_game()