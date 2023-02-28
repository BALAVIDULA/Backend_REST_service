import json
import psycopg2
from flask import Flask,request

API = Flask(__name__)

import http.server


#CASE1

@API.route("/api/search")
def case1():
    conn = psycopg2.connect(database="postgres", user='postgres', password='1234', host='127.0.0.1', port= '5432')

    conn.autocommit = True
    cursor = conn.cursor()

    Request_URL = 'SELECT ifsc,bank_id,branch,address,city,district,state from my_db WHERE ((ifsc like %s) or (branch like %s) or (address like %s) or (city like %s) or (district like %s) or (state like %s) or (bank_name like %s)) order by ifsc limit %s offset %s'
    Declaration=['%'+request.args.get("q").upper()+'%','%'+request.args.get("q").upper()+'%','%'+request.args.get("q").upper()+'%','%'+request.args.get("q").upper()+'%','%'+request.args.get("q").upper()+'%','%'+request.args.get("q").upper()+'%','%'+request.args.get("q").upper()+'%',int(request.args.get("limit")),int(request.args.get("offset"))]
    
    #Retrieving data
    cursor.execute(Request_URL,Declaration)
    fetched = cursor.fetchall()

    conn.commit()
    conn.close()

    print("Total rows are:  ", len(fetched))
    print("Printing each row")
    
    # Create the dictionary
    JSON_OBJECTS = []
    for i in fetched:
        branch1 = {
            'ifsc': i[0],
            'bank_id': i[1],
            'branch': i[2],
            'address': i[3],
            'city': i[4],
            'district': i[5],
            'state': i[6]
        }
        JSON_OBJECTS.append(branch1)

    JSON = {'branches': JSON_OBJECTS}
    result = json.dumps(JSON)

    return result




#CASE2

@API.route("/api/branch")
def case2():
   
    conn = psycopg2.connect(database="postgres", user='postgres', password='1234', host='127.0.0.1', port= '5432')

    conn.autocommit = True
    cursor = conn.cursor()

    Request_URL='SELECT ifsc,bank_id,branch,address,city,district,state from my_db WHERE (branch LIKE %s) ORDER BY ifsc desc LIMIT %s OFFSET %s'
    Declaration=[request.args.get("q"), int(request.args.get("limit")), int(request.args.get("offset"))-1]

    #Retrieving data
    cursor.execute(Request_URL,Declaration)
    fetched = cursor.fetchall()

    conn.commit()
    conn.close()

    print("Total rows are:  ", len(fetched))
    print("Printing each row")

    JSON_OBJECTS = []
    for i in fetched:
        branch = {
            'ifsc': i[0],
            'bank_id': i[1],
            'branch': i[2],
            'address': i[3],
            'city': i[4],
            'district': i[5],
            'state': i[6]
        }
        JSON_OBJECTS.append(branch)

    JSON = {'branches': JSON_OBJECTS}
    result = json.dumps(JSON)
    
    return result
