from glob import glob
import os
from os.path import exists, join
from pathlib import Path
import shutil
import sys
import yaml
import argparse

def get_names(path: str) -> list[str]:
    with open(path, 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        return list(yaml_data['names'])

def try_mkdir(path: str):
    if not exists(path):
        os.makedirs(path)

def main(
    input_dir: str,
    output_dir: str,
    input_header: str,
    output_header: str,
    name_format: str
):
    input_names = get_names(input_header)
    output_names = get_names(output_header)
    index_map = { }
    index_c = 0

    input_images_path = join(input_dir, 'images')
    input_labels_path = join(input_dir, 'labels')
    output_images_path = join(output_dir, 'images')
    output_labels_path = join(output_dir, 'labels')

    try_mkdir(output_dir)
    try_mkdir(output_labels_path)
    try_mkdir(output_images_path)

    for i, name in enumerate(input_names):
        index = output_names.index(name)

        if index == -1:
            print('no match:', name)
            continue

        index_map[i] = index

        print(f'{name}: {i} -> {index}')
    
    print('\n')
    empty_str = ' ' * 20
    empty_strs = ' ' * 80 + '\n'

    input_labels = glob(join(input_labels_path, '*.txt'))
    input_labels_len = len(input_labels)

    for i, label_path in enumerate(input_labels):
        name = Path(label_path).stem
        image_path = join(input_images_path, name) + '.jpg'

        if not exists(image_path):
            print('no image:', name)
            continue
        
        lines = []

        with open(label_path, 'r') as f:
            for line in f.readlines():
                line = line.split(' ')

                if len(line) != 5:
                    continue

                index = index_map.get(int(line[0]), -1)

                if index == -1:
                    continue

                line[0] = str(index)
                lines.append(' '.join(line))

        index_c += 1
        file_name = name_format.format(original_name=name, label_name=output_names[index], index=index_c)

        with open(join(output_labels_path, f'{file_name}.txt'), 'w') as f:
            f.writelines(lines)

        shutil.copyfile(join(input_images_path, f'{name}.jpg'), join(output_images_path, f'{file_name}.jpg'))

        proc_per = (i+1)/input_labels_len

        sys.stdout.write(empty_strs)
        sys.stdout.write("\033[F")
        sys.stdout.write(f'{name} -> {file_name}\t{i+1}/{input_labels_len}\t[{"■"*int(15*proc_per)}{" "*(15-int(15*proc_per))}] {proc_per*100:.2f}%{empty_str}\r\n\033[F')

parser = argparse.ArgumentParser(description='Merge YOLOv5 dataset')
parser.add_argument('-I', '--input-dir', type=str, required=True, help='input dataset directory path\nexample: ./dataset/plants/train')
parser.add_argument('-O', '--output-dir', type=str, required=True, help='output dataset directory path\nexample: ./dataset/plants_merged/train')
parser.add_argument('-i', '--input-header', type=str, required=True, help='input header file path\nexample: ./dataset/plants/data.yaml')
parser.add_argument('-o', '--output-header', type=str, required=True, help='output header file path\nexample: ./dataset/plants_merged/data.yaml')
parser.add_argument('-n', '--name', type=str, default='{original_name}_{index}', help='name format\n{original_name} is original name, {label_name} is label name, {index} is index\nexample: plant_{label_name}_{index}\ndefault: {original_name}_{index}')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    main(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        input_header=args.input_header,
        output_header=args.output_header,
        name_format=args.name
    )
