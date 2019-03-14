import pygame
import random
from pygame.sprite import Sprite
import datetime

class Game_Boss(Sprite):
	def __init__(self,game_settings,screen,player):
		super().__init__()
		self.pos_i = 0.0
		self.pos_j = 0.0
		self.pos_k = 0.0
		self.game_settings = game_settings
		self.screen = screen
		self.image = pygame.image.load('images/boss/left/move/bz1.png')
		self.rect = self.image.get_rect()
		self.rect.x = self.game_settings.screen_width-self.rect.width
		self.rect.bottom = 370
		self.x = float(self.rect.x)#敌人的位置
		self.speed_factor = self.game_settings.enemy_speed_factor
		self.boss_start_Y = 370#开始boss人物的高度
		self.boss_Y = self.boss_start_Y
		self.attack1_order = 0
		self.player = player
		self.mx = self.x

	def blitme(self):
		self.screen.blit(self.image,self.rect)

	def update(self):
		if self.game_settings.boss_alive:
			self.direction()
			self.rand_att()
			if  self.game_settings.attack_1:
				if self.game_settings.boss_direction == 1:
					self.attack_1('left')
				else:
					self.attack_1('right')

			elif self.game_settings.attack_2:
				if self.game_settings.boss_direction == 1:
					self.attack_2('left')
				else:
					self.attack_2('right')

			elif self.game_settings.boss_jump:
				self.jump()

			elif self.game_settings.boss_run:
				if self.game_settings.boss_direction == 1:
					self.run('left')
				else:
					self.run('right')
					
			elif self.player.rect.centerx > self.rect.x:
				self.x += self.speed_factor
				self.rect.x = self.x
				self.move('right')
			elif self.player.rect.centerx < self.rect.x:
				self.x -= self.speed_factor
				self.rect.x = self.x
				self.move('left')
		else:
			self.boom()
			self.game_settings.game_win = True

	def rand_att(self):
		random.seed(datetime.datetime.now())
		if self.game_settings.attack_1 == False and self.game_settings.attack_2 == False and self.game_settings.boss_jump == False and self.game_settings.boss_run == False:
			self.rand_num = random.randint(1,70)
			if self.rand_num == 1:
				self.game_settings.attack_1 = True
			elif self.rand_num == 2:
				self.game_settings.attack_2 = True
			elif self.rand_num == 3:
				self.game_settings.boss_jump =True
			elif self.rand_num == 4:
				self.game_settings.boss_run = True


	def attack_1(self,direction):
		self.rect.bottom = 410#做此动作时人物的位置
		self.names1 = locals()
		self.players1 = []
		for self.j in range(0,34):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/boss/'+direction+'/attack_1/%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_i)]
		self.pos_i += 0.5
		if self.pos_i >= 34.0 :#循环完成后:
			self.pos_i = 0.0
			self.game_settings.attack_1 = False

	def attack_2(self,direction):
		self.rect.bottom = 355
		self.names1 = locals()
		self.players1 = []
		for self.j in range(0,30):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/boss/'+direction+'/attack_2/%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_i)]
		self.pos_i += 0.5
		if self.pos_i >= 30:
			self.pos_i = 0.0
			self.game_settings.attack_2 = False

	def move(self,direction):#循环图片
		self.rect.bottom = 370
		self.names1 = locals()
		self.players1 = []
		for self.j in range(1,7):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/boss/'+direction+'/move/bz%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_i)]
		self.pos_i += 0.1#图片变化速率
		if self.pos_i > 6.0:#敌人bag有4个动作
			self.pos_i = 0.0

	def run(self,direction):
		self.rect.bottom = 400
		self.names1 = locals()
		self.players1 = []
		for self.j in range(0,6):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/boss/'+direction+'/run/%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_i)]
		self.pos_i += 0.3
		if self.pos_i >= 6:
			self.pos_i = 0.0
			self.game_settings.boss_run = False

		if self.player.rect.centerx > self.rect.x :#or self.x < self.mx:
			self.x += 6
			self.rect.x = self.x
		elif self.player.rect.centerx < self.rect.x :#or self.x > self.mx:
			self.x -= 6
			self.rect.x = self.x
			
	def jump(self):			
		self.rect.bottom = self.boss_Y
		if self.game_settings.boss_jump_vel < 0:
			self.game_settings.boss_jump_vel += 0.6#跳跃上升的增加的速率
		elif self.game_settings.boss_jump_vel > 0:
			self.game_settings.boss_jump_vel += 0.8#跳跃下降增加的速率
		self.boss_Y += self.game_settings.boss_jump_vel
		if self.boss_Y > self.boss_start_Y:
			self.game_settings.boss_jump = False#结束跳跃
			self.boss_Y = self.boss_start_Y
			self.game_settings.boss_jump_vel = -12.0#恢复跳跃开始的速度

		if self.player.rect.centerx > self.rect.x :#or self.x < self.mx:
			self.x += self.speed_factor
			self.rect.x = self.x
		elif self.player.rect.centerx < self.rect.x :#or self.x > self.mx:
			self.x -= self.speed_factor
			self.rect.x = self.x

		self.names1 = locals()
		self.players1 = []
		for self.j in range(3,10):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/boss/left/jump/%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_j)]
		self.pos_j += 0.4#跳跃旋转速率
		if self.pos_j >= 7:#跳跃有7个动作
			self.pos_j = 0.0

	def direction(self):
		if self.player.rect.centerx > self.rect.x:
			self.game_settings.boss_direction = -1
		else:
			self.game_settings.boss_direction = 1


	def boom(self):
		self.names1 = locals()
		self.players1 = []
		for self.j in range(1,4):
			self.names1['player_image%s' %self.j] = pygame.image.load('images/boss/boom%s.png' %self.j)
			self.players1.append(self.names1['player_image%s' %self.j])
		self.image = self.players1[int(self.pos_k)]
		self.pos_k += 0.05
		if self.pos_k >= 3.0:
			#self.game_settings.boom_end = True
			self.game_settings.boss_boom_end = True


 	
 	