from extrair import get_airlines, get_aircraft_types, get_destinations, get_flights_agendado_hoje
from salvar import salvar
from transformar import transformar_airlines, transformar_aircraft_types_paginas, transformar_destinations, transformar_flights

def main_etl():
    #Extract
    flights_paginas = get_flights_agendado_hoje()
    #airlines_paginas = get_airlines()
    #aircraft_types_paginas = get_aircraft_types()
    #destinations_paginas = get_destinations()

    #Transform
    flights = transformar_flights(flights_paginas)
    #airlines = transformar_airlines(airlines_paginas)
    #aircraft_types = transformar_aircraft_types_paginas(aircraft_types_paginas)
    #destinations = transformar_destinations(destinations_paginas)
    #Load

    salvar("../", 
                [
                    flights,
                    #airlines, 
                    #aircraft_types, 
                    #destinations
                ],
                [
                    "flights",
                    #"airlines", 
                    #"aircraft_types",
                    #"destinations"
                ]
            )


if __name__ == "__main__":
    main_etl()