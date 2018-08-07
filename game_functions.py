import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from item import Item
import random
import time

def ship_move(event,ship,state):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = state
    elif event.key == pygame.K_LEFT:
        ship.moving_left = state
    elif event.key == pygame.K_UP:
        ship.moving_up = state
    elif event.key == pygame.K_DOWN:
        ship.moving_down = state

def item_effect(event,ai_settings,stats,aliens,bullets):
    if event.key == pygame.K_1 and stats.item_1 > 0:
        stats.item_1 -= 1
        ai_settings.bullet_width *= 2 # 飞船子弹宽度乘以 2
        ai_settings.timekeep[1].append((time.time()))
    elif event.key == pygame.K_2 and stats.item_2 > 0:
        stats.item_2 -= 1
        ai_settings.fleet_drop_speed /= 2 # 外星人下降速度除以 2
        ai_settings.timekeep[2].append((time.time()))
    elif event.key == pygame.K_3 and stats.item_3 > 0:
        stats.item_3 -= 1
        ai_settings.energy_bullet = False # 普通子弹升级为高能子弹
        ai_settings.timekeep[3].append((time.time()))
    elif event.key == pygame.K_4 and stats.item_4 > 0:
        stats.item_4 -= 1
        aliens.empty()
        bullets.empty() # 清除屏幕上所有外星人

def check_keydown_events(event,ai_settings,screen,stats,ship,aliens,bullets,state):
    '''响应按键'''
    ship_move(event,ship,state)
    if event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(ai_settings,screen,ship,bullets)
        else:
            reset_game(ai_settings,screen,stats,ship,aliens,bullets)
    elif event.key == pygame.K_p:
        stats.game_active = not stats.game_active
    elif event.key == pygame.K_q:
        sys.exit()
    item_effect(event,ai_settings,stats,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    '''如果还没有达到子弹数量限制，就发射一颗子弹'''
    # 创建一颗子弹，并将其加入到编组 Bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship,state):
    '''响应松开'''
    ship_move(event,ship,state)

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
    '''响应按键和鼠标事件'''
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,ship,aliens,bullets,True)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship,False)

def reset_game(ai_settings,screen,stats,ship,aliens,bullets):
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏信息
    stats.reset_stats()
    stats.game_active = True
    ai_settings.initialize_dynamic_settings()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings,screen,aliens)
    ship.center_ship()

def check_bullet_alien_collisions(ai_settings,screen,stats,ship,aliens,bullets,items):
    '''响应子弹与外星人的碰撞'''
    # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,ai_settings.energy_bullet,True)

    # 计分
    if collisions:
        for aliens_hit in collisions.values():
            stats.hit_number += len(aliens_hit)
            if stats.hit_number // ai_settings.base > Item.count:
                item = Item(ai_settings,screen)
                item.caculate_number()
                items.add(item)
            stats.score += ai_settings.alien_points * len(aliens_hit)
            stats.check_highest_score()

    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人
        bullets.empty()
        # 提高游戏等级
        ai_settings.increase_speed()
        stats.level += 1
        create_fleet(ai_settings,screen,aliens)

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,items):
    # 更新子弹的位置
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,ship,aliens,bullets,items)

def ship_hit(ai_settings,screen,stats,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        # 将 ships_left 减 1
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,aliens)
        ship.center_ship()

        # 暂停 0.5 秒
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_items(ai_settings,screen,stats,ship,items):
    '''更新道具'''
    if len(items.sprites()) > 0:
        items.sprites()[0].check_fleet_edges(items)
        items.sprites()[0].check_floatings_bottom(items)
    items.update()

    if pygame.sprite.spritecollideany(ship,items):
        item = items.sprites()[0]
        if item.kind == 1:
            stats.item_1 += 1
        elif item.kind == 2:
            stats.item_2 += 1
        elif item.kind == 3:
            stats.item_3 += 1
        elif item.kind == 4:
            stats.item_4 += 1
        items.remove(item)
    if ai_settings.timekeep[1] and (time.time() - ai_settings.timekeep[1][0] >= ai_settings.effect_time):
        ai_settings.bullet_width /= 2
        ai_settings.timekeep[1].pop(0)
    if ai_settings.timekeep[2] and (time.time() - ai_settings.timekeep[2][0] >= ai_settings.effect_time):
        ai_settings.fleet_drop_speed *= 2
        ai_settings.timekeep[2].pop(0)
    if ai_settings.timekeep[3] and (time.time() - ai_settings.timekeep[3][0] >= ai_settings.effect_time):
        ai_settings.energy_bullet = True
        ai_settings.timekeep[3].pop(0)

def update_aliens(ai_settings,screen,stats,ship,aliens,bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    alien = Alien(ai_settings,screen)
    alien.check_fleet_edges(aliens)
    # 检查是否有外星人到达屏幕底端
    alien.check_floatings_bottom(aliens)
    aliens.update()

    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,ship,aliens,bullets)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button,items):
    '''更新屏幕上的图像'''
    screen.fill(ai_settings.bg_color)

    # # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    items.draw(screen)

    # 显示统计数据
    sb.prep_all()
    sb.show()

    # 如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def create_fleet(ai_settings,screen,aliens):
    '''创建外星人群'''
    for i in range(3):
        for j in range(3):
            alien = Alien(ai_settings,screen)
            aliens.add(alien)