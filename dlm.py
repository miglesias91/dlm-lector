import getopt, sys
import time
import json
import datetime
from collections import defaultdict
import yaml
import pathlib

#import numpy as np

# from medios.diarios.diarios import Clarin, ElDestape, Infobae, LaNacion, PaginaDoce, CasaRosada
from medios.diarios.clarin import Clarin
from medios.diarios.lanacion import LaNacion
from medios.diarios.eldestape import ElDestape
from medios.diarios.paginadoce import PaginaDoce
from medios.diarios.infobae import Infobae
from medios.diarios.telam import Telam
from medios.diarios.perfil import Perfil
from medios.diarios.ambito import Ambito
from medios.diarios.tn import TN
from medios.diarios.popular import Popular
from medios.diarios.casarosada import CasaRosada

# from bd.kiosco import Kiosco
from bd.kioscomongo import Kiosco

def leer_medio(medio):
    medio.leer()

    kiosco = Kiosco()
    kiosco.actualizar_diario(medio)

def leer_medios(parametros):
    medios_a_leer = set(parametros['medios'])

    medios = [Clarin(), LaNacion(), ElDestape(), PaginaDoce(), Infobae(), Telam(), Perfil(), Ambito(), TN(), CasaRosada(), Popular()]
    
    for medio in medios:
        if medio.etiqueta in medios_a_leer or len(medios_a_leer) == 0:
           leer_medio(medio)

def usage(parametros):
    print("dlm-lector (dicenlosmedios scrapper) v1.0")
    print("ACCIONES")
    print("--leer [MEDIO_1] [MEDIO_2] ... [MEDIO_N] - actualiza las noticias de todos los diarios, a menos que se especifiquen los MEDIOS en particular")
    print("--leer-historico - lee historico de 'casarosada': discursos desde la fecha hasta 2003")
    print("PARAMETROS OPCIONALES")
    print("--categorias c1-c2-...-cn - lee noticias de las categorias c1, c2, ..., cn: CATEGORIAS DISPONIBLES: 'politica', 'economia', 'sociedad', 'internacional', 'cultura', 'espectaculos', 'deportes'")
    print("--fecha AAAAMMDD - lee noticias con fecha AAAMMDD")
    print("--fecha AAAAMMDD-AAAAMMDD - lee noticias dentro del rango de fechas AAAAMMDD->AAAAMMDD")
    print("--solo-titulos - lee solo títulos")

def main():
    accion = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "leer", "leer-historico", "solo-titulos"])
    except getopt.GetoptError as err:
        print(err)
        usage(None)
        sys.exit(2)

    parametros = {'medios':args, 'fecha':datetime.datetime.now().date(), 'twittear':False, 'solo_titulos':False, 'categorias':''}
    for o, a in opts:
        if o == "--help" or o == "-h":
            accion=usage
        elif o == "--leer":
            accion=leer_medios
        elif o == "--fecha":
            fecha = None
            if len(a.split('-')) == 2:
                desde = datetime.datetime.strptime(a.split('-')[0], "%Y%m%d")
                desde.replace(hour=0, minute=0, second=0)
                hasta = datetime.datetime.strptime(a.split('-')[1], "%Y%m%d")
                hasta.replace(hour=23, minute=59, second=59)
                fecha = {'desde':desde, 'hasta':hasta}
            else:
                fecha = datetime.datetime.strptime(a, "%Y%m%d")

            parametros['fecha'] = fecha

        elif o == "--categorias":
            parametros['categorias'] = a.split('-')

        elif o == "--solo-titulos":
            parametros['solo_titulos'] = True
        else:
            assert False, "opción desconocida"
    
    # ejecuto accion con sus parametros
    accion(parametros)

if __name__ == "__main__":
    main()