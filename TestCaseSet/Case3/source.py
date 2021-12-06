import numpy as np
import tensorflow as tf

def main():
    # Encoder Network
    input_a = tf.keras.Input(shape=(10,4))
    x = tf.keras.layers.Flatten()(input_a)
    x = tf.keras.layers.Dense(100, activation='relu')(x)
    x = tf.keras.layers.Dense(20, activation='relu')(x)
    x = tf.keras.layers.Dense(10, activation='relu')(x)
    upstream_network = tf.keras.Model(input_a, x)

    # Downstream network, from merge to final prediction
    input_downstream_a = tf.keras.Input(shape = upstream_network.layers[-1].output_shape[1:])
    input_downstream_b = tf.keras.Input(shape = upstream_network.layers[-1].output_shape[1:])
    x = tf.keras.layers.subtract([input_downstream_a, input_downstream_b])
    x = tf.keras.layers.Dense(20, activation='relu')(x)
    x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    downstream_network = tf.keras.Model((input_downstream_a, input_downstream_b), x)

    # Full network
    input_full_a = tf.keras.Input(shape=(10,4))
    input_full_b = tf.keras.Input(shape=(10,4))
    intermed_a = upstream_network(input_full_a)
    intermed_b = upstream_network(input_full_b)
    res = downstream_network([intermed_a, intermed_b])
    full_network = tf.keras.Model([input_full_a, input_full_b], res)
    full_network.compile(loss='binary_crossentropy')

    # Experiment
    population = np.random.random((600, 10, 4))

    out = upstream_network.predict(population)
    indices = np.mgrid[range(population.shape[0]), range(population.shape[0])].reshape(2, -1)
    downstream_network.predict([out[indices[0]], out[indices[1]]])

if __name__ == '__main__':
    main()