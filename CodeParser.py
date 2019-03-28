import javalang
from itertools import count
import os
import sys
# import requests
from javalang.tree import *
from fetch_filenames import fetchJavaFiles
from fetch_repository import fetchProjects

# 1. Fetch project from github
# 2. Recursively iterate all the directories
#     File Name
#         Class Name
#             Constructor, Annotation, line number
#             Method, Annotation, line number
#             Field, Annotation, line number


# 3. Final CSV output

#     File Name, Class Name, Type, Annotation Name, Line Number

#     Type is an enum [Constructor, Method,Field]1. Fetch project from github
# 2. Recursively iterate all the directories
#     File Name
#         Class Name
#             Constructor, Annotation, line number
#             Method, Annotation, line number
#             Field, Annotation, line number


# 3. Final CSV output

#     Project Name, File Name, Class Name, Type, Annotation Name, Line Number

#     Type is an enum [Constructor, Method,Field]

def printAnn(node, response):
    name = ''
    if type(node) != FieldDeclaration:
        name = node.name

    for annotation in node.annotations:
        response.append((name, str(type(node)).split('.')[-1][:-2], annotation.name))


def process(node, response):
    if type(node) in [MethodDeclaration, ClassDeclaration,
                      ConstructorDeclaration, FieldDeclaration]:
        printAnn(node, response)
    if type(node) == list:
        for n in node:
            process(n, response)
    elif type(node) in [MethodDeclaration, ClassDeclaration, ConstructorDeclaration]:
        process(node.body, response)


def writeOutputCSV(output):
    f = open('output' + os.sep + 'data.csv', 'w')
    for project_name, file_path, annotations in output:
        file_name = os.sep.join(file_path.split(os.sep)[9:])
        for ann in annotations:
            f.write("{},{},{},{}\n".format(
                project_name, file_name, ann[0], ann[1], ann[2]))
    f.close()


if __name__ == '__main__':
    threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    base_path = os.path.abspath('data')
    project_urls = map(lambda x: x.strip('\n'), open('project_urls.txt', 'r').readlines())
    project_names = map(lambda url: url.split('/')[-1], project_urls)
    projects_present = os.listdir(base_path)
    projects_present_paths = map(lambda x: base_path + os.sep + x, projects_present)
    projects_to_fetch = map(lambda x: x[1], filter(
        lambda x: project_names[x[0]] not in projects_present, enumerate(project_urls)))

    fetched_projects = fetchProjects(projects_to_fetch, base_path)
    fetched_projects = map(lambda x: x[0], filter(lambda x: x[1] == 1, fetched_projects))

    projects_present_paths.extend(fetched_projects)
    response = {}
    for project_path in projects_present_paths:
        name = project_path.split(os.sep)[-1]
        response[name] = []
        fetchJavaFiles(project_path, response[name])

    counter = count()
    final_response = []
    for project_path in response:
        project_name = os.path.split(project_path)[-1]
        for file in response[project_path]:
            annotations = []
            code = open(file, 'r').read()
            try:
                tree = javalang.parse.parse(code)
                process(tree.children, annotations)
                if threshold != -1 and next(counter) > threshold:
                    break
                final_response.append((project_name, file, annotations))
            except javalang.parser.JavaSyntaxError:
                print "error while parsing " + file

    writeOutputCSV(final_response)
