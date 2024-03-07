import random
import json
import os

menu_principal = {"1": "ABM (Alta, baja y modificación)","2": "Calificación de títulos","3":"Reportes y estadísticas","4": "Salir",}
menu_abm = {"1": "Alta de nueva película","2": "Modificación de película existente","3": "Baja de película (eliminar)","4": "Volver",}
menu_modif_elim = {"1": "Buscar por id","2": "Buscar por titulo","3": "Volver",}
menu_repor_estad = {"1": "Listado de películas","2": "Películas de mayor puntaje","3":"Porcentaje de películas disponibles", "4":"Películas eliminadas", "5": "Volver",}
menu_calificacion = {"1":"Calificación de películas","2": "Volver"}
generos = {"1":"Acción", "2":"Animación", "3":"Comedia", "4":"Drama", "5":"Ciencia ficción", "6":"Terror", "7":"Suspenso", "8":"Romántica", "9": "Fantasía", "10": "Familiar"}
clasificaciones = {"1":"ATP","2":"PG","3": "PG-13","4": "R", "5":"NC-17"}
llaves = {"1":"id", "2": "titulo", "3": "genero", "4": "sinopsis", "5": "duracion", "6":"pais de origen", "7": "idioma", "8": "clasificacion", "9": "calificacion", "10": "disponible"}
pelicula_nueva = {} 

def leer_pelis(archivo):
    with open(archivo, "r") as contenido:
        peliculas=json.load(contenido)
    return peliculas

peliculas = leer_pelis("peliculas.json")
pelis_eliminadas = leer_pelis("pelis_eliminadas.json")

def escribir_archivo(nombre_archivo, lista):
    with open(nombre_archivo, "w") as conexion:
        json.dump(lista, conexion)

#funciones para agregar, modificar y eliminar peliculas
def agregar_pelicula():
    while True:
        numero_pelis = (input("¿Cuántas peliculas desea agregar?: "))
        if str.isnumeric(numero_pelis):
            numero_pelis = int(numero_pelis)
            break
        else:
            print("Ingrese un número por favor.")
            continue
    for i in range(0, numero_pelis):
        pelicula_nueva["id"] = len(peliculas) + len(pelis_eliminadas) + 1    
        while True:
            pelicula_nueva["titulo"] = input("Ingrese el título de la película: ").upper()
            for peli in peliculas:
                if pelicula_nueva["titulo"] == peli["titulo"]:
                    print("El titulo ya existe, intente otra vez. ")
                    break
            if pelicula_nueva["titulo"] == peli["titulo"]:
                continue
            else:
                break
        print("Ingrese el Genero de la Película")    
        pelicula_nueva["genero"] = []
        genero = (ingresar(generos))
        pelicula_nueva["genero"].append(genero)
        while True:
            otro =  input("¿Desea ingresar otro Género para la misma película? s/n: ")
            if otro == "s":
                genero = (ingresar(generos))
                pelicula_nueva["genero"].append(genero)
            elif otro == "n":
                break
            else:
                ("opcion incorrecta, ingrese \"s\" o \"n\".")
                continue
        while True:
            pelicula_nueva["duracion"] = (input("Ingrese la duración de la película en minutos: "))
            if str.isnumeric(pelicula_nueva["duracion"]):
                pelicula_nueva["duracion"] = int(pelicula_nueva["duracion"])
                break
            else:
                print("Por favor, ingrese un número entero.")
                continue   
        pelicula_nueva["sinopsis"] = input("Ingrese una breve sinopsis: ").capitalize()
        pelicula_nueva["pais de origen"] = input("Ingrese el país de origen: ").capitalize()
        pelicula_nueva["idioma"] = input("Ingrese el idioma: ").capitalize()
        print("Ingrese la Clasificación: ")
        pelicula_nueva["clasificacion"] = ingresar(clasificaciones)
        while True:
            pelicula_nueva["calificacion"] = (input("Ingrese la calificación: "))
            if str.isnumeric(pelicula_nueva["calificacion"]):
                pelicula_nueva["calificacion"] = int(pelicula_nueva["calificacion"])
                if pelicula_nueva["calificacion"] < 1 or pelicula_nueva["calificacion"] > 10:
                        print("El numero debe ser entre 1 y 10")
                        continue
                else:
                    pelicula_nueva["calificacion"] = float(pelicula_nueva["calificacion"])
                    break
            else:
                print("Ingrese un número por favor.")
                continue   
        pelicula_nueva["disponible"] = es_verdadero()
        peliculas.append(pelicula_nueva.copy())
    return peliculas

