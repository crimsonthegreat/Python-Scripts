from jinja2 import Template

# Define a basic Jinja2 template
template = Template("hostname {{ name }}")

# Render the template with a variable
output = template.render(name="R1")

print(output)