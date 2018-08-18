# import sqlparse
# from sqlparse import sql
# import sys
#
# sql1 = '''SELECT Street, City, SalesOrg, customerid, CustomerName, Longitude, Latitude, TradeChannel, CustomerType, repid, classification, SalesOrg_, TradeChannel_, CustomerType_, personNo, firstname, lastname, outlet_class FROM ( SELECT a.*, org.CodeDesc AS SalesOrg_, g.CodeDesc AS TradeChannel_, h.CodeDesc AS CustomerType_, i.personNo, i.firstname, i.lastname, j.CodeDesc AS outlet_class FROM ( SELECT Street, City, SalesOrg, trim(customerid,"0") as customerid, CustomerName, Longitude, Latitude, TradeChannel, CustomerType, repid, classification FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime,1,4) AS int64),CAST(SUBSTR(changedatetime,6,2) AS int64),CAST(SUBSTR(changedatetime,9,2) AS int64)) DESC) AS r_n FROM `indochina_tccc_prod.sapCustomer_BASE` WHERE customerid !='null' AND salesorg LIKE '%MM%') WHERE r_n=1) AS a LEFT JOIN ( SELECT SalesOrgDesc AS CodeDesc, SalesOrg AS CodeValue, CountryId AS CTRY FROM indochina_tccc_prod.sapSalesOrg_BASE WHERE DeleteFlag IS FALSE) AS org ON a.SalesOrg = org.CodeValue LEFT JOIN ( SELECT CodeDesc, CodeValue, SalesOrg, CountryId FROM indochina_tccc_prod.sapCodeDesc_BASE WHERE UPPER(CodeCategory) ='TRADE_CHANNEL' AND DeleteFlag IS FALSE) AS g ON a.TradeChannel = g.CodeValue AND a.SalesOrg= g.SalesOrg AND g.CountryId = org.CTRY LEFT JOIN ( SELECT CodeDesc, CodeValue, SalesOrg, CountryId FROM indochina_tccc_prod.sapCodeDesc_BASE WHERE UPPER(CodeCategory) ='CUSTOMER_TYPE' AND DeleteFlag IS FALSE) AS h ON a.customertype = h.CodeValue AND a.SalesOrg= h.SalesOrg AND h.CountryId = org.CTRY LEFT JOIN ( SELECT DISTINCT personNo, firstname, lastname FROM `indochina_tccc_prod.sapPerson_BASE` WHERE deleteflag IS FALSE AND personNo != '00000000') AS i ON i.personNo = a.repid LEFT JOIN ( SELECT CodeDesc, CodeValue, SalesOrg, CountryId FROM indochina_tccc_prod.sapCodeDesc_BASE WHERE UPPER(CodeCategory) ='CLASSIFICATION' ) AS j ON a.Classification = j.CodeValue AND a.SalesOrg= j.SalesOrg)'''
#
# # parsed = sqlparse.parse(sql1)
# # print (parsed[0].tokens)
# sys.setrecursionlimit(7500)
#
# result = []
# # print (sqlparse.format(sql1))
# # parsed = sqlparse.parse(sql1)
# # stmt = parsed[0].
# #
# # print (stmt)
#
#
# def parsing(s):
#     parsed = sqlparse.parse(s)
#     # print ("Parsed >>>>>>>>>>" + str(parsed[0].tokens))
#     for i in parsed[0].tokens:
#         if isinstance(i, sqlparse.sql.Parenthesis):
#             sq = str(i).strip("()")
#             parsing(sq)
#         elif isinstance(i, sqlparse.sql.Identifier) and 'SELECT' in str(i):
#             sq = str(i).strip("()")
#             parsing(sq)
#         else:
#             if i.is_whitespace:
#                 pass
#             else:
#                  result.append(i)
#
#
# parsing(sql1)
# print(result)
#
#
# dic={}
# for i in range(len(result)):
#     fro={}
#     sel={}
#     if result[i].value == 'SELECT':
#         sel={
#             'select':result[i+1].value
#         }
#     if result[i].value == 'FROM':
#         fro={
#             'from':result[i+1].value
#         }
#     try:
#         dic=sel.update(fro)
#         sel={}
#         fro={}
#     except Exception as e:
#         print(e)
#         pass
#
#
# print(dic)









































import json
from networkx import json_graph


