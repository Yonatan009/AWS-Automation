from user_input import collect_user_inputs
from jinja2_generator import generate_terraform_file
from terraform_executor import TerraformExecutor

# Step 1: Collect user input
inputs = collect_user_inputs()

ami_options = {
    "ubuntu": "ami-0d1b5a8c13042c939",
    "amazon-linux": "ami-0eb9d6fc9fab44d24",
}

variables = {
    "region": inputs["region"],
    "ami": ami_options.get(inputs["ami_choice"], "ami-xxxxxxxx"),
    "instance_type": inputs["instance_type"],
    "load_balancer_name": inputs["load_balancer_name"],
}

# Step 2: Generate main.tf
generate_terraform_file(
    variables,
    template_path="/Users/yonatanabutbul/PycharmProjects/Terraform_Project/templates/terraform_template.j2",
    output_file="terraform_workspace/main.tf",
)

# Step 3: Deploy infrastructure
executor = TerraformExecutor()
if not executor.run_terraform_init():
    print("Terraform init failed. Exiting.")
    exit(1)
if not executor.run_terraform_plan():
    print("Terraform plan failed. Exiting.")
    exit(1)
if not executor.run_terraform_apply():
    print("Terraform apply failed. Exiting.")
    exit(1)
