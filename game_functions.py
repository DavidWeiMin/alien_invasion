import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from item import Item
import random
from time import time

def ship_move(event,ship,state):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = state
    elif event.key == pygame.K_LEFT:
        ship.moving_left = state
    elif event.key == pygame.K_UP:
        ship.moving_up = state
    elif event.key == pygame.K_DOWN:
        ship.moving_down = state

def item_effect(event,ai_settings,screen,stats,aliens,bullets,items):
    if event.key == pygame.K_1 and stats.item_1 > 0:
        stats.item_1 -= 1
        ai_settings.bullet_width *= 8 # 飞船子弹宽度乘以 8
        ai_settings.timekeep[1].append((time()))
    elif event.key == pygame.K_2 and stats.item_2 > 0:
        stats.item_2 -= 1
        ai_settings.floating_drop_speed /= 2 # 外星人下降速度除以 2
        ai_settings.timekeep[2].append((time()))
    elif event.key == pygame.K_3 and stats.item_3 > 0:
        stats.item_3 -= 1
        ai_settings.energy_bullet = False # 普通子弹升级为高能子弹
        ai_settings.timekeep[3].append((time()))
    elif event.key == pygame.K_4 and stats.item_4 > 0:
        stats.killed_number += len(aliens.sprites())
        stats.score += len(aliens.sprites()) * ai_settings.alien_points
        stats.check_highest_score()
        stats.item_4 -= 1
        aliens.empty()
        bullets.empty() # 清除屏幕上所有外星人
        # todo  两个if单独定义函数
        if stats.killed_number // ai_settings.award_base > Item.count:
            item = Item(ai_settings,screen)
            item.caculate_number()
            items.add(item)
        if stats.killed_number // ai_settings.level_base > stats.level:
            ai_settings.increase_speed()
            stats.level += 1
    elif event.key == pygame.K_5 and stats.item_5 > 0:
        stats.item_5 -= 1
        ai_settings.bullets_allowed *= 2
        ai_settings.timekeep[5].append((time()))

def check_keydown_events(event,ai_settings,screen,stats,ship,aliens,bullets,state,items):
    '''响应按键'''
    ship_move(event,ship,state)
    if event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(ai_settings,screen,stats,ship,bullets)
        else:
            reset_game(ai_settings,screen,stats,ship,aliens,bullets,items)
            stats.which = random.choice(ai_settings.play_list)
            play_bgm(stats)
            # stats.player_name = input('please enter your account:\n')
            # sleep(3)
    elif event.key == pygame.K_p:
        if stats.game_active:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        stats.game_active = not stats.game_active
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_HOME:
        if pygame.mixer.music.get_busy() == 1: 
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    elif event.key == pygame.K_PAGEUP:
        play_last(stats)
    elif event.key == pygame.K_PAGEDOWN:
        play_next(stats)
    item_effect(event,ai_settings,screen,stats,aliens,bullets,items)

def fire_bullet(ai_settings,screen,stats,ship,bullets):
    '''如果还没有达到子弹数量限制，就发射一颗子弹'''
    # 创建一颗子弹，并将其加入到编组 Bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
        stats.generate_bullet_number += 1

def check_keyup_events(event,ship,state):
    '''响应松开'''
    ship_move(event,ship,state)

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,items):
    '''响应按键和鼠标事件'''
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,ship,aliens,bullets,True,items)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship,False)

def reset_game(ai_settings,screen,stats,ship,aliens,bullets,items):
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏信息
    stats.reset_stats()
    stats.game_active = True
    Item.count = 0
    ai_settings.initialize_dynamic_settings()

    # 清空外星人列表、子弹列表和道具列表
    aliens.empty()
    bullets.empty()
    items.empty()
    

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    stats.create_alien_time = time()
    create_fleet(ai_settings,screen,stats,aliens)
    ship.center_ship()

