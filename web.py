import socket
from views import index, blog

URLS = {
    '/': index,
    '/blog': blog
}


# Парсим
def parsing_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def gen_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)
    return ('HTTP/1.1 200 OK\n\n', 200)


# ответ на 404, 405
def gen_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()


def gen_response(request):
    method, url = parsing_request(request)
    headers, code = gen_headers(method, url)
    body = gen_content(code, url)
    return (headers + body).encode()


# запуск
def run():
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind(('localhost', 5000))
    srv_socket.listen()

    while True:
        cl_socket, addr = srv_socket.accept()
        request = cl_socket.recv(1024)
        print(request)
        print()
        print(addr)

        response = gen_response(request.decode('utf-8'))

        cl_socket.sendall(response)
        cl_socket.close()


if __name__ == '__main__':
    run()
