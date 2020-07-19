import json
import requests
import lxml.html

urlLoginpage = 'https://portalpersonas.bancochile.cl/persona'
urlLogin = 'https://login.bancochile.cl/oam/server/auth_cred_submit'
urlCartola = 'https://portalpersonas.bancochile.cl/mibancochile/rest/persona/movimientos/getcartola'
payloadCartola = {
    "cabecera": {
        "fechaFin": None,
        "fechaInicio": None,
        "paginacionDesde": {},
        "statusGenerico": True,
    },
    "cuentasSeleccionadas": [{
        "alias": None,
        "claseCuenta": "CCNMN1",
        "codigoProducto": "CTD",
        "mascara": "****9106",
        "moneda": "CLP",
        "nombreCliente": "Philipp Grothaus .",
        "numero": "3330159106",
        "rutCliente": "25801702-1",
        "selected": True,
    }]
}

username = "25.801.702-1"
usernameInt = 258017021
usernameFormatted = str(usernameInt)
pw = "1GDhEfjh"

payload = [
    ("username2", usernameInt),
    ("username2", username),
    ("userpassword", pw),
    ("request_id", None),
    ("ctx", "persona"),
    ("username", usernameFormatted),
    ("password", pw),
]

dataStr = "username2=258017021&username2=25.801.702-1&userpassword=1GDhEfjh&request_id=&ctx=persona&username=258017021&password=1GDhEfjh"

headersLogin={
    'origin': 'https://login.bancochile.cl',
    'referer': 'https://login.bancochile.cl/bancochile-web/persona/login/index.html',
    'ch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
}

with requests.Session() as session:
    login = session.get(urlLoginpage)
    req = requests.Request('POST', urlLogin, data=dataStr, headers=headersLogin)
    req = session.prepare_request(req)

    print('HEADERS')
    print(req.headers)
    print('BODY')
    print(req.body)

    print('SESSION COOKIE KEYS')
    print(session.cookies.keys())
    #hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    #form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    #print(form)
    postLogin = session.post(
        urlLogin,
        data=dataStr,
        headers={
            'origin': 'https://login.bancochile.cl',
            'referer': 'https://login.bancochile.cl/bancochile-web/persona/login/index.html',
            'ch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-419,es;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-length': '125',
            'content-type': 'application/x-www-form-urlencoded',
        },
        allow_redirects=False,
        )
    print('POST LOGIN')
    print('STATUS CODE')
    print(postLogin.status_code)
    print('HEADERS')
    print(postLogin.headers)
    print('TEXT')
    print(postLogin.text)
    redirectUrl = postLogin.headers["Location"]
    print(redirectUrl)
#    r = session.post(url=redirectUrl, data=dataStr)
#    print('REDIRECTED LOGIN')
#    print(r.status_code)
#    print(r.headers)
#    print(r.text)
#
#    r = session.post(urlCartola, data=payloadCartola)
#    print('POST_CARTOLA')
#    print('STATUS CODE')
#    print(r.status_code)
#    print('HEADERS')
#    print(r.headers)
#    print('TEXT')
#    print(r.text)
#    print('CONTENT')
#    print(r.content)
#    print('JSON')
#    print(r.json())
