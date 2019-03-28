import subprocess
import os


def fetchByGithubUrl(url, project_name, output_location):
    url = url.rstrip('/')
    response = []
    absolute_path = output_location + os.sep + project_name
    try:
        subprocess.check_output(['git', 'clone', url, absolute_path])
        response.append((absolute_path, 1))
    except subprocess.CalledProcessError:
        response.append((absolute_path, 0))
    return response


def fetchProjects(urls, output_location, repo_type='github'):
    if repo_type == 'github':
        response = []
        for url in urls:
            project_name = url.split('/')[-1]
            response = fetchByGithubUrl(url, project_name, output_location)
        return response
