import pygame
from floating import Floating
from time import time,sleep

class Ship(Floating):
    '''表示单个飞船的类
    
    [description]
    
    Arguments:
        Floating {Floating 对象} -- Ship 的父类
    '''


    def __init__(self,ai_settings,screen):
        '''初始化飞船并设置初始位置'''
        super(Ship,self).__init__(ai_settings,screen)
        # 飞船属性
        self.speed = ai_settings.ship_speed
        # 子弹属性
        self.bullets = pygame.sprite.Group()
        self.bullet_speed = ai_settings.ship_bullet_speed
        self.bullet_height = ai_settings.ship_bullet_height
        self.bullet_width = ai_settings.ship_bullet_width
        self.bullet_color = ai_settings.ship_bullet_color
        self.bullets_allowed = ai_settings.ship_bullets_allowed
        self.bullet_direction = -1
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center中储存小数值
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

    def update_move(self):
        '''根据移动标志调整飞船的位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.speed
        if self.moving_up and self.rect.top > 10 + self.rect.height:
            self.bottom -= self.speed
        
        # 根据 self.center 更新 rect 对象
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        '''让飞船在屏幕底居中'''
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
    
    def hit(self,stats):
        '''响应被外星人撞到的飞船'''
        stats.die_time.append((time()))
        if stats.item_[0] > 1:
            # 生命 -1
            stats.item_[0] -= 1
            sleep(0.5)
        else:
            pygame.mixer.music.stop()
            stats.game_over_time = time()
            stats.save_stats()
            stats.game_active = False
            pygame.mouse.set_visible(True)
            self.play_die()

    def play_die(self):
        pygame.mixer.music.load('sounds/die music.mp3')
        pygame.mixer.music.play(loops=-1,start=90.6)
        sleep(3)