from flask import Flask
from flask import request
from flask_cors import CORS

from latex2sympy_custom4.process_latex import process_sympy
from sympy import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST'])
def hello_world():
    request_data = request.get_json()

    latex_expression = request_data['latexExpression']

    print(latex_expression)

    print(process_sympy(latex_expression))

    return '''
                   The latex_expression value is: {}
                   '''.format(latex_expression)


if __name__ == '__main__':
    app.run()

