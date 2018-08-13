import sys
import pygame
from shipbullet import ShipBullet
from alienbullet import AlienBullet
from alien import Alien
from time import sleep
from item import Item
import random
from time import time

def ship_move(event,stats,ship,state):
    if event.key == pygame.K_RIGHT:
        stats.key_right += 1
        ship.moving_right = state
    elif event.key == pygame.K_LEFT:
        stats.key_left += 1
        ship.moving_left = state
    elif event.key == pygame.K_UP:
        stats.key_up += 1
        ship.moving_up = state
    elif event.key == pygame.K_DOWN:
        stats.key_down += 1
        ship.moving_down = state

def item_effect(event,ai_settings,screen,stats,aliens,ship_bullets,items):
    if event.key == pygame.K_1 and stats.item_[1] - len(ai_settings.timekeep[1]) > 0:
        stats.item_[1] -= 1
        stats.killed_number += len(aliens.sprites())
        stats.score += len(aliens.sprites()) * ai_settings.alien_points
        empty(aliens,ship_bullets)
        ask_item(ai_settings,screen,stats,items)
        ask_increase_level(ai_settings,stats)
    elif event.key == pygame.K_2 and stats.item_[2] - len(ai_settings.timekeep[2]) > 0:
        ai_settings.effect_time *= 2
        ai_settings.timekeep[2].append((time()))
    elif event.key == pygame.K_3 and stats.item_[3] - len(ai_settings.timekeep[3]) > 0:
        ai_settings.energy_bullet = False # 普通子弹升级为高能子弹
        ai_settings.timekeep[3].append((time()))
    elif event.key == pygame.K_4 and stats.item_[4] - len(ai_settings.timekeep[4]) > 0:
        ai_settings.ship_bullet_width *= 8 # 飞船子弹宽度乘以 8
        ai_settings.timekeep[4].append((time()))
    elif event.key == pygame.K_5 and stats.item_[5] - len(ai_settings.timekeep[5]) > 0:
        ai_settings.timekeep[5].append(time())
    elif event.key == pygame.K_6 and stats.item_[6] - len(ai_settings.timekeep[6]) > 0:
        ai_settings.floating_drop_speed /= 2 # 外星人下降速度除以 2
        ai_settings.timekeep[6].append((time()))

def ask_item(ai_settings,screen,stats,items):
    '''判断是否奖励道具'''
    if stats.killed_number // ai_settings.award_base > Item.count:
        item = Item(ai_settings,screen)
        item.caculate_number()
        items.add(item)

def ask_increase_level(ai_settings,stats):
    '''判断是否提升游戏等级'''
    if stats.killed_number // ai_settings.level_base > stats.level:
        if stats.level < 20:
            ai_settings.increase_speed()
            stats.level += 1

def empty(*args):
    '''清空传入的编组'''
    [i.empty() for i in args]

def check_keydown_events(event,ai_settings,screen,stats,ship,aliens,ship_bullets,state,items):
    '''响应按键'''
    stats.key += 1
    ship_move(event,stats,ship,state)
    if event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(ai_settings,screen,stats,ship,ship_bullets)
        else:
            reset_game(ai_settings,screen,stats,ship,aliens,ship_bullets,items)
            # stats.player_name = input('please enter your name:\n')#remove vsc运行请删除此行
            # sleep(3)#remove vsc运行请删除此行
            stats.which = random.choice(ai_settings.play_list)
            play_bgm(stats)
    elif event.key == pygame.K_p:
        if stats.game_active:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        stats.game_active = not stats.game_active
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_HOME:
        if stats.play_music:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        stats.play_music = not stats.play_music
    elif event.key == pygame.K_PAGEUP:
        play_last(stats)
    elif event.key == pygame.K_PAGEDOWN:
        play_next(stats)
    item_effect(event,ai_settings,screen,stats,aliens,ship_bullets,items)

def fire_bullet(ai_settings,screen,stats,ship,ship_bullets):
    '''如果还没有达到子弹数量限制，就发射一颗子弹'''
    # 创建一颗子弹，并将其加入到编组 Bullets 中
    if len(ship_bullets) < ai_settings.ship_bullets_allowed:
        new_bullet = ShipBullet(ai_settings,screen,ship)
        ship_bullets.add(new_bullet)
        stats.generate_bullet_number += 1

def check_keyup_events(event,stats,ship,state):
    '''响应松开'''
    ship_move(event,stats,ship,state)

def check_events(ai_settings,screen,stats,play_button,ship,aliens,ship_bullets,items):
    '''响应按键和鼠标事件'''
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,ship,aliens,ship_bullets,True,items)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,stats,ship,False)

def reset_game(ai_settings,screen,stats,ship,aliens,ship_bullets,items):
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏信息
    stats.reset_stats()
    stats.game_active = True
    Item.count = 0
    ai_settings.initialize_dynamic_settings()

    # 清空外星人列表、飞船子弹列表和道具列表
    empty(aliens,ship_bullets,items)
    

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    stats.create_alien_time = time()
    create_fleet(ai_settings,screen,stats,aliens)
    ship.center_ship()

