import boto3
import json
import fire
import sys

#python ecsServiceRestart.py restart --services="app app2" --cluster=test
class ecsServiceRestart(object):

    def __init__(self):

        self.client = boto3.client('ecs',region_name="us-east-1")


    def returnServiceTaskDefinition(self, service, cluster):
        """
        Return service attached task definition
        @INPUT: service cluster
        @OUTPUT: task-definition or False
        """
        try:
            response = self.client.describe_services(cluster=cluster,services=[service])
            return response['services'][0]['deployments'][0]['taskDefinition']
        except:
            return False

    def registerTaskDefinition(self, taskDefinitionDescription):
        """
        Registering cloned task definition
        @INPUT: taskDefinitionDescription
        @OUTPUT: cloned task definition
        """
        try:
            taskRoleArn = taskDefinitionDescription['taskDefinition']['taskRoleArn']
        except:
            taskRoleArn = ""
        try:
            executionRoleArn = taskDefinitionDescription['taskDefinition']['executionRoleArn']
        except:
            executionRoleArn = ""
        try:
            volumes = taskDefinitionDescription['taskDefinition']['volumes']
        except:
            volumes = []
        try:
            placementConstraints = taskDefinitionDescription['taskDefinition']['placementConstraints']
        except:
            placementConstraints = []
        try:
            requiresCompatibilities = taskDefinitionDescription['taskDefinition']['requiresCompatibilities']
        except:
            requiresCompatibilities = []
        try:
            cpu = taskDefinitionDescription['taskDefinition']['cpu']
        except:
            cpu = ""
        try:
            memory = taskDefinitionDescription['taskDefinition']['memory']
        except:
            memory = ""

        response = self.client.register_task_definition(
        family=taskDefinitionDescription['taskDefinition']['family'],
        networkMode=taskDefinitionDescription['taskDefinition']['networkMode'],
        taskRoleArn=taskRoleArn,
        executionRoleArn=executionRoleArn,
        containerDefinitions=taskDefinitionDescription['taskDefinition']['containerDefinitions'],
        volumes=volumes,
        placementConstraints=placementConstraints,
        requiresCompatibilities=requiresCompatibilities,
        cpu=cpu,
        memory=memory)
        return response

    def updateService(self, service, cluster, taskDefinitionArn):
        """
        Update service new task definition
        @INPUT: service cluster taskDefinitionArn
        @OUTPUT service desiredCount
        """
        response = self.client.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=taskDefinitionArn
        )
        return response['service']['desiredCount']

    def restart(self, services,cluster):
        services = services.split(' ')

        for service in services:
            print "Starting restart " + service + " " + cluster
            #current taskDefinition
            taskDefinition = self.returnServiceTaskDefinition(service, cluster)
            if taskDefinition == False:
                print "Service " + service + " does not exist."
                sys.exit(1)

            #Describe taskDefinition
            taskDefinitionDescription = self.client.describe_task_definition(taskDefinition=taskDefinition)
            #Clone last taskDefinition
            response = self.registerTaskDefinition(taskDefinitionDescription)

            #Update service with new cloned task difinition
            self.updateService(service, cluster,response['taskDefinition']['taskDefinitionArn'])

            #Wait for service be stable
            waiter = self.client.get_waiter('services_stable')
            waiter.wait(
              cluster=cluster,
              services=[service]
            )
            print "Finished restart " + service + " " + cluster

if __name__ == '__main__':
  fire.Fire(ecsServiceRestart)
