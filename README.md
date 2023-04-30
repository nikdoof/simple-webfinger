# Simple Webfinger

A simple, Flask-based webfinger handler.

Simple Webfinger was created to provide an ODIC href from a basic YAML configuration file. Ideally to use with Tailscale and Authentik.

## Configuration

The `example-config.yaml` has the basic layout of the YAML file, which has the following fields. This should be provided as `config.yaml` in the working directory you're running the process.

| Key         | Value Example               | Description                                                   |
| ----------- | --------------------------- | ------------------------------------------------------------- |
| `domain`    | `doofnet.uk`                | The domain to respond to, it'll return 404s for anything else |
| `oidc_href` | `https://id.doofnet.uk/...` | The href to return for OIDC rels                              |


