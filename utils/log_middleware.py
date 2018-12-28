import time

from django.utils.deprecation import MiddlewareMixin
import logging
#定义log
log = logging.getLogger(__name__)

class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 绑定一个访问时间到request上
        request.init_time = time.time()


    def process_response(self, request, response):
        # 算出请求到返回执行耗时
        count_time = time.time() - request.init_time
        # 响应状态码
        code = response.status_code
        # 请求地址
        path = request.path
        # 请求方式
        method = request.method
        # 取出响应内容
        try:
            content = response.content
        except:
            content = response.streaming_content
        # 组装日志信息
        log_str = '%s %s %s %s %s' % (path, method, code,
                                      count_time, content)
        #交给logger处理日志
        log.info(log_str)

        return response





