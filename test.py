"""
Archivo de prueba para el cliente de la API CuboPago
Este script muestra ejemplos de cómo utilizar todas las funcionalidades
del cliente CuboClient para procesar pagos y generar links de suscripción.
"""

from cuboClient import CuboClient

# Inicializar el cliente con una API Key (demo)
# Nota: Esta API Key es ficticia y solo se usa para fines de demostración
client = CuboClient(api_key="93aab3a749aa8da9")

def test_pay_method():
    """
    Ejemplo de uso del método pay() para procesar un pago único
    """
    print("\n=== PRUEBA DE PAGO ÚNICO ===")
    
    # Datos del pago
    payment_data = {
        "clientName": "John Doe",
        "clientEmail": "cliente@ejemplo.com",
        "clientPhone": "+50322577777",
        "description": "Compra de productos",
        "amount": 10.50,  # Se convertirá automáticamente a 1050 centavos
        "cardHolder": "John Doe",
        "cardNumber": "4000000000000416",
        "cvv": "123",
        "month": "12",
        "year": "26"
    }
    
    print("Enviando solicitud de pago...")
    # Procesar el pago
    response = client.pay(payment_data)
    
    print("\nRespuesta del servidor:")
    print(response)
    
    # Manejar la respuesta
    result = client.handle_response(response)
    
    print("\nRespuesta procesada:")
    print(result)
    
    # Verificar si el pago fue exitoso
    if result.get("success"):
        print("\n✅ Pago procesado exitosamente")
        print(f"Referencia: {result.get('reference_id')}")
        print(f"Código de autorización: {result.get('authorization_code')}")
        print(f"Fecha de procesamiento: {result.get('processed_at')}")
    else:
        print("\n❌ Error al procesar el pago")
        print(f"Mensaje: {result.get('message')}")

def test_subscription_method():
    """
    Ejemplo de uso del método subscription() para procesar un pago de suscripción
    """
    print("\n=== PRUEBA DE PAGO DE SUSCRIPCIÓN ===")
    
    # Datos de la suscripción
    subscription_data = {
        "clientName": "Jane Smith",
        "clientEmail": "jane@ejemplo.com",
        "clientPhone": "+50311223344",
        "description": "Suscripción Premium",
        "amount": 15.99,  # Se convertirá automáticamente a 1599 centavos
        "cardHolder": "Jane Smith",
        "cardNumber": "4000000000000416",
        "cvv": "456",
        "month": "10",
        "year": "25",
        "installments": 12  # 12 meses de suscripción
    }
    
    print("Enviando solicitud de suscripción...")
    # Procesar el pago de suscripción
    response = client.subscription(subscription_data)
    
    print("\nRespuesta del servidor:")
    print(response)
    
    # Manejar la respuesta
    result = client.handle_subscription_response(response)
    
    print("\nRespuesta procesada:")
    print(result)
    
    # Verificar si la suscripción fue exitosa
    if result.get("success"):
        print("\n✅ Suscripción procesada exitosamente")
        print(f"Referencia: {result.get('reference_id')}")
        print(f"Código de autorización: {result.get('authorization_code')}")
        print(f"Fecha de procesamiento: {result.get('processed_at')}")
    else:
        print("\n❌ Error al procesar la suscripción")
        print(f"Mensaje: {result.get('message')}")

def test_create_subscription_link():
    """
    Ejemplo de uso del método create_subscription_link() para generar un link de pago de suscripción
    """
    print("\n=== PRUEBA DE GENERACIÓN DE LINK DE SUSCRIPCIÓN ===")
    
    # Datos del link de suscripción
    link_data = {
        "description": "Plan Anual Premium",
        "amount": 99.99,  # Se convertirá automáticamente a 9999 centavos
        "installments": 12,  # 12 meses de suscripción
        "redirectUri": "https://ejemplo.com/confirmacion"
    }
    
    print("Generando link de suscripción...")
    # Generar el link de suscripción
    response = client.create_subscription_link(link_data)
    
    print("\nRespuesta procesada:")
    print(response)
    
    # Verificar si el link fue generado exitosamente
    if response.get("success"):
        print("\n✅ Link de suscripción generado exitosamente")
        print(f"Token: {response.get('payment_intent_token')}")
        print(f"Descripción: {response.get('description')}")
        print(f"Monto: {response.get('amount')}")
        print(f"Moneda: {response.get('currency', {}).get('iso', 'USD')}")
        print(f"Cuotas: {response.get('installments')}")
        print(f"Fecha de inicio: {response.get('starting_date')}")
        print(f"Fecha de finalización: {response.get('ending_date')}")
        print(f"URL de pago: {response.get('redirect_uri')}")
    else:
        print("\n❌ Error al generar el link de suscripción")
        print(f"Mensaje: {response.get('message')}")

if __name__ == "__main__":
    # Ejecutar todas las pruebas
    test_pay_method()
    test_subscription_method()
    test_create_subscription_link()
    
    print("\n=== RESUMEN DE PRUEBAS ===")
    print("Todas las pruebas han sido ejecutadas.")
    print("Para usar este cliente en tu aplicación, sigue estos pasos:")
    print("1. Importa la clase CuboClient")
    print("2. Inicializa el cliente con tu API Key")
    print("3. Llama al método correspondiente según tu necesidad")
    print("4. Procesa la respuesta utilizando los métodos handle_*")