% Motor de consultas para gimnasio.pl.
% El codigo Python interpreta el español y envia únicamente atomos validados.
% Este archivo usa los hechos y las reglas de la primera entrega.

:- use_module(library(http/json)).
:- use_module(library(lists)).
:- consult('gimnasio.pl').

% Atributos de un ejercicio.
atributo(Ejercicio, musculo, Valor) :- trabaja_musculo(Ejercicio, Valor).
atributo(Ejercicio, equipo, Valor) :- utiliza_equipo(Ejercicio, Valor).
atributo(Ejercicio, nivel, Valor) :- tiene_nivel(Ejercicio, Valor).
atributo(Ejercicio, tipo, Valor) :- tipo_ejercicio(Ejercicio, Valor).

% Condiciones sobre ejercicios, incluyendo la regla trabaja_grupo/2.
cumple(Ejercicio, musculo, Valor) :- trabaja_musculo(Ejercicio, Valor).
cumple(Ejercicio, equipo, Valor) :- utiliza_equipo(Ejercicio, Valor).
cumple(Ejercicio, nivel, Valor) :- tiene_nivel(Ejercicio, Valor).
cumple(Ejercicio, tipo, Valor) :- tipo_ejercicio(Ejercicio, Valor).
cumple(Ejercicio, grupo, Valor) :- trabaja_grupo(Ejercicio, Valor).
cumple(_Ejercicio, ninguno, ninguno).

% Elimina los resultados repetidos causados por reglas de inferencia.
consulta(atributo, Ejercicio, Campo, _Valor, _FiltroCampo, _FiltroValor, Resultado) :-
    findall(Dato, atributo(Ejercicio, Campo, Dato), Datos),
    sort(Datos, Resultado).
consulta(buscar, _Ejercicio, Campo, Valor, FiltroCampo, FiltroValor, Resultado) :-
    findall(Ejercicio,
            (cumple(Ejercicio, Campo, Valor),
             cumple(Ejercicio, FiltroCampo, FiltroValor)),
            Datos),
    sort(Datos, Resultado).

% Entrada por argumentos, salida JSON en stdout.
% swipl -q -s motor_chatbot.pl -g main -- atributo press_banca musculo ninguno ninguno ninguno
main :-
    current_prolog_flag(argv, Argumentos),
    ( Argumentos = [Accion, Ejercicio, Campo, Valor, FiltroCampo, FiltroValor],
      catch(consulta(Accion, Ejercicio, Campo, Valor, FiltroCampo, FiltroValor, Resultado), _, fail)
    -> json_write_dict(current_output, _{ok:true, resultados:Resultado})
    ;  json_write_dict(current_output, _{ok:false, error:'Consulta no valida'})
    ),
    nl,
    halt.
