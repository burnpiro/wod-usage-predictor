import tensorflow as tf
from model.create_model import get_model
from datetime import datetime
from model.data_preprocessor import generate_lstm_data
from model.config import HISTORY_SIZE
from helpers.settings import *

EVALUATION_INTERVAL = 200
EPOCHS = 2
BATCH_SIZE = 8
BUFFER_SIZE = 500
dataset_file = './data/model_input.csv'

if __name__ == '__main__':
    tensorboard_cbk = tf.keras.callbacks.TensorBoard(log_dir=f'./logs-{datetime.now().strftime("%Y%m%d-%H%M%S")}')

    checkpoint_cbk = tf.keras.callbacks.ModelCheckpoint(
        filepath='mode/weights/bikenet_weights.{epoch:02d}-{val_loss:.2f}.hdf5',
        save_best_only=False,
        monitor='val_loss',
        verbose=1
    )

    train_x, train_y, val_x, val_y, _ = generate_lstm_data(
        dataset_file,
        history_size=HISTORY_SIZE,
        index_col='timestamp',
        norm_cols=NORM_COLS,
        scale_cols=SCALE_COLS,
        adjust_cols=ADJUST_COLUMNS,
        filter_cols={
            'lat': [
                51.108004
            ],
            'lng': [
                17.039528
            ]
        },
        cat_cols=None,
        extra_columns=EXTRA_COLS
    )

    print(train_x.shape)
    print(train_x[0])

    train_data_single = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    train_data_single = train_data_single.cache().batch(BATCH_SIZE).repeat()

    val_data_single = tf.data.Dataset.from_tensor_slices((val_x, val_y))
    val_data_single = val_data_single.batch(BATCH_SIZE).repeat()

    model = get_model()
    print(model)

    model.fit(
        train_data_single,
        epochs=EPOCHS,
        steps_per_epoch=EVALUATION_INTERVAL,
        verbose=1,
        validation_data=val_data_single,
        validation_steps=50,
        callbacks=[
            tensorboard_cbk,
            checkpoint_cbk
        ]
    )

    print('done')
