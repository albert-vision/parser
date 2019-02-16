from flask import Flask, request, jsonify, send_file
import json
import zipfile
import os

import config

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello():
    content = request.json
    my_handler(content)
    response = jsonify({"uuid": "asdasd"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return send_file("../file.zip", mimetype='application/zip')
    return response


def my_handler(event):
    for c in event['classes']:
        create_class(c, event['language'])

    newzip = zipfile.ZipFile(os.path.join(os.getcwd(), "file.zip"), 'w')

    for file in os.listdir("./"):
        if file.find("."+event['language']) != -1:
            print(os.path.join("./", file))
            newzip.write(file)
    newzip.close()


def create_class(c, language):
    cl = {
        "name": c['name'],
        "identifier": "public"
    }
    fields = c['properties']
    for f in fields:
        f['identifier'] = "private"

    in_field = False
    field_rows = []
    res = []

    def print_field_rows(field_rows_param):
        for field in fields:
            for i in field_rows_param:
                res.append(i.replace("<field_name>", field['name']).replace("<field_type>", field['type']).replace(
                    "<field_identifier>", field['identifier']))

    for line in config.LANGUAGE_SYNTAX[language]:
        if line.startswith('.'):
            res_file_name_ext = line[:-1]
            f = open(cl['name'] + res_file_name_ext, "w+")
            continue
        if line == "field\n":
            in_field = True
            continue
        if in_field:
            if line == "end\n":
                in_field = False
                print_field_rows(field_rows)
                field_rows = []
                continue
            field_rows.append(line)
            continue
        res.append(line.replace("<class_identifier>", cl['identifier']).replace("<class_name>", cl['name']))
    f.writelines(res)
    f.close()


app.run(host= '0.0.0.0',debug=True, threaded=False)