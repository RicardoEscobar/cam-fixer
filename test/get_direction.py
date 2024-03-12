import re

pattern = r'\((\-?\d+(\.\d+)?, \-?\d+(\.\d+)?)\)'
text = '[(97.1, -237.0), (87.1, -227.0), (87.1, -146.0), (97.1, -136.0), (160.1, -136.0), (170.1, -146.0), (170.1, -227.0), (160.1, -237.0), (128.6, -237.0), (112.9, -237.0)]'

matches = re.findall(pattern, text)
print(matches)


# pos1=get_WKT(pos1)
# pos2=get_WKT(pos2)
# pos3=get_WKT(pos3)
# #Coordenada de los ultimos 3 puntos.
# pos4=get_WKT(pos4)
# pos5=get_WKT(pos5)
# pos6=get_WKT(pos6)
# print(f"Las tres primeras coordenadas de puntos del bloque main son ",pos1, pos2, pos3)
# print(f"Las coordenadas del ultimo y anteultimo puntos son respectivamente: ",pos4,pos5,pos6)
# #Coordenadas primeros 3 puntos
# x1, y1 = pos1[0]
# x2, y2 = pos2[0]
# x3, y3 = pos3[0]
# #Coordenada del ultimo punto
# x4, y4 = pos4[0]
# x5, y5 = pos5[0]
# x6, y6 = pos6[0]
# print(f"Las coordenadas de los puntos 1 2 y 2 son respectivamente :",x1,y1, x2,y2, x3,y3)
# print(f"Las coordenadas de los ultimos 2 puntos son. :",x4,y4, x5,y5, x5,y6)          
# # Calculo vector1 y vector2
# vector1 = (x2 - x1, y2 - y1)
# vector2 = (x3 - x2, y3 - y2)
# # Calculo vector3.
# vector3 = (x1 - x4, y1 - y4)
# vector4 = (x4 - x5, y4 - y5)
# vector5 = (x5 - x6, y5 - y6)       
# print(f"Los resultados de los vectores 1 y 2 son :",vector1, vector2)
# print(f"Los resultados de los vectores 3, 4 y5 son :",vector3, vector4, vector5)   
# # Realizo la multiplicacion vectorial del vector1 X vector2
# produto_cruz1 = vector1[0] * vector2[1] - vector1[1] * vector2[0]
# produto_cruz2 = vector4[0] * vector3[1] - vector4[1] * vector3[0]
# produto_cruz3 = vector5[0] * vector4[1] - vector5[1] * vector4[0] 
# print(f"El resultado del producto cruz1 es", produto_cruz1)
# print(f"El resultado del producto cruz2 es", produto_cruz2)       
# print(f"El resultado del producto cruz3 es", produto_cruz3)                    
# if produto_cruz1 <= 0:
#     if produto_cruz2 <=0:
#         if produto_cruz3 <=0:
#             is_ccw = False
#             print(f"El sentido del recorrido de la pieza es Horario.")
# else:
#     is_ccw = True
#     print(f"El sentido del recorrido de la pieza es Anti-Horario.")