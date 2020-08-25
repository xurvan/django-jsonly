from datetime import datetime
from itertools import chain

from django.db import models


def fancy_dict(model: models.Model) -> dict:
    valid_types = (str, int, datetime)
    # noinspection PyProtectedMember
    opts = model._meta
    data = dict()

    def obj_to_dict(obj):
        return {k: v for k, v in obj.__dict__.items() if isinstance(v, valid_types)}

    for f in chain(opts.concrete_fields, opts.private_fields):
        if f.one_to_one:
            continue

        value = f.value_from_object(model)
        if f.many_to_one:
            attr = getattr(model, f.name)
            data[f.name] = obj_to_dict(attr)
        elif isinstance(value, valid_types):
            data[f.name] = value
    for f in opts.many_to_many:
        data[f.name] = [obj_to_dict(i) for i in f.value_from_object(model)]
    return data
