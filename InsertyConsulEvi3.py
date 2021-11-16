import sqlite3
from sqlite3 import Error
import sys
import datetime

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
        descripcion=input('Ingrese la descripción del articulo: ')
        piezas=int(input('Ingrese el número de piezas vendidas: '))
        precio=float(input('Ingrese el precio del articulo vendido: '))
        suma_parcial=piezas*precio
        total=total+suma_parcial
        try:
            with sqlite3.connect("Ventas.db") as conn: #Puente
                mi_cursor = conn.cursor() #Mensajero
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
    print(f"Total de venta: {total}")
    print(f"Iva de venta: {iva}")
    print(f"Total final: {total_final}")


def consulta_folio():
    folio_consulta=int(input("ingrese la clave a buscar: "))
    total=0
    try:
        with sqlite3.connect("Ventas.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM articulos WHERE clave = ?",(folio_consulta,))
            registro1 = c.fetchall()
            if registro1:
                c.execute("""SELECT venta.clave, venta.fecha, articulos.descripcion, articulos.piezas,\
                            articulos.precio\
                            FROM articulos \
                            INNER JOIN venta on articulos.clave = venta.clave \
                            WHERE articulos.clave = ?;""",(folio_consulta,))
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
                print("La clave que busca no existe")
    except Error as e:
        print(e)
    except Exception:
        print(f"Error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()

def reporte_ventas():
    fecha_consulta=input("ingrese la fecha de venta a buscar(YYY-MM-DD): ")
    total=0
    try:
        with sqlite3.connect("Ventas.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM venta WHERE fecha = ?",(fecha_consulta,))
            registro1 = c.fetchall()
            if registro1:
                c.execute("""SELECT venta.clave, venta.fecha, articulos.descripcion, articulos.piezas,\
                            articulos.precio\
                            FROM articulos \
                            INNER JOIN venta on articulos.clave = venta.clave \
                            WHERE venta.fecha = ?;""",(fecha_consulta,))
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
    print("*"*50)
    print("MENÚ")
    print("1) Agregar datos")
    print("2) Consulta")
    print("3) Generar reporte de venta ")
    print("4) Salir")
    respuesta = int(input("Elija una opción: "))

    if respuesta == 1:
        print(venta())

    if respuesta == 2:
        print(consulta_folio())

    if respuesta == 3:
        print(reporte_ventas())

    if respuesta == 4:
        print("Gracias por utilizar nuestro programa")
        break

