import sys
import pygame
from bullet import Bullet
from enemy import Enemy 
from game_boss import Game_Boss

def check_keydown_events(event,game_settings,screen,player,bullets):
	if event.key == pygame.K_k:#跳跃
		player.player_jump = True

	if event.key == pygame.K_d:#向右
		game_settings.bullet_direction = 'right' 
		if player.player_down or player.player_up:
			player.moving_right = False
		else:
			player.moving_right = True
		player.player_direction = 1	

	if event.key == pygame.K_a:#向左
		game_settings.bullet_direction = 'left'
		if player.player_down or player.player_up:
			player.moving_left = False
		else:
			player.moving_left = True
		player.player_direction = -1

	elif event.key == pygame.K_s:#向下
		player.player_down = True
		player.player_moving = False
		player.moving_left = False
		player.moving_right = False

	elif event.key == pygame.K_w:#向上
		player.player_up = True
		player.player_moving = False
		player.moving_left = False
		player.moving_right = False

	elif event.key == pygame.K_j:#射击
		new_bullet = Bullet(game_settings,screen,player)
		bullets.add(new_bullet)
		player.player_shooting = True

	elif event.key == pygame.K_p:
		sys.exit()

def check_keyup_events(event,player):
	if event.key == pygame.K_d:#右
		player.image = pygame.image.load('images/PR/player.png')
		player.moving_right = False
		player.player_moving = False
	elif event.key == pygame.K_a:#左
		player.image = pygame.image.load('images/PL/player.png')
		player.player_moving = False
		player.moving_left = False
	elif event.key == pygame.K_s:#下
		player.player_down = False
		if player.player_direction == 1:
			player.image = pygame.image.load('images/PR/player.png')
		if player.player_direction == -1:
			player.image = pygame.image.load('images/PL/player.png')
	elif event.key == pygame.K_w:#上
		player.player_up = False
		if player.player_direction == 1:
			player.image = pygame.image.load('images/PR/player.png')
		if player.player_direction == -1:
			player.image = pygame.image.load('images/PL/player.png')
	
def check_events(game_settings,screen,player,bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			player.player_moving = True
			check_keydown_events(event,game_settings,screen,player,bullets)		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,player)

def update_screen(game_settings,bg,pos_x,screen,player,bullets,enemys,boss,win_button):
	screen.blit(bg,(pos_x,0))
	for bullet in bullets.sprites():
		bullet.blit_bullet()
	"""if game_settings.boom_end:#击中敌人爆炸
		enemys.empty()
		game_settings.boom_end = False"""
	player.blitme()
	if game_settings.boss_appear:
		boss.draw(screen)
	enemys.draw(screen)

	if game_settings.game_win:
		win_button.draw_button()
	pygame.display.flip()

def update_bullet(game_settings,bullets,screen,enemys,boss):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.centerx<0 or bullet.rect.centery<0 or bullet.rect.centerx > game_settings.screen_width:
			bullets.remove(bullet)
	check_bullet_enemy_collisions(game_settings,bullets,screen,enemys)
	check_bullet_boss_collisions(game_settings,bullets,boss)
	

def check_bullet_enemy_collisions(game_settings,bullets,screen,enemys):
	if game_settings.enemy_is_alive:
		collisions = pygame.sprite.groupcollide(bullets,enemys,True,False)
	else:
		collisions = pygame.sprite.groupcollide(bullets,enemys,True,True)
	if collisions != {}:
		game_settings.enemy_is_alive = False
	if len(enemys) == 0:
		create_legion(game_settings,screen,enemys)

def check_bullet_boss_collisions(game_settings,bullets,boss):
	if game_settings.boss_alive:
		collisions = pygame.sprite.groupcollide(boss,bullets,False,True)
	else:
		collisions = pygame.sprite.groupcollide(boss,bullets,True,True)

	if collisions != {}:
		game_settings.boss_lift -= 1
	if game_settings.boss_lift == 0:
		game_settings.boss_alive = False

def create_legion(game_settings,screen,enemys):
	for enemy_number in range(1):
		game_settings.enemy_is_alive = True
		enemy = Enemy(game_settings,screen)
		enemys.add(enemy)

def update_enemys(game_settings,enemys):
	if game_settings.boss_appear == False:#判断boss是否出现，出现则不出现小兵
		enemys.update()

		for enemy in enemys.copy():
			if enemy.rect.centerx<0:
				enemys.remove(enemy)
			if game_settings.boom_end:#击中敌人爆炸
				enemys.remove(enemy)
				game_settings.boom_end = False
				game_settings.boss_appear = True

def update_player(game_settings,stats,player,enemys):
	player.update()
	if pygame.sprite.spritecollideany(player,enemys):
		player_hit(game_settings,stats,player)
	if game_settings.player_die_end == True:
		player.revive_player()
		game_settings.player_die_end = False

def player_hit(game_settings,stats,player):
	stats.players_left -= 1
	game_settings.player_is_alive = False
	
def update_boss(game_settings,boss):
	if game_settings.boss_appear:
		boss.update()
	if game_settings.boss_boom_end:
		boss.empty()

def create_boss(game_settings,screen,player,boss):
	bo = Game_Boss(game_settings,screen,player)
	boss.add(bo)