def check_bullet_alien_collisions(ai_settings,screen,stats,ship,aliens,ship_bullets,items):
    '''响应子弹与外星人的碰撞'''
    # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(ship_bullets,aliens,ai_settings.energy_bullet,True)

    # 计分
    if collisions:
        for aliens_hit in collisions.values():
            stats.killed_number += len(aliens_hit)
            stats.bullet_killed_number += len(aliens_hit)
            stats.score += ai_settings.alien_points * len(aliens_hit)
            ask_item(ai_settings,screen,stats,items)
            ask_increase_level(ai_settings,stats)

def update_ship_bullets(ai_settings,screen,stats,sb,ship,aliens,ship_bullets,items):
    '''更新飞船子弹的位置以及删除屏幕外的子弹'''
    # 更新子弹的位置
    ship_bullets.update()

    # 删除屏幕外的子弹
    for ship_bullet in ship_bullets.copy():
        if ship_bullet.rect.bottom <= 0:
            ship_bullets.remove(ship_bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,ship,aliens,ship_bullets,items)
    check_bullet_bullet_collisions(ai_settings,ship_bullets,aliens)

def update_alien_bullets(ai_settings,stats,ship,aliens):
    '''更新外星人子弹的位置以及删除屏幕外的子弹'''
    for alien in aliens.sprites():
        alien.alien_bullets.update()
        for alien_bullet in alien.alien_bullets.copy():
            if alien_bullet.rect.top >= ai_settings.screen_height:
                alien.alien_bullets.remove(alien_bullet)
    check_bullet_ship_collisions(ai_settings,stats,ship,aliens)

def check_bullet_ship_collisions(ai_settings,stats,ship,aliens):
    for alien in aliens.sprites():
        collisions = pygame.sprite.spritecollideany(ship,alien.alien_bullets)
        if collisions and (time() - stats.die_time[-1] > ai_settings.unstoppable_time):
            if len(ai_settings.timekeep[5]) == 0 or (time() - ai_settings.timekeep[5][0] > ai_settings.effect_time):
                ship_hit(stats)
            break

def check_bullet_bullet_collisions(ai_settings,ship_bullets,aliens):
    for alien in aliens.sprites():
        pygame.sprite.groupcollide(ship_bullets,alien.alien_bullets,ai_settings.energy_bullet,True)
                
def ship_hit(stats):
    '''响应被外星人撞到的飞船'''
    stats.die_time.append((time()))
    if stats.item_[0] > 1:
        # 将 ships_left 减 1
        stats.item_[0] -= 1
        sleep(0.5)
    else:
        pygame.mixer.music.stop()
        stats.game_over_time = time()
        stats.save_stats()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        play_die()

def update_items(ai_settings,screen,stats,ship,items):
    '''更新道具,拾取道具与道具失效'''
    if len(items.sprites()) > 0:
        items.sprites()[0].check_floating_edges(items)
        items.sprites()[0].check_floatings_bottom(items)
    items.update()
    if pygame.sprite.spritecollideany(ship,items):
        item = items.sprites()[0]
        for i in ai_settings.item_list:
            if item.kind == i:
                stats.item_cum[i] += 1
                stats.item_[i] += 1
                break
        items.remove(item)

    for i in ai_settings.item_list[2:]:
       if ai_settings.timekeep[i] and (time() - ai_settings.timekeep[i][0] >= ai_settings.effect_time):
            stats.item_[i] -= 1
            ai_settings.timekeep[i].pop(0)
            if i == 2:
                ai_settings.effect_time /= 2
            elif i == 3:
                ai_settings.energy_bullet = True
            elif i == 4:
                ai_settings.ship_bullet_width /= 8
            elif i == 5:
                pass
            elif i == 6:
                ai_settings.floating_drop_speed *= 2

def update_aliens(ai_settings,screen,stats,ship,aliens,ship_bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    alien = Alien(ai_settings,screen)
    alien.check_floating_edges(aliens)
    # 检查是否有外星人到达屏幕底端
    alien.check_floatings_bottom(aliens)
    for alien in aliens.sprites():
        if time() - alien.fire_time > ai_settings.fire_interval:
            alien.alien_bullets.add(AlienBullet(ai_settings,screen,alien))
            alien.fire_time = time()
    aliens.update()

    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens) and (time() - stats.die_time[-1] > ai_settings.unstoppable_time):
        if len(ai_settings.timekeep[5]) == 0 or (time() - ai_settings.timekeep[5][0] > ai_settings.effect_time):
            ship_hit(stats)
    
    if time() - stats.create_alien_time > ai_settings.generate_interval / ai_settings.speedup_scale ** 3.5:
        stats.create_alien_time = time()
        create_fleet(ai_settings,screen,stats,aliens)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,ship_bullets,play_button,items):
    '''更新屏幕上的图像'''
    screen.fill(ai_settings.bg_color)

    # # 在飞船和外星人后面重绘所有子弹
    [ship_bullet.draw_bullet() for ship_bullet in ship_bullets.sprites()]
    for alien in aliens.sprites():
        [alien_bullet.draw_bullet() for alien_bullet in alien.alien_bullets]
            
    ship.blitme()
    aliens.draw(screen)
    items.draw(screen)

    # 显示统计数据
    stats.stats_analysis()
    stats.check_highest_score()
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
    pygame.mixer.music.play(loops=-1,start=0)

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
    pygame.mixer.music.play(loops=-1,start=90.6)
    sleep(6)

if __name__=='__main__':
    a = {i:[] for i in range(4)}
    # print([del a[7]])
    # del b[7]
    # print(b)
    print(a[0])
    
    