def test_index_route(client):
    """
    Check that the index route is 404
    """
    response = client.get("/")
    assert response.status_code == 404


def test_webfinger_route(client):
    """
    Check a basic GET to the webfinger route returns a 400
    """
    response = client.get("/.well-known/webfinger")
    # We don't provide any arguments, so this should be a 400
    assert response.status_code == 400


def test_domain(app, client):
    """
    Check a correct call to the webfinger endpoint returns a valid response
    """
    response = client.get("/.well-known/webfinger?resource=acct:nikdoof@doofnet.uk")
    assert response.status_code == 200


def test_invalid_domain(app, client):
    """
    Check a invalid domain name results in a 404
    """
    response = client.get("/.well-known/webfinger?resource=acct:nikdoof@xxxx.uk")
    assert response.status_code == 404


def test_invalid_user(app, client):
    """
    Check a invalid user results in a 404
    """
    response = client.get("/.well-known/webfinger?resource=acct:nikxxxdoof@doofnet.uk")
    assert response.status_code == 404

def test_invalid_user_request(app, client):
    """
    Check a invalid user request (without acct) results in a 404
    """
    response = client.get("/.well-known/webfinger?resource=nikdoof@doofnet.uk")
    assert response.status_code == 404
