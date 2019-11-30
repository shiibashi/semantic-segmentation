#!/bin/bash
# Usage:
#   bash convert_tfrecord.sh $1 $2 $3
#     $1: /tmp/sample/image # 元画像(.jpg)ディレクトリ
#     $2: /tmp/sample/annotation # アノテーションラベル画像(.png)ディレクトリ
#     $3: /tmp/sample # アノテーションラベル画像からカラーマップを取り除いた画像を出力するディレクトリ
#    example: bash convert_tfrecord.sh /tmp/sample/image /tmp/sample/annotation /tmp/sample

set -e
jpg_dir=$1
png_dir=$2
output_dir=$3
echo "jpg_dir=${jpg_dir}"
echo "png_dir=${png_dir}"
echo "output_dir=${output_dir}"
current=$(cd $(dirname $0); pwd)
cd $current
bw_dir=${output_dir}/annotation_bw
cd ../models/research/deeplab/datasets

# original_gt_folder: アノテーションラベル画像(.png)ディレクトリ
python remove_gt_colormap.py \
  --original_gt_folder="${png_dir}"\
  --output_dir="${bw_dir}"

segmentation_txt_dir=${output_dir}/segmentation_txt
# $1: bw_dir
# $2: segmentation_txt_dir: train,val,testに使う画像情報を保存
python train_val_test_split.py ${bw_dir} ${segmentation_txt_dir}

tfrecord_dir=${output_dir}/tfrecord
mkdir -p "${tfrecord_dir}"
# image_folder: 元画像(.jpg)ディレクトリ
# semantic_segmentation_folder: remove_gt_colormap.pyのoutput_dir, カラーマップを除いた
# list_folder: $segmentation_txt_dir: train,valをファイル名で指定
# output_dir: tfrecordを出力するディレクトリ名
python build_voc2012_data.py\
  --image_folder="${jpg_dir}"\
  --semantic_segmentation_folder="${bw_dir}"\
  --list_folder="${segmentation_txt_dir}"\
  --image_format="jpg"\
  --output_dir="${tfrecord_dir}"
