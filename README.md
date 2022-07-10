# yolov5-dataset-merge
yolov5 dataset merge tool

Merges two datasets labeled with different indexes.

## use

```shell
usage: yolov5_dataset_merge.py [-h] -I INPUT_DIR -O OUTPUT_DIR -i INPUT_HEADER -o OUTPUT_HEADER [-n NAME]

Merge YOLOv5 dataset

options:
  -h, --help            show this help message and exit
  -I INPUT_DIR, --input-dir INPUT_DIR
                        input dataset directory path example: ./dataset/plants/train
  -O OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output dataset directory path example: ./dataset/plants_merged/train
  -i INPUT_HEADER, --input-header INPUT_HEADER
                        input header file path example: ./dataset/plants/data.yaml
  -o OUTPUT_HEADER, --output-header OUTPUT_HEADER
                        output header file path example: ./dataset/plants_merged/data.yaml
  -n NAME, --name NAME  name format {original_name} is original name, {label_name} is label name, {index} is index
                        example: plant_{label_name}_{index} default: {original_name}_{index}
  -m MARGE_LABEL [MARGE_LABEL ...], --marge-label MARGE_LABEL [MARGE_LABEL ...]
                        marge label example: lettuce.leaf:lettuce tomato.leaf,tomato.healthy.leaf:tomato.fruit
  -e, --ignore-empty-label
                        ignore empty label

```

```shell
python3.10 yolov5_dataset_merge.py \
-I ./dataset/plants/train \ # input dataset directory
-O ./dataset/plants_merged/train \ # output dataset directory
-i ./dataset/plants/data.yaml \ # input header file
-o ./dataset/plants_merged/data.yaml \ # output header file
-n {label_name}_{index} \ # name format
-m lettuce.leaf:lettuce tomato.leaf,tomato.healthy.leaf:tomato.fruit \ # marge labels
-e # ignore empty label

eggplants_fruit: 0 -> 7
eggplants_flower: 1 -> 8
eggplants_leaf: 2 -> 9
...

enforce_tomato_9993 -> tomato_leaf_6553 6553/6553       [■■■■■■■■■■■■■■■] 100.00%
```

