"""This module contains the function to get the text that defines a block from a cam file."""
import numpy as np
import ast
import cmath
import math
from shapely.geometry import Polygon
from shapely.geometry import Point
# from camfixer.get_direction import get_direction
# from camfixer.es_pieza import es_pieza
from camfixer.get_WKT import get_WKT
from camfixer.get_max_min import get_max_min
from math import atan2, degrees
# from camfixer.is_arc_in import is_arc_in


def get_orientacion(ncoordinates, centro_x, centro_y) -> str:
    producto_cruzado = sum((x2 - centro_x) * (y1 - centro_y) - (x1 - centro_x) * (y2 - centro_y) for (x1, y1), (x2, y2) in zip(ncoordinates, ncoordinates[1:] + [ncoordinates[0]]))
    # print(f"El resultado del producto cruz total de todos los vectores es ",producto_cruzado)

    # Determina la orientación
    orientacion = "antihoraria" if producto_cruzado < 0 else "horaria" if producto_cruzado > 0 else "indeterminada"

    return orientacion

def _block_generator(cam_file):
    """This generator function yields the text that defines blocks from a cam file.
    The initial line is the initial.
    The start of a block is defined by the line "M04" and the previous two lines, ignoring empty white lines.
    The arc of the block is defined by the next two lines after the start of the block.
    Anything between the arc and end of a block is considered the block.
    The end of a block is defined by the line "M03" and the next line "G40", ignoring empty white lines.

    example file:
    BOF
    G90
    G00X+264.2Y-23.4
    G41
    M04
    G01X+258.5Y-29.0
    G03X+269.8Y-29.0I+264.2J-23.4
    G01X+276.0Y-22.8
    G02X+346.7Y-22.8I+311.4J-58.2
    G01X+371.5Y-47.6
    G02X+392.2Y-81.4I+311.4J-107.7
    G01X+502.9Y-422.0
    G02X+490.7Y-472.8I+455.3J-437.5
    G01X+428.8Y-534.7
    G03X+417.2Y-553.0I+464.2J-570.0
    G01X+391.3Y-624.5
    G02X+226.4Y-595.6I+311.4J-595.6
    G01X+226.4Y-107.7
    G02X+251.3Y-47.6I+311.4J-107.7
    G01X+263.6Y-35.2
    G01X+269.8Y-29.0
    M03
    G40
    M02
    EOF

    Output:
    {
        'initial': ['G00X+264.2Y-23.4'],
        'start': ['G41', 'M04'],
        'arc': ['G01X+258.5Y-29.0', 'G03X+269.8Y-29.0I+264.2J-23.4'],
        'main': ['G01X+269.8Y-29.0', 'G01X+263.6Y-35.2', 'G02X+251.3Y-47.6I+311.4J-107.7', 'G01X+226.4Y-107.7', 'G02X+226.4Y-595.6I+311.4J-595.6', 'G01X+391.3Y-624.5', 'G03X+417.2Y-553.0I+464.2J-570.0', 'G01X+428.8Y-534.7', 'G02X+490.7Y-472.8I+455.3J-437.5', 'G01X+502.9Y-422.0', 'G02X+392.2Y-81.4I+311.4J-107.7', 'G01X+371.5Y-47.6', 'G02X+346.7Y-22.8I+311.4J-58.2', 'G01X+276.0Y-22.8'],
        'end': ['M03', 'G40'],
        'text': 'G00X+264.2Y-23.4\nG41\nM04\nG01X+258.5Y-29.0\nG03X+269.8Y-29.0I+264.2J-23.4\nG01X+269.8Y-29.0\nG01X+263.6Y-35.2\nG02X+251.3Y-47.6I+311.4J-107.7\nG01X+226.4Y-107.7\nG02X+226.4Y-595.6I+311.4J-595.6\nG01X+391.3Y-624.5\nG03X+417.2Y-553.0I+464.2J-570.0\nG01X+428.8Y-534.7\nG02X+490.7Y-472.8I+455.3J-437.5\nG01X+502.9Y-422.0\nG02X+392.2Y-81.4I+311.4J-107.7\nG01X+371.5Y-47.6\nG02X+346.7Y-22.8I+311.4J-58.2\nG01X+276.0Y-22.8\nM03\nG40'
    }

    Args:
        cam_file (str): The path to the cam file.

    Yields:
        dict: The dict that defines a block from a cam file.
    """
    centro = ()
    nuevo_ini = []
    ini_coordinates = ()
    coordinates = []
    ncoordinates = []
    block_initial = []
    block_start = []
    block_arc = []
    block_main = []
    block_end = []
    block_main_start = 0
    num_block = 0
    is_piece = False
    is_arc_in = None
    is_circle = None
    contained_in = None

    with open(cam_file, "r", encoding="utf-8") as file:
        cam_text = file.read()

    # Gets the lines from the cam file.
    lines = cam_text.split("\n")

    # Removes empty lines.
    lines = list(filter(None, lines))

    # Iterates over the lines.
    print("Empezando a generar los bloques...")

    for i, line in enumerate(lines):
        if line == "M04":
            # Gets the initial coordinate of the arc.
            block_initial = [lines[i - 2]]
            # Gets the previous two lines.
            block_start = lines[i - 1 : i + 1]
            # Gets the next two lines.
            # Esto podria no ser asi, dependiendo de como se genere el archivo.cam en el programa PEAK. Podria tener una sola linea de arco en vez de dos.
            block_arc = lines[i + 1 : i + 3]
            block_arc1 = [lines[i+1]]
            block_arc2 = [lines[i+2]]
            block_main_start = i + 3
        if line == "M03" and lines[i + 1] == "G40":
            # Gets the next two lines.
            block_end = lines[i : i + 2]
            # Suma +1 a la variable num_block
            num_block += 1
            # Joins the lines and yields the block.
            text = "\n".join(block_initial + block_start + block_arc + block_main + block_end)

            # Imprime en pantalla el numero de bloque
            # print(f"Bloque ", [num_block], " detectado correctamente.")
            # print("________________________________________________________________________________________________________")
            # print("________________________________________________________________________________________________________")
            # print("________________________________________________________________________________________________________")
            # print(f"La coordenada inicial es  {block_initial}\n El start{block_start}\n El arco es {block_arc}\nEl bloque main es {block_main}\n Y el final {block_end}")
            #Imprime en pantalla el bloque encontrado.
            # print(text)

            #Imprimo las coordenadas WKT
            coordinates = Polygon(get_WKT(block_main))
            # print(f"Imprimiendo las coordenadas WKT del bloque ",num_block, ":", coordinates)

            #Guarda el punto donde pincha el arco.
            ini_coordinates = Point(get_WKT(block_initial))

