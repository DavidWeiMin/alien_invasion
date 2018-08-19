import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from item import Item
import random
from time import time

#%% check events
def check_events(ai_settings,screen,stats,ship,aliens,items):
    '''响应按键和鼠标事件'''
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,ship,aliens,True,items)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,stats,ship,False)

def check_keydown_events(event,ai_settings,screen,stats,ship,aliens,state,items):
    '''响应按键'''
    stats.key += 1
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(stats,ship)
        else:
            reset_game(ai_settings,stats,ship,aliens,items)
            # stats.player_name = input('please enter your name:\n')#remove vsc运行请删除此行
            # sleep(3)#remove vsc运行请删除此行
            stats.which = random.choice(ai_settings.play_list)
            play_bgm(stats)
    elif ship_move(event,stats,ship,state):
        pass
    elif event.key == pygame.K_1:
        if stats.item_[1] - len(ai_settings.timekeep[1]) > 0:
            stats.item_[1] -= 1
            stats.killed_number += len(aliens)
            stats.score += len(aliens) * ai_settings.alien_points
            empty(aliens,ship.bullets)
            ask_item(ai_settings,screen,stats,items)
            ask_increase_level(ai_settings,stats)
    elif event.key == pygame.K_2:
        if stats.item_[2] - len(ai_settings.timekeep[2]) > 0:
            ai_settings.effect_time *= 2
            ai_settings.timekeep[2].append((time()))
    elif event.key == pygame.K_3:
        if stats.item_[3] - len(ai_settings.timekeep[3]) > 0:
            ai_settings.bullet_energy = False # 普通子弹升级为高能子弹
            ai_settings.timekeep[3].append((time()))
    elif event.key == pygame.K_4:
        if stats.item_[4] - len(ai_settings.timekeep[4]) > 0:
            ai_settings.ship_bullet_width *= 8 # 飞船子弹宽度乘以 8
            ai_settings.timekeep[4].append((time()))
    elif event.key == pygame.K_5:
        if stats.item_[5] - len(ai_settings.timekeep[5]) > 0:
            ai_settings.timekeep[5].append(time())
    elif event.key == pygame.K_6:
        if stats.item_[6] - len(ai_settings.timekeep[6]) > 0:
            ai_settings.alien_drop_speed /= 2 # 外星人下降速度除以 2
            ai_settings.item_drop_speed /= 2 # 外星人下降速度除以 2
            ai_settings.timekeep[6].append((time()))
    elif event.key == pygame.K_p:#todo 修复bug：暂停或死亡时道具效果仍在倒计时，应当停止计时
        if stats.game_active:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        stats.game_active = not stats.game_active
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

def fire_bullet(stats,ship):
    '''如果还没有达到子弹数量限制，就发射一颗子弹'''
    # 创建一颗子弹，并将其加入到编组 Bullets 中
    if len(ship.bullets) < ship.bullets_allowed:
        ship.bullets.add(Bullet(ship))
        stats.generate_bullet_number += 1

def reset_game(ai_settings,stats,ship,aliens,items):
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏信息
    stats.reset_stats()
    stats.game_active = True
    Item.count = 0
    ai_settings.initialize_dynamic_settings()
    empty(aliens,ship.bullets,items)
    
    # 将飞船放到屏幕底端中央
    ship.center_ship()

def play_bgm(stats):
    pygame.mixer.music.load('sounds/background music' + str(stats.which % len(stats.ai_settings.play_list)) + '.mp3')
    pygame.mixer.music.play(loops=-1,start=0)

def ship_move(event,stats,ship,state):
    if event.key == pygame.K_LEFT:
        stats.key_left += 1
        ship.moving_left = state
    elif event.key == pygame.K_RIGHT:
        stats.key_right += 1
        ship.moving_right = state
    elif event.key == pygame.K_UP:
        stats.key_up += 1
        ship.moving_up = state
    elif event.key == pygame.K_DOWN:
        stats.key_down += 1
        ship.moving_down = state
    else:
        return False
    return True

def empty(*floatings):
    '''清空传入的悬浮物'''
    [floating.empty() for floating in floatings]

def play_last(stats):
    stats.which -= 1
    pygame.mixer.music.stop()
    play_bgm(stats)

def play_next(stats):
    stats.which += 1
    pygame.mixer.music.stop()
    play_bgm(stats)

def check_keyup_events(event,stats,ship,state):
    '''响应松开'''
    ship_move(event,stats,ship,state)

#%% update ship,aliens,items,bullets
def update(ai_settings,screen,stats,ship,aliens,items):
    ship.update_move()
    ship.update_bullets()

    update_direction(ai_settings,aliens)
    update_delete(aliens)
    for alien in aliens:
        alien.update_move()
        alien.update_bullets()
        
    update_direction(ai_settings,items)
    update_delete(items)
    for item in items:
        item.update_move()

    update_aliens(ai_settings,screen,stats,aliens)
    update_items(ai_settings,screen,stats,items)

