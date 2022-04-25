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
    print(taskId)
    query1 = """
            match (t:Task{task_id:$taskId})-[r:happened]-(v:Visit)
            return distinct(v.engineer_skill_level) AS engineer_skill_level
            """
    print(query1)
    obj = {"taskId": taskId}
    try:
        results = session.run(query1, obj)
        resultsData = results.data()
        return jsonify(resultsData)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    api.run(debug=True)
