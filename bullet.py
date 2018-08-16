import pygame
# fron pygame.sprite import Sprite

class Bullet(pygame.sprite.Sprite):
    '''子弹类'''

    def __init__(self,floating):
        '''在飞船所属的位置创建一个子弹对象'''
        super(Bullet,self).__init__()
        self.floating = floating

        # 在 (0,0) 处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,floating.bullet_width,floating.bullet_height)
        self.rect.center = floating.rect.center

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update_move(self):
        '''移动子弹'''
        # 更新表示子弹位置的小数值
        self.y += (self.floating.bullet_speed * self.floating.bullet_direction)
        # 更新表示子弹矩形rect的位置
        self.rect.y = self.y

    def update_delete(self,bullets):
        # 删除屏幕外的子弹
        if self.rect.bottom <= 0 or self.rect.top >=self.floating.screen_rect.bottom:
            bullets.remove(self)

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.floating.screen,self.floating.bullet_color,self.rect)


