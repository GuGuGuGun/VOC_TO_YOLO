import re
import os
from pathlib import Path

pre_dir = Path(r'D:/deeplearning/yolo8-test/coco/annotations')  # annotations位置
txt_dir = 'D:/deeplearning/yolo8-test/coco/labels' # 目标文件夹


def FindName(pre_dir):
    s = set()
    obj = re.compile(r'<name>(?P<name>.*?)</name>')
    for path in pre_dir.iterdir():
        with open(path, 'r') as f:
            content = f.read()
        result1 = obj.finditer(content)
        for item in result1:
            s1 = item.group('name')
            s.add(s1)
    return s


name = FindName(pre_dir)
classes = list(name)  # 分类名
print(classes)


def Number(number, n):
    a = int(number * 10 ** n) / 10 ** n
    return a


def FindFileAllData(path):
    full_data = []
    size_data = []
    box_data = []
    find_size = re.compile(r'<width>(?P<width>.*?)</width>.*'
                           r'<height>(?P<height>.*?)</height>.*'
                           r'<depth>(?P<depth>.*?)</depth>.*', re.S)
    find_bndbox = re.compile(r'<name>(?P<name>.*?)</name>.*?'
                             r'<xmin>(?P<xmin>.*?)</xmin>.*?'
                             r'<ymin>(?P<ymin>.*?)</ymin>.*?'
                             r'<xmax>(?P<xmax>.*?)</xmax>.*?'
                             r'<ymax>(?P<ymax>.*?)</ymax>.*?', re.S)
    with open(path, 'r') as f:
        content = f.read()
        data_size = find_size.finditer(content)
        data_bndbox = find_bndbox.finditer(content)
        for item in data_size:
            width = item.group('width')
            height = item.group('height')
            depth = item.group('depth')
            size_data.append(width)
            size_data.append(height)
            size_data.append(depth)
        for item in data_bndbox:
            name = item.group(('name'))
            x_min = item.group('xmin')
            y_min = item.group('ymin')
            x_max = item.group('xmax')
            y_max = item.group('ymax')
            box_data.append(name)
            box_data.append(x_min)
            box_data.append(y_min)
            box_data.append(x_max)
            box_data.append(y_max)
        box_length = int(len(box_data) / 5)
        full_data.append(size_data)
        full_data.append(box_data)
        full_data.append(box_length)
        return full_data


def Divide(box_data, box_length):
    box_data_dict = {}
    for i in range(1, box_length + 1):
        box_data_dict[f'list_{i}'] = []
        for j in range(5 * (i - 1), 5 * i):
            box_data_dict[f'list_{i}'].append(box_data[j])
    return box_data_dict


def CountAndWrite(pre_dir, txt_dir, classes):
    for path in pre_dir.iterdir():
        size_data, box_data, box_length = FindFileAllData(path)
        box_data_dict = Divide(box_data, box_length)
        file_name = os.path.splitext(os.path.basename(path))[0]
        data = []
        for i in box_data_dict.values():
            for j in range(5):
                if j > 0:
                    data.append(int(i[j]))
                else:
                    data.append(i[j])

            name = classes.index(data[0])
            first = ('%.8f' % (((data[3] + data[1]) / 2) / int(size_data[0])))
            second = ('%.8f' % (((data[4] + data[2]) / 2) / int(size_data[1])))
            third = ('%.8f' % (((data[3] - data[1])) / int(size_data[0])))
            four = ('%.8f' % (((data[4] - data[2])) / int(size_data[1])))
            with open(f'{txt_dir}/{file_name}.txt', 'a') as f:
                f.write(f'{name} {first} {second} {third} {four}\n')
                data.clear()


if __name__ == '__main__':
    CountAndWrite(pre_dir, txt_dir, classes)
