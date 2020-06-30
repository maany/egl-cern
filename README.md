# EGL Server

## How to setup EGL server?

All configuration settings used for setting up an EGL server is passed through environment variables through the `.env` file for local/docker development or `.env.okd` for deploying to OpenShift/OKD. Templates for those can be found in `env_templates/` directory.

### Local installation (docker-compose) (recommended)
0. Install `docker` and `docker-compose`
1. Get the required API keys.
- Mapquest Geolocation API key [from here](https://developer.mapquest.com/)
- Request API keys from CERN ServiceNow (request to MONIT team) for the following data sources
  - 7794 for FTS transfer data
  - 9023 for ATLAS job status data
2. Put API keys and other setup settings (PostgreSQL config, Django admin, etc.) in `.env or .env.okd` file in the root directory of the project according to the template  in `env_templates/`
3. Run with `docker-compose up`. It will create 2 containers, a `db` container that runs Postgres and a `web` container running the EGL server.
4. `docker-compose down` to stop it.
  

### Local installation

1. Make a virtualenv and run `pip install -r requirements.txt` in it.
2. Install PostgreSQL. (e.g. in Ubuntu `sudo apt-get update && sudo apt-get install postgresql postgresql-contrib`)
3. Get the required API keys.
- Mapquest Geolocation API key [from here](https://developer.mapquest.com/)
- Request API keys from CERN ServiceNow (request to MONIT team) for the following data sources
  - 7794 for FTS transfer data
  - 9023 for ATLAS job status data
  
4. Put API keys and other setup settings (PostgreSQL config, Django admin, etc.) in `.env or .env.okd` file according to the template  in `env_templates/`