def update_delete(floatings):
    '''检查是否有物体到达了屏幕底端'''
    for floating in floatings:
        if floating.rect.top >= floating.screen_rect.bottom:
            floatings.remove(floating)

def update_direction(ai_settings,floatings):
    '''有外星人到达边界采取相应的措施'''
    for floating in floatings:
        if floating.check_edges():
            if floatings.sprites()[0].__class__.__name__=='Alien':
                ai_settings.alien_direction *= -1
            elif floatings.sprites()[0].__class__.__name__=='Item':
                ai_settings.item_direction *= -1
            break

def update_items(ai_settings,screen,stats,items):
    '''更新道具位置，方向，消失,拾取道具与道具失效检测'''
    # 道具失效检测
    for i in ai_settings.item_list[2:]:
       if ai_settings.timekeep[i] and (time() - ai_settings.timekeep[i][0] >= ai_settings.effect_time):
            stats.item_[i] -= 1
            ai_settings.timekeep[i].pop(0)
            if i == 2:
                ai_settings.effect_time /= 2
            elif i == 3:
                ai_settings.bullet_energy = True
            elif i == 4:
                ai_settings.ship_bullet_width /= 8
            elif i == 5:
                pass
            elif i == 6:
                ai_settings.alien_drop_speed *= 2
                ai_settings.item_drop_speed /= 2 # 外星人下降速度除以 2

def update_aliens(ai_settings,screen,stats,aliens):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    # 外星人射击
    for alien in aliens:
        if time() - alien.fire_time > ai_settings.fire_interval:
            alien.bullets.add(Bullet(alien))
            alien.fire_time = time()
    
    if time() - stats.create_alien_time > ai_settings.generate_interval / ai_settings.speedup_scale ** 3.5:
        stats.create_alien_time = time()
        create_alien(ai_settings,screen,stats,aliens)

def create_alien(ai_settings,screen,stats,aliens):
    '''创建外星人'''
    alien = Alien(ai_settings,screen)
    aliens.add(alien)
    stats.generate_alien_number += 1

def display(ai_settings,screen,stats,ship,aliens,items,sb,play_button):
    '''更新屏幕上的图像'''
    screen.fill(ai_settings.bg_color)

    # # 在飞船和外星人后面重绘所有子弹
    [ship_bullet.draw_bullet() for ship_bullet in ship.bullets]
    for alien in aliens:
        [alien_bullet.draw_bullet() for alien_bullet in alien.bullets]
            
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

#%% check collisions
def check_collisions(ai_settings,screen,stats,ship,aliens,items):
    check_bullets_ship_collisions(ai_settings,stats,ship,aliens)
    check_bullets_aliens_collisions(ai_settings,screen,stats,ship.bullets,aliens,items)
    check_ship_aliens_collisions(ai_settings,stats,ship,aliens)
    check_ship_items_collisions(ai_settings,stats,ship,items)
    check_bullets_bullets_collisions(ai_settings,ship,aliens)

def check_bullets_ship_collisions(ai_settings,stats,ship,aliens):
    collisions = False
    for alien in aliens:
        collisions = pygame.sprite.spritecollideany(ship,alien.bullets)
        if collisions:
            break
    if collisions and (time() - stats.die_time[-1] > ai_settings.unstoppable_time):
        if len(ai_settings.timekeep[5]) == 0 or (time() - ai_settings.timekeep[5][0] > ai_settings.effect_time):
            ship.hit(stats)

def check_bullets_aliens_collisions(ai_settings,screen,stats,bullets,aliens,items):
    '''响应子弹与外星人的碰撞'''
    # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,ai_settings.bullet_energy,True)

    # 计分
    if collisions:
        for aliens_hit in collisions.values():
            stats.killed_number += len(aliens_hit)
            stats.bullet_killed_number += len(aliens_hit)
            stats.score += ai_settings.alien_points * len(aliens_hit)
            ask_item(ai_settings,screen,stats,items)
            ask_increase_level(ai_settings,stats)

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

def check_ship_aliens_collisions(ai_settings,stats,ship,aliens):
    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens) and (time() - stats.die_time[-1] > ai_settings.unstoppable_time):
        if len(ai_settings.timekeep[5]) == 0 or (time() - ai_settings.timekeep[5][0] > ai_settings.effect_time):
            ship.hit(stats)

def check_ship_items_collisions(ai_settings,stats,ship,items):
    # 道具拾取
    if pygame.sprite.spritecollideany(ship,items):
        item = items.sprites()[0]
        for i in ai_settings.item_list:
            if item.kind == i:
                stats.item_cum[i] += 1
                stats.item_[i] += 1
                break
        items.remove(item)

def check_bullets_bullets_collisions(ai_settings,ship,aliens):
    for alien in aliens:
        pygame.sprite.groupcollide(ship.bullets,alien.bullets,ai_settings.bullet_energy,True)
