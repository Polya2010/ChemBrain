class ChemicalElementData:
    def __init__(self, symbol, full_name, atomic_num, weight, group_num, period_num, classification):
        self.symbol = symbol
        self.full_name = full_name
        self.atomic_num = atomic_num
        self.weight = weight
        self.group_num = group_num
        self.period_num = period_num
        self.classification = classification
        self.electron_config = ""
        self.electronegativity_val = None
        self.melting_point = None
        self.boiling_point = None
        self.density_val = None
        self.discovery_year = ""
        self.discoverer_info = ""
        self.element_description = ""
        self.interesting_facts_list = []
        self.common_uses_list = []
    
    def configure_physical_properties(self, config, electro, melt, boil, density):
        self.electron_config = config
        self.electronegativity_val = electro
        self.melting_point = melt
        self.boiling_point = boil
        self.density_val = density
    
    def set_discovery_info(self, year, discoverer, description):
        self.discovery_year = year
        self.discoverer_info = discoverer
        self.element_description = description
    
    def set_additional_data(self, facts, uses):
        self.interesting_facts_list = facts
        self.common_uses_list = uses