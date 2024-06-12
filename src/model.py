import numpy as np
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.callbacks as callbacks

def build_model(conv_size, conv_depth):
    model = models.Sequential()

    # adding convolution layers
    model.add(layers.Conv2D(conv_size, kernel_size=3, padding='same', input_shape=(12,8,8), activation='relu'))
    for _ in range(conv_depth):
        model.add(layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, 'relu'))
    model.add(layers.Dense(1, 'sigmoid'))
    model.compile(loss='mean_squared_error')

    return model

def get_dataset():
    dataset = np.load("dataset.npz")
    b, v = dataset['b'], dataset['v']
    b = b[:, :12, :, :]
    print(b)
    v = np.asarray(v / abs(v).max() / 2 + 0.5, dtype=np.float32)
    return b, v

def train():
    X_train, y_train = get_dataset()
    print(X_train.shape)
    print(y_train.shape)

    model = build_model(32,4)
    model.summary()
    model.fit(
        X_train,
        y_train,
        epochs=1000,
        verbose=1,
        validation_split=0.1,
        callbacks=[callbacks.ReduceLROnPlateau(monitor="loss", patience=10),
                   callbacks.EarlyStopping(monitor="loss", patience=15)]
    )

    model.save('model.h5')



if __name__ == "__main__":
    train()