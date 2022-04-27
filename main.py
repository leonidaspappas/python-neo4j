import csv

from flask import Flask, jsonify, make_response
from neo4j import GraphDatabase

# establish connection
with open("creds/cred.txt") as f1:
    data = csv.reader(f1, delimiter=",")
    for row in data:
        username = row[0]
        pwd = row[1]
        uri = row[2]
driver = GraphDatabase.driver(uri=uri, auth=(username, pwd))
session = driver.session()
api = Flask(__name__)


@api.route("/uncompletedTasks", methods=["GET"])
def display_node():
    q1 = """
    Match(t:Task)
    where t.outcome = "FAIL"
    RETURN count(t) as count    
    """
    results = execute_query(q1)

    return create_response(results, 200)


@api.route("/distinctEngineerLvl/taskId=<string:taskId>", methods=["GET"])
def disting_engineer_lvl(taskId):
    checkQuery = """
            match (t:Task{task_id:$taskId})
            return t
            """
    query1 = """
            match (t:Task{task_id:$taskId})-[r:happened]-(v:Visit)
            return distinct(v.engineer_skill_level) AS engineer_skill_level
            """
    obj = {"taskId": taskId}
    checkRes = execute_query(checkQuery, obj)

    if len(checkRes) == 0:
        return create_response("Task id " + taskId + " does not exist in db", 404)
    results = execute_query(query1, obj)
    return create_response(results, 200)


def create_response(data, code):
    if code == 200:
        return make_response(jsonify({"result": data, "code": code}), 200, )
    else:
        return make_response(jsonify({"errorMessage": data, "code": code}), code, )


def execute_query(*args):
    try:
        if len(args) == 1:
            result = session.run(args[0])
        else:
            result = session.run(args[0], args[1])
        return result.data()
    except ValueError as e:
        return jsonify("error communicating with DB"), 400
    except Exception as e:
        return jsonify("general exception error"), 400
        return str(e)


if __name__ == "__main__":
    api.run(debug=True)
