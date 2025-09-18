# hello_app.py

def application(environ, start_response):
    # HTTP válasz fejlécek beállítása
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    # Üzenet a válasz törzsében
    response_body = b'Hello FSZ Python!'
    print(f"response is {response_body}")
    # Válasz küldése a böngészőnek
    start_response(status, headers)
    return [response_body]