#funciones para modificar peliculas por id, titulo
def modificar_pelicula_por_id(peliculas, id_buscado):
        indice = buscar_id(peliculas, id_buscado)
        if indice == -1:
            print("El ID no fue encontrado, vuelva a intentar. ")   
            cinema_abm(peliculas)    
        else:
            print(f"Vamos a modificar la pelicula: {peliculas[indice]['titulo']} ")
            modificar = ingresar_modificar(llaves)
            if modificar == "titulo" or modificar == "sinopsis" or modificar == "idioma" or modificar == "pais de origen":
                peliculas[indice][modificar] = input(f"Ingrese el nuevo dato para {modificar}: ")
            elif modificar == "genero":
                genero = (ingresar(generos))
                peliculas[indice]["genero"].append(genero)
                while True:
                    otro = input("¿Desea ingresar otro género para la misma película? s/n")
                    if otro == "s":
                        genero = (ingresar(generos))
                        peliculas["genero"].append(genero)
                    elif otro == "n":
                        break
                    else:
                        ("opcion incorrecta, ingrese \"s\" o \"n\".")
                        continue
            elif modificar == "duracion":
                while True:
                    peliculas[indice]["duracion"] = input(f"Ingrese el nuevo dato para {modificar}: ")
                    if str.isnumeric(peliculas[indice]["duracion"]):
                        peliculas[indice]["duracion"] = int(peliculas[indice]["duracion"])
                        break
                    else:
                        print("Por favor, ingrese un número entero.")
                        continue
            elif modificar == "clasificacion":
                peliculas[indice]["clasificacion"] = ingresar(clasificaciones)
            elif modificar == "calificacion":
                peliculas[indice]["calificacion"] = float(input(f"Ingrese el nuevo dato para {modificar}: "))
            elif modificar == "disponible":
                while True:
                    disp = input("¿Está disponible? s/n: ").lower()
                    if disp == "s":
                        peliculas[indice]["disponible"] = True
                        break
                    elif disp == "n":
                        peliculas[indice]["disponible"] = False
                        break
                    else:
                        print("Por favor ingrese una opción válida: s/n")
                        continue
            modificacion = peliculas[indice][modificar]
        return modificacion
 
def modificar_pelicula_por_tit(peliculas, tit_buscado):
    indice = buscar_titulo(peliculas, tit_buscado)
    if indice == -1:
        print("El ID indicado no corresponde a las opciones, vuelva a intentar.")
        cinema_abm(peliculas)
    else:
        print(f"Vamos a a modificar la pelicula: {peliculas[indice]['titulo']} ")
        modificar = ingresar_modificar(llaves)
        if modificar == "titulo" or modificar == "sinopsis" or modificar == "idioma" or modificar == "pais de origen":
            peliculas[indice][modificar] = input(f"Ingrese el nuevo dato para {modificar}: ")
        elif modificar == "genero":
            imprimir_submenu("Modificación por Titulo")
            genero = (ingresar(generos))
            peliculas[indice]["genero"] = []
            peliculas[indice]["genero"].append(genero)
            while True:
                otro = input("¿Desea ingresar otro género para la misma película? s/n")
                if otro == "s":
                    genero = (ingresar(generos))
                    peliculas[indice]["genero"].append(genero)
                elif otro == "n":
                    break
                else:
                    ("opcion incorrecta, ingrese \"s\" o \"n\".")
                    continue
        elif modificar == "duracion":
            while True:
                peliculas[indice]["duracion"] = input(f"Ingrese el nuevo dato para {modificar}: ")
                if str.isnumeric(peliculas[indice]["duracion"]):
                    peliculas[indice]["duracion"] = int(peliculas[indice]["duracion"])
                    break
                else:
                    print("Por favor, ingrese un número entero.")
                    continue
        elif modificar == "clasificacion":
            peliculas[indice]["clasificacion"] = ingresar(clasificaciones)
        elif modificar == "calificacion":
            peliculas[indice]["calificacion"] = float(input(f"Ingrese el nuevo dato para {modificar}: "))
        elif modificar == "disponible":
            while True:
                disp = input("¿Está disponible? s/n: ").lower()
                if disp == "s":
                    peliculas[indice]["disponible"] = True
                    break
                elif disp == "n":
                    peliculas[indice]["disponible"] = False
                    break
                else:
                    print("Por favor ingrese una opción válida: s/n")
                    continue
            
        return peliculas

          
