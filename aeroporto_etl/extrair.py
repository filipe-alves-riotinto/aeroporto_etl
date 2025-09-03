import os
import ipdb
import requests
import re
import time
import pytz

from datetime import datetime, timedelta

import logging
from pathlib import Path

from constantes import BASE_URL

logging.basicConfig(filename=os.path.join(str("/home/filipe/scripts/pessoais-projetos/etl/aeroporto_etl/aeroporto_etl"), "aeroporto.log"),
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_endpoint(endpoint, endpoint_id = None, params = None):
    headers = {
        "Accept": "application/json",
        "app_id": os.getenv("APP_ID"),
        "app_key": os.getenv("APP_KEY"),
        "ResourceVersion": "v4"
    }

    url = BASE_URL + endpoint
    if endpoint_id:
        url = url + "/" + endpoint_id

    resultados = []

    resultado_get = requests.get(url=url, headers= headers, params=params)
    resultado_get.raise_for_status()

    resultados.append(resultado_get.json())

    numero_paginas = processar_headers_numero_paginas(resultado_get.headers)

    while link := processar_headers_next(resultado_get.headers):
        time.sleep(0.5)
        logging.info(f"Páginas: {numero_paginas} link: {link}")
        resultado_get = requests.get(url=link, headers= headers)
        resultado_get.raise_for_status()

        resultados.append(resultado_get.json())
    return resultados

    #ipdb.set_trace()

def processar_headers_next(headers):

    headers_link = headers.get("link")

    if not headers_link:
        return None
    exp_regular = r"<(.*)>"
    
    link_partes = headers_link.split(",")

    for link_parte in link_partes:
        if 'rel="next"' in link_parte:
            link = link_parte.split(";")[0]
            link = re.search(exp_regular, link)
            return link.groups()[0]

def processar_headers_numero_paginas(headers):

    headers_link = headers.get("link")
    if not headers_link:
        return '0'
    
    link_partes = headers_link.split(",")

    exp_regular = r".*page=([0-9]+).*"

    for link_parte in link_partes:
        if 'rel="last' in link_parte:
            numero = link_parte.split(";")[0]
            numero = re.search(exp_regular, numero)

            return numero.groups()[0]
    return '0'

def get_flights_agendado_hoje():
    return get_endpoint("flights")

def get_flights_agendado_ontem():
    agora = datetime.now(pytz.timezone("Europe/Amsterdam"))
    ontem = agora.date() - timedelta(days=1)
    ontem = ontem.strftime("%Y-%m-%d")

    params = {"scheduleDate": ontem}
    print(params)
    return get_endpoint(endpoint="flights", params=params)

def get_flight_por_id(flight_id):
    return get_endpoint(endpoint='flights', endpoint_id=flight_id)

def get_airlines():
    return get_endpoint(endpoint="airlines")

def get_airlines_por_iata_icao(iata_icao):
    return get_endpoint(endpoint='airlines', endpoint_id=iata_icao)

def get_aircraft_types():
    return get_endpoint(endpoint="aircrafttypes")

def get_destinations():
    return get_endpoint(endpoint="destinations")

def get_destinations_iata(destinations_iata):
    return get_endpoint(endpoint='destinations', endpoint_id=destinations_iata)

