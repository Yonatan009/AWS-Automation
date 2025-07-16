import json
import os.path
from python_terraform import Terraform


class TerraformExecutor:
    def __init__(self, working_dir="terraform_workspace"):
        self.working_dir = working_dir
        self.tf = Terraform(working_dir=working_dir)
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
            print(f"created dir {working_dir}")

    def create_terraform_file(self, terraform_content, filename="main.tf"):
        try:
            file_path = os.path.join(self.working_dir, filename)
            with open(file_path, mode="w") as file:
                file.write(terraform_content)
            return True
        except Exception as e:
            print(f"Error with write the {terraform_content} error log: {e}")
            return False

    def run_terraform_init(self):
        print("Start init to main.tf....")
        try:
            return_code, stdout, stderr = self.tf.init()
            print(stdout)
            if return_code != 0:
                print(f"Terraform init failed {stderr}")
                return False
            print("Terraform init successes")
            return True
        except Exception as e:
            print(f"Terraform init failed : {e}")
            return False

    def run_terraform_plan(self):
        print("Running terraform plan ...")
        try:
            return_code, stdout, stderr = self.tf.plan()
            print(stdout)
            if return_code not in [0, 2]:
                print(f"Terraform plan failed:\n{stderr}")
                return False
            print("Terraform plan succeeded.")
            return True

        except Exception as e:
            print(f"Error running terraform plan: {e}")
            return False

    def run_terraform_apply(self):
        print("Start apply to main.tf....")
        try:
            return_code, stdout, stderr = self.tf.apply(
                skip_plan=True, auto_approve=True
            )
            print(stdout)
            if return_code != 0:
                print(f"Terraform apply failed: {stderr}")
                return False
            print("Terraform apply succeeded!")
            return True
        except Exception as e:
            print(f"Terraform apply execution error: {e}")
            return False

    def get_terraform_outputs(self):
        print("Retrieving terraform outputs...")
        try:
            return_code, stdout, stderr = self.tf.output()

            if return_code != 0:
                print("Error retrieving outputs:")
                print(stderr)
                return None

            outputs = json.loads(stdout)

            print("Terraform Outputs:")
            for key, value in outputs.items():
                print(f"{key}: {value['value']}")

            return outputs

        except Exception as e:
            print(f"Error retrieving terraform outputs: {e}")
            return None

    def deploy_infrastructure(self, terraform_content):
        print("Starting infrastructure deployment...")

        if not self.create_terraform_file(terraform_content):
            return None

        if not self.run_terraform_init():
            return None

        if not self.run_terraform_plan():
            return None

        if not self.run_terraform_apply():
            return None

        outputs = self.get_terraform_outputs()
        if outputs is None:
            return None
        print("Infrastructure deployment completed successfully!")
        return outputs
