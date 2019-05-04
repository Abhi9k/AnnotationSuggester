import os


def fetchJavaFiles(path, response):
    if os.path.isfile(path):
        if path.endswith('.java'):
            response.append(path)
    else:
        try:
            files = os.listdir(path)
            path = path.rstrip(os.sep)
            paths = map(lambda x: path + os.sep + x, files)
            for p in paths:
                fetchJavaFiles(p, response)
        except Exception:
            pass