# ########### Inicio analisis de sentido de la pieza #############
            #Guarda el recorrido de la pieza.
            ncoordinates = get_WKT(block_main)
            # print(f"Las coordenadas son: ",ncoordinates)

            # Centro de la figura
            centro_x = sum(x for x, y in ncoordinates) / len(ncoordinates)
            centro_y = sum(y for x, y in ncoordinates) / len(ncoordinates)

            #Lo agrego al diccionario
            centro = (centro_x, centro_y)

            # print("Promedio de coordenadas X:", centro_x)
            # print("Promedio de coordenadas Y:", centro_y)

            # Determina la orientación
            orientacion = get_orientacion(ncoordinates, centro_x, centro_y)

            # Imprime la orientación
            # print("Orientacion:", orientacion
########### Termina analisis de orientacion de la pieza ############


########### Inicio analisis de posicion de arco #############
            #Guardo TRUE or FALSE dependiendo si la coordenada inicial esta contenida dentro del recorrido main. Y arregla posibles falsos negativos para circunferencias.
            # print(f"Las coordenadas son",coordinates, "y las coordenadas iniciales son",ini_coordinates)
            if coordinates.contains(ini_coordinates):
                is_arc_in = True
                # print(f"El arco esta contenido dentro del recorrido")
            else:
                is_arc_in = False
                # print(f"El arco esta por fuera del recorrido",is_arc_in)

            if len(block_main)==4:
                for i in block_main:
                    # print(i)
                    if line.startswith("G01"):
                        # is_arc_in = False
                        # print(f"El bloque ",num_block, "tiene 4 lineas, pero no es un agujero")
                        continue
                    else:
                        is_arc_in = True
                        is_circle = True
                        # print(f"El bloque ",num_block, "tiene exactamente 4 lineas y es CIRCUNFERENCIA")
            if is_arc_in:
                is_arc_in = True
                # print(f"El arco del bloque",num_block," esta contenido dentro.")
                # print(f"El valor del arco es TRUE=DENTRO, FALSE=FUERA",is_arc_in)

