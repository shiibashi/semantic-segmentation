import os
import sys

train_rate = 0.9
trainval_rate = 0.08
test_rate = 0.02

def write_file(filepath, data_list):
    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write("\n".join(data_list))

def without_prefix(filelist):
    d = [f.replace(".png", "") for f in filelist]
    return d

if __name__ == "__main__":
    bw_dirpath = sys.argv[1]
    segmentation_txt_dir = sys.argv[2]

    os.makedirs(segmentation_txt_dir, exist_ok=True)

    filepath_list = sorted(os.listdir(bw_dirpath))
    n = len(filepath_list)
    train_list = filepath_list[0:int(train_rate * n)]
    trainval_list = filepath_list[0:int((train_rate+trainval_rate)*n)]
    val_list = filepath_list[int(train_rate * n):int((train_rate+trainval_rate)*n)]
    test_list = filepath_list[int((train_rate+trainval_rate)*n):]

    print("train_num={}".format(len(train_list)))
    print("trainval_num={}".format(len(trainval_list)))
    print("val_num={}".format(len(val_list)))
    print("test_num={}".format(len(test_list)))

    for f in filepath_list:
        assert ".png" in f, "Invalid name included"
        f_without_prefix = f.replace(".png", "")

    output_path = "{}/train.txt".format(segmentation_txt_dir)
    write_file(output_path, without_prefix(train_list))

    output_path = "{}/trainval.txt".format(segmentation_txt_dir)
    write_file(output_path, without_prefix(trainval_list))

    output_path = "{}/val.txt".format(segmentation_txt_dir)
    write_file(output_path, without_prefix(val_list))

    output_path = "{}/test.txt".format(segmentation_txt_dir)
    write_file(output_path, without_prefix(test_list))

