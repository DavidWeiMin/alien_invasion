import pygame.font
import pygame.sprite
from ship import Ship
from item import Item
from time import time

class Scoreboard():
    '''数据展示面板类
    
    用于在游戏界面展示需要的实时信息，比如得分，道具拥有情况，道具效果倒计时。
    '''


    def __init__(self,ai_settings,screen,stats):
        '''初始化
        
        初始化得分，道具等信息
        
        Arguments:
            ai_settings {Settings 对象} -- [description]
            screen {Screen 对象} -- [description]
            stats {Game_Stats 对象} -- [description]
        '''

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,24)
        self.font2 = pygame.font.SysFont(None,16)

        # 初始化道具效果倒数计时
        self.count_down = {i:[] for i in self.ai_settings.item_list}
        self.count_image = {i:[] for i in self.ai_settings.item_list}
        self.count_rect = {i:[] for i in self.ai_settings.item_list}

        # 准备所有图像
        self.prep_all()

    def prep_score(self):
        '''渲染得分图像
        
        [description]
        '''

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
        '''渲染最高分图像
        
        [description]
        '''

        rounded_highest_score = int(round(self.stats.adjust_highest_score))
        rounded_highest_score = '{:,}'.format(rounded_highest_score)
        highest_score_str = str('Highest Score:%s' % rounded_highest_score)
        self.highest_score_image = self.font.render(highest_score_str,True,self.text_color,self.ai_settings.bg_color)

        # 设置最高得分图像位置
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.score_rect.top

    def prep_level(self):
        '''渲染游戏等级图像
        
        [description]
        '''

        self.level_image = self.font.render('Level:%s' % str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)

        # 设置等级图像位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.left - 10
        self.level_rect.top = self.score_rect.top
    
    def prep_kills(self):
        '''渲染击杀数图像
        
        [description]
        '''

        self.kills_image = self.font.render('Kill:%s' % str(self.stats.killed_number),True,self.text_color,self.ai_settings.bg_color)

        # 设置击杀数图像位置
        self.kills_rect = self.kills_image.get_rect()
        self.kills_rect.right = self.level_rect.left - 10
        self.kills_rect.top = self.level_rect.top

    def prep_item(self):
        '''渲染道具图像
        
        [description]
        '''

        for key,value in self.ai_settings.timekeep.items():
            for j in value:
                self.count_down[key].append(str(round(self.ai_settings.effect_time + j - time(),1)))
                self.count_image[key].append(self.font2.render(self.count_down[key][-1],True,self.text_color,self.ai_settings.bg_color))
                self.count_rect[key].append(self.count_image[key][-1].get_rect())

        self.items = pygame.sprite.Group()
        for kind,number in self.stats.item_.items():
            if len(self.items.sprites()) == 0:
                position = 10
            else:
                position = self.items.sprites()[-1].rect.right + 10
            for item_number in range(number):
                self.item = Item(self.ai_settings,self.screen)
                self.item.set_kind(kind)
                self.item.image = pygame.image.load('images/item' + str(self.item.kind) + '.png')
                self.item.rect.left = position
                position = self.item.rect.right
                self.item.rect.top = self.score_rect.top
                if item_number < len(self.ai_settings.timekeep[kind]):
                    self.count_rect[kind][item_number].centerx = self.item.rect.centerx
                    self.count_rect[kind][item_number].bottom = self.item.rect.top
                self.items.add(self.item)
    
    def prep_all(self):
        '''渲染所有图像
        
        [description]
        '''

        self.prep_score()
        self.prep_level()
        self.prep_highest_score()
        self.prep_kills()
        self.prep_item()

    def show(self):
        '''显示渲染的图像
        
        [description]
        '''

        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.kills_image,self.kills_rect)
        # 绘制道具
        self.items.draw(self.screen)
        for i in self.ai_settings.timekeep:
            for j in range(len(self.ai_settings.timekeep[i])):
                self.screen.blit(self.count_image[i][j],self.count_rect[i][j])
        self.count_down = {i:[] for i in self.ai_settings.item_list}
        self.count_image = {i:[] for i in self.ai_settings.item_list}
        self.count_rect = {i:[] for i in self.ai_settings.item_list}