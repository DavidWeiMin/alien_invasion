import pygame
import random

class Floating(pygame.sprite.Sprite):
    '''可移动物体的类
    
    游戏中 Ship,Alien,Item 的父类
    
    Arguments:
        pygame {Sprite 对象} -- [description]
    
    Returns:
        [bool] -- 检测可移动物体是否到达屏幕边缘，到达边缘返回 True，否则返回 False
    '''

    def __init__(self,ai_settings,screen):
        '''初始化物体并设置其起始位置
        
        [description]
        
        Arguments:
            ai_settings {Settings 对象} -- [description]
            screen {Screen 对象} -- [description]
        '''

        super(Floating,self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
    def blitme(self):
        '''绘制物体
        
        [description]
        '''

        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        '''检测物体是否到达屏幕边缘
        
        [description]
        
        Returns:
            [bool] -- 检测可移动物体是否到达屏幕边缘，到达边缘返回 True，否则返回 False
        '''

        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True       
    
    def update_bullets(self):
        '''更新子弹的移动和删除
        
        [description]
        '''

        # 更新子弹的位置
        for bullet in self.bullets:
            bullet.update_move()
            bullet.update_delete(self.bullets)


