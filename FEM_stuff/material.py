class Material():
    def __init__(self, name = "default_steel", youngs_modulus = 200e9, yield_strength = 250e6, density = 7850):
        self.name = name
        self.youngs_modulus = youngs_modulus
        self.yield_strength = yield_strength
        self.density = density