import typing

from django.db.models import ProtectedError
from django.http import HttpRequest
from django.http import JsonResponse


def response_success(list: typing.List = None) -> JsonResponse:
    response = {'code': 1}
    if list is not None:
        response['list'] = list
    return JsonResponse(response)


def response_error(msg: str, code=0, status=500) -> JsonResponse:
    return JsonResponse({
        'code': code,
        'msg': msg
    }, status=status)


def hold_exception(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            return response_error(str(e))

    return wrapper


def check_login(func):
    def wrapper(request: HttpRequest, *args, **kw):
        if request.user.is_authenticated:
            return func(request, *args, **kw)
        else:
            return response_error('login required', status=403)

    return wrapper


def check_admin(func):
    def wrapper(request: HttpRequest, *args, **kw):
        if request.user.is_staff:
            return func(request, *args, **kw)
        else:
            return response_error('permission denied', status=403)

    return wrapper


def general_get(model, params: dict):
    try:
        result = model.objects.filter(**params).values()
        return response_success(list(result))
    except Exception as e:
        return response_error(str(e))


def general_add(model, params: dict):
    try:
        if 'id' not in params:
            return response_error('missing id')
        if model.objects.filter(id=params['id']):
            return response_error('id exists')
        model(**params).save()
        return response_success()
    except Exception as e:
        return response_error(str(e))


def general_del(model, params: dict):
    try:
        model.objects.filter(**params).delete()
        return response_success()
    except ProtectedError:
        return response_error('entries are referenced by foreign key')
    except Exception as e:
        return response_error(str(e))


def general_mod(model, where: dict, update: dict):
    try:
        if 'id' in update:  # id 不能修改
            return response_error('can not modify id')
        model.objects.filter(**where).update(**update)
        return response_success()
    except Exception as e:
        return response_error(str(e))
