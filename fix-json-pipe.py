#!/usr/bin/env python3

# ~ import json
import sys

import simplejson as json


# ~ Открываем файлы и загружаем из них данные. После загрузки файлы закрываются
# ~ автоматически
src1 = json.load(open(sys.argv[1]), use_decimal=True)
src2 = json.load(sys.stdin, use_decimal=True)

# ~ Оптимизированная под поиск структура первого файла
struct = {}

# ~ Проходим структуру первого, "эталонного" файла.
# ~ Создаётся "двухслойный" словарь: на первом уровне ключом служит значение
# ~ поля param_id, на втором - period_id. Значение - поле val.
for obj in src1:
    struct[obj['param_id']] = {}
    for val in obj['vals']:
        struct[obj['param_id']][val['period_id']] = val['val']

# ~ Проходим структуру второго файла. В первом цикле перебираем объекты из
# ~ списка первого уровня
for obj_l1 in src2:

    # ~ Во втором цикле перебираем объекты из списка второго уровня, размещённого в
    # ~ поле parameters объекта, являющегося элементом списка первого уровня
    for obj_l2 in obj_l1['parameters']:

        # ~ Проверяем, присутствует ли значение поля param_inner_id среди
        # ~ идентификаторов объектов из первого файла. Если нет, то дальнейшие
        # ~ проверки не имеют смысла, поэтмоу переходим к следующему объекту.
        if obj_l2['param_inner_id'] not in struct:
            continue

        # ~ В третьем цикле перебираем элементы списка третьего уровня,
        # ~ расколоженного в поле values.
        for value in obj_l2['values']:

            # ~ Проверяем, есть ли среди "значений" (vals) найденного объекта
            # ~ "период" с таким же идентификатором, как у текущего.
            # ~ Если нет - переходим к следующему "периоду".
            if value['period_id'] not in struct[obj_l2['param_inner_id']]:
                continue

            # ~ Производим замену.
            value['base_value'] = struct[obj_l2['param_inner_id']][value['period_id']]

# ~ Сохраняем изменения в выходной файл
json.dump(
    src2,
    sys.stdout,
    indent=4,
    ensure_ascii=False,
    use_decimal=True
)
