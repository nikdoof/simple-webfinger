from urllib.parse import urlparse

from flask import Flask, request, abort
import yaml

app = Flask(__name__)

with open('config.yaml', 'rb') as fobj:
    data = yaml.load(fobj, yaml.SafeLoader)


def get_account_links(user):
    links = []
    account_data = data['accounts'][user]

    # Append custom links
    if 'links' in account_data:
        links.extend(account_data['links'])

    if 'mastodon' in account_data:
        account, domain = account_data['mastodon'].split('@')
        links.extend([
            {'rel': 'http://webfinger.net/rel/profile-page', 'type': 'text/html', 'href': 'https://{0}/@{1}'.format(domain, account)},
            {'rel': 'self', 'type': 'application/activity+json', 'href': 'https://{0}/users/{1}'.format(domain, account)},
            {'rel': 'http://ostatus.org/schema/1.0/subscribe', 'template': "https://{0}/authorize_interaction?uri={{uri}}".format(domain)}
        ])

    # Append the OIDC link
    if 'oidc_href' in data:
        links.append({
            'rel': 'http://openid.net/specs/connect/1.0/issuer',
            'href': data['oidc_href'],
        })

    return links


def filter_links(links, rel):
    new_links = []
    for link in links:
        if link['rel'] == rel:
            new_links.append(link)
    return new_links


@app.route("/.well-known/webfinger")
def webfinger():
    resource = request.args.get('resource')

    # No resource requested, so return a HTTP 400
    if not resource:
        abort(400)

    account, domain = urlparse(resource).path.split('@')

    # If the request is not for the correct domain, or for an account that doesn't exist, return 404
    if domain != data['domain'] or account not in data['accounts']:
        abort(404)

    links = get_account_links(account)

    # If we have a 'rel' value on the request, filter down to the requested rel
    # https://datatracker.ietf.org/doc/html/rfc7033#section-4.3
    rel = request.args.get('rel')
    if rel:
        links = filter_links(links, rel)

    return {
        'subject': resource,
        'links': links
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
