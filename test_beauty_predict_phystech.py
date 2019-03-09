import pathlib
from statistics import mean

from beauty_predict import beauty_predict
from config import output_path, parent_path


def get_name(file_name):
    s = file_name.stem
    return s[:len(s) - int(s[-1].isdigit())].lower()


test_path = parent_path / 'photos' / '2018'

names = sorted({get_name(name) for name in test_path.iterdir()})
for name in names:
    print()
    print('Testing', name)
    names = ['', '1', '2', '3', '4', '5']
    outs = []
    variants = []
    for i in names:
        path1 = name + i + '.jpg'
        path2 = name.capitalize() + i + '.jpg'
        variants.append(path1)
        variants.append(path2)

    for v in variants:
        path = test_path / v
        if path.exists():
            print(path)
            outs.append(beauty_predict(test_path, path.name))
    print(mean(outs), outs)