def check_bullet_alien_collisions(ai_settings,screen,stats,ship,aliens,bullets,items):
    '''响应子弹与外星人的碰撞'''
    # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,ai_settings.energy_bullet,True)

    # 计分
    if collisions:
        for aliens_hit in collisions.values():
            stats.killed_number += len(aliens_hit)
            stats.bullet_killed_number += len(aliens_hit)
            stats.score += ai_settings.alien_points * len(aliens_hit)
            stats.check_highest_score()
            # todo  两个if单独定义函数
            if stats.killed_number // ai_settings.award_base > Item.count:
                item = Item(ai_settings,screen)
                item.caculate_number()
                items.add(item)
            if stats.killed_number // ai_settings.level_base > stats.level:
                ai_settings.increase_speed()
                stats.level += 1

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,items):
    # 更新子弹的位置
    bullets.update()

    # 删除屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,ship,aliens,bullets,items)

def ship_hit(ai_settings,screen,stats,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    stats.die_time.append((time()))
    if stats.ships_left > 1:
        # 将 ships_left 减 1
        stats.ships_left -= 1
        sleep(0.5)
    else:
        pygame.mixer.music.stop()
        stats.game_over_time = time()
        stats.save_stats()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        play_die()
        # sleep(3)

def update_items(ai_settings,screen,stats,ship,items):
    '''更新道具'''
    if len(items.sprites()) > 0:
        items.sprites()[0].check_floating_edges(items)
        items.sprites()[0].check_floatings_bottom(items)
    items.update()

    if pygame.sprite.spritecollideany(ship,items):
        item = items.sprites()[0]
        if item.kind == 1:
            stats.item_1 += 1
            stats.item_1_cum += 1
        elif item.kind == 2:
            stats.item_2 += 1
            stats.item_2_cum += 1
        elif item.kind == 3:
            stats.item_3 += 1
            stats.item_3_cum += 1
        elif item.kind == 4:
            stats.item_4 += 1
            stats.item_4_cum += 1
        elif item.kind == 5:
            stats.item_5 += 1
            stats.item_5_cum += 1           
        elif item.kind == 6:
            stats.ships_left += 1
            stats.item_6 += 1
        items.remove(item)
    if ai_settings.timekeep[1] and (time() - ai_settings.timekeep[1][0] >= ai_settings.effect_time):
        ai_settings.bullet_width /= 8
        ai_settings.timekeep[1].pop(0)
    if ai_settings.timekeep[2] and (time() - ai_settings.timekeep[2][0] >= ai_settings.effect_time):
        ai_settings.floating_drop_speed *= 2
        ai_settings.timekeep[2].pop(0)
    if ai_settings.timekeep[3] and (time() - ai_settings.timekeep[3][0] >= ai_settings.effect_time):
        ai_settings.energy_bullet = True
        ai_settings.timekeep[3].pop(0)
    if ai_settings.timekeep[5] and (time() - ai_settings.timekeep[5][0] >= ai_settings.effect_time):
        ai_settings.bullets_allowed /= 2
        ai_settings.timekeep[5].pop(0)
def update_aliens(ai_settings,screen,stats,ship,aliens,bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    alien = Alien(ai_settings,screen)
    alien.check_floating_edges(aliens)
    # 检查是否有外星人到达屏幕底端
    alien.check_floatings_bottom(aliens)
    aliens.update()

    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens) and (time() - stats.die_time[-1] > ai_settings.unstoppable_time):
        ship_hit(ai_settings,screen,stats,ship,aliens,bullets)
    
    if time() - stats.create_alien_time > 0.75 / ai_settings.speedup_scale ** 2:
        stats.create_alien_time = time()
        create_fleet(ai_settings,screen,stats,aliens)

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

def create_fleet(ai_settings,screen,stats,aliens):
    '''创建外星人群'''
    alien = Alien(ai_settings,screen)
    aliens.add(alien)
    stats.generate_alien_number += 1

def play_bgm(stats):
    pygame.mixer.music.load('sounds/background music' + str(stats.which % len(stats.ai_settings.play_list)) + '.mp3')
    pygame.mixer.music.play(loops=100,start=0)

def play_last(stats):
    stats.which -= 1
    pygame.mixer.music.stop()
    play_bgm(stats)

def play_next(stats):
    stats.which += 1
    pygame.mixer.music.stop()
    play_bgm(stats)

def play_die():
    pygame.mixer.music.load('sounds/die music.mp3')
    pygame.mixer.music.play(loops=100,start=90.6)
    sleep(2)

if __name__=='__main__':
    # pygame.mixer.init()
    # play_die()
    print(-0%11)
    