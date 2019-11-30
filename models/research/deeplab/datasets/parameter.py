import os

def _read_file(filepath):
    with open(filepath, "r") as f:
        d = f.readlines()
    return d

def _count_label(label_data):
    c = 0
    ignore_label = None
    for d in label_data[1:]: # ヘッダーは除外
        label_id, class_name = d.replace("\n", "").split(",")
        if class_name == "Ignore":
            ignore_label = label_id
        else:
            c += 1
    return c, int(ignore_label)

def load_parameter():
    assert os.environ.get("DATAPATH") is not None, "export DATAPATH, when sample, export DATAPATH='/tmp/sample'"
    datapath = os.environ["DATAPATH"]

    label_filepath = "{}/label.txt".format(datapath)
    splits_to_sizes_dirpath = "{}/segmentation_txt".format(datapath)

    filepath = "{}/train.txt".format(splits_to_sizes_dirpath)
    train_size = len(_read_file(filepath))

    filepath = "{}/trainval.txt".format(splits_to_sizes_dirpath)
    trainval_size = len(_read_file(filepath))

    filepath = "{}/val.txt".format(splits_to_sizes_dirpath)
    val_size = len(_read_file(filepath))

    #filepath = "{}/test.txt".format(splits_to_sizes_dirpath)
    #test_size = len(_read_file(filepath))

    label_data = _read_file(label_filepath)
    num_classes, ignore_label = _count_label(label_data)

    splits_to_sizes = {
        "train": train_size,
        "trainval": trainval_size,
        "val": val_size
    }
    return splits_to_sizes, num_classes, ignore_label

if __name__ == "__main__":
    os.environ["DATAPATH"] = "/tmp/sample"
    load_parameter()

