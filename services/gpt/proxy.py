import os

def set_proxy():
    os.environ["HTTP_PROXY"] = "http://sfjXSk:Yn7tKN@170.244.95.124:9543"
    os.environ["HTTPS_PROXY"] = "http://sfjXSk:Yn7tKN@170.244.95.124:9543"

def clear_proxy():
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