def es_verdadero():
        while True:
            respuesta = input("¿Está disponible? sí(s) / no(n): ").lower()
            if respuesta not in ("sn"):
                 print("Respuesta incorrecta, ingrese (s/n) por favor.")
                 continue
            else:
                 break
        if respuesta == "s":
            disponible = True
        else:
            disponible = False
        return disponible
        
def ingresar(datos):
    for i in datos.keys():
             print(i+"."+ datos[i])
    while True:
        clave = input("Ingrese el número de la opción deseada: ")
        if clave in datos:
                break
        else:
            print("Ingrese un número válido: ")
            continue
    return datos[clave]

def ingresar_modificar(datos):
    for i in datos.keys():
             print(i +"."+ datos[i])
    while True:
        clave = input("Ingrese el número de la opción que desea modificar: ")
        if clave in datos:
                break
        else:
            print("Ingrese un número válido: ")
            continue
    return datos[clave]

def mostrar_menu(menu):
    for i in menu.keys():
        print(i +". "+ menu[i])
    while True:    
        eleccion = input("Seleccione el número de la opción deseada: ")
        if eleccion not in menu.keys():
            print("El número es incorrecto. Intentelo de nuevo.")
            continue
        return eleccion   
    
#funcion de calificacion de peliculas
def calificacion(peliculas):
    imprimir_submenu("Calificación de 10 Peliculas al Azar")
    pelis = random.sample(peliculas, 10)
    print(f"\n\t\t\t Comencemos la calificación.\n ")
    for i in pelis:
        calificar = input(f"¿Desea calificar \"{i['titulo']}\"? s/n: ").lower()
        if calificar == "s":
            while True:
                numero = input("Califique con un numero del 1 al 10: ")
                if str.isnumeric(numero):
                    numero = float(numero)
                    if numero < 1 or numero > 10:
                        print("El numero debe ser entre 1 y 10")
                        continue
                    else:
                        break
                else:
                    print("Ingrese un numero entero .")
                    continue
                
            promedio = (numero + i["calificacion"])/2
            i["calificacion"] = round(promedio, 1)
        elif calificar == "n":
            continue
        else:
            print("Opción incorrecta, ingrese una letra válida: s/n")
            continue
        print(f"\"{i['titulo']}\" tiene \"{i['calificacion']}\" de calificación.")    
    return peliculas


def buscar_id(peliculas, id_buscado):
    for i in peliculas:
        if id_buscado == i["id"]:
            indice = peliculas.index(i)
            return indice    
    return-1

def seguro(indice):
        while True:
            seguro = input(f"¿Está seguro de que desea eliminar la pelicula: {peliculas[indice]['titulo']}? s/n ")
            if seguro == "s":
                pelis_eliminadas.append(peliculas[indice])
                peliculas.pop(indice)
                break
            elif seguro == "n":
                print("Eliminacion cancelada.")
                cinema_mas(peliculas)
                break
            else:
                print("Opción incorrecta. Ingrese \"s\" o \"n\"")
                continue
        return peliculas

#funciones para el menu de reporte y estadisticas
def obtener_puntaje(pelicula):
    return pelicula["calificacion"]

