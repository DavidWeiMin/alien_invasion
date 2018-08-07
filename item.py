import pygame
import random
from alien import Alien

class Item(Alien):
    '''表示单个道具的类'''
    count = 0

    def __init__(self,ai_settings,screen):
        '''初始化道具并设置其起始位置'''
        self.kind = random.choice([1,2,3])
        super(Item,self).__init__(ai_settings,screen)

    def load_image(self):
        self.image = pygame.image.load('images/item' + str(self.kind) + '.png')
        self.rect = self.image.get_rect()
    
    def set_random_kind(self):
        '''随机产生道具种类'''
        self.kind = random.choice([1,2,3])

    def set_kind(self,kind):
        '''手动设置道具种类'''
        self.kind = kind
    
    def caculate_number(self):
        '''统计累计产生道具的数量'''
        Item.count += 1
    
        
