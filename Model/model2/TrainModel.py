from Model.model2.Model import Model

from config import EPOCHS_COUNT


class TrainModel(Model):
	def train(self, x, y, x_val, y_val):
		model = self.get_model()

		model.fit(x,
		          y,
		          n_epoch=EPOCHS_COUNT,
		          validation_set=(x_val, y_val),
		          shuffle=True,
		          show_metric=True,
		          batch_size=32,
		          snapshot_step=10,
		          snapshot_epoch=True,
		          run_id='NvidiaModel')
		model.save(self.model_dir)
