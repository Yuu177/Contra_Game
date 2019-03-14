import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
	def __init__(self,game_settings,screen):
		super().__init__()
		self.pos_j = 0.0
		self.pos_i = 0.0

		self.game_settings = game_settings
		self.screen = screen
		self.image = pygame.image.load('images/enemy/EL/bag1.png')
		#self.image = pygame.image.load('images/enemy/EL/bz1.png')
		self.rect = self.image.get_rect()
		self.rect.x = self.game_settings.screen_width+self.rect.width*2
		self.rect.bottom = 367
		self.x = float(self.rect.x)#敌人的位置
		self.speed_factor = self.game_settings.enemy_speed_factor

	def blitme(self):
		self.screen.blit(self.image,self.rect)

	def update(self):
		if self.game_settings.enemy_is_alive:
			if self.game_settings.screen_rolling:
				self.x -= self.speed_factor+1 #屏幕滚动速度减去敌人移动速度
				self.rect.x = self.x
			self.x -= self.speed_factor
			self.rect.x = self.x
			self.update_run_direction('EL')
		else:
			if self.game_settings.screen_rolling:
				self.x -= self.speed_factor+1 #屏幕滚动速度减去敌人移动速度
				self.rect.x = self.x
			self.boom()
		
	def boom(self):
		self.names1 = locals()
		self.players1 = []
		for self.j in range(1,3):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/enemy/boom%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_i)]
		self.pos_i += 0.1
		if self.pos_i > 2.0:
			self.game_settings.boom_end = True
			
	def update_run_direction(self,direction):#循环图片
		self.names1 = locals()
		self.players1 = []
		for self.j in range(1,5):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/enemy/'+direction+'/bag%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_j)]
		self.pos_j += 0.1#图片变化速率
		if self.pos_j > 4.0:#敌人bag有4个动作
			self.pos_j = 0.0

