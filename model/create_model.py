import tensorflow as tf
from model.config import INPUT_SHAPE


def get_model(input_shape=INPUT_SHAPE):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(64, input_shape=input_shape),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop()

    model.compile(
        loss=tf.keras.losses.MeanAbsoluteError(),
        optimizer=optimizer,
        metrics=['mae', 'mse', 'accuracy', tf.keras.metrics.RootMeanSquaredError()]
    )
    return model
