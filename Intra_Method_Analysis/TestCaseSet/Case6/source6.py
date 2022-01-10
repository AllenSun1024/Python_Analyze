import tensorflow as tf
import numpy as np

def get_padding_mask(words_chars_ids, emb_size):
    padding_mask = tf.map_fn(
        lambda x: tf.map_fn(
            lambda y: tf.map_fn(
                    lambda z: tf.cond(tf.less(z, 1),
                    lambda: tf.zeros([emb_size, ], dtype=tf.int32),
                    lambda: tf.ones([emb_size, ], dtype=tf.int32)
                ),
            y),
        x),
    words_chars_ids)
    return padding_mask           

def main():
    words_chars_ids = tf.constant(np.random.randint(1,100,([6,200,20])), dtype=tf.int32)
    emb_size = 2
    get_padding_mask(words_chars_ids,emb_size)

if __name__ == '__main__':
    main()