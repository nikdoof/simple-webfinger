from urllib.parse import urlparse

import yaml
from flask import Flask, abort, request, Response
from prometheus_flask_exporter import PrometheusMetrics

from simple_webfinger.models.webfinger import JSONResourceDefinition


def get_account_links(user: str, data: dict) -> list:
    links = []
    account_data = data["accounts"][user]

    # Append the OIDC link
    if "oidc_href" in data:
        links.append(
            {
                "rel": "http://openid.net/specs/connect/1.0/issuer",
                "href": data["oidc_href"],
            }
        )

    # Append custom links
    if account_data:
        if "links" in account_data:
            links.extend(account_data["links"])

        if "mastodon" in account_data:
            account, domain = account_data["mastodon"].split("@")
            links.extend(
                [
                    {
                        "rel": "http://webfinger.net/rel/profile-page",
                        "type": "text/html",
                        "href": "https://{0}/@{1}".format(domain, account),
                    },
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": "https://{0}/users/{1}".format(domain, account),
                    },
                    {
                        "rel": "http://ostatus.org/schema/1.0/subscribe",
                        "template": "https://{0}/authorize_interaction?uri={{uri}}".format(
                            domain
                        ),
                    },
                ]
            )

    return links


def filter_links(links: dict[str, str], rel: list[str]) -> list:
    """
    Filter links by rel provided.
    """
    new_links = []
    for link in links:
        if link["rel"] in rel:
            new_links.append(link)
    return new_links


def create_app(config={}):
    app = Flask("simple_webfinger")

    metrics = PrometheusMetrics(app)
    metrics.info('app_info', 'Application info', version='0.1.0')
    
    app.webfinger_config = {
        "domain": None,
        "accounts": {},
    }
    app.config.from_prefixed_env("SIMPLE_WEBFINGER")
    app.config.from_object(config)

    if "CONFIG_FILE" in app.config:
        with open(app.config["CONFIG_FILE"], "rb") as fobj:
            app.webfinger_config = yaml.load(fobj, yaml.SafeLoader)

    if not app.webfinger_config["domain"]:
        app.logger.warning(
            "No domain is configured for webfinger, this instance will not operate correctly."
        )

    @app.after_request
    def inject_cors(response: Response) -> Response:
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    @app.route("/.well-known/webfinger")
    def webfinger():
        resource = request.args.get("resource")

        # No resource requested, so return a HTTP 400
        if not resource:
            abort(400)

        parsed_resource = urlparse(resource)
        scheme = parsed_resource.scheme
        account, domain = parsed_resource.path.split("@")

        # If the request is not for the correct domain, return 404
        if domain != app.webfinger_config["domain"]:
            abort(404)

        # Handle acct resource requests
        if scheme == "acct":
            if account not in app.webfinger_config["accounts"]:
                abort(404)

            account_data = app.webfinger_config["accounts"][account]
            links = get_account_links(account, app.webfinger_config)

            # If we have a 'rel' value on the request, filter down to the requested rel
            # https://datatracker.ietf.org/doc/html/rfc7033#section-4.3
            rel = request.args.getlist("rel")
            if rel:
                links = filter_links(links, rel)

            response = {"subject": resource, "links": links}
            
            # Add properties if defined in the config
            if account_data and "properties" in account_data and len(account_data["properties"]):
                response.update({"properties": account_data["properties"]})

            return app.response_class(
                response=JSONResourceDefinition(**response).model_dump_json(
                    exclude_none=True
                ),
                status=200,
                mimetype="application/jrd+json",
            )

        # Anything else, 404 for now
        abort(404)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8000)
