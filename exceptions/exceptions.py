from django.conf import settings
from rest_framework.views import exception_handler

from exceptions.internal_code_errors import DEFAULT_ERROR_CODE


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        data = {'detail': {'message': []}}
        if not hasattr(exc, 'detail'):
            if exc.args:
                exc.detail = exc.args[0]
            else:
                try:
                    class_name = context.get('view').__class__.__name__
                except KeyError:
                    class_name = 'Unknown'

                exc.detail = (
                    f"Error without message. From view: {class_name}, "
                    f"action: {getattr(context.get('view'), 'action', None)}"
                )
        if not isinstance(exc.detail, (dict, list)):
            data['detail'] = {'message': [exc.detail]}
        else:
            # convert string messages to list
            if isinstance(exc.detail, dict):
                for key, value in exc.detail.items():
                    if key == 'error_code':
                        data['detail']['error_code'] = value
                    if not isinstance(value, list):
                        exc.detail[key] = [value]
                    else:
                        data['detail']['message'].extend(value)
            else:
                data['detail'] = exc.detail
        if not 'error_code' in data['detail']:
            data['detail']['error_code'] = DEFAULT_ERROR_CODE
        response.data = data
        response.data['status_code'] = response.status_code
    return response
