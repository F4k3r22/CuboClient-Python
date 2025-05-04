from cuboClient import CuboClient

client = CuboClient(api_key="93aab3a749aa8da9")

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

# Procesar el pago
response = client.pay(payment_data)

print(response)


# Manejar la respuesta
result = client.handle_response(response)
print(result)