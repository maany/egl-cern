# EGL Server

## How to setup EGL server?

All configuration settings used for setting up an EGL server is passed through environment variables through the `.env` file for local/docker development or `.env.okd` for deploying to OpenShift/OKD. Templates for those can be found in `env_templates/` directory.

### Local installation (using docker-compose)
0. Install `docker` and `docker-compose`
1. Get the required API keys.
- Mapquest Geolocation API key [from here](https://developer.mapquest.com/)
- Request API keys from CERN ServiceNow (request to MONIT team) for the following data sources
  - 7794 for FTS transfer data
  - 9023 for ATLAS job status data
2. Put API keys and other setup settings (PostgreSQL config, Django admin, etc.) in `.env` file in the root directory of the project according to the template  in `env_templates/`
3. Run with `docker-compose up`. It will create 2 containers, a `db` container that runs Postgres and a `web` container running the EGL server.
4. `docker-compose down` to stop it.

### OpenShift/OKD installation
0. Create a PaaS project from [CERN Web Services](https://webservices.web.cern.ch/webservices/). Install the `oc`(OpenShift client) tool locally.
1. Get the required API keys.
- Mapquest Geolocation API key [from here](https://developer.mapquest.com/)
- Request API keys from CERN ServiceNow (request to MONIT team) for the following data sources
  - 7794 for FTS transfer data
  - 9023 for ATLAS job status data
3. Put API keys and other setup settings (PostgreSQL config, Django admin, etc.) in `.env.okd` file in the root directory of the project according to the template  in `env_templates/`. Make sure you also fill in `OKD_FQDN` as this field is used by the Django application to allow access from the host.
4. Once it's activated go to [openshift](https://openshift.cern.ch/) and `Copy login command`. Execute in a terminal.
5. `oc project <YOUR PROJECT NAME>` to select your project.
6. Copy [PostgreSQL template](https://github.com/openshift/origin/blob/master/examples/db-templates/postgresql-persistent-template.json). In OpenShift `Add to Project -> Import YAML/JSON` and paste the template JSON.
7. Create an instance with DB name, username, and password matching the ones in `.env.okd` and the service has to be named `postgresql` (The application will use those to connect to the DB in the postgresql container)
8. In `openshift/django_with_postgres/deploy.sh` change the GitHub URL with an URL to your fork and the tags of the Docker image to point to your DockerHub account.
9. Execute `cd openshift/django_with_postgres && ./deploy.sh` to deploy to OpenShift.