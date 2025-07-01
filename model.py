class TerraformResource:
    def __init__(self, type, name, properties, depends_on=None):
        self.type = type
        self.name = name
        self.properties = properties
        self.depends_on = depends_on if depends_on is not None else []
    
    def full_id(self):
        return f"{self.type}.{self.name}"