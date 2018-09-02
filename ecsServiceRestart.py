import boto3
import json
import fire
import sys
import os

#python ecsServiceRestart.py restart --services="app app2" --cluster=test
class ecsServiceRestart(object):

    def __init__(self):
        try:
            self.client = boto3.client('ecs',region_name=os.environ['AWS_DEFAULT_REGION'])
        except Exception as e:
            print e
            sys.exit(1)

    def updateService(self, service, cluster):
        """
        Restart service
        @INPUT: service cluster
        @OUTPUT boolean
        """
        try:
            response = self.client.update_service(
            cluster=cluster,
            service=service,
            forceNewDeployment=True
            )
        except Exception as e:
            print e
            return False
        return True

    def restart(self, services,cluster):
        services = services.split(' ')

        for service in services:
            print "Starting restart " + service + " " + cluster
            #Force new deployment
            if(self.updateService(service, cluster) == False):
                sys.exit(1)
            #Wait for service be stable
            try:
                waiter = self.client.get_waiter('services_stable')
                waiter.wait(
                  cluster=cluster,
                  services=[service]
                )
            except:
                print "Failed restart service after 40 checks."
                sys.exit(1)
            print "Finished restart " + service + " " + cluster

if __name__ == '__main__':
  fire.Fire(ecsServiceRestart)
