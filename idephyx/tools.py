



def check_annotations(annotations, annotations_for_naming):
    #check annotations
    _all_ann_names = []
    for p in annotations:
        assert '_' not in p['name'], 'Problem in annotations. Donot use "_"'
        assert '=' not in p['name'], 'Problem in annotations. Donot use "="'
        _all_ann_names.append(p['name'])

    for _name in annotations_for_naming:
        assert _name in _all_ann_names, 'Problem in annotations naming'




def get_dict_from_group_param(param, cascade = False):
    assert param.type() == 'group'
    d = {}
    for p in param.children():
        if p.type() == 'group':
            if cascade:
                d[p.name()] = get_dict_from_group_param(p, cascade = True)
            continue
        else:
            d[p.name()] = p.value()
    return d