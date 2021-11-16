import sqlite3
from sqlite3 import Error
import sys
import datetime
import re

separador = '*' * 80
def venta():
    folio=input('Ingrese el folio de venta: ')
    fecha= datetime.date.today()
    fecha=fecha.strftime('%Y-%m-%d')
    print(f"Folio de venta: {folio}")
    print(f"Fecha de venta: {fecha}")
    total=0
    try:
        with sqlite3.connect("Ventas.db") as conn: #Puente
            mi_cursor = conn.cursor() #Mensajero
            mi_cursor.execute("INSERT INTO venta VALUES(?, ?)",(folio,fecha))
            print("Registro agregado exitosamente")
    except Error as e:
        print (e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()


    while True:
        while True:
            descripcion=input('Ingrese la descripción del articulo: ')
            if re.match("^[A-Za-z0-9_-]*$",descripcion):
                break
            else:
                print('Ingrese una descripción valida')

        while True:
            piezas = int(input('Ingresa la cantidad de piezas: '))
            precio = float(input('Ingresa el precio del articulo: '))
            if piezas > 0 and precio > 0:
                break
            else:
                print('La cantidad o el precio ingresado no son validos, favor de registrarlos nuevamente')
                input('Presiona ENTER para continuar')
                print(separador)

        suma_parcial=piezas*precio
        total=total+suma_parcial
        try:
            with sqlite3.connect("Ventas.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("INSERT INTO articulos VALUES(?, ?, ?, ?)",(descripcion,piezas,precio,folio))
                print("Registro agregado exitosamente")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

        continuar=input("Desea agregar otro articulo?(S/N): ")
        if continuar == "N":
            break

    iva=total*16/100
    total_final=iva+total
    print(f"Total de venta: {total}\n")
    print(f"Iva de venta: {iva}\n")
    print(f"Total final: {total_final}\n")
    print(f"Fecha de registro de la venta: {fecha}")




def reporte_ventas():
    while True:
            fecha_actual = datetime.date.today()
            fecha_venta = input("Dime la fecha de la venta(YYYY-MM-DD): \n")
            fecha_venta_procesada = datetime.datetime.strptime(fecha_venta,"%Y-%m-%d").date()
            print(fecha_venta_procesada)
            print(fecha_actual)
            if fecha_venta_procesada <= fecha_actual:
                print(separador)
                break
            else:
                print("La fecha ingresa es superior a la del sistema")
                print(separador)

    total=0
    try:
        with sqlite3.connect("Ventas.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM venta WHERE fecha = ?",(fecha_venta,))
            registro1 = c.fetchall()
            if registro1:
                c.execute("""SELECT venta.clave, venta.fecha, articulos.descripcion, articulos.piezas,\
                            articulos.precio\
                            FROM articulos \
                            INNER JOIN venta on articulos.clave = venta.clave \
                            WHERE venta.fecha = ?;""",(fecha_venta,))
                registros = c.fetchall()
                if registros:
                    print("Clave\tFecha\t\tDescripción\tPiezas\tPrecio")
                    print("*"*50)
                    for clave, fecha, descripcion, piezas, precio in registros:
                        print(f"{clave}\t{fecha}\t{descripcion}\t\t{piezas}\t${precio:,.2f}")
                        suma_parcial=piezas*precio
                        total=total+suma_parcial
                    print("*"*50)
                iva=total*16/100
                total_final=iva+total
                print(f"Total de venta: {total}")
                print(f"Iva de venta: {iva}")
                print(f"Total final: {total_final}")
            else:
                print("La fecha que busca no existe")
    except Error as e:
        print(e)
    except Exception:
        print(f"Error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()


while True:
    print(separador)
    print("MENÚ")
    print("1) Agregar datos")
    print("2) Consulta por fecha")
    print("3) Salir")
    respuesta = int(input("Elija una opción: "))
    #try:
    if respuesta == 1:
        print(venta())

    if respuesta == 2:
        print(reporte_ventas())

    if respuesta == 3:
        print("Gracias por utilizar nuestro programa")
        break
    else:
        print("Opción no valida")