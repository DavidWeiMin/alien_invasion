''' 本书配套资源网站：https/www.ituring.cn/book/1861'''

'''改进余地
加入背景音效、击杀音效、道具拾取音效、死亡音效
加入加命道具
改进外星人出现方式
加入三列子弹道具
加入大招
加入复活后无敌时间
加入向上飞行效果
保存最高分
改进飞船移动问题（一次移动距离过大）
加入设置按钮
设计自动射击，无限子弹模式
加入外星人射击
设计不同类型的外星人，不同的外星人得分不同
设计飞船护甲
双人模式
'''

import pygame
from settings import Settings
from ship import Ship
from game_stats import Game_stats
from button import Button
from scoreboard import Scoreboard
from item import Item
import time
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
    bullets = pygame.sprite.Group()
    # 创建一个外星人编组
    aliens = pygame.sprite.Group()
    # 创建一组道具
    items = pygame.sprite.Group()

    # 创建一个用于储存游戏统计信息的对象
    stats = Game_stats(ai_settings)

    # 创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)

    # 创建外星人群
    stats.create_alien_time = time.time()
    gf.create_fleet(ai_settings,screen,aliens)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)
        
        if stats.game_active:
            # 更新状态
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,items)
            gf.update_items(ai_settings,screen,stats,ship,items)
            gf.update_aliens(ai_settings,screen,stats,ship,aliens,bullets)
            
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,items) 

run_game()