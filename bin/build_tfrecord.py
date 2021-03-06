""" script to build tfrecord """

from wgan.dataset_tool import TFRecorder
import os
import argparse

PATH_TFRECORD = os.getenv('PATH_TFRECORD', './datasets/tfrecords')
PATH_DATA = dict(
    celeba='./datasets/celeba/img/img_align_celeba',
    lsun='./datasets/lsun/train',
    celeba_v1='./datasets/celeba_v1/128_crop',
    hanzi_resize = "../datasets/hanzi_resize"
)


def get_options(parser):
    share_param = {'nargs': '?', 'action': 'store', 'const': None, 'choices': None, 'metavar': None}
    parser.add_argument('-c', '--crop', help='number.', default=None, type=int, **share_param)
    parser.add_argument('-r', '--resize', help='number.', default=64, type=int, **share_param)
    parser.add_argument('--data', help='Dataset.', required=True, type=str, **share_param)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_options(
        argparse.ArgumentParser(description='This script is ...', formatter_class=argparse.RawTextHelpFormatter))
    recorder = TFRecorder(dataset_name=args.data,
                               path_to_dataset=PATH_DATA[args.data],
                               tfrecord_dir=PATH_TFRECORD)
import os
import time
from PIL import Image

import tensorflow as tf

# 将图片裁剪为 128 x 128
OUTPUT_SIZE = 128
# 图片通道数，3 表示彩色
DEPTH = 3


def _int64_feature(value):
    return tf.train.Feature(int64_list = tf.train.Int64List(value = [value]))
def _bytes_feature(value):
    return tf.train.Feature(bytes_list = tf.train.BytesList(value = [value]))


def convert_to(data_path, name):

    """
    Converts s dataset to tfrecords
    """

    rows = 128
    cols = 128
    depth = DEPTH
    for ii in range(1):
        writer = tf.python_io.TFRecordWriter(name + '.tfrecord')
        for img_name in os.listdir(data_path):
            # 打开图片
            img_path = data_path + img_name
            img = Image.open(img_path)
            # 设置裁剪参数
            #h, w = img.size[:2]
            #j, k = (h - OUTPUT_SIZE) / 2, (w - OUTPUT_SIZE) / 2
            #box = (j, k, j + OUTPUT_SIZE, k+ OUTPUT_SIZE)
            # 裁剪图片
            #img = img.crop(box = box)
            # image resize
            #img = img.resize((rows,cols))
            # 转化为字节
            img_raw = img.tobytes()
            # 写入到 Example
            example = tf.train.Example(features = tf.train.Features(feature = {
                                        'height': _int64_feature(rows),
                                        'width': _int64_feature(cols),
                                        'depth': _int64_feature(depth),
                                        'image_raw': _bytes_feature(img_raw)}))
            writer.write(example.SerializeToString())
        writer.close()


if __name__ == '__main__':

    current_dir = os.getcwd()
    data_path = '../datasets/hanzi_resize/'
    name = '../datasets/hanzi_resize'
    start_time = time.time()

    print('Convert start')
    print('\n' * 2)

    convert_to(data_path, name)

    print('\n' * 2)
    print('Convert done, take %.2f seconds' % (time.time() - start_time))
    # recorder.create(
    #     crop_value=args.crop,
    #     resize_value=args.resize
    # )
