import requests
import json

class CuboClient:
    def __init__(self, api_key: str, url="https://api.cubo.com"):
        """ Cliente API de Cubopago.com """
        self.api_key = api_key
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        self.url = url

    def convert_centv(self, amount):
        return int(amount * 100)

    def pay(self, data):
        """
        Procesa un pago utilizando la API de CuboPago
        
        Args:
            data (dict): Datos del pago
            
        Returns:
            dict: Respuesta de la API o error
        """
        url = f"{self.url}/api/v1/transactions"
        
        # Asegurarse que data sea un diccionario
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"error": "Los datos proporcionados no son un JSON válido"}
        
        # Convertir amount a centavos si es necesario
        if 'amount' in data and isinstance(data['amount'], float):
            data['amount'] = self.convert_centv(data['amount'])
        
        try:
            # Imprimir información de depuración
            print(f"URL: {url}")
            print(f"Headers: {self.headers}")
            print(f"Datos: {json.dumps(data, indent=2)}")
            
            # Realizar la solicitud
            response = requests.post(url=url, headers=self.headers, json=data)
            
            # Imprimir respuesta para depuración
            print(f"Código de estado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
            # Verificar si la respuesta tiene contenido
            if response.content:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {"error": f"La respuesta no es un JSON válido: {response.text[:100]}..."}
            else:
                return {"error": "Respuesta vacía del servidor"}
                
        except requests.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}

    def handle_response(self, response):
        """
        Procesa la respuesta de la API
        
        Args:
            response (dict): Respuesta de la API
            
        Returns:
            dict: Información procesada
        """
        # Primero verificar si hay error en la respuesta
        if "error" in response:
            return {
                "success": False,
                "message": response["error"]
            }
            
        # Verificar respuesta exitosa de la API
        if "status" in response and response["status"] == "SUCCEEDED":
            return {
                "success": True,
                "reference_id": response.get("referenceId"),
                "authorization_code": response.get("authorizationCode"),
                "processed_at": response.get("processedAt")
            }
        else:
            return {
                "success": False,
                "message": response.get("message", "Error desconocido")
            }

    def subscription(self, data):
        """
        Procesa un pago de suscripción utilizando la API de CuboPago
        
        Args:
            data (dict): Datos del pago de suscripción que deben incluir:
                - clientName: Nombre del cliente
                - clientEmail: Correo electrónico del cliente
                - clientPhone: Teléfono del cliente con código de país
                - description: Descripción de la transacción
                - amount: Cantidad de dinero a pagar (en centavos)
                - cardHolder: Nombre del titular de la tarjeta
                - cardNumber: Número de la tarjeta
                - cvv: Código de seguridad
                - month: Mes de expiración (formato MM)
                - year: Año de expiración (formato YY)
                - installments: Cantidad de cuotas mensuales
            
        Returns:
            dict: Respuesta de la API o error
        """
        url = f"{self.url}/api/v1/transactions/subscription"
        
        # Asegurarse que data sea un diccionario
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"error": "Los datos proporcionados no son un JSON válido"}
        
        # Convertir amount a centavos si es necesario
        if 'amount' in data and isinstance(data['amount'], float):
            data['amount'] = self.convert_centv(data['amount'])
        
        # Verificar campos requeridos
        required_fields = [
            'clientName', 'clientEmail', 'clientPhone', 'description', 
            'amount', 'cardHolder', 'cardNumber', 'cvv', 'month', 'year', 'installments'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}
        
        try:
            # Imprimir información de depuración
            print(f"URL: {url}")
            print(f"Headers: {self.headers}")
            print(f"Datos: {json.dumps(data, indent=2)}")
            
            # Realizar la solicitud
            response = requests.post(url=url, headers=self.headers, json=data)
            
            # Imprimir respuesta para depuración
            print(f"Código de estado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
            # Verificar si la respuesta tiene contenido
            if response.content:
                try:
                    response_data = response.json()
                    # Procesar la respuesta utilizando el método handle_response
                    return self.handle_response(response_data)
                except json.JSONDecodeError:
                    return {"error": f"La respuesta no es un JSON válido: {response.text[:100]}..."}
            else:
                return {"error": "Respuesta vacía del servidor"}
                
        except requests.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}

    def create_subscription_link(self, data):
        """
        Genera un link de pago de suscripción utilizando la API de CuboPago
        
        Args:
            data (dict): Datos de la suscripción que deben incluir:
                - description: Descripción de la suscripción
                - amount: Cantidad de dinero a pagar
                - installments: Cantidad de cuotas mensuales
                - redirectUri: URL de redirección tras completar el pago
            
        Returns:
            dict: Respuesta de la API o error
        """
        url = f"{self.url}/api/v1/links/subscription"
        
        # Asegurarse que data sea un diccionario
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"error": "Los datos proporcionados no son un JSON válido"}
        
        # Convertir amount a centavos si es necesario
        if 'amount' in data and isinstance(data['amount'], float):
            data['amount'] = self.convert_centv(data['amount'])
        
        # Verificar campos requeridos
        required_fields = ['description', 'amount', 'installments', 'redirectUri']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}
        
        try:
            # Imprimir información de depuración
            print(f"URL: {url}")
            print(f"Headers: {self.headers}")
            print(f"Datos: {json.dumps(data, indent=2)}")
            
            # Realizar la solicitud
            response = requests.post(url=url, headers=self.headers, json=data)
            
            # Imprimir respuesta para depuración
            print(f"Código de estado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
            # Verificar si la respuesta tiene contenido
            if response.content:
                try:
                    response_data = response.json()
                    # Procesar la respuesta utilizando el método específico para links de suscripción
                    return self.handle_subscription_link_response(response_data)
                except json.JSONDecodeError:
                    return {"error": f"La respuesta no es un JSON válido: {response.text[:100]}..."}
            else:
                return {"error": "Respuesta vacía del servidor"}
                
        except requests.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}

    def handle_subscription_link_response(self, response):
        """
        Procesa la respuesta de la API para crear links de suscripción
        
        Args:
            response (dict): Respuesta de la API
            
        Returns:
            dict: Información procesada
        """
        # Verificar si hay error en la respuesta
        if "statusCode" in response and response.get("error"):
            return {
                "success": False,
                "message": response.get("message", "Error desconocido"),
                "error": response.get("error")
            }
            
        # Verificar respuesta exitosa de la API
        if "paymentIntentToken" in response:
            return {
                "success": True,
                "payment_intent_token": response.get("paymentIntentToken"),
                "description": response.get("description"),
                "amount": response.get("amount"),
                "currency": response.get("currency"),
                "installments": response.get("installments"),
                "starting_date": response.get("startingDate"),
                "ending_date": response.get("endingDate"),
                "redirect_uri": response.get("cuboRedirectUri")
            }
        else:
            return {
                "success": False,
                "message": "Respuesta inesperada del servidor"
            }

    def handle_subscription_response(self, response):
        """
        Procesa la respuesta de la API para pagos de suscripción
    
        Args:
            response (dict): Respuesta de la API de pago de suscripción
        
        Returns:
            dict: Información procesada con formato unificado
        """
        # Verificar si hay error en la respuesta (código de estado diferente a 2xx)
        if "statusCode" in response and response.get("statusCode") >= 400:
            return {
                "success": False,
                "message": response.get("message", "Error desconocido"),
                "error_code": response.get("statusCode")
            }
    
        # Verificar si hay un error genérico
        if "error" in response:
            return {
                "success": False,
                "message": response.get("error")
            }
            
        # Verificar respuesta exitosa de la API
        if "status" in response and response["status"] == "SUCCEEDED":
            return {
                "success": True,
                "reference_id": response.get("referenceId"),
                "authorization_code": response.get("authorizationCode"),
                "processed_at": response.get("processedAt"),
                "status": response.get("status")
            }
        else:
            # En caso de que la respuesta no tenga el formato esperado
            return {
                "success": False,
                "message": "Respuesta inesperada o pago rechazado",
                "raw_response": response
            }