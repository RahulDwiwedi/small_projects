from sqlparse import format
import json
from networkx.readwrite import json_graph
import networkx as nx
import matplotlib.pyplot as plt


k='''{"select":[{"value":"a.*"},{"value":"org.CodeDesc","name":"SalesOrg_"},{"value":"g.CodeDesc","name":"TradeChannel_"},{"value":"h.CodeDesc","name":"CustomerType_"},{"value":"i.personNo"},{"value":"i.firstname"},{"value":"i.lastname"},{"value":"j.CodeDesc","name":"outlet_class"}]}'''


j = '''{
    "select": [
        {
            "value": "SalesOrg_"
        },
        {
            "value": "TradeChannel_"
        },
        {
            "value": "CustomerType_"
        },
        {
            "value": "personNo"
        },
        {
            "value": "firstname"
        },
        {
            "value": "lastname"
        },
        {
            "value": "outlet_class"
        }
    ],
    "from": {
        "query": {
            "select": [
                {
                    "value": "a.*"
                },
                {
                    "value": "org.CodeDesc",
                    "name": "SalesOrg_"
                },
                {
                    "value": "g.CodeDesc",
                    "name": "TradeChannel_"
                },
                {
                    "value": "h.CodeDesc",
                    "name": "CustomerType_"
                },
                {
                    "value": "i.personNo"
                },
                {
                    "value": "i.firstname"
                },
                {
                    "value": "i.lastname"
                },
                {
                    "value": "j.CodeDesc",
                    "name": "outlet_class"
                }
            ],
            "from": [
                {
                    "query": {
                        "select": [
                            {
                                "value": "Street"
                            },
                            {
                                "value": "City"
                            },
                            {
                                "value": "SalesOrg"
                            },
                            {
                                "value": {
                                    "trim": [
                                        "customerid",
                                        "0"
                                    ]
                                },
                                "name": "customerid"
                            },
                            {
                                "value": "CustomerName"
                            },
                            {
                                "value": "Longitude"
                            },
                            {
                                "value": "Latitude"
                            },
                            {
                                "value": "TradeChannel"
                            },
                            {
                                "value": "CustomerType"
                            },
                            {
                                "value": "repid"
                            },
                            {
                                "value": "classification"
                            }
                        ],
                        "from": {
                            "query": {
                                "select": [
                                    {
                                        "value": "*"
                                    },
                                    {
                                        "over": {
                                            "partitionby": "customerid",
                                            "orderby": {
                                                "value": {
                                                    "date": [
                                                        {
                                                            "cast": [
                                                                {
                                                                    "substr": [
                                                                        "changedatetime",
                                                                        1,
                                                                        4
                                                                    ]
                                                                },
                                                                "as",
                                                                "int64"
                                                            ]
                                                        },
                                                        {
                                                            "cast": [
                                                                {
                                                                    "substr": [
                                                                        "changedatetime",
                                                                        6,
                                                                        2
                                                                    ]
                                                                },
                                                                "as",
                                                                "int64"
                                                            ]
                                                        },
                                                        {
                                                            "cast": [
                                                                {
                                                                    "substr": [
                                                                        "changedatetime",
                                                                        9,
                                                                        2
                                                                    ]
                                                                },
                                                                "as",
                                                                "int64"
                                                            ]
                                                        }
                                                    ]
                                                },
                                                "sort": "desc"
                                            }
                                        },
                                        "name": "r_n"
                                    }
                                ],
                                "from": {
                                    "tablename": "indochina_tccc_prod.sapCustomer_BASE"
                                },
                                "where": {
                                    "and": [
                                        {
                                            "neq": [
                                                "customerid",
                                                {
                                                    "literal": "null"
                                                }
                                            ]
                                        },
                                        {
                                            "like": [
                                                "salesorg",
                                                {
                                                    "literal": "%MM%"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        },
                        "where": {
                            "eq": [
                                "r_n",
                                1
                            ]
                        }
                    },
                    "name": "a"
                },
                {
                    "left join": {
                        "query": {
                            "select": [
                                {
                                    "value": "SalesOrgDesc",
                                    "name": "CodeDesc"
                                },
                                {
                                    "value": "SalesOrg",
                                    "name": "CodeValue"
                                },
                                {
                                    "value": "CountryId",
                                    "name": "CTRY"
                                }
                            ],
                            "from": {
                                "tablename": "indochina_tccc_prod.sapSalesOrg_BASE"
                            },
                            "where": {
                                "exists": "DeleteFlag"
                            }
                        },
                        "name": "org"
                    },
                    "on": {
                        "eq": [
                            "a.SalesOrg",
                            "org.CodeValue"
                        ]
                    }
                },
                {
                    "left join": {
                        "query": {
                            "select": [
                                {
                                    "value": "CodeDesc"
                                },
                                {
                                    "value": "CodeValue"
                                },
                                {
                                    "value": "SalesOrg"
                                },
                                {
                                    "value": "CountryId"
                                }
                            ],
                            "from": {
                                "tablename": "indochina_tccc_prod.sapCodeDesc_BASE"
                            },
                            "where": {
                                "and": [
                                    {
                                        "eq": [
                                            {
                                                "upper": "CodeCategory"
                                            },
                                            {
                                                "literal": "TRADE_CHANNEL"
                                            }
                                        ]
                                    },
                                    {
                                        "exists": "DeleteFlag"
                                    }
                                ]
                            }
                        },
                        "name": "g"
                    },
                    "on": {
                        "and": [
                            {
                                "eq": [
                                    "a.TradeChannel",
                                    "g.CodeValue"
                                ]
                            },
                            {
                                "eq": [
                                    "a.SalesOrg",
                                    "g.SalesOrg"
                                ]
                            },
                            {
                                "eq": [
                                    "g.CountryId",
                                    "org.CTRY"
                                ]
                            }
                        ]
                    }
                },
                {
                    "left join": {
                        "query": {
                            "select": [
                                {
                                    "value": "CodeDesc"
                                },
                                {
                                    "value": "CodeValue"
                                },
                                {
                                    "value": "SalesOrg"
                                },
                                {
                                    "value": "CountryId"
                                }
                            ],
                            "from": {
                                "tablename": "indochina_tccc_prod.sapCodeDesc_BASE"
                            },
                            "where": {
                                "and": [
                                    {
                                        "eq": [
                                            {
                                                "upper": "CodeCategory"
                                            },
                                            {
                                                "literal": "CUSTOMER_TYPE"
                                            }
                                        ]
                                    },
                                    {
                                        "exists": "DeleteFlag"
                                    }
                                ]
                            }
                        },
                        "name": "h"
                    },
                    "on": {
                        "and": [
                            {
                                "eq": [
                                    "a.customertype",
                                    "h.CodeValue"
                                ]
                            },
                            {
                                "eq": [
                                    "a.SalesOrg",
                                    "h.SalesOrg"
                                ]
                            },
                            {
                                "eq": [
                                    "h.CountryId",
                                    "org.CTRY"
                                ]
                            }
                        ]
                    }
                },
                {
                    "left join": {
                        "query": {
                            "select": [
                                {
                                    "value": {
                                        "distinct": "personNo"
                                    }
                                },
                                {
                                    "value": "firstname"
                                },
                                {
                                    "value": "lastname"
                                }
                            ],
                            "from": {
                                "tablename": "indochina_tccc_prod.sapPerson_BASE"
                            },
                            "where": {
                                "and": [
                                    {
                                        "exists": "deleteflag"
                                    },
                                    {
                                        "neq": [
                                            "personNo",
                                            {
                                                "literal": "00000000"
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        "name": "i"
                    },
                    "on": {
                        "eq": [
                            "i.personNo",
                            "a.repid"
                        ]
                    }
                },
                {
                    "left join": {
                        "query": {
                            "select": [
                                {
                                    "value": "CodeDesc"
                                },
                                {
                                    "value": "CodeValue"
                                },
                                {
                                    "value": "SalesOrg"
                                },
                                {
                                    "value": "CountryId"
                                }
                            ],
                            "from": {
                                "tablename": "indochina_tccc_prod.sapCodeDesc_BASE"
                            },
                            "where": {
                                "eq": [
                                    {
                                        "upper": "CodeCategory"
                                    },
                                    {
                                        "literal": "CLASSIFICATION"
                                    }
                                ]
                            }
                        },
                        "name": "j"
                    },
                    "on": {
                        "and": [
                            {
                                "eq": [
                                    "a.Classification",
                                    "j.CodeValue"
                                ]
                            },
                            {
                                "eq": [
                                    "a.SalesOrg",
                                    "j.SalesOrg"
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
}'''

