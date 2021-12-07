from tensorflow.keras.layers import *
from tensorflow.keras import *
import tensorflow as tf
import GPUtil

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

def main():
    GPUs = GPUtil.getGPUs()
    total_mem = 0
    for i in range(len(GPUs)):
        total_mem += GPUs[i].memoryTotal
    frac = 6097 / total_mem  # MB

    config = ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = frac
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024 * 12)])
        except RuntimeError as e:
            print(e)
    sample_size = 100
    n_width = 640
    n_height = 640
    n_channels = 1
    X_shape = (sample_size, 1, n_width, n_height, n_channels)
    Y_shape = (sample_size, 1)
    X = tf.random.normal(X_shape)
    Y = tf.random.normal(Y_shape)
    X = tf.data.Dataset.from_tensor_slices(X).batch(1)
    Y = tf.data.Dataset.from_tensor_slices(Y).batch(1)
    dataset = tf.data.Dataset.zip((X,Y))

    img_input_1 = Input(shape=(1, n_width, n_height, n_channels))

    conv_1 = TimeDistributed(Conv2D(96, (11,11), activation='relu', padding='same'))(img_input_1)

    pool_1 = TimeDistributed(MaxPooling2D((3,3)))(conv_1)

    conv_2 = TimeDistributed(Conv2D(128, (11,11), activation='relu', padding='same'))(pool_1)

    flat_1 = TimeDistributed(Flatten())(conv_2)

    dense_1 = TimeDistributed(Dense(4096, activation='relu'))(flat_1)

    drop_1 = TimeDistributed(Dropout(0.5))(dense_1)

    lstm_1 = LSTM(17, activation='linear')(drop_1)

    dense_2 = Dense(4096, activation='relu')(lstm_1)

    dense_output_2 = Dense(1, activation='sigmoid')(dense_2)

    model = Model(inputs=img_input_1, outputs=dense_output_2)

    op = optimizers.Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.001)

    model.compile(loss='mean_absolute_error', optimizer=op, metrics=['accuracy'])

    model.fit(dataset, epochs=3)

if __name__ == '__main__':
    main()
