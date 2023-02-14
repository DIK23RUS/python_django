from django.http import HttpRequest
import time


def setup_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('response count', self.responses_count)
        return response

    def process_exeption(self, request: HttpRequest, exeption: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exeptions so far")


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.users_ip = {}

    def collect_data(self, ip, data):
        fix_the_time = time.time()
        if ip in data:
            data[ip].append(fix_the_time)
        else:
            data[ip] = []
            data[ip].append(fix_the_time)

    def chec_func(self, data):
        for ips in data:
            if len(data[ips]) >= 2:
                t1 = data[ips][-1]
                t2 = data[ips][-2]
                time_interval = round(t1 - t2, 2)
                if time_interval <= 5:
                    self.users_ip[ips].clear()
                    return True
                else:
                    self.users_ip[ips].clear()

    def __call__(self, request: HttpRequest):
        ip = request.META.get('REMOTE_ADDR')
        if self.chec_func(data=self.users_ip) is True:
            print('Превышено количество запросов в секунду')
        response = self.get_response(request)
        self.collect_data(ip=ip, data=self.users_ip)

        return response
