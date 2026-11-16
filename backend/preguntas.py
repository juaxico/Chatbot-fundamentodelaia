"""Las 20 preguntas de la primera entrega y resultados de referencia del .pl.

Los resultados esperados están expresados como conjuntos: el orden de salida
no es criterio de corrección y los duplicados no cuentan dos veces.
"""
PREGUNTAS = [
    {"id": 1, "categoria": "Directa", "pregunta": "¿Qué músculos trabaja el press banca?", "esperados": ["pecho", "triceps", "hombros"]},
    {"id": 2, "categoria": "Directa", "pregunta": "¿Qué equipamiento utiliza la sentadilla?", "esperados": ["barra"]},
    {"id": 3, "categoria": "Directa", "pregunta": "¿Cuál es la dificultad del peso muerto?", "esperados": ["avanzado"]},
    {"id": 4, "categoria": "Directa", "pregunta": "¿Qué equipamiento utiliza el curl de bíceps?", "esperados": ["mancuernas"]},
    {"id": 5, "categoria": "Directa", "pregunta": "¿Qué músculos trabaja el press militar?", "esperados": ["hombros", "triceps"]},
    {"id": 6, "categoria": "Directa", "pregunta": "¿Qué equipamiento utiliza el jalón al pecho?", "esperados": ["polea", "maquina"]},
    {"id": 7, "categoria": "Directa", "pregunta": "¿Cuál es la dificultad de las elevaciones laterales?", "esperados": ["principiante"]},
    {"id": 8, "categoria": "Inversa", "pregunta": "¿Qué ejercicios trabajan pecho?", "esperados": ["press_banca", "press_inclinado_con_mancuernas", "aperturas_con_mancuernas"]},
    {"id": 9, "categoria": "Inversa", "pregunta": "¿Qué ejercicios trabajan espalda?", "esperados": ["dominadas", "remo_con_barra", "jalon_al_pecho", "peso_muerto"]},
    {"id": 10, "categoria": "Inversa", "pregunta": "¿Qué ejercicios utilizan mancuernas?", "esperados": ["press_inclinado_con_mancuernas", "aperturas_con_mancuernas", "elevaciones_laterales", "curl_de_biceps", "zancadas"]},
    {"id": 11, "categoria": "Inversa", "pregunta": "¿Qué ejercicios son de nivel principiante?", "esperados": ["aperturas_con_mancuernas", "jalon_al_pecho", "elevaciones_laterales", "curl_de_biceps", "extension_de_triceps_en_polea", "zancadas", "extension_de_cuadriceps", "curl_femoral"]},
    {"id": 12, "categoria": "Inversa", "pregunta": "¿Qué ejercicios utilizan barra?", "esperados": ["press_banca", "remo_con_barra", "press_militar", "sentadilla", "peso_muerto"]},
    {"id": 13, "categoria": "Inversa", "pregunta": "¿Qué ejercicios utilizan máquina?", "esperados": ["jalon_al_pecho", "extension_de_cuadriceps", "curl_femoral"]},
    {"id": 14, "categoria": "Inversa", "pregunta": "¿Qué ejercicios trabajan bíceps?", "esperados": ["dominadas", "remo_con_barra", "jalon_al_pecho", "curl_de_biceps"]},
    {"id": 15, "categoria": "Combinada", "pregunta": "¿Qué ejercicios de pecho utilizan mancuernas?", "esperados": ["press_inclinado_con_mancuernas", "aperturas_con_mancuernas"]},
    {"id": 16, "categoria": "Combinada", "pregunta": "¿Qué ejercicios de piernas utilizan barra?", "esperados": ["sentadilla", "peso_muerto"]},
    {"id": 17, "categoria": "Combinada", "pregunta": "¿Qué ejercicios principiantes trabajan bíceps?", "esperados": ["jalon_al_pecho", "curl_de_biceps"]},
    {"id": 18, "categoria": "Combinada", "pregunta": "¿Qué ejercicios principiantes utilizan mancuernas?", "esperados": ["aperturas_con_mancuernas", "elevaciones_laterales", "curl_de_biceps", "zancadas"]},
    {"id": 19, "categoria": "Combinada", "pregunta": "¿Qué ejercicios de espalda utilizan barra?", "esperados": ["remo_con_barra", "peso_muerto"]},
    {"id": 20, "categoria": "Combinada", "pregunta": "¿Qué ejercicios de nivel principiante utilizan máquina?", "esperados": ["jalon_al_pecho", "extension_de_cuadriceps", "curl_femoral"]},
]
