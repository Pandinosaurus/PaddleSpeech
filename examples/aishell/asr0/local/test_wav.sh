#!/bin/bash

if [ $# != 4 ];then
    echo "usage: ${0} config_path decode_config_path ckpt_path_prefix audio_file"
    exit -1
fi

ngpu=$(echo $CUDA_VISIBLE_DEVICES | awk -F "," '{print NF}')
echo "using $ngpu gpus..."

config_path=$1
decode_config_path=$2
ckpt_prefix=$3
audio_file=$4

mkdir -p data
wget -nc https://paddlespeech.cdn.bcebos.com/datasets/single_wav/zh/demo_01_03.wav -P data/
if [ $? -ne 0 ]; then
   exit 1
fi

if [ ! -f ${audio_file} ]; then
    echo "Plase input the right audio_file path"
    exit 1
fi

# download language model
bash local/download_lm_ch.sh
if [ $? -ne 0 ]; then
   exit 1
fi

python3 -u ${BIN_DIR}/test_wav.py \
--ngpu ${ngpu} \
--config ${config_path} \
--decode_cfg ${decode_config_path} \
--result_file ${ckpt_prefix}.rsl \
--checkpoint_path ${ckpt_prefix} \
--audio_file ${audio_file}

if [ $? -ne 0 ]; then
    echo "Failed in evaluation!"
    exit 1
fi


exit 0
