# Air Quality Monitoring System [MONAQ]

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue)

A small backend system for collecting, storing, and displaying air quality data from sensors that use MQTT. This project provides a RESTful API to serve sensor data and is flexible enough to support any frontend, currently implemented using Streamlit.

> [!NOTE]
> This project was made as part of 2-Wekk "internship" at [Datové centrum ústeckého kraje](https://dcuk.cz/) utilizing the data platform called [Portabo](https://www.portabo.org/)

## Table of Contents

- [Screenshots](#screenshots)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Docker Support](#docker-support)
- [Contributing](#contributing)
- [License](#license)

## Screenshots
![MainPage](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/2b8d9c0a-733b-4802-bdc7-c686d554744c)
![SensorsList](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/c5a1d50f-4e37-4140-8b8f-c0c5ec24a4d3)
![SensorDetail](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/e9cbf55a-cd00-43e9-a09f-bb73776851a1)
![Graphs](https://github.com/DEPSTRCZ/MONAQ/assets/77269898/1e3e591f-92ed-49e5-b18b-2196becf5ac0)


## Features

- **MQTT Integration**: Collects data from air quality sensors using the MQTT protocol.
- **RESTful API**: Serves the collected data via a FastAPI-based API.
- **Data Storage**: Utilizes MariaDB for storing historical air quality data.
- **Data Analysis**: Supports data analysis with Pandas and Plotly for data visualization.
- **Flexible Frontend**: Provides a flexible frontend interface with Streamlit, easily replaceable with any other technology.

## Technologies Used

- **Python**: Core language for the backend.
- **FastAPI**: For creating RESTful APIs.
- **MariaDB**: For database storage.
- **Docker**: Containerization of the application.
- **Paho-MQTT**: For MQTT communication.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For creating interactive plots and graphs.
- **Streamlit**: (Current) Frontend framework.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- MariaDB (optional)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/DEPSTRCZ/MONAQ.git
   cd MONAQ
   ```

2. **Configure Docker-Compose**:

   Rename the `example-docker-compose.yml` to `docker-compose.yml`.
   Fill in all the enviroment variables.

   If wanted uncomment the MariaDB section for MariaDB server that can be used. (Follow step 2.1)

  > [!IMPORTANT]
  > Vendor does not need to be enabled! It just collects data and saves the to DB. So unless you want to use this seriously and give it data using MQTT you don't need to.

  > [!NOTE]
  > MapBox api token is needed for the frontend to work.

2.1. **Setting up sample data for database.**:
  - Connect to your database.
  - Run/Import the `sample-data.sql`
  > That can be done using HeidiSQL, DBeaver (Or the included PhpMyAdmin that can be enabled in `docker-compose.yml`

  > [!TIP]
  > You can also uncomment phpmyadmin to make importing the DB easier.

## Running
```bash
docker-compose up --build
```

> Thats it! The project should be available:
- [FrontEnd](http://localhost)
- [FastAPI Swagger UI](https://localhost:8002/docs)

## Frontend

The current frontend is implemented using Streamlit.
The BackEnd was made mostly flexible. So it should work with any backend.
