
class ModelMapper():
    def map(self, model, toModel):
        return toModel.__dict__.update(model)
