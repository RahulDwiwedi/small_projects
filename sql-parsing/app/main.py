# -*- coding: utf-8 -*-

# import ordereddict
import os

try:
    from BeautifulSoup import BeautifulSoup as bs
except ImportError:
    from bs4 import BeautifulSoup as bs

from moz_sql_parser import parse
from flask import json, url_for
from flask import Flask
from flask import request
import html
from flask import render_template, render_template_string
from sqlparse import format
from json2html import *

app = Flask(__name__)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def my_form():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    sql_text = request.form['sql']
    sql_text = sql_text.replace("`", "")
    sql_text = format(sql_text, reindent=True,keyword_case='upper')
    parsed_sql = parse(sql_text)
    semi_sql_json = json.dumps(parsed_sql, sort_keys=False)
    sql_json = json.dumps(parsed_sql, sort_keys=False, indent=4)

    res_final = findkeys(semi_sql_json)
    final = findtablenames(res_final)

    tables_used = list(set(final))
    columns = findcolumn(semi_sql_json)

    html_list = jsontohtmllist(semi_sql_json)

    processed_text = json2html.convert(json=semi_sql_json,
                                       table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")

    return render_template("index.html",columns=columns, html_list=html_list, tables_used=tables_used, processed_text=processed_text,
                           sql=sql_text,
                           json=sql_json)


def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # Return value ignored.
    return results


def iterJson(ordered_json, style):
    global a
    a = a + style
    for k, v in ordered_json.items():
        a = a + '<tr>'
        a = a + '<th>' + str(k) + '</th>'
        if (v == None):
            v = str("")
        if (isinstance(v, list)):
            a = a + '<td><ul>'
            for i in range(0, len(v)):
                if (isinstance(v[i], str)):
                    a = a + '<li>' + str(v[i]) + '</li>'
                elif (isinstance(v[i], int) or isinstance(v, float)):
                    a = a + '<li>' + str(v[i]) + '</li>'
                elif (isinstance(v[i], list) == False):
                    iterJson(v[i], style)
            a = a + '</ul></td>'
            a = a + '</tr>'
        elif (isinstance(v, str)):
            a = a + '<td>' + str(v) + '</td>'
            a = a + '</tr>'
        elif (isinstance(v, int) or isinstance(v, float)):
            a = a + '<td>' + str(v) + '</td>'
            a = a + '</tr>'
        else:
            a = a + '<td>'
            # a=a+ '<table border="1">'
            iterJson(v, style)
            a = a + '</td></tr>'
    a = a + '</table>'


def htmlConvertor(ordered_json, style):
    '''
    converts JSON Object into human readable HTML representation
    generating HTML table code with raw/bootstrap styling.
    '''
    global a
    try:
        for k, v in ordered_json.items():
            pass
        iterJson(ordered_json, style)

    except Exception as e:
        print(e)
        for i in range(0, len(ordered_json)):
            if (isinstance(ordered_json[i], str)):
                a = a + '<li>' + str(ordered_json[i]) + '</li>'
            elif (isinstance(ordered_json[i], int) or isinstance(ordered_json[i], float)):
                a = a + '<li>' + str(ordered_json[i]) + '</li>'
            elif (isinstance(ordered_json[i], list) == False):
                htmlConvertor(ordered_json[i], style)

    return a


def findkeys(res):
    keys_list = ["left join", "tablename", "join", "cross join", "right join"]
    res_final = []
    for keys in keys_list:
        res_final.append(find_values(keys, res))
    res_final = [x for x in res_final if x]
    return res_final


def findtablenames(res_final):
    final = []
    for keys in res_final:
        if isinstance(keys, list):
            for key in keys:
                print(type(key))
                if isinstance(key, str):
                    final.append(key)
                    print("tables : {0}".format(key))
                elif isinstance(key, dict):
                    key = json.dumps(key)
                    temp = findkeys(key)
                    for i in temp:
                        print("table list : {0}".format(i))
                    final += i
    return final


def jsontohtmllist(j):
    j = j.replace("'", "\"")
    j = json.loads(j)

    result = []

    def test(j):
        node = j
        if isinstance(node, dict):
            result.append('<ul>')
            for key, v in node.items():
                k = list(node.keys())
                if isinstance(v, str):
                    result.append('<li>{0} <ul>'.format(key))
                    result.append('<li>{0}</li></ul></li>'.format(v))
                else:
                    result.append('<li>{0}'.format(key))
                    test(v)
                    result.append("</li>")
                # if str(key) == k[-1]:
                #     result.append('</ul></li>')
            result.append('</ul>')
        if isinstance(node, list):

            for v in node:
                if isinstance(v, str):
                    result.append('<ul>')
                    result.append('<li>{0}</li>'.format(v))
                    result.append('</ul>')
                else:
                    test(v)

        return result

    final = test(j)
    final = "".join(final)
    return final


def findcolumn(j):
    j = j.replace("'", "\"")
    j = json.loads(j)
    result=[]
    res =dict()
    def findfrom(j,col,val=None):
        for k,v in j.items():
            if k=='select':
                if val is None:
                    flag = str(col) in str(v)
                else:
                    flag = str(val) in str(v)
                if flag:
                    f = j.get("from")
                    if isinstance(f,list):
                        for i in f:
                            keys_list = ["left join", "tablename", "join", "cross join", "right join"]
                            for keys in keys_list:
                                if str(keys) in i:
                                    tbl = f.get(keys)
                                    res[col]=tbl
                                    return res
                            if 'select' in i:
                                sel = i.get('query')
                                # sel = sel.get('select')
                                re = findfrom(sel,col,val)
                                return re
                    if isinstance(f,dict):
                        if 'select' in f:
                            sel = f.get('query')
                            # sel = sel.get('select')
                            re = findfrom(sel, col,val)
                            return re
                        keys_list = ["left join", "tablename", "join", "cross join", "right join"]
                        for keys in keys_list:
                            if str(keys) in f:
                                tbl = f.get(keys)
                                res[col] = tbl
                                return res


    for k,v in j.items():
        if str(k)=='select':
            if isinstance(v,list):
                for i in v:
                    if isinstance(i['value'],str):
                        column = i['value']
                        r = findfrom(j,column)
                        result.append(r)
                    if isinstance(i['value'], dict):
                        val=i['value']
                        val_list =[v for v in val.values()]
                        column2 = i['name']
                        r=[]
                        for value in val_list:
                            r.append(findfrom(j,column2,value))
                        result.append(r)
            if isinstance(v,dict):
                if isinstance(v['value'], str):
                    column = v['value']
                    r = findfrom(j, column)
                    result.append(r)
                if isinstance(v['value'], dict):
                    val = v['value']
                    val_list = [v for v in val.values()]
                    column2 = v['name']
                    r = []
                    for value in val_list:
                        r.append(findfrom(j, column2, value))
                    result.append(r)
    print(result)
    super_dict = {}
    for d in result:
        if isinstance(d, list):
            for i in d:
                for k, v in i.items():
                    super_dict.setdefault(k, []).append(v)
        if isinstance(d, dict):
            for k, v in d.items():
                super_dict.setdefault(k, []).append(v)
    for k, v in super_dict.items():
        v = list(set(v))
        super_dict[k] = v

    return super_dict


if __name__ == '__main__':
    app.run(debug=True)
