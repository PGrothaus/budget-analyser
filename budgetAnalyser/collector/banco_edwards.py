import time
import json

from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys

urlLoginPage = "https://login.bancochile.cl/bancochile-web/persona/login/index.html"
urlLoginSubmit = "https://login.bancochile.cl/oam/server/auth_cred_submit"

driver = webdriver.Firefox()

driver.implicitly_wait(15)

driver.get(urlLoginPage)

# u = driver.find_elements_by_xpath("//div[2]/div[1]/article")
usr = driver.find_element_by_id("iduserName")
pw = driver.find_element_by_name("userpassword")

usr.send_keys("111111111")
pw.send_keys("asdfghj")
pw.send_keys(Keys.RETURN)

time.sleep(15)

urlMovs = "https://portalpersonas.bancochile.cl/mibancochile-web/front/personaBEC/index.html#/cuentas/movimientosCuenta"
driver.get(urlMovs)

time.sleep(15)

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        if "getcartola" in request.url:
            print(
                request.url,
                request.response.status_code,
                request.response.headers["Content-Type"],
            )
            res = json.loads(request.response.body)
            with open("./test.response.json", "w") as f:
                json.dump(res, f)
