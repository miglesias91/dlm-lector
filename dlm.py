import getopt, sys
import datetime

from medios.diarios.clarin import Clarin
from medios.diarios.lanacion import LaNacion
from medios.diarios.eldestape import ElDestape
from medios.diarios.paginadoce import PaginaDoce
from medios.diarios.infobae import Infobae
from medios.diarios.telam import Telam
from medios.diarios.perfil import Perfil
from medios.diarios.ambito import Ambito
from medios.diarios.tn import TN
# from medios.diarios.popular import Popular
from medios.diarios.diariodeleuco import DiarioDeLeuco
from medios.diarios.casarosada import CasaRosada

# from bd.kiosco import Kiosco
from bd.kioscomongo import Kiosco

def leer_medio(medio):

    try:
        medio.leer()
    except:
        print('error leyendo ' + medio.etiqueta + ': ' + str(sys.exc_info()[0]))
        return False

    try:
        kiosco = Kiosco()
        kiosco.actualizar_diario(medio)
    except:
        print('error actualizando noticias de ' + medio.etiqueta + ': ' + str(sys.exc_info()[0]))
        return False

    return True

def leer_medios(parametros):
    medios_a_leer = set(parametros['medios'])

    # medios = [Clarin(), LaNacion(), ElDestape(), Infobae(), Telam(), Perfil(), Ambito(), TN(), CasaRosada(), Popular(), PaginaDoce(), DiarioDeLeuco()]
    medios = [Clarin(), LaNacion(), ElDestape(), Infobae(), Perfil(), Ambito(), TN(), CasaRosada(), PaginaDoce(), DiarioDeLeuco()]

    print('leyendo medios:')
    for medio in medios:
        if medio.etiqueta in medios_a_leer or len(medios_a_leer) == 0:
            leer_medio(medio)

def usage(parametros):
    print("dlm-lector (dicenlosmedios scrapper) v1.0")
    print("ACCIONES")
    print("--leer [MEDIO_1] [MEDIO_2] ... [MEDIO_N] - actualiza las noticias de todos los diarios, a menos que se especifiquen los MEDIOS en particular")
    # print("--leer-historico - lee historico de 'casarosada': discursos desde la fecha hasta 2003")
    print("PARAMETROS OPCIONALES")
    print("--secciones s1-s2-...-sn - lee noticias de las secciones s1, s2, ..., sn: SECCIONES DISPONIBLES: 'politica', 'economia', 'sociedad', 'internacional', 'cultura', 'espectaculos', 'deportes'")
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

    parametros = {'medios':args, 'fecha':datetime.datetime.now().date(), 'twittear':False, 'solo_titulos':False, 'secciones':''}
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

        elif o == "--secciones":
            parametros['secciones'] = a.split('-')

        elif o == "--solo-titulos":
            parametros['solo_titulos'] = True
        else:
            assert False, "opción desconocida"
    
    # ejecuto accion con sus parametros
    accion(parametros)

if __name__ == "__main__":
    main()