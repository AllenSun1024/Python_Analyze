import tensorflow as tf
import keras.backend as K

def main():
    x1 = [[[0, 0, 0] * 1000000, 
    [0, 0, 0] * 1000000, 
    [1, 1, 1] * 1000000, 
    [-1, -1, 0] * 1000000,
    [0, 0, 0] * 1000000,
    [1, 1, 1] * 1000000,
    [1, -1, 0] * 1000000
    ]]
    x1 = tf.convert_to_tensor(x1, dtype=tf.float32)
    mask_3 = K.cast(tf.equal(x1, 0), 'float32')
    mask_4 = K.sum(K.ones_like(x1), axis=-1)
    mask_5 = K.sum(mask_3, axis=-1)
    mask_6 = mask_5 < mask_4
    mask_6 = tf.cast(mask_6, 'float32')

if __name__ == '__main__':
    main()