# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Example DAG demonstrating the usage of the BashOperator."""

from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator


args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

dag = DAG(
    dag_id='msan_testSSH',
    default_args=args,
    schedule_interval=timedelta(days=1),
    dagrun_timeout=timedelta(minutes=60),
)

sshHook = SSHHook(
    remote_host='dltseb764000007.redmond.corp.microsoft.com', 
    username='weouyan', 
    key_file='//dltseastusv100lowprioritystorage.redmond.corp.microsoft.com/weouyan/.ssh/id_rsa', 
    port=32523, 
    timeout=10, 
    keepalive_interval=30)


t1 = SSHOperator(
    task_id="connectionDLTS",
    bash_command='mkdir fromAirflow',
    ssh_hook=sshHook,
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

t1>>t2