from floating import Floating
import pygame

class Alien(Floating):#加入不同类型的外星人（大小等）
    '''表示单个外星人的类'''

    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置其起始位置'''
        super(Alien,self).__init__(ai_settings,screen)
        self.initial()

    def load_image(self):
        self.alien_bullets = pygame.sprite.Group()
        self.fire_time = 0
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

    def check_floatings_bottom(self,floatings):
        '''检查是否有物体到达了屏幕底端'''
        for floating in floatings.sprites():
            if floating.rect.bottom >= self.screen_rect.bottom:
                floatings.remove(floating)

    def change_floating_direction(self,floatings):
        '''将整群外星人向下移，并改变它们的方向'''
        for floating in floatings.sprites():
            floating.rect.y += self.ai_settings.floating_drop_speed
        self.ai_settings.alien_direction *= -1

    def check_floating_edges(self,floatings):
        '''有外星人到达边界采取相应的措施'''
        for floating in floatings.sprites():
            if floating.check_edges():
                self.change_floating_direction(floatings)
                break
