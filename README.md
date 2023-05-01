# Simple Webfinger

A simple, Flask-based webfinger handler.

Simple Webfinger was created to provide an OIDC href from a basic YAML configuration file. Ideally for use with Tailscale and Authentik.

## Configuration

The `example-config.yaml` has the basic layout of the YAML file, which has the following fields. This should be provided as `config.yaml` in the working directory you're running the process.

| Key         | Value Example               | Description                                                   |
| ----------- | --------------------------- | ------------------------------------------------------------- |
| `domain`    | `doofnet.uk`                | The domain to respond to, it'll return 404s for anything else |
| `oidc_href` | `https://id.doofnet.uk/...` | The href to return for OIDC rels                              |

### Accounts

Accounts can be defined under the `accounts` key, and a key for each user, for example:

```yaml
accounts:
  nikdoof:
    mastodon: nikdoof@mastodon.incognitus.net
    aliases: []
    properties: []
    links: []
```

The app will only reply to accounts listed in the configuration, otherwise, it'll return a 404.

| Key          | Value Example                     | Description                                                     |
| ------------ | --------------------------------- | --------------------------------------------------------------- |
| `mastodon`   | `nikdoof@mastodon.incognitus.net` | A Mastodon account to generate the related links/properties for |
| `aliases`    | `[]`                              | A list of aliases to include in the response for the account    |
| `links`      | `[]`                              | A list of dicts to include in the response                      |
| `properties` | `[]`                              | A list of dicts to include in the response                      |
