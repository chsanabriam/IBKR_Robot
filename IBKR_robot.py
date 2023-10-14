import requests
import urllib3
import json
import time
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IBKRobot():

    def __init__(self):
        # Esta es la base para todos los request que hagamos en
        # la API
        self.base_url = "https://localhost:5000/v1/api/"

        # Se trae el número de cuenta usando el request de account
        endpoint = "iserver/accounts"
        accts_req = requests.get(url=self.base_url+endpoint, verify=False)
        if accts_req.status_code == 200:
            self.acct_id = accts_req.json()["accounts"][0]
        else:
            print(f"Error de conexión: {accts_req.status_code}")


    """
        Esta función se utiliza para salir de la sesión.
    """

    def logout(self):
        endpoint = "logout"

        logout_req = requests.post(url=self.base_url+endpoint, verify=False)
        print(logout_req.status_code)
        print(logout_req.text)

    """
        Esta función se utiliza para conocer el status de la conexión
    """

    def confirmStatus(self):
        # endpoint para validar el status de conexión
        endpoint = "iserver/auth/status"
        
        auth_req = requests.get(url=self.base_url+endpoint, verify=False)
        print(auth_req)
        print(auth_req.text)

    """
        Esta función es para mantener activa la sesión. Revisar con
        cuidado la documentación de la API para usar mejor este tema.
    """

    def ticklePin(self):
        endpoint = "tickle"

        tickle_req = requests.post(url=self.base_url+endpoint, verify=False)
        print(tickle_req)
        print(tickle_req.text)


    """
        Esta función busca el conid a partir del ticker de una acción.
    """
    def contractSearch(self):
        endpoint = "iserver/secdef/search"

        symbol = "symbol=AAPL"
        
        request_url = "".join([self.base_url, endpoint, "?", symbol])

        contract_req = requests.post(url=request_url, verify=False)
        contract_json = json.dumps(contract_req.json(), indent=2)

        print(contract_req)
        print(contract_json)


    """
        Esta función nos da la información actual de una acción. Revisar
        la documentación de la API para validar más resultados que se pueden traer.
        Por ahora de esta función nos interesa traer los datos del nombre de la acción,
         el precio actual y la hora actual del precio.
    """

    def marketSnapshot(self):
        endpoint = "iserver/marketdata/snapshot"

        # Establecer los conid (ticker)
        # Ver documentación de la API
        # conid = "conids=265598,8314"
        conid = "conids=265598"

        # Since es el valor de tiempo en milisegundos en epocas
        # Se puede obviar y el resultado es igual
        # since = "since=[]"

        fields = "fields=31,55,84,86"
        # fields = "fields=[]"


        params = "&".join([conid, fields])
        request_url = "".join([self.base_url, endpoint, "?", params])

        md_req = requests.get(url=request_url, verify=False)
        md_json = json.dumps(md_req.json(), indent=2)

        time_updated_epoch = md_req.json()[0]["_updated"]
        time_updated = datetime.datetime.fromtimestamp(time_updated_epoch / 1000.0)

        print(md_req)
        print(md_json)
        print(f"Hora de actualización: {time_updated}")


    """
        Esta función traera la data histórica de una acción.
    """

    def historicalData(self):
        endpoint = "hmds/history"

        # Establecer los conid (ticker)
        # Ver documentación de la API
        conid = "conid=265598"
        period = "period=1w"
        bar = "bar=1d"
        outsideRth = "outsideRth=true" #Regular Trading Hours
        barType = "barType=midpoint"

        params = "&".join([conid, period, bar, outsideRth, barType])
        request_url = "".join([self.base_url, endpoint, "?", params])

        hd_req = requests.get(url=request_url, verify=False)
        hd_json = json.dumps(hd_req.json(), indent=2)

        print(hd_req)
        print(hd_json)

    
    """
        Esta función lista las ordenes que se tengan
    """

    def listOrders(self):
        endpoint = "iserver/account/orders"

        order_list_req = requests.get(url=self.base_url+endpoint, verify=False)
        order_list_json = json.dumps(order_list_req.json(), indent=2)

        print(order_list_req)
        print(order_list_json)
    
    """
        Esta función se utiliza para hacer una solicitud de orden.
        Para más información ver la documentación de la API
    """

    def orderRequest(self):
        endpoint = "iserver/account/"+self.acct_id+"/orders"

        json_body = {
            "orders": [{
                "conid": 265598,
                "orderType": "MKT",
                "side": "BUY",
                "tif": "DAY",
                "quantity": 10
            }]
        }

        order_req = requests.post(url=self.base_url+endpoint, verify=False, json=json_body)
        order_json = json.dumps(order_req.json(), indent=2)

        print(order_req.status_code)
        print(order_json)
    
    """
        Esta función me devuelve las cuentas que se pueden usar.
    """

    def getAccounts(self):
        endpoint = "iserver/accounts"

        accts_req = requests.get(url=self.base_url+endpoint, verify=False)
        accts_json = json.dumps(accts_req.json(), indent=2)

        print(accts_req.status_code)
        print(accts_json)

    
    """
        Esta función se utiliza para traer el resumen de la cuenta
        Account Summary
    """

    def acctSummary(self):
        endpoint = "portfolio/"+self.acct_id+"/summary"

        summ_req = requests.get(url=self.base_url+endpoint, verify=False)
        summ_json = json.dumps(summ_req.json(), indent=2)

        print(summ_req.status_code)
        print(summ_json)


if __name__ == "__main__":
    ibkrob = IBKRobot()
    # ibkrob.confirmStatus()
    ibkrob.ticklePin()
    # ibkrob.contractSearch()
    # ibkrob.marketSnapshot()
    # ibkrob.historicalData()
    # ibkrob.orderRequest()
    # ibkrob.getAccounts()
    ibkrob.acctSummary()
    #ibkrob.listOrders()