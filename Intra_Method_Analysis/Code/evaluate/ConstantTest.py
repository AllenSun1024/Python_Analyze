import ast

# print(ast.dump(ast.parse('eval_results={_WER_KEY:total_wer, _CER_KEY:total_cer, tf.compat.v1.GraphKeys.Global_STEP:global_step,}'), indent=4))

print(ast.dump(ast.parse("SubpixelConv2d(scale=2, n_out_channels=None, act=tf.nn.relu)(n)"), indent=4))

# Elementwise(tf.add)([n, nn])

# SubpixelConv2d(scale=2, n_out_channels=None, act=tf.nn.relu)(n)

# tf.data.Dataset.from_generator(generator_train, output_types=(tf.float32))

# tf.cast(tf.multiply(
#       input_length, ctc_time_steps), dtype=tf.float32)

# estimator.get_variable_value(tf.compat.v1.GraphKeys.GLOBAL_STEP)

# isinstance(op, tf.NodeDef)

# tf.layers.dense(
#           summary,
#           d_model,
#           activation=tf.tanh,
#           kernel_initializer=initializer,
#           name='summary')

# if mode == tf.compat.v1.estimator.ModeKeys.PREDICT

# NotImplementedError("options are not supported for TF < 2.3.x,"
#                                 " Current version: %s" % tf.__version__)

# tf.cast(rt.row_starts(), tf.int64)

# return tf.keras.optimizers.Adam

# tf.py_function(data_aug, [image], [tf.float32])[0]
