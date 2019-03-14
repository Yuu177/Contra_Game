class Settings():
	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 750
		self.player_speed = 5
		self.jump_vel = -14.0#跳跃开始的速度,这里改动，game_player那里也要改动
		self.bullet_speed_factor = 17
		self.enemy_speed_factor = 4#屏幕滚动速度减去敌人移动速度为1（屏幕为5，敌人为4）移动时候才平滑。这里改动，enemy的update那里也要改
		self.screen_rolling = False
		self.enemy_is_alive = True
		self.boom_end = False
		self.players_limit = 3
		self.player_is_alive = True
		self.player_die_end = False
		self.boss_jump_vel = -12.0
		self.attack_1 = False
		self.attack_2 = False
		self.boss_jump = False
		self.boss_run = False
		self.boss_appear = False
		self.boss_direction = 1#1位向左，-1为向右
		self.boss_lift = 15
		self.boss_alive = True
		self.game_win = False
		self.boss_boom_end = False