"""JSON helper functions"""
try:
    import simplejson as json
except ImportError:
    import json

from rest_framework.response import Response


def JsonResponse(data={}, dump=True, status=200):
    try:
        data['error']
    except KeyError:
        data['success'] = "1"
    except TypeError:
        pass
    return Response(data,status=status,)
    return Response(
        json.dumps(data) if dump else data,
        content_type='application/json',
        status=status,
    )


def JsonError(error_string, status=200):
    data = {
        'success': "0",
        'error': error_string,
    }
    return JSONResponse(data)


def JsonResponseBadRequest(error_string):
    return JsonError(error_string, status=400)


def JsonResponseUnauthorized(error_string):
    return JsonError(error_string, status=401)


def JsonResponseForbidden(error_string):
    return JsonError(error_string, status=403)


def JsonResponseNotFound(error_string):
    return JsonError(error_string, status=404)


def JsonResponseNotAllowed(error_string):
    return JsonError(error_string, status=405)


def JsonResponseNotAcceptable(error_string):
    return JsonError(error_string, status=406)


# For backwards compatability purposes
JSONResponse = JsonResponse
JSONError = JsonError
