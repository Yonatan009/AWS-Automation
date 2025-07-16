# 🚀 AWS Infrastructure Automation using Terraform & Python

Automate AWS infrastructure deployment in minutes with a Python‑based workflow that renders Terraform code from **Jinja2** templates, provisions resources, and verifies them – all from one command‑line interaction.

---

## 🗺️ What This Project Does

| Layer            | Role in the project                                                                         |
|------------------|----------------------------------------------------------------------------------------------|
| **Python**       | *Orchestration* – collects user inputs, renders `main.tf` via Jinja2, and calls Terraform    |
| **Jinja2**       | *Templating* – turns variables into a ready‑to‑run Terraform configuration                   |
| **Terraform**    | *Provisioning* – creates an **Application Load Balancer**, **EC2** instances, Security Group |
| **AWS CLI/Boto3**| *(Optional)* validation helpers & ad‑hoc queries                                             |

The tool asks a few questions (AMI, instance type, ALB name, region) → builds `terraform_workspace/main.tf` → runs `terraform init/plan/apply` automatically → prints the ALB DNS + EC2 public IPs.

---

## 📂 Project Structure

### project/
├── main.py # Entry‑point: coordinates everything
├── user_input.py # Friendly CLI prompts & validation
├── jinja2_generator.py # Renders Terraform template
├── terraform_executor.py # Wraps 'terraform init/plan/apply/destroy'
├── templates/
│ └── terraform_template.j2 # Jinja2 file → becomes main.tf
├── terraform_workspace/ # Auto‑generated TF files + state live here
└── screenshots/ # Proof‑of‑life images (see below)
├── image1.png # ALB created (console)
├── image2.png # ALB DNS output
├── image3.png # EC2 instance list
└── image4.png # Successful TF apply
---

Screenshots

1️⃣ Load Balancer Created (AWS Console)Image: screenshots/load_balancers.png

2️⃣ Target Group Status (AWS Console)Image: screenshots/target_group.png

3️⃣ EC2 Instance Running (AWS Console)Image: screenshots/ec2_vm.png

4️⃣ Successful Terraform Apply (Terminal Output)Image: screenshots/terraform_apply.png

## 🛠️ Prerequisites

| Requirement | Notes |
|-------------|-------|
| **AWS account** with IAM permissions | EC2, ELB, VPC, IAM (standard personal “AdministratorAccess” works for testing). |
| **Existing networking**              | 1 VPC + **2 public subnets** (different AZs) + attached **Internet Gateway**. |
| **Local tools**                      | Python 3.x, Terraform ≥ 1.5, Git, AWS CLI. |

### Export AWS credentials (**one‑liner demo**)

```bash
export AWS_ACCESS_KEY_ID="AKIAEXAMPLE123"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-2"     # region must match your subnets


---

## 📸 Screenshots

| Screenshot               | Description                                  |
|--------------------------|----------------------------------------------|
| `screenshots/image1.png` | Load Balancer created in AWS Console         |
| `screenshots/image2.png` | ALB **DNS name** & health status             |
| `screenshots/image3.png` | EC2 instances running                        |
| `screenshots/image4.png` | Terminal output – successful `terraform apply` |

---

## 🛠️ Prerequisites

| Requirement | Notes |
|-------------|-------|
| **AWS account** with IAM permissions | EC2, ELB, VPC, IAM (standard personal “AdministratorAccess” works for testing). |
| **Existing networking**              | 1 VPC + **2 public subnets** (different AZs) + attached **Internet Gateway**. |
| **Local tools**                      | Python 3.x, Terraform ≥ 1.5, Git, AWS CLI. |

### Export AWS credentials (**one‑liner demo**)

```bash
export AWS_ACCESS_KEY_ID="AKIAEXAMPLE123"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-2"     # region must match your subnets

# 1. Clone
git clone https://github.com/<your‑user>/<your‑repo>.git
cd <your‑repo>

# 2. Install Python dependencies
pip install -r requirements.txt           # python-terraform, jinja2, boto3 (optional)

# 3. Launch the wizard
python project/main.py

✓ Renders templates/terraform_template.j2  → terraform_workspace/main.tf
✓ terraform init
✓ terraform plan
✓ terraform apply  (auto-approve)

ALB DNS  : my-alb-1234567890.us-east-2.elb.amazonaws.com
EC2 IP A : 18.117.42.101
EC2 IP B : 3.145.88.22

cd terraform_workspace
terraform destroy

| File                                 | Responsibility                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| **main.py**                          | Entry‑point. Imports helpers, orchestrates user flow and Terraform execution. |
| **user\_input.py**                   | Validates CLI prompts (AMI list, instance types, region whitelist, ALB name). |
| **jinja2\_generator.py**             | Opens `templates/terraform_template.j2`, injects variables, writes `main.tf`. |
| **terraform\_executor.py**           | Shell‑wraps Terraform commands, captures output, handles errors.              |
| **templates/terraform\_template.j2** | Parameterised Terraform config (provider, data sources, resources).           |
| **terraform\_workspace/**            | Generated directory: `main.tf`, `.terraform/`, `terraform.tfstate` etc.       |
| **screenshots/**                     | Optional images for README / demo.                                            |

| Symptom                                       | Fix                                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------------------ |
| `Failed to query available provider packages` | Check internet / proxy; run `terraform init` after setting `https_proxy` if needed.  |
| `InvalidGroup.Duplicate` security‑group       | Change SG `name` or use `name_prefix`.                                               |
| Internet‑gateway limit error                  | Your VPC already has an IGW – use `data "aws_internet_gateway"` instead of resource. |
| Stuck at `aws_lb.* Still creating…`           | Ensure subnets are *public* (route table → 0.0.0.0/0 → IGW).                         |
| No default VPC error on EC2                   | Supply `vpc_security_group_ids`, not `security_groups` by name.                      |

| Resource | Pricing highlights                                                   |
| -------- | -------------------------------------------------------------------- |
| **ALB**  | Charged per hour **and** per LCU; starts billing once `active`.      |
| **EC2**  | Billed per second (minimum 60 s) for Linux on modern instance types. |
| **EBS**  | Root‑volume storage persists (charged) until instance is terminated. |
