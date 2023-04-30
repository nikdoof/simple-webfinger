from flask import Flask, request, abort
import yaml

app = Flask(__name__)

with open('config.yaml', 'rb') as fobj:
    data = yaml.load(fobj, yaml.SafeLoader)


@app.route("/.well-known/webfinger")
def webfinger():
    resource = request.args.get('resource')

    if resource.split('@')[1] != data['domain']:
        abort(404)

    return {
        'subject': resource,
        'links': [{
            'rel': "http://openid.net/specs/connect/1.0/issuer",
            'href': data['oidc_href'],
        }]
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
