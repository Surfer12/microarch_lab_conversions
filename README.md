import os

import subprocess

def generate_readme(path):
    """Generates a README.md file with information about the project."""

    # Extract project name from path
    project_name = os.path.basename(os.path.dirname(path))

    # Create README content
    readme_content = f"# {project_name}\n\n"
    readme_content += "This project contains...\n\n"
    readme_content += "## Getting Started\n\n"
    readme_content += "These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n"
    readme_content += "### Prerequisites\n\n"
    readme_content += "What you need to install the software:\n\n"
    readme_content += "```bash\n"
    readme_content += "# Example: Install Python\n"
    readme_content += "sudo apt-get update\n"
    readme_content += "sudo apt-get install python3\n"
    readme_content += "```\n\n"
    readme_content += "### Installing\n\n"
    readme_content += "A step by step series of examples that tell you have to get a development env running\n\n"
    readme_content += "```bash\n"
    readme_content += "# Example: Clone the repository\n"
    readme_content += "git clone https://github.com/<username>/<repository>.git\n"
    readme_content += "```\n\n"
    readme_content += "## Running the tests\n\n"
    readme_content += "Explain how to run the automated tests for this system\n\n"
    readme_content += "```bash\n"
    readme_content += "# Example: Run tests\n"
    readme_content += "pytest\n"
    readme_content += "```\n\n"
    readme_content += "## Built With\n\n"
    readme_content += "* Markdown\n"
    readme_content += "* Python\n\n"
    readme_content += "## Contributing\n\n"
    readme_content += "Contributions are welcome!\n\n"
    readme_content += "## License\n\n"
    readme_content += "This project is licensed under the MIT License - see the LICENSE.md file for details.\n\n"


    # Write README content to file
    with open(path, "w") as f:
        f.write(readme_content)

    # Print success message
    print(f"README.md generated successfully at {path}")

# Example usage
generate_readme("/Users/ryanoates/microarch_lab_conversions/README.md")
