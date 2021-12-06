import tensorflow as tf

def main():
    ds = tf.data.TFRecordDataset('train.record')
    ds = ds.repeat(10000)
    ds = ds.batch(1)
    counter = ds.as_numpy_iterator()
    num = 0
    for ex in counter:
        num += 1
    print(num)

if __name__ == '__main__':
    main()