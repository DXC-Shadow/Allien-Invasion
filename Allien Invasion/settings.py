class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # self.ship_speed_factor = 1
        # self.bullet_speed_factor = 1.1
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 250, 150, 60
        self.bullets_allowed = 4
        # self.alien_speed_factor = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit = 3
        self.bomb_drop_speed = 10
        self.bomb_color = 255, 0, 0
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 3
        self.fleet_direction = 1
        self.alien_points = 50
        self.bomb_drop_speed_factor = 3

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
