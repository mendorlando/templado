from flask import Flask, jsonify, render_template
import math
import random

app = Flask(__name__)

def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    return total

def simulated_annealing(ruta, coord):
    T = 20
    T_min = 0
    V_enfriamiento = 100
    while T > T_min:
        dist_actual = evalua_ruta(ruta, coord)
        for _ in range(V_enfriamiento):
            i, j = random.sample(range(len(ruta)), 2)
            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
            dist_nueva = evalua_ruta(ruta_tmp, coord)
            delta = dist_actual - dist_nueva
            if dist_nueva < dist_actual or random.random() < math.exp(-delta / T):
                ruta = ruta_tmp[:]
                dist_actual = dist_nueva
        T -= 0.005
    return ruta

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/optimizar")
def optimizar_ruta():
    coord = {
        'Jiloyork': (19.916012, -99.580580),
        'Toluca': (19.289165, -99.655697),
        'Atlacomulco': (19.799520, -99.873844),
        'Guadalajara': (20.677754, -103.346253),
        'Monterrey': (25.691611, -100.321838),
        'QuintanaRoo': (21.163111, -86.802315),
        'Michohacan': (19.701400, -101.208296),
        'Aguascalientes': (21.876410, -102.264386),
        'CDMX': (19.432713, -99.133183),
        'QRO': (20.597194, -100.386670)
    }

    ruta = list(coord.keys())
    random.shuffle(ruta)

    distancia_inicial = evalua_ruta(ruta, coord)
    ruta_optimizada = simulated_annealing(ruta, coord)
    distancia_optimizada = evalua_ruta(ruta_optimizada, coord)

    return jsonify({
        "ruta_inicial": ruta,
        "distancia_inicial": distancia_inicial,
        "ruta_optimizada": ruta_optimizada,
        "distancia_optimizada": distancia_optimizada
    })
