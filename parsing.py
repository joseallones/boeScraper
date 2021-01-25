#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Parsing(object):

    @classmethod
    def extraeRamas(cls, organismo, title):

        ramas = []

        organismo = organismo.lower()
        title = title.lower()

        title = title.replace("boletín oficial ", "").replace("diario oficial ","")

        palabrasRelevantesTIC = [ 'informati','informáti', 'tecnolox', 'tecnolog', ' tic ', 'programador', 'cixtec', 'programador', 'software',
                                 'inteligencia artificial', 'intelixencia artificial', 'computaci', 'técnico/a medio/a sistemas', 'computad', 'robótic',
                                 'técnico de sistemas', 'xestor de sistemas', 'gestor de sistemas', 'xestión de sistemas', 'gestión de sistemas',
                                  'especialidad programación', 'administración de sistemas', 'automática', 'sistemas de información', 'sistema de información',
                                  'base de datos', 'bases de datos', 'recuperación de información', 'telecomunicaci', 'telemática',
                                 'deseño gráfic', 'diseño gráfic', 'deseñador/a gráfic', 'diseñador/a gráfic', 'deseñador gráfic',
                                 'xestor de contidos', 'gestor de contenidos', 'xestor/a de contidos', 'teleformación', 'teledocencia', 'learning']
        palabrasRelevantesInvestigacion = ['innovaci', 'investiga', 'i + d', 'i+d', 'centro tecnol', 'subescala I+D', 'proyectos europe', 'proxectos europe']

        if (any(palabraRelevante in organismo for palabraRelevante in palabrasRelevantesTIC) or any(
                palabraRelevante in title for palabraRelevante in palabrasRelevantesTIC)):
            ramas.append('TIC')

        if (any(palabraRelevante in organismo for palabraRelevante in palabrasRelevantesInvestigacion) or any(
                palabraRelevante in title for palabraRelevante in palabrasRelevantesInvestigacion)):
            ramas.append('Investigación')

        return ramas



    @classmethod
    def esPlazaPersonal(cls, text):

        text = text.lower()

        palabrasRelevantesParteInicial = ["convocatoria",
                                          "provisión",
                                          "cobertura",
                                          "oposición",
                                          "contratación"]

        palabrasRelevantesParteFinal = [ " emprego",
                                         " empleo",
                                         " persona",
                                         " persoal",
                                         " selección",
                                         " selectivo",
                                         " posto",
                                         " praza",
                                         " trabajador"]

        if (any(palabraRelevante in text for palabraRelevante in palabrasRelevantesParteInicial) and
             any(palabraRelevante in text for palabraRelevante in palabrasRelevantesParteFinal)):
            return True

        return False

    @classmethod
    def esPlazaPersonalBOE(cls, text):
        text = text.lower()

        frasesExcluyentes = ["destinos definitivo",
                             "ampliación del plazo"
                             "nota aclaratoria",
                             "deja sin efecto",
                             "se modifica la resoluci",
                             "se declara inhábil",
                             "corrección de errores",
                             "corrigen errores",
                             "pública la actualización definitiva de méritos",
                             "pública la actualización provisional de méritos",
                             "públicas las listas definitivas",
                             "públicas las listas provisio",
                             "se resuelve la convocatoria",
                             "prórroga vixencia das listas",
                             "recurso contencios",
                             "relación de plazas desiertas"]

        if (any(fraseExc in text for fraseExc in frasesExcluyentes)):
            return False

        return True

    @classmethod
    def extraeDetallePrazas(cls, web, simplificado, title):
        detalles = buscaDetallesPlazas(web, simplificado, title)
        return normalizaTextoPrazas(detalles)


def normalizaTextoPrazas(textoprazas):

    if textoprazas:
        textoprazas = textoprazas.strip()
        if textoprazas.startswith(";") or textoprazas.startswith("_") or textoprazas.startswith("–"):
            textoprazas = textoprazas[1:]
        if textoprazas.endswith(";") or textoprazas.endswith(","):
            textoprazas = textoprazas[:-1]
        textoprazas = textoprazas.strip()
    return textoprazas


def buscaDetallesPlazas(web, simplificado, title):

    textoprazas =""
    contadorPlazas = 0

    for p in web.find_all("p"):

        text = p.getText()

        if(title and text==title):
            continue

        if text.lower() == 'nº prazas':
            continue

        if ( " plaza" in text or
            " puesto de" in text or
            " puestos de" in text or
            "selección d" in text ):

            contadorPlazas = contadorPlazas + 1
            text = "..." + normalizaTextoPrazas(text)

            textoprazas = textoprazas + "<span class=\"brmedium\">" + text + "</span>"

            if (simplificado and (contadorPlazas > 4 or len(textoprazas)>1200)):
                textoprazas = textoprazas + "..."
                break

    return textoprazas