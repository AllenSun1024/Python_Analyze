import tensorflow as tf
import keras.backend as backend

def main():
    BATCH_SIZE = 1000
    D2_SIZE = 200
    D3_SIZE = 200
    CHANNELS = 64
    x = tf.random.uniform([BATCH_SIZE, D2_SIZE, D3_SIZE, CHANNELS])
    y, group = [], []
    for i in range(BATCH_SIZE):
        for j in range(CHANNELS):
            y.append(backend.sum(x[i, :, :, j]))
        group.append(tf.convert_to_tensor(y, dtype=tf.float32))
        y = []
    yy = backend.stack(group, axis=0)
    tensor_stack = backend.reshape(yy, [BATCH_SIZE, CHANNELS])

if __name__ == '__main__':
    main()