import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import random

def ship_move(event,ship,state):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = state
    elif event.key == pygame.K_LEFT:
        ship.moving_left = state
    elif event.key == pygame.K_UP:
        ship.moving_up = state
    elif event.key == pygame.K_DOWN:
        ship.moving_down = state

def check_keydown_events(event,ai_settings,screen,sb,stats,ship,aliens,bullets,state):
    '''响应按键'''
    ship_move(event,ship,state)
    if event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(ai_settings,screen,ship,bullets)
        else:
            reset_game(ai_settings,screen,stats,sb,ship,aliens,bullets)
    elif event.key == pygame.K_p:
        stats.game_active = not stats.game_active
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    '''如果还没有达到子弹数量限制，就发射一颗子弹'''
    # 创建一颗子弹，并将其加入到编组 Bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship,state):
    '''响应松开'''
    ship_move(event,ship,state)

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    '''响应按键和鼠标事件'''
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,sb,stats,ship,aliens,bullets,True)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship,False)

def reset_game(ai_settings,screen,stats,sb,ship,aliens,bullets):
    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏信息
    stats.reset_stats()
    stats.game_active = True
    ai_settings.initialize_dynamic_settings()

    # 重置记分牌图像
    sb.prep_level()
    sb.prep_ships()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings,screen,sb,ship,aliens)
    ship.center_ship()

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    '''在玩家点击 Play 时开始游戏'''
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        reset_game(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''响应子弹与外星人的碰撞'''
    # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    # 计分
    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)
            sb.prep_score()
            check_highest_score(stats,sb)

    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人
        bullets.empty()
        # 提高游戏等级
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,sb,ship,aliens)

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    # 更新子弹的位置
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
    '''有外星人到达边界采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人向下移，并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        # 将 ships_left 减 1
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,sb,ship,aliens)
        ship.center_ship()

        # 暂停 0.5 秒
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            # ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            # break
            aliens.remove(alien)

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 删除已经消失的外星人
    # for alien in aliens.copy():
    #     if alien.rect.top >= ai_settings.screen_height:
    #         aliens.remove(alien)

    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
        # print('Ship hit!!!')
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    '''更新屏幕上的图像'''
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blitme()
    # alien.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.prep_score()
    sb.prep_ships()
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def get_number_aliens_x(ai_settings,alien_width):
    '''计算每行可容纳多少个外星人'''
    # 外星人的间距为外星人宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = ai_settings.screen_height - max([alien_height,ship_height])
    number_rows = int(available_space_y / alien_height)
    return number_rows

def create_alien(ai_settings,screen,sb,ship,aliens,alien_number,row_number):
    '''创建一个外星人并添加到当前行'''
    alien = Alien(ai_settings,screen)
    # alien_width = alien.rect.width
    # alien.x = alien_width + 2 * alien_width * alien_number
    alien.x = random.randint(0,ai_settings.screen_width - alien.rect.width)
    alien.rect.x = alien.x
    # alien.rect.y = alien.rect.height * row_number
    alien.y = random.randint(sb.score_rect.height + sb.level_rect.height,ai_settings.screen_height - 10 * ship.rect.height)
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings,screen,sb,ship,aliens):
    '''创建外星人群'''
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # alien = Alien(ai_settings,screen) # 为了获取宽度，创建一个对象
    # number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    # number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    # 创建外星人并加入到当前行
    # for row_number in range(number_rows):
    #     for alien_number in range(number_aliens_x):
    #         create_alien(ai_settings,screen,aliens,alien_number,row_number)
    for row_number in range(3):
        for alien_number in range(3):
            create_alien(ai_settings,screen,sb,ship,aliens,alien_number,row_number)

def check_highest_score(stats,sb):
    '''检测是否诞生了新的最高得分'''
    if stats.score > stats.highest_score:
        stats.highest_score = stats.score
        sb.prep_highest_score()
