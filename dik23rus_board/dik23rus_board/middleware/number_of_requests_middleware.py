import time


class NumberOFRequestsEx(Exception):
    pass


users_ip = {}


def collect_data(ip, data):
    fix_the_time = time.time()
    if ip in data:
        data[ip].append(fix_the_time)
    else:
        data[ip] = []
        data[ip].append(fix_the_time)


def chec_func(data):
    for ips in data:
        if len(data[ips]) >= 2:
            t1 = data[ips][-1]
            t2 = data[ips][-2]
            time_interval = round(t1 - t2, 2)
            if time_interval <= 5:
                users_ip[ips].clear()
                return True
            else:
                users_ip[ips].clear()


def number_of_requests(get_response):
    def middleware(request):
        global users_ip
        ip = request.META.get('REMOTE_ADDR')
        if chec_func(data=users_ip) is True:
            raise NumberOFRequestsEx('Превышено количество запросов в секунду')
        response = get_response(request)
        """Тут то, что отвечает"""
        collect_data(ip=ip, data=users_ip)

        return response

    return middleware

