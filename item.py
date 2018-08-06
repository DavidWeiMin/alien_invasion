import pygame
import random
from alien import Alien

class Item(Alien):
    '''表示单个道具的类'''
    count = 0

    def __init__(self,ai_settings,screen):
        '''初始化道具并设置其起始位置'''
        Item.count += 1
        super(Item,self).__init__()

    def load_image(self):
        self.kind = random.choice([1,2,3])
        self.image = pygame.image.load('images/item' + str(self.kind) + '.bmp')
        self.rect = self.image.get_rect()
