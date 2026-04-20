class PowerUp:
    def __init__(self, type, duration=5):
        self.type = type
        self.duration = duration

    def apply(self, player, wallet=None):
        if self.type == "speed":
            player.speed = player.base_speed * 2
        if self.type == "shield":
            player.has_shield = True
        if self.type == "coin_multiplier":
            wallet.multiplier *= 2

    def remove(self, player, wallet=None):
        if self.type == "speed":
            player.speed = player.base_speed
        if self.type == "shield":
            player.has_shield = False
        if self.type == "coin_multiplier":
            wallet.multiplier = int(wallet.multiplier / 2)