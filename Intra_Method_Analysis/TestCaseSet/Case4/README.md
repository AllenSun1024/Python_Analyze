### Description:
- 包含numpy, pickle, cv2, sklearn, keras
- 特征：方法内API调用序列特别长，而且存在if-else分支(目前对这种情况的结果记录形式或许是不合理的？)
- 注意：有main和convert_image_to_array两个方法，前者调用了后者，目前只考虑方法内的，因此sizeof(这份文件)=2