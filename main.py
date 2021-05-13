from sympy import *
from sympy.abc import x
from flask import Flask
from flask import request
from flask_cors import CORS
from xml.dom import minidom

from latex2sympy_custom4.process_latex import process_sympy

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST'])
def parse_expression():
    request_data = request.get_json()

    latex_expression = request_data['latexExpression']

    latex_expression = latex_expression.replace('f(x)=', '')

    print(latex_expression)

    sympy_expression = process_sympy(latex_expression)

    print('{} - sympy expression'.format(sympy_expression))

    print(get_contest_file_name(str(12)))

    create_contest_file(get_contest_file_name(str(8)), 'test', 'testEn')

    print(sympy_expression.evalf(subs={x: 10}))

    print(process_sympy(latex_expression))

    return 'The latex_expression value is: {}'.format(latex_expression)


def create_contest_file(cont_id, name, en_name):
    contest_file = minidom.Document()

    xml = contest_file.createElement('root')
    contest_file.appendChild(xml)

    product_child = contest_file.createElement('product')
    product_child.setAttribute('name', 'Geeks for Geeks')

    xml.appendChild(product_child)

    xml_str = contest_file.toprettyxml(indent="\t")

    save_path_file = "000008.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)

    return 0


def get_contest_file_name(cont_id):
    name = '000000'
    return name[:-len(cont_id)] + cont_id


if __name__ == '__main__':
    app.run()

