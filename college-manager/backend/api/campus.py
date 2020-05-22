import json

import django.views.decorators.csrf
from django.views.decorators.http import require_http_methods

from .general import *
from .models import *

where_params = ['id', 'name', 'address']


def check_params(params: dict) -> dict:
    return {
        k: v for k, v in params.items()
        if k in where_params
    }


# done

@check_login
@hold_exception
@require_http_methods(['GET'])
@django.views.decorators.csrf.csrf_exempt
def get(request: HttpRequest):
    params = check_params(request.GET.dict())
    return general_get(Campus, params)


@check_admin
@hold_exception
@require_http_methods(['POST'])
@django.views.decorators.csrf.csrf_exempt
def add(request: HttpRequest):
    params = json.loads(request.body.decode())
    params = check_params(params)
    return general_add(Campus, params)


@check_admin
@hold_exception
@require_http_methods(['GET'])
@django.views.decorators.csrf.csrf_exempt
def delete(request: HttpRequest):
    params = check_params(request.GET.dict())
    return general_del(Campus, params)


@check_admin
@hold_exception
@require_http_methods(['POST'])
@django.views.decorators.csrf.csrf_exempt
def mod(request: HttpRequest):
    params = json.loads(request.body.decode())
    where = check_params(params.get('where', {}))
    update = check_params(params.get('update', {}))
    return general_mod(Campus, where, update)
