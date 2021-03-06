import pygame
from floating import Floating

class Ship(Floating):

    def __init__(self,ai_settings,screen):
        '''初始化飞船并设置初始位置'''
        super(Ship,self).__init__(ai_settings,screen)
        self.initial()
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def load_image(self):
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

    def position(self):
        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中储存小数值
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

    def update(self):
        '''根据移动标志调整飞船的位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 10 + self.rect.height:
            self.bottom -= self.ai_settings.ship_speed_factor
        
        # 根据 self.center 更新 rect 对象
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        '''让飞船在屏幕底居中'''
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom