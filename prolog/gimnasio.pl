:- discontiguous trabaja_musculo/2.
:- discontiguous utiliza_equipo/2.
:- discontiguous tiene_nivel/2.
:- discontiguous tipo_ejercicio/2.

% --- Base de Conocimiento ---

% Press banca
trabaja_musculo(press_banca, pecho).
trabaja_musculo(press_banca, triceps).
trabaja_musculo(press_banca, hombros).
utiliza_equipo(press_banca, barra).
utiliza_equipo(press_banca, banco).
tiene_nivel(press_banca, intermedio).
tipo_ejercicio(press_banca, compuesto).

% Press inclinado con mancuernas
trabaja_musculo(press_inclinado_con_mancuernas, pecho).
trabaja_musculo(press_inclinado_con_mancuernas, triceps).
trabaja_musculo(press_inclinado_con_mancuernas, hombros).
utiliza_equipo(press_inclinado_con_mancuernas, mancuernas).
utiliza_equipo(press_inclinado_con_mancuernas, banco).
tiene_nivel(press_inclinado_con_mancuernas, intermedio).
tipo_ejercicio(press_inclinado_con_mancuernas, compuesto).

% Aperturas con mancuernas
trabaja_musculo(aperturas_con_mancuernas, pecho).
utiliza_equipo(aperturas_con_mancuernas, mancuernas).
utiliza_equipo(aperturas_con_mancuernas, banco).
tiene_nivel(aperturas_con_mancuernas, principiante).
tipo_ejercicio(aperturas_con_mancuernas, aislamiento).

% Dominadas
trabaja_musculo(dominadas, espalda).
trabaja_musculo(dominadas, biceps).
utiliza_equipo(dominadas, barra_de_dominadas).
tiene_nivel(dominadas, intermedio).
tipo_ejercicio(dominadas, compuesto).

% Remo con barra
trabaja_musculo(remo_con_barra, espalda).
trabaja_musculo(remo_con_barra, biceps).
utiliza_equipo(remo_con_barra, barra).
tiene_nivel(remo_con_barra, intermedio).
tipo_ejercicio(remo_con_barra, compuesto).

% Jalón al pecho
trabaja_musculo(jalon_al_pecho, espalda).
trabaja_musculo(jalon_al_pecho, biceps).
utiliza_equipo(jalon_al_pecho, polea).
utiliza_equipo(jalon_al_pecho, maquina).
tiene_nivel(jalon_al_pecho, principiante).
tipo_ejercicio(jalon_al_pecho, compuesto).

% Press militar
trabaja_musculo(press_militar, hombros).
trabaja_musculo(press_militar, triceps).
utiliza_equipo(press_militar, barra).
tiene_nivel(press_militar, intermedio).
tipo_ejercicio(press_militar, compuesto).

% Elevaciones laterales
trabaja_musculo(elevaciones_laterales, hombros).
utiliza_equipo(elevaciones_laterales, mancuernas).
tiene_nivel(elevaciones_laterales, principiante).
tipo_ejercicio(elevaciones_laterales, aislamiento).

% Curl de bíceps
trabaja_musculo(curl_de_biceps, biceps).
utiliza_equipo(curl_de_biceps, mancuernas).
tiene_nivel(curl_de_biceps, principiante).
tipo_ejercicio(curl_de_biceps, aislamiento).

% Extensión de tríceps en polea
trabaja_musculo(extension_de_triceps_en_polea, triceps).
utiliza_equipo(extension_de_triceps_en_polea, polea).
tiene_nivel(extension_de_triceps_en_polea, principiante).
tipo_ejercicio(extension_de_triceps_en_polea, aislamiento).

% Sentadilla
trabaja_musculo(sentadilla, cuadriceps).
trabaja_musculo(sentadilla, gluteos).
trabaja_musculo(sentadilla, isquiotibiales).
utiliza_equipo(sentadilla, barra).
tiene_nivel(sentadilla, intermedio).
tipo_ejercicio(sentadilla, compuesto).

% Peso muerto
trabaja_musculo(peso_muerto, espalda).
trabaja_musculo(peso_muerto, gluteos).
trabaja_musculo(peso_muerto, isquiotibiales).
utiliza_equipo(peso_muerto, barra).
tiene_nivel(peso_muerto, avanzado).
tipo_ejercicio(peso_muerto, compuesto).

% Zancadas
trabaja_musculo(zancadas, cuadriceps).
trabaja_musculo(zancadas, gluteos).
trabaja_musculo(zancadas, isquiotibiales).
utiliza_equipo(zancadas, mancuernas).
tiene_nivel(zancadas, principiante).
tipo_ejercicio(zancadas, compuesto).

% Extensión de cuádriceps
trabaja_musculo(extension_de_cuadriceps, cuadriceps).
utiliza_equipo(extension_de_cuadriceps, maquina).
tiene_nivel(extension_de_cuadriceps, principiante).
tipo_ejercicio(extension_de_cuadriceps, aislamiento).

% Curl femoral
trabaja_musculo(curl_femoral, isquiotibiales).
utiliza_equipo(curl_femoral, maquina).
tiene_nivel(curl_femoral, principiante).
tipo_ejercicio(curl_femoral, aislamiento).


% --- Reglas de Inferencia ---

% Agrupación de músculos por zonas para consultas generales
grupo_muscular(piernas, cuadriceps).
grupo_muscular(piernas, gluteos).
grupo_muscular(piernas, isquiotibiales).
grupo_muscular(torso_superior, pecho).
grupo_muscular(torso_superior, espalda).
grupo_muscular(torso_superior, hombros).
grupo_muscular(brazos, biceps).
grupo_muscular(brazos, triceps).

% Regla: Un ejercicio trabaja un grupo muscular si afecta a algún músculo de ese grupo
trabaja_grupo(Ejercicio, Grupo) :-
    grupo_muscular(Grupo, Musculo),
    trabaja_musculo(Ejercicio, Musculo).