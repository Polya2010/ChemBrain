class ElementInfo:
    def __init__(
        self,
        symbol,
        name,
        atomic_number,
        atomic_mass,
        group,
        period,
        type_class
    ):
        self.symbol = symbol
        self.name = name
        self.atomic_number = atomic_number
        self.atomic_mass = atomic_mass
        self.group = group
        self.period = period
        self.type_class = type_class
        self.electron_configuration = ""
        self.electronegativity_value = None
        self.melting_temperature = None
        self.boiling_temperature = None
        self.density_value = None
        self.year_of_discovery = ""
        self.discoverer = ""
        self.detailed_description = ""
        self.interesting_facts = []
        self.common_applications = []

    def setup_properties(
        self,
        electron_config,
        electronegativity,
        melting_temp,
        boiling_temp,
        density
    ):
        self.electron_configuration = electron_config
        self.electronegativity_value = electronegativity
        self.melting_temperature = melting_temp
        self.boiling_temperature = boiling_temp
        self.density_value = density

    def setup_history(
        self,
        discovery_year,
        discoverer_name,
        description_text
    ):
        self.year_of_discovery = discovery_year
        self.discoverer = discoverer_name
        self.detailed_description = description_text

    def setup_additional(
        self,
        fact_list,
        application_list
    ):
        self.interesting_facts = fact_list
        self.common_applications = application_list
