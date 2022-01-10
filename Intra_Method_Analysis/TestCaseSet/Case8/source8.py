import numpy as np
import tensorflow as tf

def main():
    input_1 = tf.keras.Input(shape=(10,))
    dense_1 = tf.keras.layers.Dense(4)(input_1)
    input_2 = tf.keras.Input(shape=(10,))
    dense_2 = tf.keras.layers.Dense(4)(input_2)
    x = tf.keras.layers.Concatenate()([dense_1, dense_2])
    y = tf.keras.layers.Dense(2)(x)
    model = tf.keras.Model([input_1, input_2], y)
    dataset_size = 1600
    batch_size = 16
    input_1_values = np.random.random((dataset_size, 10))
    input_2_values = np.random.random((dataset_size, 10))
    output_values = np.random.random((dataset_size, 2))

    dataset = tf.data.Dataset.from_tensor_slices(((input_1_values, input_2_values, output_values)))
    dataset = dataset.repeat().shuffle(buffer_size=100).batch(batch_size)
    model.compile(optimizer="adam", loss="binary_crossentropy")
    steps = 10
    epochs = 5
    count = 0

    for _ in range(epochs):
        for _ , (X1, X2, Y) in zip(range(steps), dataset):
            print("step %d:" % count)
            model.fit(x=[X1, X2], y=Y)
            count += 1

if __name__ == '__main__':
    main()