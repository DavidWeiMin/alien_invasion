import pygame.font
import pygame.sprite
from ship import Ship
from item import Item
from time import time

class Scoreboard():#todo加入道具效果倒计时
    '''显示得分信息的类'''

    def __init__(self,ai_settings,screen,stats):
        '''初始化显示得分涉及的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,24)
        self.font2 = pygame.font.SysFont(None,16)

        # 初始化道具效果倒数计时
        self.count_down = {i:[] for i in range(1,8)}
        self.count_image = {i:[] for i in range(1,8)}
        self.count_rect = {i:[] for i in range(1,8)}

        # 准备所有图像
        self.prep_all()

    def prep_score(self):
        '''将得分转换为一副渲染的图像'''
        self.stats.stats_analysis()
        rounded_score = int(round(self.stats.adjust_score))
        rounded_score = '{:,}'.format(rounded_score)
        score_str = str('Score:%s' % rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        # 设置得分图像位置
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 15

    def prep_highest_score(self):
        '''将最高得分转换为渲染的图像'''
        rounded_highest_score = int(round(self.stats.adjust_highest_score))
        rounded_highest_score = '{:,}'.format(rounded_highest_score)
        highest_score_str = str('Highest Score:%s' % rounded_highest_score)
        self.highest_score_image = self.font.render(highest_score_str,True,self.text_color,self.ai_settings.bg_color)

        # 设置最高得分图像位置
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.score_rect.top

    def prep_level(self):
        '''将等级转换为渲染的图像'''
        self.level_image = self.font.render('Level:%s' % str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)

        # 设置等级图像位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.left - 10
        self.level_rect.top = self.score_rect.top
    
    def prep_hits(self):
        '''将击杀数转换为渲染的图像'''
        self.hits_image = self.font.render('Kill:%s' % str(self.stats.killed_number),True,self.text_color,self.ai_settings.bg_color)

        # 设置击杀数图像位置
        self.hits_rect = self.hits_image.get_rect()
        self.hits_rect.right = self.level_rect.left - 10
        self.hits_rect.top = self.level_rect.top

    def prep_ships(self):
        '''显示还余下多少飞船'''
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_left):
            self.ship = Ship(self.ai_settings,self.screen)
            self.ship.image = pygame.image.load('images/item7.png')
            self.ship.rect = self.ship.image.get_rect()
            self.ship.rect.x = 10 + ship_number * self.ship.rect.width
            self.ship.rect.y = self.score_rect.top
            self.ships.add(self.ship)

    def prep_item(self):
        '''准备道具图像'''
        for key,value in self.ai_settings.timekeep.items():
            for j in value:
                self.count_down[key].append(str(round(self.ai_settings.effect_time + j - time(),1)))
                self.count_image[key].append(self.font2.render(self.count_down[key][-1],True,self.text_color,self.ai_settings.bg_color))
                self.count_rect[key].append(self.count_image[key][-1].get_rect())

        self.items = pygame.sprite.Group()
        item_collection = [self.stats.item_1,self.stats.item_2,self.stats.item_3,self.stats.item_4,self.stats.item_5,self.stats.item_6]
        for kind,number in enumerate(item_collection):
            if len(self.items.sprites()) == 0:
                if self.stats.ships_left > 0:#alert 如果没有命了就会导致ship对象不存在
                    seperation = self.stats.ships_left * self.ship.rect.width + 20
                else:
                    seperation = 10
            else:
                seperation = self.items.sprites()[-1].rect.right + 10
            for item_number in range(number):
                self.item = Item(self.ai_settings,self.screen)
                self.item.set_kind(kind + 1)
                self.item.load_image()
                self.item.rect.x = seperation + item_number * self.item.rect.width
                self.item.rect.y = self.score_rect.top
                if item_number < len(self.ai_settings.timekeep[kind + 1]):
                    self.count_rect[kind + 1][item_number].centerx = self.item.rect.centerx
                    self.count_rect[kind + 1][item_number].bottom = self.item.rect.top
                self.items.add(self.item)
    # todo 在屏幕上显示当前玩家与游戏持续时间，显示当前已经产生外星人数量与击杀率
    
    def prep_all(self):
        '''准备所有图像'''
        self.prep_score()
        self.prep_ships()
        self.prep_level()
        self.prep_highest_score()
        self.prep_hits()
        self.prep_item()

    def show(self):
        '''在屏幕上显示'''
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.hits_image,self.hits_rect)
        # 绘制飞船
        self.ships.draw(self.screen)
        # 绘制道具
        self.items.draw(self.screen)
        for i in self.ai_settings.timekeep:
            for j in range(len(self.ai_settings.timekeep[i])):
                self.screen.blit(self.count_image[i][j],self.count_rect[i][j])
        self.count_down = {i:[] for i in range(1,8)}
        self.count_image = {i:[] for i in range(1,8)}
        self.count_rect = {i:[] for i in range(1,8)}