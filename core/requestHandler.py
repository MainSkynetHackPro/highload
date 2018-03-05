import os

import datetime
import urllib


class RequestHandler:
    allowed_methods = ["GET", "HEAD"]

    def __init__(self, request, document_root):
        self.request = request
        self.document_root = document_root
        self.headers, self.method, self.uri, self.version_protocol = self.__parse_request(request)
        self.uri = urllib.unquote(self.uri)
        self.uri = self.uri.split('?')[0]

    def get_response(self):
        if not self.method in self.allowed_methods:
            return self.__http403()
        path = self.__get_path()

        if '../' in path:
            return self.__http404()
        if self.method == 'HEAD':
            return self.__build_head_response(path)
        return self.__build_response(path)

    def __parse_request(self, request):
        data = request.split('\r\n\r\n')
        data_for_headers = data[0].split('\r\n')

        return [dict((elem.split(': ')[0], elem.split(': ')[1])for elem in data_for_headers[1:])] + data_for_headers[0].split(' ')

    def __get_path(self):
        if self.uri[-1] == '/':
            path = '%(uri)sindex.html' % {'uri': self.uri}
        else:
            path = self.uri

        return '%(root)s%(path)s' % {'root': self.document_root, 'path': path}

    def __build_response(self, path):
        try:
            f = open(path)
            body = f.read()
            f.close()
        except IOError:
            return self.__http404()

        response = "HTTP/1.1 200 ACCEPTED\n"
        response += self.__get_server_str()
        response += self.__get_extension_content_type(path)
        response += self.__get_conection_str()
        response += self.__get_date_str()
        response += "Content-Length: %(i)s\n" % {'i': len(body)}
        response += "\n"

        response += body

        return response

    def __build_head_response(self, path):
        try:
            f = open(path)
            body = f.read()
            f.close()
        except IOError:
            return self.__http404()

        response = "HTTP/1.1 200 ACCEPTED\r\n"
        # response += self.__get_server_str()
        # response += self.__get_conection_str()
        # response += self.__get_date_str()
        response += "Content-Length: %(i)s\n" % {'i': len(body)}

        response += "\r\n\r\n"

        return response

    def __http404(self):
        response = "HTTP/1.1 404 NOT FOUND\n"
        response += self.__get_server_str()
        response += self.__get_conection_str()
        response += self.__get_date_str()
        response += "Content-Type: text/html; charset=UTF-8\n"
        response += "\n"
        return response

    def __http403(self):
        response = "HTTP/1.1 405 METHOD NOT ALLOWED\n"
        response += self.__get_server_str()
        response += self.__get_conection_str()
        response += self.__get_date_str()
        response += "Content-Type: text/html; charset=UTF-8\n"
        response += "\n"
        return response

    def __get_extension_content_type(self, path):
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.swf': 'application/x-shockwave-flash',
            '.txt': 'text/txt',
        }
        filename, file_extension = os.path.splitext(path)
        try:
            return "Content-Type: %(content_type)s\n" % {'content_type': content_types[file_extension]}
        except KeyError:
            return "Content-Type: text/txt"

    def __get_server_str(self):
        return "Server: Custom Server\n"

    def __get_conection_str(self):
        return "Connection: close"

    def __get_date_str(self):
        date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        return "Date: %(date)s\n" % {'date': date}