########## True = DENTRO del recorrido, False = FUERA del recorrido ##############
########## Termina analisis de posicion de arco ############
                
##################Analisis del arco para luego modificar###############
            block_arc1 = Point(get_WKT(block_arc1))
            block_arc2 = Point(get_WKT(block_arc2))
            # print(f"imprimo arco1 y 2 {block_arc1} y {block_arc2}")
#######################                       ############################   
            #Esto guarda todas las variables del bloque en un diccionario.
            result = {
                "initial":block_initial,
                "start": block_start,
                "arc": block_arc,
                "main": block_main,
                "end": block_end,
                "text": text,
                "polygon": coordinates,
                "ini_coordinates": ini_coordinates,
                "num_block": num_block,
                "orientacion": orientacion,
                "is_arc_in": is_arc_in,
                "is_piece": is_piece,
                "is_circle": is_circle,
                "contained_in": contained_in,
                "arco1": block_arc1,
                "arco2": block_arc2,
                "nuevo_ini" : nuevo_ini,
                "centro" : centro,
            }
            
            #Imprimo en pantalla todo el diccionario
            # print(f"Imprimiendo la totalidad del diccionario del bloque", num_block)
            # print(result)

            yield result 

            # Resets the block variables.
            is_arc_in = None
            ini_coordinates = ()
            ncoordinates = []
            coordinates = []
            block_initial = []
            block_start = []
            block_arc = []
            block_main = []
            block_end = []
            block_main_start = 0
        elif block_main_start > 0 and i >= block_main_start:
            block_main.append(line) 
    print("Se generaron todos los bloques correctamente.")

def block_generator(cam_file):
    """Esta funcion modifica los bloques dependiendo de diferentes aspectos.
    Args:
        cam_file (str): The path to the cam file.
    Returns:
        List[Dict]: A list of dictionaries with the data of the blocks.
    """
######################Funcion para saber si contiene al otro bloque o no #########################
    def check_containment(poly1: Polygon, poly2: Polygon) -> bool:
        return poly1.contains(poly2)
                                        # 'or poly1.contains(poly2.centroid)
    

#################### Funcion para corregir el arco ##############################   
    def corregir_arco(ini, distancia, direccion):
        x, y = ini.x, ini.y
        x_nuevo = x + distancia * cmath.cos(direccion)
        y_nuevo = y + distancia * cmath.sin(direccion)
        nuevo_ini = Point(x_nuevo.real, y_nuevo.real)
        result = f"G00X{nuevo_ini.x:+.1f}Y{nuevo_ini.y:+.1f}"
        return result
    
##################Termina funcion########################################
    block_gen = _block_generator(cam_file)
    blocks = list(block_gen)
########################### Analisis de que bloque contiene a que otro bloque ##########################   
    for idx, block in enumerate(blocks):
        is_piece = False
        for other_block in blocks[:idx] + blocks[idx+1:]:

            # print(f"Este es el bloque 'other_block' = {other_block['num_block']}")
            # print(f" Y este es el 'bloque' {block['num_block']}")

            if check_containment(block["polygon"], other_block["polygon"]):
                # print(f"El bloque {block['num_block']} contiene al bloque {other_block['num_block']}")
                other_block['contained_in'] = block["num_block"]
                other_block['is_piece'] = True
                # print(f"Entonces el bloque {other_block['num_block']} esta contenido dentro de {block['num_block']}")
##################################### Termina analisis ####################################################
                
#########Impresion en pantalla para verificacion visual############

