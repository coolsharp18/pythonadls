import os
import pandas as pd

from io import StringIO
from flask import Flask, request
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError


app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')

account_name = os.getenv("accountname")
credential = os.getenv("accountkey")
account_url = "https://{}.dfs.core.windows.net/".format(account_name)

@app.route('/')
def index():
    return 'Server Works!'


@app.route('/accountBalance')
def say_hello():

    datalake = DataLakeServiceClient(
        account_url=account_url, credential=credential)

    file_system = os.getenv("filesystem")
    filesystem_client = datalake.get_file_system_client(file_system)

    # try:
    #     filesystem_client = datalake.create_file_system(file_system=file_system)
    # except ResourceExistsError as e:
    #     filesystem_client = datalake.get_file_system_client(file_system)

    # dir_client = filesystem_client.get_directory_client("incoming")
    # dir_client.create_directory()
    #
    # data = """name,population
    # Berlin, 3406000
    # Munich, 1275000
    # """
    #
    # file_client = dir_client.create_file("cities.csv")
    # file_client.append_data(data, 0, len(data))
    # file_client.flush_data(len(data))

    file_client = filesystem_client.get_file_client('input/account.csv')
    text = file_client.read_file()
    s = str(text, 'utf-8')

    data = StringIO(s)

    df = pd.read_csv((data))

    jsondata = df.to_json(orient='records')

    print(jsondata)

    dir_client = filesystem_client.get_directory_client("outgoing")
    dir_client.create_directory()
    file_client = dir_client.create_file("cities.json")
    file_client.append_data(jsondata, 0, len(jsondata))
    file_client.flush_data(len(jsondata))
    return jsondata

