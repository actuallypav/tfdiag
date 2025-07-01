class TerraformResource:
    def __init__(self, type, name, properties):
        self.type = type
        self.name = name
        self.properties = properties
        self.depends_on = []