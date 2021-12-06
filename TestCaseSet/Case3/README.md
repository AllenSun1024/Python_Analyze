### Description:
- 包含tensorflow、numpy
- 特征：API调用序列比较长
- 注意：在upstream_network = tf.keras.Model(input_a, x)的基础上，intermed_a = upstream_network(input_full_a)实际是在调用tensorflow.keras.Model.__call__
