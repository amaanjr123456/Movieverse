import tensorflow as tf
import tensorflow as tf
layers = tf.keras.layers
models = tf.keras.models

def build_model():
    model = models.Sequential([
        layers.Input(shape=(3,)),
        layers.Dense(9, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model