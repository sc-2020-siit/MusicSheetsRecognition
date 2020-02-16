from tensorflow_core.python.keras.callbacks import ModelCheckpoint, LambdaCallback

from model import create_model
from sequence_train import SequenceFactory


def train_network(model, train_generator, val_generator):
    weights_path = "weights-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(weights_path, monitor='loss', verbose=0, save_best_only=True, mode='min')
    batch_log = LambdaCallback(on_batch_end=batch_output)
    callbacks_list = [checkpoint, batch_log]

    model.fit_generator(train_generator, epochs=256, callbacks=callbacks_list, validation_data=val_generator,
                        validation_freq=4)


def batch_output(batch, logs):
    print('Finished batch: ' + str(batch))
    print(logs)


if __name__ == '__main__':
    sequence_factory = SequenceFactory('data/primus_dataset', 'data/train.txt',
                                       'data/vocabulary_semantic.txt',
                                       16, 128, 1, False, 0.1)
    model = create_model(4, sequence_factory.vocabulary_size)
    train_sequence = sequence_factory.get_training_sequence()
    val_sequence = sequence_factory.get_validation_sequence()
    train_network(model, train_sequence, val_sequence)
