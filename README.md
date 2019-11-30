https://github.com/tensorflow/models/blob/master/research/deeplab/g3doc/pascal.md

## サンプルデータ構造
```
tree
/annotation
 - 2008_008252.png
/image
 - 2008_008252.jpg
/label.txt
```

# 実行スクリプト
```
tar -zxvf sample.tar.gz -C /tmp/
pip install tensorflow-gpu==1.14
pip install pillow==6.2.1
export PYTHONPATH="../:${PYTHONPATH}"
export PYTHONPATH="../slim:${PYTHONPATH}"
bash script/convert_tfrecord.sh /tmp/sample/image /tmp/sample/annotation /tmp/sample
rm -rf /tmp/log
export DATAPATH="/tmp/sample" # sampleデータを保存しているディレクトリ

cd models/research/deeplab/

# 学習
python train.py\
  --train_logdir="/tmp/log/train_log"\
  --log_steps=10\
  --save_interval_secs=1200\
  --save_summaries_secs=600\
  --model_variant="xception_65"\
  --save_summaries_images=true\
  --profile_logdir="/tmp/log/profile_log"\
  --training_number_of_steps=20\
  --train_batch_size=4\
  --train_crop_size=513,513\
  --atrous_rates=12\
  --atrous_rates=24\
  --atrous_rates=36\
  --output_stride=8\
  --decoder_output_stride=4\
  --dataset="sample"\
  --train_split="train"\
  --dataset_dir="/tmp/sample/tfrecord"
  #--tf_initial_checkpoint="deeplabv3_pascal_train_aug/model.ckpt" # チェックポイントから学習

# 評価
python eval.py \
    --logtostderr \
    --eval_split="val" \
    --model_variant="xception_65" \
    --atrous_rates=12 \
    --atrous_rates=24 \
    --atrous_rates=36 \
    --output_stride=8 \
    --decoder_output_stride=4 \
    --eval_crop_size="513,513" \
    --dataset="sample" \
    --checkpoint_dir="/tmp/log/train_log"\
    --eval_logdir="/tmp/log/eval_log"\
    --dataset_dir="/tmp/sample/tfrecord"\
    --max_number_of_evaluations=1

# 推論
python vis.py\
  --vis_batch_size=1\
  --model_variant="xception_65"\
  --vis_crop_size=513,513\
  --atrous_rates=12\
  --atrous_rates=24\
  --atrous_rates=36\
  --output_stride=8\
  --decoder_output_stride=4\
  --dataset="sample"\
  --dataset_dir="/tmp/sample/tfrecord"\
  --colormap_type="pascal"\
  --logtostderr\
  --vis_split="val"\
  --vis_logdir="/tmp/log/vis_log"\
  --checkpoint_dir="/tmp/log/train_log"\
  --max_number_of_iterations=1
# log/vis_logに推論結果が出力される
```
