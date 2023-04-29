Displays building permits in the City of Edmonton in a simple interface.

Run locally with 

`python -m flask --app server.py run`

## Deploying

`gunicorn -w 2 'server:app'`

`caddy start`