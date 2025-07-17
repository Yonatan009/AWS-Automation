# AWS Infrastructure Automation using Terraform & Python

## Project Overview

This project automates AWS infrastructure deployment using:

* **Python** to collect user inputs and generate Terraform configuration using Jinja2 templates.
* **Terraform** to provision:

  * Application Load Balancer (ALB)
  * EC2 Instance
  * Based on existing VPC and Subnets

The system dynamically creates the `main.tf` file and runs Terraform commands automatically (init, plan, apply).

---

## Screenshots

**1️⃣ Load Balancer Created (AWS Console)**
Image: `screenshots/load_balancers.png`

**2️⃣ Target Group Status (AWS Console)**
Image: `screenshots/target_group.png`

**3️⃣ EC2 Instance Running (AWS Console)**
Image: `screenshots/ec2_vm.png`

**4️⃣ Successful Terraform Apply (Terminal Output)**
Image: `screenshots/terraform_apply.png`

---

## Project Structure

```plaintext
project/
├── main.py
├── user_input.py
├── jinja2_generator.py
├── terraform_executor.py
├── terraform_workspace/   # created automatically
├── templates/
│   └── terraform_template.j2
└── screenshots/
    ├── load_balancers.png
    ├── target_group.png
    ├── ec2_vm.png
    └── terraform_apply.png
```

| File                                 | Responsibility                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| **main.py**                          | Entry‑point. Imports helpers, orchestrates user flow and Terraform execution. |
| **user\_input.py**                   | Validates CLI prompts (AMI list, instance types, region whitelist, ALB name). |
| **jinja2\_generator.py**             | Opens `templates/terraform_template.j2`, injects variables, writes `main.tf`. |
| **terraform\_executor.py**           | Shell‑wraps Terraform commands, captures output, handles errors.              |
| **templates/terraform\_template.j2** | Parameterised Terraform config (provider, data sources, resources).           |
| **terraform\_workspace/**            | Generated directory: `main.tf`, `.terraform/`, `terraform.tfstate` etc.       |
| **screenshots/**                     | Optional images for README / demo.                                            |

---

## Setup & Usage Guide

### Prerequisites

* AWS account with IAM permissions (EC2, ELB, VPC, IAM)
* Existing VPC ID
* 2 Public Subnets (in different AZs)
* Internet Gateway attached to VPC
* Python 3.x installed
* Terraform ≥ 1.5 installed
* AWS CLI installed

### Export AWS credentials (Example)

```bash
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="us-east-2"
```

### Installation

```bash
pip install python-terraform jinja2
```

### Deployment Steps

1. Prepare AWS manually (VPC, Subnets, IGW).
2. Run the project:

```bash
python project/main.py
```

3. Provide:

   * AMI choice (ubuntu / amazon-linux)
   * Instance type (t2.micro)
   * AWS region (only us-east-2 supported)
   * Load Balancer name (optional, from env var)

4. The script will:

   * Generate `main.tf`
   * Run Terraform init, plan, and apply
   * Display ALB DNS and EC2 Public IP

5. Validate resources via AWS Console.

6. Destroy resources to avoid charges:

```bash
cd terraform_workspace
tf destroy
```

---

## Troubleshooting

| Symptom                                       | Fix                                                                                 |
| --------------------------------------------- | ----------------------------------------------------------------------------------- |
| `Failed to query available provider packages` | Check internet / proxy; run `terraform init` after setting `https_proxy` if needed. |
| `InvalidGroup.Duplicate` security‑group       | Change SG `name` or use `name_prefix`.                                              |
| Internet‑gateway limit error                  | Use `data "aws_internet_gateway"` for existing IGW.                                 |
| Stuck at `aws_lb.* Still creating…`           | Ensure subnets are *public* (route table → 0.0.0.0/0 → IGW).                        |
| No default VPC error on EC2                   | Use `vpc_security_group_ids`, not `security_groups` by name.                        |

---

## AWS Pricing Notes

| Resource | Pricing highlights                                                   |
| -------- | -------------------------------------------------------------------- |
| **ALB**  | Charged per hour **and** per LCU; starts billing once `active`.      |
| **EC2**  | Billed per second (minimum 60 s) for Linux on modern instance types. |
| **EBS**  | Root‑volume storage persists (charged) until instance is terminated. |

---

## Important Notes

* Always clean up resources after testing to avoid unexpected costs.
* ALB billing starts as soon as it becomes active.

---
