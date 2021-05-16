import os

from sympy import *
from sympy.abc import x
from flask import Flask
from flask import request
from flask_cors import CORS
from xml.dom import minidom
from xml.etree import ElementTree as ET

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

    contest_id = '8'
    contest_dir_name = get_contest_file_name(contest_id)
    problem_id = '33'
    short_name = 'test'
    long_name = 'teeeeest'
    variants_count = '5'
    user_variants_dict = {"user1": 2, "user2": 1, "user3": 3}

    create_config_file(contest_id, contest_dir_name, problem_id, short_name, long_name, variants_count)

    generate_contest_file(contest_dir_name, contest_id, 'testName', 'testNameEn')

    print(sympy_expression.evalf(subs={x: 10}))

    print(process_sympy(latex_expression))

    users = get_users_from_db()

    generate_variant_map(user_variants_dict)

    print(users)

    # os.system(' ./shell_scripts/main_script.sh {} {}'.format(str('3'), str('4')))

    return 'The latex_expression value is: {}'.format(latex_expression)


def generate_contest_file(cont_dir_name, cont_id, name, en_name):
    file = create_xml_file(str(cont_id), name, en_name, cont_dir_name)

    save_path_file = './output_files/' + cont_dir_name + '.xml'

    with open(save_path_file, "w") as f:
        f.write(file)

    return 0


def get_contest_file_name(cont_id):
    name = '000000'
    return name[:-len(cont_id)] + cont_id


def create_xml_file(inp_id, inp_name, inp_name_en, inp_dir_name):
    contest_file = minidom.Document()

    contest = contest_file.createElement('contest')
    contest.setAttribute('id', inp_id)
    contest.setAttribute('autoregister', 'yes')
    contest.setAttribute('disable_team_password', 'yes')
    contest.setAttribute('managed', 'yes')
    contest.setAttribute('run_managed', 'yes')
    contest_file.appendChild(contest)

    name_child = contest_file.createElement('name')
    name_text = contest_file.createTextNode(inp_name)
    name_child.appendChild(name_text)
    contest.appendChild(name_child)

    name_en_child = contest_file.createElement('name_en')
    name_en_text = contest_file.createTextNode(inp_name_en)
    name_en_child.appendChild(name_en_text)
    contest.appendChild(name_en_child)

    register_access_child = contest_file.createElement('register_access')
    register_access_child.setAttribute('default', 'allow')
    contest.appendChild(register_access_child)

    users_access_child = contest_file.createElement('users_access')
    users_access_child.setAttribute('default', 'allow')
    contest.appendChild(users_access_child)

    team_access_child = contest_file.createElement('team_access')
    team_access_child.setAttribute('default', 'allow')
    contest.appendChild(team_access_child)

    judge_access_child = contest_file.createElement('judge_access')
    judge_access_child.setAttribute('default', 'allow')
    contest.appendChild(judge_access_child)

    master_access_child = contest_file.createElement('master_access')
    master_access_child.setAttribute('default', 'allow')
    contest.appendChild(master_access_child)

    serve_control_access_child = contest_file.createElement('serve_control_access')
    serve_control_access_child.setAttribute('default', 'allow')
    contest.appendChild(serve_control_access_child)

    caps_child = contest_file.createElement('caps')

    cap_child = contest_file.createElement('cap')
    cap_child.setAttribute('login', 'ejudge')
    cap_text = contest_file.createTextNode('FULL_SET,')
    cap_child.appendChild(cap_text)
    caps_child.appendChild(cap_child)

    contest.appendChild(caps_child)

    client_flags = contest_file.createElement('client_flags')
    client_flags_text = contest_file.createTextNode('IGNORE_TIME_SKEW,')
    client_flags.appendChild(client_flags_text)
    contest.appendChild(client_flags)

    root_dir_child = contest_file.createElement('root_dir')
    root_dir_text = contest_file.createTextNode(inp_dir_name)
    root_dir_child.appendChild(root_dir_text)
    contest.appendChild(root_dir_child)

    return contest_file.toprettyxml(indent="\t")


def create_config_file(cont_id, dir_name, problem_id, short_name, long_name, variants_count):
    check_words = ('input_contest_id', 'input_root_dir', 'input_problem_id', 'input_problem_short_name',
                   'input_problem_long_name', 'input_problem_variant_num')
    rep_words = (cont_id, dir_name, problem_id, short_name, long_name, variants_count)

    input_file = open('templates/serve.cfg', 'r')
    result_file = open('output_files/serve.cfg', 'w')

    for line in input_file:
        for check, rep in zip(check_words, rep_words):
            line = line.replace(check, rep)
        result_file.write(line)
    input_file.close()
    result_file.close()


def get_users_from_db():
    user_logins = []
    os.system('./shell_scripts/test_script_by_root.sh')
    tree = ET.parse('./input_files/users_db.xml')
    xml_root = tree.getroot()
    for user in xml_root.findall('user'):
        user_logins.append(user.find('login').text)
    return user_logins


def generate_variant_map(user_variants_dict):
    input_file = open('templates/variant.map', 'r')
    result_file = open('output_files/variant.map', 'w')

    users_variant_part = ''

    for key in user_variants_dict:
        users_variant_part += '\n\t{0} {1}'.format(key, user_variants_dict[key])

    for line in input_file:
        line = line.replace('input_variant_map', users_variant_part)
        result_file.write(line)
    input_file.close()
    result_file.close()


if __name__ == '__main__':
    app.run()