j='''{
    "select": [
        {
            "value": "total_volume"
        },
        {
            "value": "user_id"
        },
        {
            "value": "YEAR"
        },
        {
            "value": "MONTH"
        },
        {
            "value": "period_date"
        },
        {
            "value": "cur_date"
        }
    ],
    "from": {
        "query": {
            "select": [
                {
                    "value": {
                        "distinct": {
                            "cast": [
                                "user_id",
                                "as",
                                "int64"
                            ]
                        }
                    },
                    "name": "user_id"
                },
                {
                    "value": {
                        "sum": {
                            "cast": [
                                "QUANTITY_CONFIRMED",
                                "as",
                                "float64"
                            ]
                        }
                    },
                    "name": "total_volume"
                },
                {
                    "value": "YEAR"
                },
                {
                    "value": "MONTH"
                },
                {
                    "value": {
                        "date_sub": [
                            {
                                "current_date": {}
                            },
                            "INTERVAL",
                            1,
                            "DAY"
                        ]
                    },
                    "name": "period_date"
                },
                {
                    "value": {
                        "current_date": {}
                    },
                    "name": "cur_date"
                }
            ],
            "from": {
                "tablename": "indochina_tccc_test.BI_SALES_DETAIL"
            },
            "where": {
                "and": [
                    {
                        "between": [
                            {
                                "cast": [
                                    {
                                        "substr": [
                                            "CONFIRMED_DATE",
                                            1,
                                            10
                                        ]
                                    },
                                    "as",
                                    "DATE"
                                ]
                            },
                            {
                                "select": {
                                    "value": "Start_Date"
                                },
                                "from": {
                                    "tablename": "indochina_tccc_prod.COKE_CALENDAR"
                                },
                                "where": {
                                    "and": [
                                        {
                                            "eq": [
                                                "YEAR",
                                                {
                                                    "select": {
                                                        "value": "YEAR",
                                                        "name": "mn"
                                                    },
                                                    "from": {
                                                        "tablename": "indochina_tccc_prod.COKE_CALENDAR"
                                                    },
                                                    "where": {
                                                        "between": [
                                                            {
                                                                "date_sub": [
                                                                    {
                                                                        "current_date": {
                                                                            "literal": "Asia/Saigon"
                                                                        }
                                                                    },
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            },
                                                            "start_date",
                                                            {
                                                                "date_sub": [
                                                                    "end_date",
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    "limit": 1
                                                }
                                            ]
                                        },
                                        {
                                            "eq": [
                                                "MONTH",
                                                {
                                                    "select": {
                                                        "value": "MONTH",
                                                        "name": "mn"
                                                    },
                                                    "from": {
                                                        "tablename": "indochina_tccc_prod.COKE_CALENDAR"
                                                    },
                                                    "where": {
                                                        "between": [
                                                            {
                                                                "date_sub": [
                                                                    {
                                                                        "current_date": {
                                                                            "literal": "Asia/Saigon"
                                                                        }
                                                                    },
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            },
                                                            "start_date",
                                                            {
                                                                "date_sub": [
                                                                    "end_date",
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    "limit": 1
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "orderby": {
                                    "value": "week_num"
                                },
                                "limit": 1
                            },
                            {
                                "date_sub": [
                                    {
                                        "current_date": {
                                            "literal": "Asia/Saigon"
                                        }
                                    },
                                    "INTERVAL",
                                    1,
                                    "DAY"
                                ]
                            }
                        ]
                    },
                    {
                        "eq": [
                            {
                                "upper": {
                                    "trim": "country"
                                }
                            },
                            {
                                "literal": "VIETNAM"
                            }
                        ]
                    },
                    {
                        "eq": [
                            "MONTH",
                            {
                                "select": {
                                    "value": "month_num"
                                },
                                "from": {
                                    "tablename": "indochina_tccc_prod.COKE_CALENDAR"
                                },
                                "where": {
                                    "and": [
                                        {
                                            "eq": [
                                                "YEAR",
                                                {
                                                    "select": {
                                                        "value": "YEAR",
                                                        "name": "mn"
                                                    },
                                                    "from": {
                                                        "tablename": "indochina_tccc_prod.COKE_CALENDAR"
                                                    },
                                                    "where": {
                                                        "between": [
                                                            {
                                                                "date_sub": [
                                                                    {
                                                                        "current_date": {
                                                                            "literal": "Asia/Saigon"
                                                                        }
                                                                    },
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            },
                                                            "start_date",
                                                            {
                                                                "date_sub": [
                                                                    "end_date",
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    "limit": 1
                                                }
                                            ]
                                        },
                                        {
                                            "eq": [
                                                "MONTH",
                                                {
                                                    "select": {
                                                        "value": "MONTH",
                                                        "name": "mn"
                                                    },
                                                    "from": {
                                                        "tablename": "indochina_tccc_prod.COKE_CALENDAR"
                                                    },
                                                    "where": {
                                                        "between": [
                                                            {
                                                                "date_sub": [
                                                                    {
                                                                        "current_date": {
                                                                            "literal": "Asia/Saigon"
                                                                        }
                                                                    },
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            },
                                                            "start_date",
                                                            {
                                                                "date_sub": [
                                                                    "end_date",
                                                                    "INTERVAL",
                                                                    1,
                                                                    "DAY"
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    "limit": 1
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "orderby": {
                                    "value": "week_num"
                                },
                                "limit": 1
                            }
                        ]
                    }
                ]
            },
            "groupby": [
                {
                    "value": "user_id"
                },
                {
                    "value": "YEAR"
                },
                {
                    "value": "MONTH"
                },
                {
                    "value": "period_date"
                },
                {
                    "value": "CURRENT_DATE"
                }
            ]
        }
    }
}'''

def read_json_file(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

def read_json_f(f):
    print(type(f))
    j= json.dumps(f)
    print(type(j))
    js_graph = json.loads(j)
    print(type(json_graph))
    return json_graph.node_link_graph(js_graph)
#
d=read_json_f(j)





