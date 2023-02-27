
class ModelMapper():
    def __init__(self, model, toModel):
        self.model = model
        self.toModel = toModel

    def map(self):
        return self.toModel(**self.model)