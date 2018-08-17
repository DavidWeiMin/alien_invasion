from floating import Floating
import pygame
import random

class Alien(Floating):#todo加入不同类型的外星人（大小等）
    '''表示单个外星人的类
    
    [description]
    '''

    def __init__(self,ai_settings,screen):
        '''初始化外星人
        
        [description]
        
        Arguments:
            ai_settings {Settings 对象} -- [description]
            screen {Screen 对象} -- [description]
        '''
        super(Alien,self).__init__(ai_settings,screen)
        # 外星人设置
        self.direction = ai_settings.alien_direction
        self.speed = ai_settings.alien_speed
        self.drop_speed = ai_settings.alien_drop_speed
        # 子弹属性
        self.bullets = pygame.sprite.Group()
        self.bullet_speed = ai_settings.alien_bullet_speed
        self.bullet_height = ai_settings.alien_bullet_height
        self.bullet_width = ai_settings.alien_bullet_width
        self.bullet_color = ai_settings.alien_bullet_color
        self.bullet_direction = 1
        self.fire_time = 0
        # 加载外星人图像并获取其外接矩形
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        # 使外星人随机出现在屏幕顶端
        self.rect.x = random.randint(0,ai_settings.screen_width - self.rect.width)
        self.rect.y = random.randint(10 + self.rect.height,10 + self.rect.height + 16)
        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
                
    def update_move(self):
        '''更新外星人的移动
        
        [description]
        '''

        self.x += self.speed * self.ai_settings.alien_direction
        self.rect.x = self.x
        self.y += self.ai_settings.alien_drop_speed
        self.rect.y = self.y