https://github.com/tensorflow/models/blob/master/research/deeplab/g3doc/pascal.md

```
pip install --upgrade pip
git clone https://github.com/tensorflow/models.git
```

```
cd models/research/deeplab
pip install tensorflow-gpu==1.14
pip install pillow==6.2.1
export PYTHONPATH="../:${PYTHONPATH}" # master/research
export PYTHONPATH="../slim:${PYTHONPATH}" # master/research/slim
```

```
cd datasets
bash download_and_convert_voc2012.sh
# pascal_voc_seg/tfrecordに出力される
```


```
rm -rf log
cd ..
wget http://download.tensorflow.org/models/deeplabv3_pascal_train_aug_2018_01_04.tar.gz
tar -zxvf deeplabv3_pascal_train_aug_2018_01_04.tar.gz

python train.py\
  --train_logdir="log/train_log"\
  --log_steps=10\
  --save_interval_secs=1200\
  --save_summaries_secs=600\
  --model_variant="xception_65"\
  --save_summaries_images=true\
  --profile_logdir="log/profile_log"\
  --training_number_of_steps=200\
  --train_batch_size=8\
  --train_crop_size=513,513\
  --atrous_rates=6\
  --atrous_rates=12\
  --atrous_rates=18\
  --output_stride=16\
  --decoder_output_stride=4\
  --dataset="pascal_voc_seg"\
  --train_split="train"\
  --dataset_dir="./datasets/pascal_voc_seg/tfrecord"\
  --tf_initial_checkpoint="deeplabv3_pascal_train_aug/model.ckpt" # チェックポイントから学習
  #はじめはoutput_stride=16
```

```
python eval.py \
    --logtostderr \
    --eval_split="val" \
    --model_variant="xception_65" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --eval_crop_size="513,513" \
    --dataset="pascal_voc_seg" \
    --checkpoint_dir="log/train_log"\
    --eval_logdir="log/eval_log"\
    --dataset_dir="./datasets/pascal_voc_seg/tfrecord"
```

```
python vis.py\
  --vis_batch_size=1\
  --model_variant="xception_65"\
  --vis_crop_size=513,513\
  --atrous_rates=6\
  --atrous_rates=12\
  --atrous_rates=18\
  --output_stride=16\
  --decoder_output_stride=4\
  --dataset="pascal_voc_seg"\
  --dataset_dir="./datasets/pascal_voc_seg/tfrecord"\
  --colormap_type="pascal"\
  --logtostderr\
  --vis_split="val"\
  --vis_logdir="log/vis_log"\
  --checkpoint_dir="log/train_log"\
  --max_number_of_iterations=1
# log/vis_logに推論結果が出力される
```