j = str(j).replace("'", "\"")
j = json.loads(j)

k = str(k).replace("'", "\"")
k = json.loads(k)

# def findcolumn(j):
#     for k,v in j.items():
#         if str(k)=='select':
#             if isinstance(v,list):
#                 column =[i['value'] for i in v if isinstance(i['value'],str)]
#                 column2 = [i['name'] for i in v if isinstance(i['value'],dict)]
#                 data = column+column2
#     return data


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

def findkeys(res):
    keys_list = ["left join", "tablename", "join", "cross join", "right join"]
    res_final = []
    for keys in keys_list:
        res_final.append(find_values(keys, res))
    res_final = [x for x in res_final if x]
    return res_final

def findkeyslist(res,tbl,col,value):
    res1= json.dumps(res,sort_keys=False)
    if value is None:
        search = col
    else:
        search = value
    colums= get_columns(res)
    for colum in colums:
        if search in colum:
            keys_list = ["left join", "tablename", "join", "cross join", "right join"]
            res_final = []
            for keys in keys_list:
                res_final.append(find_values(keys, res1))
            res_final = [x for x in res_final if x]
            res_fi={col:res_final}
    return res_fi





def get_columns(j):
    result =[]
    selct = j.get("select")
    for i in selct:
        if isinstance(i['value'], str):
            if "." in i['value']:
                tbl=str(i.get('value')).split(".")[0]
                col = str(i.get('value')).split(".")[1]
                if 'name' in [v for v in i.keys()]:
                    name = i.get('name')
                else:
                    name=None
            else:
                col = i['value']
                name = None
                tbl = None
        result.append([tbl,col,name])
    return result


