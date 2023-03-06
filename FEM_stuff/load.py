class Load():
    id:int
    node_id: int
    load_tuple: tuple

    def __init__(self, node_id:int, load_tuple:tuple, id:int = 0):
        self.id = id
        self.node_id = node_id
        self.load_tuple = load_tuple