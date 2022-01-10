import tensorflow as tf
from sklearn.datasets import fetch_openml
from sklearn.utils import shuffle
import numpy as np

import GPUtil
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

def main():
    GPUs = GPUtil.getGPUs()
    total_mem = 0
    for i in range(len(GPUs)):
        total_mem += GPUs[i].memoryTotal
    frac = 3 / total_mem

    config = ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = frac
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)

    X, y = shuffle(*fetch_openml('CIFAR_10', version=1, return_X_y=True, as_frame=False))
    # X.shape: (60000, 3072), y.shape: (60000,)
    X_train, X_test, y_train, y_test = X[:50000, :], X[50000:, :], np.asarray(y[:50000], dtype=np.int), np.asarray(y[50000:], dtype=np.int)
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(X_train.shape[1],)))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(10))
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam')

    for k in range(100):
        for i in range(100):
            layers = []
            for layer in model.get_weights():
                layers.append(np.random.normal(0, 1, layer.shape))
            model.set_weights(layers)
            eval = model.evaluate(X_train, y_train)
            print("Outer: {}, Inner: {}".format(k, i))
    print("\nDone!\n")

if __name__ == '__main__':
    main()