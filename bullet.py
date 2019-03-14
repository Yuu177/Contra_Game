import pygame
from pygame.sprite import Sprite 

class Bullet(Sprite):

	def __init__(self,game_settings,screen,player):
		super().__init__()
		self.game_settings = game_settings
		self.player = player
		self.screen = screen
		self.image = pygame.image.load('images/bullet1.png')
		self.rect = self.image.get_rect()
		self.rect.left = player.rect.right-20#开始子弹默认往右射击
		if self.player.player_direction == -1:
			self.rect.right = player.rect.left+20
		self.rect.centery = player.rect.centery-15
		if self.player.player_down:
			self.rect.centery = player.rect.centery#调整子弹位置
		if self.player.player_up:
			self.rect.bottom = player.rect.top+20
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		self.mx = self.x#mx为保存初始x的坐标
		self.my = self.y
		self.speed_factor = game_settings.bullet_speed_factor

	def update(self):
		if self.y<self.my or self.y == self.my and self.x == self.mx and self.player.player_up:
			self.y -= self.speed_factor
			self.rect.y = self.y
		elif self.x < self.mx or self.x == self.mx and self.player.player_direction == -1:
			self.x -= self.speed_factor
			self.rect.x = self.x
		elif self.x>self.mx or self.x == self.mx:#默认为右方向
			self.x += self.speed_factor
			self.rect.x = self.x

	def blit_bullet(self):
	
		self.screen.blit(self.image,self.rect)

