import requests
import pandas as pd


class GeoAPI:
    API_KEY = 'd81015613923e3e435231f2740d5610b'
    LAT = '-35.836948753554054'
    LON = '-61.870523905384076'

    @classmethod
    def is_hot_in_pehuajo(cls):  # EJERCICIO NUMERO 1
        # Obtengo el dato con el metodo GET y lo guardo en la variable 'res' esta misma la formateo a Json para tener mas legibilidad, ademas guardo en una variable
        # para poder seleccionar el valor de Temperatura obtenida desde el foramto Json. Condiciono el posible error de Estado HTTP, seguido de la condicion de mayor a 28° del ejercicio.
        BASE_URL = f'https://api.openweathermap.org/data/2.5/weather?lat={GeoAPI.LAT}&lon={GeoAPI.LON}&appid={GeoAPI.API_KEY}&units=metric'
        res = requests.get(BASE_URL)
        data = res.json()
        temp = int(data['main']['temp'])
        if res.status_code < 300:
            if temp > 28:
                return True
            else:
                return False
        else:
            return False


_PRODUCT_DF = pd.DataFrame({'product_name': ['Chocolate', 'Granizado', 'Limon', 'Dulce de Leche'],
                            'quantity': [3, 10, 0, 5]})


def is_product_available(product_name, quantity):  # EJERCICIO NUMERO 2
    # Condiciono el DataFrame y lo convierto en un diccionario indexado con los parametros convertidos en llave valor: 'Chocolate': [3] para poder condicionar
    # El input del usuario. Si la condicion se cumple retorno True, si no, es asi retorna False
    filtro = _PRODUCT_DF[(_PRODUCT_DF['product_name'] == product_name) & (
        _PRODUCT_DF['quantity'] >= quantity)].set_index('product_name').T.to_dict('list')
    if filtro:
        return True
    else:
        print('No tenemos Stock de ese sabor.')
        return False


_AVAILABLE_DISCOUNT_CODES = ['Primavera2021',
                             'Verano2021', 'Navidad2x1', 'heladoFrozen']


def validate_discount_code(discount_code):  # EJERCICIO NUMERO 3
    codigo_validos = []
    for i in range(len(_AVAILABLE_DISCOUNT_CODES)):
        validos = "".join(set(_AVAILABLE_DISCOUNT_CODES[i]))
        codigo_validos.append(validos)
    codigo_mencion = "".join(set(discount_code))
    resultado = []
    for j in range(len(codigo_validos)):
        chars = codigo_validos[j]
        count = 0
        for k in range(len(chars)):
            if chars[k] not in codigo_mencion:
                count += 1
        if count >= 3:
            resultado.append(False)
        else:
            resultado.append(True)
    return any(resultado)       

def main():  # Respuestas y Inputs del Bot
    if GeoAPI.is_hot_in_pehuajo == True:
        print(
            f'\nMe derrito! ¿Me invitas un Helado?\n\nBienvenid@ a Heladeria Fronzen\n\nAqui tienes nuestros Sabores!\n\n{[_PRODUCT_DF]}\n')
    else:
        print(
            f'\nParece que esta fresquito, che... ¡Que mejor momento para comer un helado!\n\nBienvenid@ a Heladeria Fronzen\n\nAqui tienes nuestros Sabores!\n\n{[_PRODUCT_DF]}\n')
    limite = 0
    while (limite <= 4):
        try:
            limite += 1
            sabor = input('¿Qué gusto de helado vas a pedir?\n').capitalize()
            cantidad = int(input('\n¿Cuantos helados vas a llevar?\n'))
            if cantidad <= 0:
                cantidad = int(input('\nIngrese una cantidad correcta ¿Cuantos helados vas a llevar?\n'))
                if limite == 5:
                    print("¡Vuelva a intentarlo cuando tengamos Stock! Hasta PRONTO!!")
                    break
            else:
                stock = is_product_available(sabor, cantidad)
            if stock == True:
                while limite <= 4:
                    limite += 1
                    codigo_mencion = input("Ingrese un CUPON DE DESCUENTO: ")
                    Validate = validate_discount_code(codigo_mencion)
                    if Validate == True:
                        print("¡Pedido Confirmado! Gracias por tu compra")
                        break
                    else:
                        print(f'Ingrese un cupon valido!\n\n¡Intentos: {limite} de 4!\n')
                        if limite == 5:
                            print(
                                "¡Codigo Invalido!\n¡Pedido Confirmado! Gracias por tu compra")
                            break
                break
            else:
                print(f'Ingrese unos de los sabores disponibles!\n\n{[_PRODUCT_DF]}\n¡Intentos: {limite} de 4!\n')
                if limite == 5:
                    print("¡Vuelva a intentarlo cuando tengamos Stock! Hasta PRONTO!!")
                    break
        except:
            print(f'Ingrese unos de los sabores disponibles!\n\n{[_PRODUCT_DF]}\n¡Intentos: {limite} de 4!\n')
            if limite == 5:
                print("¡Vuelva a intentarlo cuando tengamos Stock! Hasta PRONTO!!")
                break


if __name__ == '__main__':
    main()
