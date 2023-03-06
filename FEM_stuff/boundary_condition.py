class BoundaryCondition():
    id: int
    node_id: int
    dof: tuple

    def __init__(self, node_id:int, dof:tuple = (1, 1, 1), id:int = 0):
        self.id = id
        self.node_id = node_id
        self.dof = dof