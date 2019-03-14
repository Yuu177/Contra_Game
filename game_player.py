import pygame

class Game_Player():
	def __init__(self,game_settings,screen):

		self.screen = screen
		self.game_settings = game_settings
		self.image = pygame.image.load('images/PR/player.png')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		self.screen_center_pos = self.screen_rect.centerx
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = 380
		self.center = float(self.rect.centerx)
		self.moving_right = False
		self.moving_left = False
		self.player_moving = False
		self.pos_i = 0.0#跑步画面改变速度
		self.pos_j = 0.0#跳跃的改变初始速度
		self.pos_n = 0.0#射击
		self.pos_d = 0.0
		self.player_direction = 1#1为右，-1为左
		self.player_down = False
		self.player_up = False
		self.player_jump = False
		self.player_start_Y = 380#开始人物的高度
		self.player_Y = self.player_start_Y
		self.player_shooting = False

	def update(self):
		if self.game_settings.player_is_alive:
			if self.moving_right and self.rect.right < self.screen_rect.right:
				if self.game_settings.boss_appear:
					self.center += self.game_settings.player_speed
				elif self.center > self.screen_center_pos:
					self.center += 0
				else:
					self.center += self.game_settings.player_speed
			if self.moving_left and self.rect.left > 0:
				self.center -= self.game_settings.player_speed
			self.rect.centerx = self.center

			self.update_image_moving()
		else:
			self.update_die()

	def update_die(self):
		self.names = locals()
		self.players = []
		for self.i in range(1,3):
			self.names['player_image%s' %self.i] = pygame.image.load('images/PR/death%s.png' %self.i)
			self.players.append(self.names['player_image%s' %self.i])
		self.image = self.players[int(self.pos_d)]
		self.pos_d += 0.1
		if self.pos_d > 2.0:
			self.pos_d = 0.0
			self.game_settings.player_die_end = True


	def update_image_moving_direction(self,direction):#循环图片
		if self.player_shooting == True:
			self.names = locals()
			self.players = []
			for self.i in range(1,4):
				self.names['player_image%s' %self.i] = pygame.image.load('images/'+direction+'/shooting%s.png' %self.i)
				self.players.append(self.names['player_image%s' %self.i])
			self.image = self.players[int(self.pos_n)]
			self.pos_n += 0.1#射击时跑步速率
			if self.pos_n > 3.0:#射击时跑步有3个动作
				self.pos_n = 0.0
		else:
			self.names = locals()
			self.players = []
			for self.i in range(1,6):
				self.names['player_image%s' %self.i] = pygame.image.load('images/'+direction+'/player%s.png' %self.i)
				self.players.append(self.names['player_image%s' %self.i])
			self.image = self.players[int(self.pos_i)]
			self.pos_i += 0.1#跑步速率
			if self.pos_i > 5.0:#跑步有5个动作
				self.pos_i = 0.0

	def update_image_jump(self,direction):#循环图片
		if self.game_settings.player_is_alive:
			if self.player_jump == True:
				self.names1 = locals()
				self.players1 = []
				for self.j in range(1,5):
					self.names1['player_image%s' %self.j] = pygame.image.load('images/'+direction+'/jump%s.png' %self.j)
					self.players1.append(self.names1['player_image%s' %self.j])
				self.image = self.players1[int(self.pos_j)]
				self.pos_j += 0.3#跳跃旋转速率
				if self.pos_j > 4.0:#跳跃有4个动作
					self.pos_j = 0.0
		else:
			self.update_die()


	def update_image_moving(self):
		if self.player_moving:
			if self.moving_right:
				self.update_image_moving_direction('PR')#PR是向右的图片
			elif self.moving_left:
				self.update_image_moving_direction('PL')

	def get_player_state(self,player_state):#检测player的状态是否为趴下，向上，跳跃等
		if self.player_direction == 1:
			self.image = pygame.image.load('images/PR/'+player_state+'.png')
		if self.player_direction == -1:
			self.image = pygame.image.load('images/PL/'+player_state+'.png')
		self.rect = self.image.get_rect()
		self.rect.centerx = self.center

	def get_player_down(self):
		self.get_player_state('down')
		self.rect.bottom = self.player_start_Y
		self.screen.blit(self.image,self.rect)

	def get_player_up(self):
		self.get_player_state('up')
		self.rect.bottom = self.player_start_Y
		self.screen.blit(self.image,self.rect)

	def get_player_jump(self):
		self.get_player_state('jump1')
		self.rect.bottom = self.player_Y
		if self.game_settings.jump_vel < 0:
			self.game_settings.jump_vel += 0.6#跳跃上升的增加的速率
		elif self.game_settings.jump_vel > 0:
			self.game_settings.jump_vel += 0.8#跳跃下降增加的速率
		self.player_Y += self.game_settings.jump_vel
		if self.player_Y > self.player_start_Y:
			self.player_jump = False
			self.player_Y = self.player_start_Y
			self.game_settings.jump_vel = -14.0#恢复跳跃开始的速度
			if self.player_direction == 1:
				self.image = pygame.image.load('images/PR/player.png')
				self.reset_player()
			if self.player_direction == -1:
				self.image = pygame.image.load('images/PL/player.png')
				self.reset_player()
		if self.player_jump == True:#判断是否处于跳跃状态来决定是否旋转跳跃的图像
			if self.player_direction == 1:
				self.update_image_jump('PR')
			if self.player_direction == -1:
				self.update_image_jump('PL')
		self.screen.blit(self.image,self.rect)

	def reset_player(self):
		self.rect = self.image.get_rect()
		self.rect.centerx = self.center
		self.rect.bottom = self.player_start_Y
		self.screen.blit(self.image,self.rect)

	def blitme(self):
		if self.player_jump:
			self.get_player_jump()
		elif self.player_down:
			self.get_player_down()
		elif self.player_up:
			self.get_player_up()
		else:
			self.reset_player()

	def revive_player(self):
		self.center = self.screen_rect.centerx
		self.game_settings.player_is_alive = True
