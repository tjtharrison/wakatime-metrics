"""Small Flask server to pull metrics from WakaTime API and display them on a webpage."""
import base64
import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Create / endpoint
@app.route("/")
def index():
    """Index page.

    Returns:
        str: The rendered index.html template.
    """
    return render_template("index.html")


# Metrics endpoint
@app.route("/metrics", methods=["GET", "POST"])
def metrics():
    """Metrics page.

    Returns:
        str: The rendered metrics.html template.
    """
    # If the request is a POST request
    if request.method == "POST":
        # Get the form data
        form_data = request.form

        try:
            wakatime_api_key = os.environ.get("WAKATIME_API_KEY")
            wakatime_api_key_bytes = wakatime_api_key.encode("ascii")
            wakatime_api_key_base64_bytes = base64.b64encode(wakatime_api_key_bytes)
            wakatime_api_key_base64_string = wakatime_api_key_base64_bytes.decode(
                "ascii"
            )
            # If the WakaTime API key is not set
            if not wakatime_api_key:
                raise KeyError("WakaTime API key not set")

            # Get metrics from WakaTime API
            wakatime_api_response = requests.get(
                f'https://wakatime.com/api/v1/users/current/stats/{form_data["period"]}',
                headers={"Authorization": "Basic " + wakatime_api_key_base64_string},
            )

            if wakatime_api_response.status_code != 200:
                raise AttributeError(
                    f"WakaTime API request failed: wakatime_api_response.status_code={wakatime_api_response.text}"
                )

            # Parse the JSON response
            wakatime_api_response_json = json.loads(wakatime_api_response.text)

            response_data = {}

            # process_languages
            languages = []
            for language in wakatime_api_response_json["data"]["languages"]:
                # Convert seconds to minutes
                if language["total_seconds"] > 60:
                    languages.append({language["name"]: language["total_seconds"] / 60})

            # process editors
            editors = []
            for editor in wakatime_api_response_json["data"]["editors"]:
                # Convert seconds to minutes
                if editor["total_seconds"] > 60:
                    editors.append({editor["name"]: editor["total_seconds"] / 60})

            # process operating_systems
            operating_systems = []
            for operating_system in wakatime_api_response_json["data"][
                "operating_systems"
            ]:
                # Convert seconds to minutes
                if operating_system["total_seconds"] > 60:
                    operating_systems.append(
                        {
                            operating_system["name"]: operating_system["total_seconds"]
                            / 60
                        }
                    )

            # Return the JSON response
            print(
                str(
                    {
                        "languages": languages,
                        "editors": editors,
                        "operating_systems": operating_systems,
                    }
                )
            )
            return {
                "status": "ok",
                "message": json.dumps(
                    {
                        "languages": languages,
                        "editors": editors,
                        "operating_systems": operating_systems,
                    }
                ),
            }
        # If the WakaTime API key is not set
        except KeyError:
            # Redirect to the index page
            logging.error("WakaTime API key not set")
            return {"status": "failed", "message": "WakaTime API key not set"}
        except AttributeError as error_message:
            # Redirect to the index page
            logging.error("WakaTime API request failed: %s", str(error_message))
            return {"status": "failed", "message": "WakaTime API request failed"}

    # Return the JSON response
    return {"status": "ok", "message": "Retrieving metrics.."}


# Launch app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
