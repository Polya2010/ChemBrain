class ElementInfo:
    def __init__(self, symbol, name, atomic_number, atomic_weight, group, period, category):
        self.symbol = symbol
        self.name = name
        self.atomic_number = atomic_number
        self.atomic_weight = atomic_weight
        self.group = group
        self.period = period
        self.category = category
        
        self.electron_config = "Не указано"
        self.electronegativity = "Не указано"
        self.melting_point = "Не указано"
        self.boiling_point = "Не указано"
        self.density = "Не указано"
        
        self.discovery_year = "Не указано"
        self.discoverer = "Не указано"
        self.description = "Описание элемента"
        
        self.facts = ["Информация отсутствует"]
        self.uses = ["Информация отсутствует"]
    
    def setup_properties(self, electron_config, electronegativity, melting_point, boiling_point, density):
        self.electron_config = electron_config
        self.electronegativity = electronegativity
        self.melting_point = melting_point
        self.boiling_point = boiling_point
        self.density = density
    
    def setup_history(self, discovery_year, discoverer, description):
        self.discovery_year = discovery_year
        self.discoverer = discoverer
        self.description = description
    
    def setup_additional(self, facts, uses):
        self.facts = facts
        self.uses = uses
    
    def __str__(self):
        return f"{self.name} ({self.symbol}) - Атомный номер: {self.atomic_number}"
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
            'atomic_number': self.atomic_number,
            'atomic_weight': self.atomic_weight,
            'group': self.group,
            'period': self.period,
            'category': self.category,
            'electron_config': self.electron_config,
            'electronegativity': self.electronegativity,
            'melting_point': self.melting_point,
            'boiling_point': self.boiling_point,
            'density': self.density,
            'discovery_year': self.discovery_year,
            'discoverer': self.discoverer,
            'description': self.description,
            'facts': self.facts,
            'uses': self.uses
        }