def mostrar_listado_peliculas(peliculas):
    imprimir_submenu("Listado de Peliculas")
    for pelicula in peliculas:
        print(f"Título: {(pelicula['titulo']).upper()}, Género: {pelicula['genero']}, Puntaje: {pelicula['calificacion']}")
        

def mostrar_peliculas_mayor_puntaje():
    imprimir_submenu("Peliculas de Mayor Puntaje")
    peliculas_ordenadas = sorted(peliculas, key=obtener_puntaje, reverse=True)
    pelis_mostradas = 0
    for pelicula in peliculas_ordenadas:
        print(f"Título: {(pelicula['titulo']).upper()}, Puntaje: {pelicula['calificacion']}")
        pelis_mostradas += 1
        if pelis_mostradas == 10:
            break

def mostrar_porcentaje_disponibles(peliculas):
    imprimir_submenu("Porcenjate de Peliculas Disponibles")
    total_peliculas = len(peliculas)
    peliculas_disponibles = 0
    for i in peliculas:
        if i['disponible'] == True:
            peliculas_disponibles += 1
    peliculas_no_disponibles = total_peliculas - peliculas_disponibles
    porcentaje_disponibles = peliculas_disponibles / total_peliculas * 100
    porcentaje_no_disponibles = peliculas_no_disponibles / total_peliculas * 100
    print("Porcentaje de películas disponibles:\n")
    print(f"Películas disponibles: {'*' * int(porcentaje_disponibles)} ({porcentaje_disponibles:.2f}%)")
    print(f"Películas no disponibles: {'*' * int(porcentaje_no_disponibles)} ({porcentaje_no_disponibles:.2f}%)\n")

def mostrar_eliminadas(pelis_eliminadas):
    imprimir_submenu("Peliculas Eliminadas")
    for i in pelis_eliminadas:
        print((f"* "+ i["titulo"]).upper())

def buscar_titulo(peliculas, tit_buscado):
    tit_encontrado = 0
    peli_encontrada = []
    for i in peliculas:
        if tit_buscado in i["titulo"]:
            print("Titulo: "+ i["titulo"] + ("\nNumero de ID: "+ str(i["id"])))
            peli_encontrada.append(i)
            tit_encontrado += 1
    if tit_encontrado >0:
            id_buscado = int(input("Seleccione el \"ID\" correspondiente o \"0\" para volver al menu: "))
            for i in peli_encontrada:
                if i["id"] == id_buscado:
                    posicion = buscar_id(peliculas, id_buscado)
                    return posicion
            else:
                return-1
    else:
        return-1
        
def cinema_abm(peliculas):
    eleccion = mostrar_menu(menu_abm)

    if eleccion == "1": #Alta de película
            imprimir_submenu("Alta de Pelicula")
            agregar_pelicula()
            escribir_archivo("peliculas.json", peliculas)
            print("La pelicula se agrego correctamente!\n")
            #print(peliculas)
            cinema_abm(peliculas)
    elif eleccion == "2": #Modificación de película
            imprimir_submenu("Modificación de Pelicula")
            eleccion = mostrar_menu(menu_modif_elim)
            if eleccion == "1": #Buscar por ID (Modificar)
                imprimir_submenu("Modificación por ID")
                id_buscado = int(input("Ingrese el ID buscado: "))
                modificacion = modificar_pelicula_por_id(peliculas, id_buscado)
                escribir_archivo("peliculas.json", peliculas)
                print("La pelicula se modifico correctamente!\n")                
                cinema_abm(peliculas)
            elif eleccion == "2": #Buscar por título (Modificar)
                imprimir_submenu("Modificación por Titulo")
                tit_buscado = input("Ingrese el título o parte del título buscado: ")
                modificacion = modificar_pelicula_por_tit(peliculas, tit_buscado)
                escribir_archivo("peliculas.json", peliculas)
                print("La pelicula se modifico correctamente! ")
                imprimir_submenu("ABM (Alta/Baja/Modificación)")
                cinema_abm(peliculas)
            else:
                cinema_abm(peliculas)
    elif eleccion == "3": #Baja de película
        imprimir_submenu("Baja de Pelicula")
        eleccion = mostrar_menu(menu_modif_elim)
        if eleccion == "1": #Buscar por ID (Baja)
            imprimir_submenu("Baja por ID")
            id_buscado = int(input("Ingrese el ID de la película que desea eliminar: "))
            indice = buscar_id(peliculas, id_buscado)
            if indice == -1:
                print("El ID seleccionado no es una de las opciones disponibles, vuelva a intentar. ")
                cinema_abm(peliculas)
            else:
                peli_eliminada = seguro(indice)
                escribir_archivo("peliculas.json", peliculas)
                escribir_archivo("pelis_eliminadas.json", pelis_eliminadas)
                for pelicula in peliculas:
                    print(f"Título: {(pelicula['titulo']).upper()},")
                cinema_abm(peliculas)
        elif eleccion == "2": #Buscar por título (Baja)
            imprimir_submenu("Baja por Titulo")
            tit_buscado = input("Ingrese el título o parte del título buscado: ")
            indice= buscar_titulo(peliculas, tit_buscado)
            if indice == -1:
                print("El título seleccionado no es una de las opciones disponibles, vuelva a intentar. ")
                cinema_abm(peliculas)
            else:
                peli_eliminada = seguro(indice)
                escribir_archivo("peliculas.json", peliculas)
                escribir_archivo("pelis_eliminadas.json", pelis_eliminadas)
                print("La Pelicula se elimino correctamente!")
                print("\t*****")
                cinema_abm(peliculas)
        else: 
            cinema_abm(peliculas)
    else:
        cinema_mas(peliculas)           

