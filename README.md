# wakatime-metrics

Python scripts for generating dashboards from wakatime metrics

# Authentication

You can authenticate with the Wakatime API using an API token from [here](https://wakatime.com/settings/api-key)

This should be stored as environment variable `WAKATIME_API_KEY`

# Local development

To develop locally, you should create a file called `.env` with the following contents:

```
WAKATIME_API_KEY=<your api key>
```

Then you can launch the server with:

```commandline
python3 main.py
```