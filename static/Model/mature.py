class Mature:
    """
        Class to represent a mature miRNA sequence entity
        """
    def __init__(self, pre_mir_name, mature_name, three_p_or_five_p, seed):
        self.pre_mir_name = pre_mir_name
        self.mature_name = mature_name
        self.threeP_or_fiveP = three_p_or_five_p
        self.seed = seed
