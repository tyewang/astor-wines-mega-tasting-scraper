import requests

def get_tastings_index():
    with open('tests/fixtures/astor_wine_sample.html') as f:
        return f.read()


def get_tasting(relative_url):
    with open('tests/fixtures/astor_wine_event_sample.html') as f:
        return f.read()
