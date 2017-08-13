from ecsServiceRestart import *
import pytest
import boto3
from moto import mock_ecs
#export PYTHONDONTWRITEBYTECODE=1
#pytest test_ecsServiceRestart.py

@mock_ecs
def test_returnServiceTaskDefinition():
    client = boto3.client('ecs', region_name='us-east-1')
    _ = client.create_cluster(
        clusterName='test_ecs_cluster'
    )
    _ = client.register_task_definition(
        family='test_ecs_task',
        containerDefinitions=[
            {
                'name': 'hello_world',
                'image': 'docker/hello-world:latest',
                'cpu': 1024,
                'memory': 400,
                'essential': True,
                'environment': [{
                    'name': 'AWS_ACCESS_KEY_ID',
                    'value': 'SOME_ACCESS_KEY'
                }],
                'logConfiguration': {'logDriver': 'json-file'}
            }
        ]
    )
    _ = client.create_service(
        cluster='test_ecs_cluster',
        serviceName='test_ecs_service1',
        taskDefinition='test_ecs_task',
        desiredCount=2
    )
    ecs = ecsServiceRestart()
    response = ecs.returnServiceTaskDefinition("test_ecs_service1", "test_ecs_cluster")
    assert response == "arn:aws:ecs:us-east-1:012345678910:task-definition/test_ecs_task:1"
    response = ecs.returnServiceTaskDefinition("test_ecs_noneExist", "test_ecs_cluster")
    assert response == False


@mock_ecs
def test_registerTaskDefinition():
    client = boto3.client('ecs', region_name='us-east-1')

    ecs = ecsServiceRestart()
    taskDefinitionDescription = {}
    taskDefinitionDescription['taskDefinition'] = {}
    taskDefinitionDescription['taskDefinition']['family'] = "test_ecs_task"
    taskDefinitionDescription['taskDefinition']['networkMode'] = "host"
    taskDefinitionDescription['taskDefinition']['taskRoleArn'] = "arn"
    taskDefinitionDescription['taskDefinition']['containerDefinitions'] = []
    response = ecs.registerTaskDefinition(taskDefinitionDescription)
    assert response['taskDefinition']['taskDefinitionArn'] == "arn:aws:ecs:us-east-1:012345678910:task-definition/test_ecs_task:1"
    assert response['taskDefinition']['family'] == "test_ecs_task"

@mock_ecs
def test_updateService():
    client = boto3.client('ecs', region_name='us-east-1')
    _ = client.create_cluster(
        clusterName='test_ecs_cluster'
    )
    _ = client.register_task_definition(
        family='test_ecs_task',
        containerDefinitions=[
            {
                'name': 'hello_world',
                'image': 'docker/hello-world:latest',
                'cpu': 1024,
                'memory': 400,
                'essential': True,
                'environment': [{
                    'name': 'AWS_ACCESS_KEY_ID',
                    'value': 'SOME_ACCESS_KEY'
                }],
                'logConfiguration': {'logDriver': 'json-file'}
            }
        ]
    )
    response = client.create_service(
        cluster='test_ecs_cluster',
        serviceName='test_ecs_service',
        taskDefinition='test_ecs_task',
        desiredCount=2
    )
    ecs = ecsServiceRestart()
    response = ecs.updateService("test_ecs_service", "test_ecs_cluster", "arn:aws:ecs:us-east-1:012345678910:task-definition/test_ecs_task:1")
    assert response == 2