def cinema_calificacion(peliculas):
    eleccion = mostrar_menu(menu_calificacion)
    if eleccion=="1":
        peliculas = calificacion(peliculas)
        escribir_archivo("peliculas.json", peliculas)
        print("Hemos finalizado la calificación.")
        cinema_calificacion(peliculas)
        
    else:
        cinema_mas(peliculas)    

def cinema_reportes(peliculas):
    eleccion = mostrar_menu(menu_repor_estad)
    if eleccion == "1":
        mostrar_listado_peliculas(peliculas)
        cinema_reportes(peliculas)
    elif eleccion == "2":
        mostrar_peliculas_mayor_puntaje()
        cinema_reportes(peliculas)
    elif eleccion == "3":
        mostrar_porcentaje_disponibles(peliculas)
        cinema_reportes(peliculas)
    elif eleccion == "4":
        mostrar_eliminadas(pelis_eliminadas)
        cinema_reportes(peliculas)
    else:
        cinema_mas(peliculas)           

def cinema_mas(peliculas):
    imprimir_titulo("Bienvenido a \"CINEMA +\"")
    eleccion = mostrar_menu(menu_principal)
    if eleccion == "1":
        imprimir_titulo("ABM (Alta/Baja/Modificación)")
        cinema_abm(peliculas)
    elif eleccion == "2":
        imprimir_titulo("Calificacion de Tilulos")
        cinema_calificacion(peliculas)
    elif eleccion == "3":
        imprimir_titulo("Reportes y estadísticas")
        cinema_reportes(peliculas)
    else:
        imprimir_despedida(f"Gracias por vistar  \"CINEMA +\"  Hasta la proxima")

#funciones de titulo, subtitulo, depedida de codigo        
def imprimir_linea_caracter(caracter, longitud):
    print(caracter * longitud)

def imprimir_despedida(despedida):
    os.system("cls")
    imprimir_linea_caracter('*', 80)
    print(despedida.center(80))
    imprimir_linea_caracter('*', 80)

def imprimir_titulo(titulo):
    os.system("cls")
    imprimir_linea_caracter('*', 80)
    print(titulo.center(80))
    imprimir_linea_caracter('*', 80)

def imprimir_submenu(submenu):
    os.system("cls")
    imprimir_linea_caracter(':', 80)
    print(submenu.center(80))
    imprimir_linea_caracter(':', 80)
    
cinema_mas(peliculas)
# son 491 lineas de código menos 35 lineas vacías para separar funciones etc. serían 456 aproximadamente