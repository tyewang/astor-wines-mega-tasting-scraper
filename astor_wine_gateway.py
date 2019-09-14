import requests

def get_tastings_index():
    result = requests.get("https://www.astorwines.com/tastingevents.aspx")
    return result.text


def get_tasting(relative_url):
    result = requests.get("https://www.astorwines.com/%s" % relative_url)
    return result.text
