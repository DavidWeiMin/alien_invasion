import pygame
import random
from floating import Floating

class Item(Floating):
    '''表示单个道具的类'''
    count = 0

    def __init__(self,ai_settings,screen):
        '''初始化道具并设置其起始位置'''
        super(Item,self).__init__(ai_settings,screen)
        # 道具属性
        self.direction = ai_settings.item_direction
        self.speed = ai_settings.item_speed
        self.drop_speed = ai_settings.item_drop_speed
        # 加载道具图像并获取其外接矩形
        self.kind = random.choice(ai_settings.item_list)
        self.image = pygame.image.load('images/item' + str(self.kind) + '.png')
        self.rect = self.image.get_rect()
        # 使道具随机出现在屏幕顶端
        self.rect.x = random.randint(0,ai_settings.screen_width - self.rect.width)
        self.rect.y = random.randint(10 + self.rect.height,10 + self.rect.height + 16)
        # 存储道具的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def set_kind(self,kind):
        '''手动设置道具种类'''
        self.kind = kind
    
    def caculate_number(self):
        '''统计累计产生道具的数量'''
        Item.count += 1
    
    def update_move(self):
        '''向左或向右移动物体'''
        self.x += self.speed * self.ai_settings.item_direction
        self.rect.x = self.x
        self.y += self.ai_settings.item_drop_speed
        self.rect.y = self.y
    
    # def update_delete(self,items):
    #     for item in items:
    #         if item.rect.top >= self.screen_rect.bottom:
    #             items.remove(item)
        