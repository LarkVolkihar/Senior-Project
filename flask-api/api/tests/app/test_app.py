class TestApp:
    def test_app(app):
        assert app

    def test_request_example(self, client):
        response = client.get("/")
        assert b"Index" in response.data
