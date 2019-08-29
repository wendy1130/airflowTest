import airflow
import requests
import json
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('submit_dlts_job', default_args=default_args, schedule_interval=timedelta(minutes=60))

def post_dlts_job():
	submit_url = "http://dltshub-aether.westus2.cloudapp.azure.com/api/dlws/postJob?cluster=Azure-EastUS-V100-LowPriority&Team=ads&Email=weouyan@microsoft.com&Key=871c0ee3"

	jobParams = {
		"cmd" : "sleep infinity",
		"dataPath" : "",
		"enabledatapath" : True,
		"enablejobpath" : True,
		"enableworkpath" : True,
		"env" : "[ ]",
		"gpuType" : "V100",
		"hostNetwork" : False,
		"image": "indexserveregistry.azurecr.io/zhrui/horizon",
		"is_interactive": True,
		"interactivePorts" : "[40001]",
		"ipython" : True,
		"isParent" : 1,
		"isPrivileged" : False,
		"jobName" : "TestAPISubmission",
		"jobType" : "training",
		"jobtrainingtype" : "RegularJob",
		"preemptionAllowed" : False,
		"resourcegpu": 0,
		"runningasroot": True,
		"ssh" : True,
		"tensorboard" : True,
		"userName" : "weouyan@microsoft.com",
		"vcName" : "ads",
		"workPath" : "weouyan"
	}
	payload = {}
	payload["Json"] = json.dumps(jobParams)

	r = requests.post(
		url=submit_url,
		data=payload
	)

t1 = PythonOperator(
    task_id='post_request',
    python_callable=post_dlts_job,
    dag=dag)



t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

t2.set_upstream(t1)
