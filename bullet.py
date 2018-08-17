import pygame

class Bullet(pygame.sprite.Sprite):
    '''表示单个子弹的类'''

    def __init__(self,floating):
        '''初始化子弹
        
        在 floating 所属的位置中心创建一个子弹对象
        
        Arguments:
            floating {Floating 对象} -- Floating 可能是 Ship 或者 Alien
        '''

        super(Bullet,self).__init__()
        self.floating = floating

        # 在 (0,0) 处创建一个表示子弹的矩形，再设置正确的位置
        if floating.__class__.__name__=='Alien':
            self.rect = pygame.Rect(0,0,floating.ai_settings.alien_bullet_width,floating.ai_settings.alien_bullet_height)
        elif floating.__class__.__name__=='Ship':
            self.rect = pygame.Rect(0,0,floating.ai_settings.ship_bullet_width,floating.ai_settings.ship_bullet_height)
        self.rect.center = floating.rect.center

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update_move(self):
        '''更新子弹的移动
        
        [description]
        '''

        # 更新表示子弹位置的小数值
        self.y += (self.floating.bullet_speed * self.floating.bullet_direction)
        # 更新表示子弹矩形rect的位置
        self.rect.y = self.y

    def update_delete(self,bullets):
        '''删除屏幕外的子弹
        
        [description]
        
        Arguments:
            bullets {[Bullet 对象组成的编组]} -- 可能是 ship.bullets 或者 alien.bullets
        '''

        if self.rect.bottom <= 0 or self.rect.top >=self.floating.screen_rect.bottom:
            bullets.remove(self)

    def draw_bullet(self):
        '''在屏幕上绘制子弹
        
        [description]
        '''
        pygame.draw.rect(self.floating.screen,self.floating.bullet_color,self.rect)