def check_column(col,l):
    for i in l:
        if col in i:
            return i


# print(get_columns(k))

def findtablenames(res_final):
    final = []
    for keys in res_final:
        if isinstance(keys, list):
            for key in keys:
                # print(type(key))
                if isinstance(key, str):
                    final.append(key)
                    # print("tables : {0}".format(key))
                elif isinstance(key, dict):
                    key = json.dumps(key)
                    temp = findkeys(key)
                    for i in temp:
                        print("table list : {0}".format(i))
                    final += i
    return final


# res_final = findkeys(j)
# final = findtablenames(res_final)
#
# tables_used = list(set(final))



def findcoltable(tbl,col,value,fro):
    re=[]
    if isinstance(fro,str):
        tblname=fro.get('tablename')
        re.append(tblname)
    if isinstance(fro, list):
        for f in fro:
            if isinstance(f, str):
                tblname = f.get('tablename')
                re.append(tblname)
            if isinstance(f,dict):
                r = findcoltable(tbl, col, value, f)
                re.append(r)
    if isinstance(fro, dict):
        query = fro.get('query')

        if query == None:
            keys_list = ["left join", "tablename", "join", "cross join", "right join"]
            for key in keys_list:

                query = fro.get(key)
                if query is not None:
                    query = fro.get('query')
                    break
        if value is None:
            search = col
        else:
            search = value
        colums = get_columns(query)
        for colum in colums:
            if search in colum:
                fr = query.get('from')
                re = findcoltable(colum[0],colum[2],colum[1],fr)
                return re






def findcolumn(j):
    j = str(j).replace("'", "\"")
    j = json.loads(j)
    result = []
    for k, v in j.items():
        if str(k) == 'select':
            colums=get_columns(j)
            for colm in colums:
                tbl=colm[0]
                col = colm[1]
                name = colm[2]
                fro = j.get('from')
                r = findcoltable(tbl,col,name,fro)
                result.append(r)


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
        # v = list(set(v))
        super_dict[k] = v

    return super_dict

#
data = findcolumn(j)
print(data)
