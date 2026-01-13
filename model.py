class TerraformResource:
    def __init__(self, type, name, properties, references=None, depends_on=None):
        self.type = type
        self.name = name
        self.properties = properties
        self.references = references or []
        self.depends_on = depends_on or []

    def full_id(self):
        return f"{self.type}.{self.name}"
