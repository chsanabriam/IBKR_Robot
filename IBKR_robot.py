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

        symbol = "symbol=SPY"
        
        request_url = "".join([self.base_url, endpoint, "?", symbol])

        contract_req = requests.post(url=request_url, verify=False)
        contract_json = json.dumps(contract_req.json(), indent=2)

        print(contract_req)
        print(contract_json)


    """
        Esta función retorna información de un contrato
    """

    def contractDetails(self):
        endpoint = "iserver/secdef/info"

        # conid = "conid=265598" # AAPL
        conid = "conid=756733" # SPY
        sectype = "sectype=OPT"
        month = "month=OCT23"
        strike = "strike=423.0"

        params = "&".join([conid, sectype, month, strike])

        req_url = "".join([self.base_url,endpoint,"?",params])

        cdetail_req = requests.get(url=req_url, verify=False)
        cdetail_json = json.dumps(cdetail_req.json(), indent=2)

        print(cdetail_req.status_code)
        print(cdetail_json)



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
        # conid = "conids=265598,756733"
        conid = "conids=656942176"

        # Since es el valor de tiempo en milisegundos en epocas
        # Se puede obviar y el resultado es igual
        # since = "since=[]"

        # fields = "fields=31,55,84,86"
        fields = "fields=[]"


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
        Esta función es market snapshot pero en la función
        Beta
    """

    def marketSnapshotBeta(self):
        endpoint = "md/snapshot"

        # conid = "conids=654752772"
        conid = "conids=265598"

        exchange = "SMART"
        # instr_type  = "instrType=STK"
        instr_type  = "STK"

        # params = conid+"@"+exchange+":"+instr_type
        params = conid+":"+instr_type

        req_url = "".join([self.base_url, endpoint, "?", params])

        md_req = requests.get(url=req_url, verify=False)
        md_json = json.dumps(md_req.json(), indent=2)

        print(md_req.status_code)
        print(md_json)


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
        Esta función devuelve los strikes de una opción dada. Se necesita:
        1.) conid de la acción
        2.) sectype que en este caso es OPT para opción
        3.) month que es el mes que se quiere ver los strikes
    """

    def optStrikes(self):
        endpoint = "iserver/secdef/strikes"

        # conid = "conid=265598"
        conid = "conid=756733"
        sectype = "sectype=OPT"
        month = "month=OCT23"

        params = "&".join([conid, sectype, month])
        req_url = "".join([self.base_url, endpoint, "?", params])

        strike_req = requests.get(url=req_url, verify=False)
        strike_json = json.dumps(strike_req.json(), indent=2)

        print(strike_req.status_code)
        print(strike_json)


    """
        Esta función lista las ordenes que se tengan
    """

    def orderRequest(self):
        endpoint = "iserver/account/orders"

        order_req = requests.get(url=self.base_url+endpoint, verify=False)
        order_json = json.dumps(order_req.json(), indent=2)

        print(order_req.status_code)
        print(order_json)
    

    """
        Esta función se utiliza para hacer una solicitud y colocación de orden.
        Para más información ver la documentación de la API
    """

    def placeOrder(self):
        endpoint = "iserver/account/"+self.acct_id+"/orders"

        # json file para crear una orden. En este caso la orden es de precio de mercado.
        # En el caso de que queramos hacer un precio limite se debe cambiar a LMT y colocar
        # un parametro de precio (price)
        json_body = {
            "orders": [{
                "conid": 265598,
                "orderType": "MKT",
                # "price": 188,
                "side": "SELL",
                "tif": "DAY",
                "quantity": 1
            }]
        }

        order_req = requests.post(url=self.base_url+endpoint, verify=False, json=json_body)
        order_json = json.dumps(order_req.json(), indent=2)

        print(order_req.status_code)
        print(order_json)

    """
        Esta función nos permite hacer una orden compleja, es decir una orden 
        que tenga tanto un stop_limit como un profit_take
    """

    def complexOrder(self):
        endpoint = "iserver/account/"+self.acct_id+"/orders"

        # json file para colocar una orden a precio de mercado pero va a
        # tener un limite para hacer un profit take y un stop loss

        json_body = {
            "orders": [
                {
                    "acctId": self.acct_id,
                    "conid": 265598,
                    "cOID": "66807300",
                    "orderType": "LMT",
                    "listingExchange": "SMART",
                    "outsideRTH": True,
                    "price": 179.5,
                    "side": "BUY",
                    "ticker": "AAPL",
                    "tif": "DAY",
                    "referrer": "ParentOrder",
                    "quantity": 1,
                    "useAdaptive": False,
                    "isClose": False
                },
                {
                    "acctId": self.acct_id,
                    "conid": 265598,
                    "orderType": "LMT",
                    "listingExchange": "SMART",
                    "outsideRTH": True,
                    "price": 181.5,
                    "side": "SELL",
                    "ticker": "AAPL",
                    "tif": "DAY",
                    "referrer": "ProfitTakerOrder",
                    "quantity": 1,
                    "useAdaptive": False,
                    "isClose": False,
                    "parentId": "66807300",
                },
                {
                    "acctId": self.acct_id,
                    "conid": 265598,
                    "orderType": "STP",
                    "listingExchange": "SMART",
                    "outsideRTH": False,
                    "price": 177.5,
                    "side": "SELL",
                    "ticker": "AAPL",
                    "tif": "DAY",
                    "referrer": "StopLossOrder",
                    "quantity": 1,
                    "useAdaptive": False,
                    "isClose": False,
                    "parentId": "66807300",
                }
            ]
        }

        order_req = requests.post(url=self.base_url+endpoint, verify=False, json=json_body)
        order_json = json.dumps(order_req.json(), indent=2)

        print(order_req.status_code)
        print(order_json)
    
    """
        Esta función permite modificar las ordenes que se hayan colocado
    """
    def orderModify(self):
        endpoint = "iserver/account/"+self.acct_id+"/order/"
        order_id = "516037338"

        # json file para modificar una orden. En este caso la orden es de precio de mercado.
        # En el caso de que queramos hacer un precio limite se debe cambiar a LMT y colocar
        # un parametro de precio (price)
        json_body = {
            "conid": 265598,
            "conidex": "265598",
            "orderType": "LMT",
            "price": 180,
            "side": "BUY",
            "tif": "DAY",
            "quantity": 1
        }

        modify_url = "".join([self.base_url, endpoint, order_id])

        order_req = requests.post(url=modify_url, verify=False, json=json_body)
        order_json = json.dumps(order_req.json(), indent=2)

        print(order_req.status_code)
        print(order_json)


    """
        Esta función responde en caso de querer cancelar una orden
    """

    def orderCancel(self):
         endpoint = "iserver/account/"+self.acct_id+"/order/"
         order_id = "602267396"

         cancel_url = "".join([self.base_url, endpoint, order_id])

         cancel_req = requests.delete(url=cancel_url, verify=False)
         cancel_json = json.dumps(cancel_req.json(), indent=2)

         print(cancel_req.status_code)
         print(cancel_json)


    """
        Esta función responde en caso de salir un warning de confirmación
    """

    def orderReply(self):
        endpoint = "iserver/reply/"
        reply_id = "7c87f00f-f303-4931-862b-ba62c5570bcd"

        json_body = {
            "confirmed": True
        }

        reply_url = "".join([self.base_url, endpoint, reply_id])

        reply_req = requests.post(url=reply_url, verify=False, json=json_body)
        reply_json = json.dumps(reply_req.json(), indent=2)

        print(reply_req.status_code)
        print(reply_json)


    """
        Esta función retorna el status de una orden
    """

    def orderStatus(self):
        endpoint = "iserver/account/order/status/"
        order_id = "516037340"

        order_url = "".join([self.base_url, endpoint, order_id])

        order_req = requests.get(url=order_url, verify=False)
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

    """
        Esta función se utiliza para hacer un request de las posiciones que
        se tienen en la cuenta
    """

    def acctPosition(self):
        endpoint = "portfolio/"+self.acct_id+"/positions/0"

        pos_req = requests.get(url=self.base_url+endpoint, verify=False)
        pos_json = json.dumps(pos_req.json(), indent=2)

        print(pos_req.status_code)
        print(pos_json)



if __name__ == "__main__":
    ibkrob = IBKRobot()
    # ibkrob.confirmStatus()
    ibkrob.ticklePin()
    # ibkrob.contractSearch()
    # ibkrob.contractDetails()
    # ibkrob.marketSnapshot()
    # ibkrob.marketSnapshotBeta()
    # ibkrob.historicalData()
    # ibkrob.optStrikes()
    # ibkrob.placeOrder()
    # ibkrob.complexOrder()
    # ibkrob.orderReply()
    # ibkrob.orderStatus()
    # ibkrob.orderModify()
    # ibkrob.orderCancel()
    # ibkrob.orderRequest()
    # ibkrob.getAccounts()
    # ibkrob.acctSummary()
    # ibkrob.acctPosition()
    # ibkrob.logout()
    