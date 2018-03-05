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

    def get_response(self):
        if not self.method in self.allowed_methods:
            return self.__http403()
        path = self.__get_path()

        return self.__build_response(path)

    def __parse_request(self, request):
        data = request.split('\r\n\r\n')
        data_for_headers = data[0].split('\r\n')

        return [{elem.split(': ')[0]: elem.split(': ')[1] for elem in data_for_headers[1:]}] + data_for_headers[0].split(' ')

    def __get_path(self):
        if self.uri[-1] == '/':
            path = '{0}index.html'.format(self.uri)
        else:
            path = self.uri

        return u'{0}{1}'.format(self.document_root, path)

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
        response += "Content-Length: {0}\n".format(len(body))
        response += "\n"

        response += body

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
            '.swf': 'application/x-shockwave-flash'
        }
        filename, file_extension = os.path.splitext(path)
        return "Content-Type: {content_type}; charset=UTF-8\n".format(**{'content_type': content_types[file_extension]})

    def __get_server_str(self):
        return "Server: Custom Server\n"

    def __get_conection_str(self):
        return "Connection: close"

    def __get_date_str(self):
        date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        return "Date: {0}\n".format(date)
