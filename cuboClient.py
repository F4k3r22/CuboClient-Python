import requests
import json

class CuboClient:
    def __init__(self, api_key: str, url="https://api.cubo.com"):
        """ Cliente API de cuboClient (No se si aun esta en funcionaminto o la url correcta para la API)"""
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