import math

class ShapeProfile():
    name:str
    area:float
    bending_MOI:float

class ShapeProfileArea(ShapeProfile):
    def __init__(self, name = "default_area_profile", area:float = 1, bending_MOI:float = 1):
        self.name = name
        self.area = area
        self.bending_MOI = bending_MOI

class ShapeProfileRoundTubing(ShapeProfile):
    def __init__(self, name = "default_round_tubing", radius = 1, thickness = 0.1):
        self.name = name
        self.radius = radius
        self.thickness = thickness

        self.area = math.pi * (self.radius**2 - (self.radius-self.thickness)**2)
        self.bending_MOI = (math.pi/64) * ((2*radius)**4 - (2*(radius-thickness))**4)

class ShapeProfileRoundBar(ShapeProfileRoundTubing):
    def __init__(self, name = "default_round_bar", radius = 1):
        super().__init__(self, name=name, thickness=radius, radius=radius)

class ShapeProfileSquareTubing(ShapeProfile):
    def __init__(self, name = "default_square_tubing", width = 1, height = 1, w_thickness = 0.1, h_thickness = 0.1):
        self.width = width
        self.height = height
        self.w_thickness = w_thickness
        self.h_thickness = h_thickness

        self.area = width*h_thickness + height*w_thickness - h_thickness*w_thickness
        self.bending_MOI = (width * (height**3))/12 - ((width-w_thickness) * ((height-h_thickness)**3))/12

class ShapeProfileSquareBar(ShapeProfileSquareTubing):
    def __init__(self, name = "default_square_bar", width = 1, height = 1):
        super().__init__(self, name=name, width = width, height = height, h_thickness=height, w_thickness=width)

# class ShapeProfileTBeam(ShapeProfile):

# class ShapeProfileIBeam(ShapeProfile):