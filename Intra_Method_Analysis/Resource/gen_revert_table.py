import json

revert_table = {}

revert_table["tensorflow.data.TFRecordDataset"] = "tf.data.Dataset"
revert_table["tensorflow.data.Dataset.from_tensor_slices"] = "tf.data.Dataset"

with open("revert_table.json", 'w') as out_file:
    json.dump(revert_table, out_file)
