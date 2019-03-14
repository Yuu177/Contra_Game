class GameStats():
	def __init__(self,game_settings):
		self.game_settings = game_settings
		self.reset_stats()

	def reset_stats(self):
		self.players_left = self.game_settings.players_limit
