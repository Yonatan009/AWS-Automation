import json

import boto3
from botocore.exceptions import ClientError


class AwsValidator:

    def __init__(self, region='us-east-2'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.elbv2 = boto3.client('elbv2', region=region)

    def retrieve_ec2_instance_info(self, instance_id):
        try:
            response = self.ec2.describe_instances(InstanceIds=[instance_id])

            if not response['Reservations']:
                print(f" Instance {instance_id} not found")
                return None
            instance = response['Reservations'][0]['Instances'][0]
            return {
                'instance_id': instance_id,
                'instance_state': instance['State']['Name'],
                'public_ip': instance.get('PublicIpAddress', 'N/A')
            }

        except ClientError as e:
            print(f" Error getting instance: {e}")
            return None

    def get_load_balancer(self, lb_name):
        try:
            response = self.elbv2.describe_load_balancers(Names=[lb_name])
            if not response['LoadBalancers']:
                print(f" Load Balancer {lb_name} not found")
                return None

            lb = response['LoadBalancers'][0]
            return {
                'load_balancer_dns': lb['DNSName'],
                'state': lb['State']['Code']
            }

        except ClientError as e:
            print(f" Error getting load balancer: {e}")
            return None

    def validate_resources(self, instance_id, lb_name):
        print(" Starting validation...")

        # Get EC2 instance
        ec2_data = self.retrieve_ec2_instance_info(instance_id)
        if not ec2_data:
            return None

        # Check if instance is running
        if ec2_data['instance_state'] != 'running':
            print(f" Instance is {ec2_data['instance_state']}, not running")
        else:
            print(f" Instance {instance_id} is running")

        # Get Load Balancer
        lb_data = self.get_load_balancer(lb_name)
        if not lb_data:
            return None

        # Check if ALB is active
        if lb_data['state'] != 'active':
            print(f"Load Balancer is {lb_data['state']}, not active")
        else:
            print(f" Load Balancer {lb_name} is active")

        # Combine results
        validation_results = {
            'instance_id': ec2_data['instance_id'],
            'instance_state': ec2_data['instance_state'],
            'public_ip': ec2_data['public_ip'],
            'load_balancer_dns': lb_data['load_balancer_dns']
        }
        return validation_results

    def save_to_json(self, data, filename='aws_validation.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f" Results saved to {filename}")
            return True
        except Exception as e:
            print(f" Error saving file: {e}")
            return False
