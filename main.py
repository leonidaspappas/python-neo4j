import csv

from flask import Flask, jsonify
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
    results = session.run(q1)
    resultsData = results.data()
    return jsonify(resultsData)


@api.route("/distinctEngineerLvl/taskId=<string:taskId>", methods=["GET"])
def create_node(taskId):
    checkQuery = """
            match (t:Task{task_id:$taskId})
            return t
            """
    query1 = """
            match (t:Task{task_id:$taskId})-[r:happened]-(v:Visit)
            return distinct(v.engineer_skill_level) AS engineer_skill_level
            """
    print(checkQuery)
    obj = {"taskId": taskId}
    try:
        checkRes = session.run(checkQuery, obj)
        if (len(checkRes.data())==0):
            return "Task id " + taskId + " does not exist in db", 404
        results = session.run(query1, obj)
        resultsData = results.data()
        return jsonify(resultsData), 200
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    api.run(debug=True)
