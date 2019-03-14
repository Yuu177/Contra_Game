import pygame
import sys
from pygame.locals import *
from settings import Settings
from game_player import Game_Player 
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from game_boss import Game_Boss
from button import Button

def run_game():
	bg = pygame.image.load("images/map01.jpeg")
	game_settings = Settings()
	pos_x = 0#地图移动
	
	pygame.init()
	screen = pygame.display.set_mode(
		(game_settings.screen_width,game_settings.screen_height))
	pygame.display.set_caption("XiaoBai Game")
	stats = GameStats(game_settings)
	player = Game_Player(game_settings,screen)
	bullets = Group()
	boss = Group()
	enemys = Group()
	win_button = Button(game_settings,screen,"YOU WIN")
	gf.create_legion(game_settings,screen,enemys)
	gf.create_boss(game_settings,screen,player,boss)

	while True:
		pygame.mouse.set_visible(False)
		gf.check_events(game_settings,screen,player,bullets)
		gf.update_player(game_settings,stats,player,enemys)
		gf.update_bullet(game_settings,bullets,screen,enemys,boss)	
		gf.update_enemys(game_settings,enemys)	
		gf.update_boss(game_settings,boss)
		gf.update_screen(game_settings,bg,pos_x,screen,player,bullets,enemys,boss,win_button)
		
		if player.moving_right and player.center > player.screen_rect.centerx and game_settings.boss_appear == False:
			game_settings.screen_rolling = True
			pos_x -= 5#屏幕滚动速度
		else:
			game_settings.screen_rolling = False
run_game()
