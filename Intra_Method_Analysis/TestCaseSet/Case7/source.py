import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.datasets import mnist

def contrastive_loss(y_true, embeddings):
  loss = 0.0

  b = embeddings.shape[0]
  
  for i in range(0,b):
    yi = y_true[i]
    xi = embeddings[i]

    for j in range(i+1,b):
      yj = y_true[j]
      xj = embeddings[j]

      yij = tf.minimum(1.0, tf.abs(tf.cast(yi-yj, dtype = tf.float32)))
      distance = tf.norm(xi-xj)
      loss = loss + (1-yij)*distance**2 + yij*tf.maximum(0.0, 0.2-distance)**2
    
  loss = 0.5 * loss 
  return loss

def main():
    (X_train, y_train), (X_test, y_test) = mnist.load_data("/tf/mydata/data/mnist")

    X_train = (X_train / 255.0).astype('float32')
    X_test = (X_test / 255.0).astype('float32')

    X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
    X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
    input_shape = (28, 28, 1)

    tf.keras.backend.clear_session()

    embedding_size = 3
    model = keras.Sequential()
    model.add(Flatten(input_shape = input_shape))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(embedding_size))

    model.compile(keras.optimizers.Adam(learning_rate=1e-4), loss=contrastive_loss)
    history = model.fit(X_train, y_train, batch_size=32, epochs=1, shuffle=True)

if __name__ == '__main__':
    main()