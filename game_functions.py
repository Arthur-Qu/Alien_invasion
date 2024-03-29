import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien
# 重构
# def check_events(ship):
	# """相应案件和鼠标事件"""
	# for event in pygame .event.get():
		# if event.type == pygame.QUIT:
			# sys.exit()
		
		# elif event.type == pygame.KEYDOWN:
			# if event.key == pygame.K_RIGHT:
				# ship.moving_right = True
			# elif event.key == pygame.K_LEFT:
				# ship.moving_left = True
		# elif event.type == pygame.KEYUP:
			# if event.key == pygame.K_RIGHT:
				# ship.moving_right = False
			# elif event.key == pygame.K_LEFT:
				# ship.moving_left = False
				# # 向右移动飞船
				# ship.rect.centerx += 1

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	# 相应按键
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		# # 创建一个子弹，并将其加入到bullets中(创建独立函数）
		# if len(bullets) < ai_settings.bullets_allowed:
			# new_bullet = Bullet(ai_settings,screen,ship)
			# bullets.add(new_bullet)
		
def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
		bullets):
	"""相应案件和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
			# 向右移动飞船
			ship.rect.centerx += 1
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,
					ship,aliens,bullets,mouse_x,mouse_y)
	
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
		bullets,mouse_x,mouse_y):
	"""在玩家单击play时开始游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#重置游戏设置
		ai_settings.initialize_dynamic_settings()
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		
		# 重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，并将飞船放到屏幕最底端中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
	play_button):
	"""更新屏幕上的图像，并切换到新屏幕上"""
	# 每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
			bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	# 显示得分
	sb.show_score()
	
	# 如果游戏处于非活动状态，就绘制play按键
	if not stats.game_active:
		play_button.draw_button()
		
	# 让最近绘制的屏幕可见
	pygame.display.flip()
	
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""更新子弹位置，并删除子弹"""
	# 更新子弹位置
	bullets.update()
	# 删除消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	# 检查子弹是否删除，删除返回0
	# print(len(bullets))
	check_bullet_alien_collisons(ai_settings,screen,stats,sb,ship,
			aliens,bullets)
	# 检查是否有子弹击中外星人
	# 如果有，删除子弹和相应的外星人
	
def check_bullet_alien_collisons(ai_settings,screen,stats,sb,ship,
		aliens,bullets):
	"""相应子弹与外星人碰撞"""
	# 删除发生碰撞的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
		# stats.score += ai_settings.alien_points
		# sb.prep_score()
	if len(aliens) == 0:
		# 删除现有子弹并新建一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		
		# 提高等级
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings,screen,ship,aliens)
	
def fire_bullet(ai_settings,screen,ship,bullets):
	"""如果还没达到限制，就发射一颗子弹"""
	# 创建一个子弹，并将其加入到bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
		
# def create_fleet(ai_settings,screen,aliens):
	# """创建外星人群"""
	# # 创建一个外星人，并计算一行容纳多少外星人
	# # 外星人间距为外星人宽度
	# alien = Alien(ai_settings,screen)
	# alien_width = alien.rect.width
	# available_space_x = ai_settings.screen_width - 2 * alien_width
	# number_aliens_x = int(available_space_x/(2 * alien_width))
	
	# 创建第一行外星人
	# for alien_number in range(number_aliens_x):
		# # 创建一个外星人并将其加入到当前行
		# alien = Alien(ai_settings,screen)
		# alien.x = alien_width + 2*alien_width*alien_number
		# alien.rect.x = alien.x
		# aliens.add(alien)
		
def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行能容纳多少外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x/(2 * alien_width))
	return number_aliens_x

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def create_fleet(ai_settings,screen,ship,aliens):
	"""创建外星人群"""
	# 创建一个外星人，并计算一行容纳多少外星人
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,
		alien.rect.height)
	# 创建外星人群
	for row_number in range(number_rows - 3):
		for alien_number in range(number_aliens_x):
			creat_alien(ai_settings,screen,aliens,alien_number,row_number)
		
def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕能容纳多少外星人"""
	available_space_y = (ai_settings.screen_height - 
		(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def check_fleet_edges(ai_settings,aliens):
	"""有外星人达到边缘时采取相应措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	"""将整群外星人下移并改变方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""检查是否有外星人到达底部"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞一样处理
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			break
	
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""更新所有外星人位置是否位于边缘，并更新外星人位置"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	# 检测外星人与飞船间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
	# 检查外星人是否达到屏幕底部
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
		
		
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""响应外星人撞到的飞船"""
	if stats.ships_left > 0:
		# 将ship_lift减1
		stats.ships_left -= 1
		
		# 更新记分牌
		sb.prep_ships()
	
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
	
		# 创建一群新的外星人，并将飞船放到屏幕最底端中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		# 暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_high_score(stats,sb):
	"""检验是否诞生了新的最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()