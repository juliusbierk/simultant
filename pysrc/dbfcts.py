import json
from collections import defaultdict
from asgiref.sync import sync_to_async
from db import Dataset, Model, Fit


@sync_to_async
def create_dataset(name, parent, content):
    info = f'{len(content["x"])} datapoints'
    Dataset(name=name, parent=parent, info=info, content=json.dumps(content)).save()


@sync_to_async
def get_data_names():
    names_info = defaultdict(list)
    for d in Dataset.objects.all():
        names_info[d.parent].append({'name': d.name, 'id': d.id, 'info': d.info})
    return dict(names_info)


@sync_to_async
def get_data_content(ID):
    try:
        d = Dataset.objects.get(id=ID)
    except Dataset.DoesNotExist:
        return None
    return json.loads(d.content)


@sync_to_async
def delete_data(parent):
    Dataset.objects.filter(parent=parent).delete()


@sync_to_async
def create_model(name, content):
    Model.objects.get_or_create(name=name, content=json.dumps(content))


@sync_to_async
def delete_model(name):
    Model.objects.get(name=name).delete()


@sync_to_async
def get_models_names():
    return [x.name for x in Model.objects.all()]


def args_to_kwargs(d):
    kwargs = {x['name']: x['value'] for x in d['args']}
    if not d['expr_mode']:
        y0 = kwargs['y0']
        del kwargs['y0']
        for i in range(len(y0)):
            kwargs[f'y0[{i}]'] = y0[i]
    return kwargs


@sync_to_async
def get_models_content(name):
    try:
        d = Model.objects.get(name=name)
    except Model.DoesNotExist:
        return

    data = json.loads(d.content)
    data['kwargs'] = args_to_kwargs(data)
    return data


@sync_to_async
def get_all_models():
    data = {x.name: json.loads(x.content) for x in Model.objects.all()}
    for m in data:
        data[m]['kwargs'] = args_to_kwargs(data[m])
    return data


if __name__ == '__main__':
    print(get_models_names())
