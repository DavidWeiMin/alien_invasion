import pygame
import random

class Floating(pygame.sprite.Sprite):
    '''表示可移动物体的类'''

    def __init__(self,ai_settings,screen):
        '''初始化物体并设置其起始位置'''
        super(Floating,self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
    def blitme(self):
        '''在指定位置绘制物体'''
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        '''如果物体位于边缘就返回 True'''
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True       
    
    def update_bullets(self):
        '''更新飞船子弹的位置以及删除屏幕外的子弹'''
        # 更新子弹的位置
        for bullet in self.bullets:
            bullet.update_move()
            bullet.update_delete(self.bullets)


