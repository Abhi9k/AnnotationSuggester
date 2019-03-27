import javalang
import requests
from javalang.tree import *


def printAnn(node):
    for annotation in node.annotations:
        print type(node), annotation.name


def process(node):
    if type(node) in [MethodDeclaration, ConstructorDeclaration, FieldDeclaration]:
        printAnn(node)
    if type(node) == list:
        for n in node:
            process(n)
    elif type(node) in [MethodDeclaration, ConstructorDeclaration]:
        process(node.body)


if __name__ == '__main__':
    code = requests.get('https://raw.githubusercontent.com/spring-projects/spring-framework/master/spring-orm/src/main/java/org/springframework/orm/ObjectRetrievalFailureException.java').content
    tree = javalang.parse.parse(code)
    children = tree.types[0].children
    for ch in children:
        process(ch)
