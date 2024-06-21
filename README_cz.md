# Air Quality Monitoring System [MONAQ]
> Monitorování kvality ovzduší [MONAQ]

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-brightgreen.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue)

Malý backendový systém pro sběr, ukládání a zobrazování dat o kvalitě ovzduší ze senzorů využívajících MQTT. Tento projekt poskytuje rozhraní RESTful API pro obsluhu dat ze senzorů a je dostatečně flexibilní, aby podporoval libovolný frontend, v současné době implementovaný pomocí knihovny Streamlit.

> Tento projekt vznikl v rámci dvoutýdenní "praxe" v [Datovém centru ústeckého kraje](https://dcuk.cz/) s využitím datové platformy [Portabo](https://www.portabo.org/).

> [!NOTE]
> Mějte na paměti, že tento projekt byl vytvořen během dvou týdnů, takže čas byl trochu tlačící. Některé části nebo kód mohly být napsány/udělány lépe.

## Obsah

- [Ukázky](#ukázka)
- [Funkce](#funkce)
- [Použité technologie](#použité-technologie)
- [Pokyny k spuštění](#pokyny-k-spuštění)
  - [Předpoklady](#předpoklady)
  - [Instalace](#instalace)
  - [Spuštění](#spuštění)
- [API Endpointy](#api-endpointy)
- [Frontend](#frontend)

## Ukázka
![MainPage](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/2b8d9c0a-733b-4802-bdc7-c686d554744c)
![SensorsList](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/c5a1d50f-4e37-4140-8b8f-c0c5ec24a4d3)
![SensorDetail](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/e9cbf55a-cd00-43e9-a09f-bb73776851a1)
![Graphs](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/1e3e591f-92ed-49e5-b18b-2196becf5ac0)


## Funkce

- **MQTT Integrace**: Sbírá data ze senzorů kvality ovzduší pomocí protokolu MQTT.
- **RESTful API**: Poskytuje shromážděná data prostřednictvím rozhraní API založeného na FastAPI.
- **UUkládání dat**: Používá databázi MariaDB pro ukládání historických dat o kvalitě ovzduší.
- **Analýza dat**: Provadí vizualizaci a analýzu dat pomocí nástrojů Pandas a Plotly.
- **Flexibilní frontend**: Poskytuje flexibilní frontendové rozhraní s technologií Streamlit, které lze nahradit jakoukoli jinou technologií.

## Použité technologie

- **Python**: Základní jazyk pro backend.
- **FastAPI**: Pro vytváření rozhraní RESTful API.
- **MariaDB**: Pro ukládání databáze.
- **Docker**: Kontejnerizace aplikace.
- **Paho-MQTT**: Pro komunikaci MQTT.
- **Pandas**: Pro manipulaci s daty a jejich analýzu.
- **Plotly**: Pro vytváření interaktivních grafů.
- **Streamlit**: (Aktuální) Frontend framework.

## Pokyny k spuštění

### Předpoklady

- Základní znalost programování a Docker technologii.
- Docker a Docker Compose
- MariaDB (nepovinné)

### Instalace
1. **Klonování GH Repa**:

   ```bash
   git clone https://github.com/DEPSTRCZ/MONAQ.git
   cd MONAQ
   ```

2. **Konfigurace Docker-Compose**:

   Přejmenujte soubor `example-docker-compose.yml` na `docker-compose.yml`.
   Vyplňte všechny proměnné prostředí.

   Pokud chcete, odkomentujte část MariaDB pro server MariaDB, který lze použít. (Postupujte podle kroku 2.1)

  > [!IMPORTANT]
  > Vendor nemusí být povolen! Pouze shromažďuje data a ukládá je do DB. Pokud tento projekt nechcete opravdu použít a nemáte MQTT, nemusíte jej zapínat.

  > [!NOTE]
  > Pro fungování frontendu je potřeba token MapBox api.

2.1. **Nastavení vzorových dat pro databázi.**:
  - Připojte se k databázi.
  - Spusťte/importujte soubor `sample-data.sql`.
  > To lze provést pomocí HeidiSQL, DBeaver (Nebo pomocí přiloženého PhpMyAdmin, který lze povolit v souboru `docker-compose.yml`.

## Spuštění
```bash
docker-compose up --build
```

> To je vše! Projekt by měl být k dispozici:
- [FrontEnd](http://localhost)
- [FastAPI Swagger UI](https://localhost:8002/docs)

## API Endpointy
- `http://localhost:8002/getAllSensors` Načte všechny senzory z databáze spolu s jejich nejnovějšími daty.
```json
{
  "count": 2,
  "sensors": [
    {
      "temperature": "28.00",
      "updated_at": "2024-05-28T11:42:46",
      "sensor_id": 1,
      "co2": 852,
      "humidity": "43.00",
      "loc_lat": "0.000000",
      "loc_long": "0.000000"
    },
    {
      "temperature": "26.70",
      "updated_at": "2024-05-29T12:12:58",
      "sensor_id": 2,
      "co2": 724,
      "humidity": "40.00",
      "loc_lat": "0.000000",
      "loc_long": "0.000000"
    }
  ]
}
```

- `http://localhost:8002/getSensor/{id}` Načte informace o zadaném senzoru.
```json
{
  "sensor_id": 1,
  "times_posted": 1,
  "last_update": "2024-06-20T15:15:36",
  "records": [
    {
      "sensor_id": 1,
      "id": 25423,
      "co2": 1891,
      "humidity": "36.00",
      "loc_lat": "0.000000",
      "loc_long": "0.000000",
      "temperature": "28.50",
      "updated_at": "2024-06-20T15:15:36"
    }
  ]
}
```

- `http://localhost:8002/getQualityInfo/{id}` Stáhne informace o kvalitě ze zadaného senzoru. Včetně rozdílů.
```json
{
  "humidity": "36.0",
  "temperature": "28.5",
  "co2": 1915,
  "delta_co2": 24,
  "delta_humidity": "0.0",
  "delta_temperature": "0.0"
}
```

## Frontend

Současný frontend je implementován pomocí knihovny Streamlit.
BackEnd byl vytvořen převážně flexibilní. Měl by tedy fungovat s jakýmkoli backendem.
