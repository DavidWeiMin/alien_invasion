import pygame
import random

class Floating(pygame.sprite.Sprite):
    '''表示可移动物体的类'''

    def __init__(self,ai_settings,screen):
        '''初始化物体并设置其起始位置'''
        super(Floating,self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings

    def initial(self):
        self.load_image()
        self.position()

    def load_image(self):
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

    def position(self):
        # 给出物体位置
        self.rect.x = random.randint(0,self.ai_settings.screen_width - self.rect.width)
        self.rect.y = random.randint(39,42)
        # 存储物体的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def blitme(self):
        '''在指定位置绘制物体'''
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        '''如果物体位于边缘就返回 True'''
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        '''向左或向右移动物体'''
        self.update_direction()
        self.rect.x = self.x
        self.y += self.ai_settings.floating_drop_speed
        self.rect.y = self.y
    
    def update_direction(self):
        '''个性化移动方向'''
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.alien_direction


