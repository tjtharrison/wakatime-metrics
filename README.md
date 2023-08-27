# wakatime-metrics

Python scripts for generating dashboards from wakatime metrics data.

# Authentication

You can authenticate with the Wakatime API using an API token from [here](https://wakatime.com/settings/api-key)

This should be stored as environment variable `WAKATIME_API_KEY`

# Local development

To develop locally, you should create a file called `.env` with the following contents:

```
WAKATIME_API_KEY=<your api key>
```

Now install the dependencies with:

```commandline
pip3 install -r requirements.txt
```

Then you can launch the server with:

```commandline
python3 main.py
```

After launching the server, you can access the dashboard at http://localhost:8080.

