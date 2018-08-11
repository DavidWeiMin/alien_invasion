import pygame
import random
from alien import Alien

class Item(Alien):
    '''表示单个道具的类'''
    count = 0

    def __init__(self,ai_settings,screen):
        '''初始化道具并设置其起始位置'''
        self.kind = random.choice(range(1,7))
        super(Item,self).__init__(ai_settings,screen)

    def load_image(self):
        self.image = pygame.image.load('images/item' + str(self.kind) + '.png')
        self.rect = self.image.get_rect()

    def set_kind(self,kind):
        '''手动设置道具种类'''
        self.kind = kind
    
    def caculate_number(self):
        '''统计累计产生道具的数量'''
        Item.count += 1

    def change_floating_direction(self,floatings):
        '''将整群外星人向下移，并改变它们的方向'''
        for floating in floatings.sprites():
            floating.rect.y += self.ai_settings.floating_drop_speed
        self.ai_settings.item_direction *= -1
    
    def update_direction(self):
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.item_direction
    
        
