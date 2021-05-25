#  esta fucion recibe una lista con las comunas = [nombre1, nombre2, .... ]
#  y una lista con las distribuciones para v0,v1,.., v12 = [dist1, dist2,...]

from random import expovariate


def diccionario_distribuciones(lista_comunas):
    diccionario_dist = {}

    for nombre_comuna in lista_comunas:
        diccionario_dist[nombre_comuna] = {}

        for i in (range(24)):
            vel = "v" + str(i)
            diccionario_dist[nombre_comuna][vel] = expovariate(i + 1)

    return diccionario_dist


hola = diccionario_distribuciones(["Recoleta", "Ñuñoa", "Macul"])

print(hola)
