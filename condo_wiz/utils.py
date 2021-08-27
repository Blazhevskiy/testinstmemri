def get_header_by_name(request, header_name):
    return request.META.get(header_name) or request.headers.get(header_name)
