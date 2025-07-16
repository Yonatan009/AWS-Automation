def collect_user_inputs():
    print("AWS Deployment Configuration ")

    ami_choice = input("Choose AMI (ubuntu / amazon-linux): ").strip().lower()
    if ami_choice not in ["ubuntu", "amazon-linux"]:
        print("Invalid AMI choice. Defaulting to Ubuntu.")
        ami_choice = "ubuntu"

    instance_type = (
        input("Choose instance type (t2.micro only for Free Tier): ").strip().lower()
    )
    if instance_type != "t2.micro":
        print("Invalid choice. Defaulting to t2.micro to stay Free Tier.")
        instance_type = "t2.micro"

    region = input("Choose AWS region (only us-east-2 allowed): ").strip().lower()
    if region != "us-east-2":
        print("Invalid region. Defaulting to us-east-2.")
        region = "us-east-2"

    alb_name = input("Enter name for Load Balancer: ").strip()

    return {
        "ami_choice": ami_choice,
        "instance_type": instance_type,
        "region": region,
        "load_balancer_name": alb_name,
    }
