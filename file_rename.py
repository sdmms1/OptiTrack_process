import os

i = 1
path = "data/20210116"
for file in os.listdir(path):
    new_name = file.replace(file, "%d.csv" % i)
    # 重命名
    os.rename(os.path.join(path, file), os.path.join(path, new_name))
    i += 1
