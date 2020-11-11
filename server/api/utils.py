def compress_to_dict(objects):
    return [obj.dict() for obj in objects]


def if_duplicated(new_obj, objects):
    return next(filter(lambda obj: obj.key == new_obj.key, objects), None)