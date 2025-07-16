from jinja2 import Template
import os


def generate_terraform_file(variables, template_path, output_file):
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    rendered_content = template.render(**variables)

    with open(output_file, "w") as output:
        output.write(rendered_content)

    print(f"✔️ Terraform file created successfully at: {output_file}")
