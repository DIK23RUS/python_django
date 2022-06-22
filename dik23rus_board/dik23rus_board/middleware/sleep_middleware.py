import time

counter = 0


def sleep_middleware(get_response):
    def middleware(request):
        global counter
        counter += 1
        response = get_response(request)
        if counter % 3 == 0:
            time.sleep(2.0)
        return response

    return middleware
