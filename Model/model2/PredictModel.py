from Model.model2.Model import Model


class PredictModel(Model):
    def predict(self, image):
        model = self.get_model()
        return model.predict(image)