############################# Modificacion del arco y de sangria segun el sentido de giro ###################################
    for block in blocks:
        #Transformo los datos para tenes los puntos donde pincha y hacia donde se mueve.
        arco2 = block['arco2']
        arco1 = block['arco1']
        ini = block['ini_coordinates']
        x1,y1  = ini.bounds[:2]
        x2,y2  = arco1.bounds[:2]
        x3,y3  = arco2.bounds[:2]

        #Me pregunto si el recorrido es un recorrido interior.
        if block['is_piece']:
            # print(f"El bloque {block['num_block']} es una pieza y esta contenido dentro del bloque {block['contained_in']}\n")

            #Me pregnuto si el recorrido tiene el arco por fuera de su propio recorrido.
            if block['is_arc_in']==False:
                print(f"\n El bloque {block['num_block']} es un agujero y tiene el arco por fuera, se tiene que modificar. \n")
                print(f"\n Las coordenadas del punto inicial son {x1, y1}, se mueve hacia {x2, y2} y luego hasta {x3, y3}. Siendo estas ultimas el primer punto del recorrido principal.")

                #Calculo la distancia y la direccion entre el punto inicial y el final.
                direccion = math.atan2 (y3 - y1, x3 - x1)
                distancia = arco2.distance(ini)
                # print(f"\nLa distancia entre el arco2 y el ini es {distancia}")
                # print(f"\n Y la direccion entre los dos puntos es {direccion} radianes respecto a al horizonatal. en sentido antihorario")
                block['initial'] = [corregir_arco(arco2, distancia, direccion)]
                print(f"\nLa nueva coordenada inicial del bloque {block['num_block']} es {block['nuevo_ini']}")

            #Me pregnuto si se recorre en sentido horario.
            if block['orientacion']=="horaria":
                print(f"\nEl bloque {block['num_block']} se esta recorriendo en sentido horario. Y al ser un agujero debe tener sangria derecha. G42")
                block['start'][0] = "G42"

            #El recorrido va en contra de las agujas del reloj si llego a este punto.
            else:
                print(f"\nEl bloque {block['num_block']} se esta recorriendo en sentido antihorario. Y al ser un agujero debe tener sangria derecha. G41")
                block['start'][0] = "G41"

        #El recorrido es un recorrido exterior si llego a este punto.
        else:
            if block['is_arc_in']:
                print(f"El bloque {block['num_block']} es una pieza exterior y el arco esta por dentro, se tiene que modificar \n")
                
                #Calculo la distancia y la direccion entre el punto inicial y el final.
                direccion = math.atan2 (y3 - y1, x3 - x1)
                distancia = arco2.distance(ini)

                block['nuevo_ini'] = corregir_arco(arco2, distancia, direccion)
                print(f"\nLa nueva coordenada inicial del bloque {block['num_block']} es {block['nuevo_ini']}")
#######################################################################################################################################
        print(f"las coordenadas del centro de la figura del bloque {block['num_block']} es {block['centro']}")


    #############################   Modificacion del arco para agujeros interiores     ##################################################
    # def resta(poly1: Point, poly2: Point) -> float:
    #     return poly1.contains(poly2) 
    # for block in blocks:
    #     if block['is_piece'] and block['is_arc_in']==False:
    #         if resta(block["arco2"], block["ini_coordinates"]):

                # print(f"Las coordenadas del punto inicial son {block['ini_coordinates']}")
                # print(f"Las lineas de codigo del arco son {block['arco1']} y {block['arco2']}")

            
            # Imprimir o usar el resultado
            # print(f"La resta es {}")

            # print(f"El bloque {block['num_block']} ya se encuentra con el arco bien posicionado")

        # Remake 'text' key.
        # Joins the lines and yields the block.
        block["text"] = "\n".join(block["initial"] + block["start"] + block["arc"] + block["main"] + block["end"])
                
        # Imprime en pantalla todos los bloques generados.
        # print("bloque generado: ", block)
        # block["contained_in"] = is_piece(block, blocks)

                
        yield block
        

if __name__ == "__main__":
    cam_file = "archivo.cam"
    for block in block_generator(cam_file):
        print(block)
        print("-" * 80)
