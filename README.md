README.md
{{ Explain: Enhance README.md generation to include project description, dependencies, usage instructions, and dynamic "Built With" section. }}
```language:README.md
import os
import toml  # for pyproject.toml
import re  # for parsing pixi.toml


def generate_readme(path):
    """Generates a detailed README.md file with project information."""

    # 1. Project Name
    project_name = os.path.basename(os.path.dirname(path))

    # 2. Project Description (from pyproject.toml)
    project_description = "A short description of your project. Update pyproject.toml!"  # Default
    try:
        with open("pyproject.toml", "r") as f:
            pyproject_data = toml.load(f)
            project_description = pyproject_data.get("project", {}).get("description", project_description)
    except FileNotFoundError:
        pass  # Use default description if pyproject.toml not found

    # 3. Dependencies (from pixi.toml)
    dependencies_list = ["- Add dependencies in pixi.toml"]  # Default
    try:
        with open("pixi.toml", "r") as f:
            pixi_content = f.read()
            dependencies_match = re.search(r"\[dependencies\](.*?)\[", pixi_content, re.DOTALL)
            if dependencies_match:
                dependencies_block = dependencies_match.group(1).strip()
                dependencies_list = [f"- `{dep.strip()}`" for dep in dependencies_block.strip().split("\n") if dep.strip()]
            else:
                dependencies_list = ["No dependencies listed in pixi.toml"]
    except FileNotFoundError:
        dependencies_list = ["pixi.toml not found, dependencies cannot be listed"]

    # 4. Scripts (from pyproject.toml)
    scripts_list = []
    try:
        with open("pyproject.toml", "r") as f:
            pyproject_data = toml.load(f)
            scripts = pyproject_data.get("project", {}).get("scripts", {})
            scripts_list = [f"- `{name} = {entry_point}`" for name, entry_point in scripts.items()]
    except FileNotFoundError:
        pass  # scripts section is optional

    # 5. Built With (Dynamic)
    built_with = ["Markdown"]  # README is markdown
    built_with.append("Python")  # Python project
    if os.path.exists("pixi.toml"):
        built_with.append("pixi")
    if os.path.exists("pyproject.toml"):
        built_with.append("setuptools")  # Implied by pyproject.toml and build-system

    # --- Construct README Content ---
    readme_content = f"# {project_name}\n\n"
    readme_content += f"{project_description}\n\n"  # Project description

    readme_content += "## Getting Started\n\n"
    readme_content += "These instructions will guide you on how to get the project up and running on your local machine for development and testing.\n\n"

    readme_content += "### Prerequisites\n\n"
    readme_content += "Before you begin, ensure you have the following installed:\n\n"
    readme_content += "```bash\n"
    readme_content += "# Example: Install pixi (package manager)\n"
    readme_content += "curl -fsSL https://pixi.sh/install.sh | sh\n"  # Example for pixi
    readme_content += "```\n\n"

    # Usage Instructions
    readme_content += "## Usage\n"
    readme_content += "```bash\n"
    readme_content += "learning-pathway-cli [command] [options]\n"
    readme_content += "```\n\n"

    # Available Scripts
    if scripts_list:
        readme_content += "## Available Scripts\n"
        readme_content += "\n".join(scripts_list) + "\n\n"

    # Dependencies
    if dependencies_list:
        readme_content += "## Dependencies\n"
        readme_content += "\n".join(dependencies_list) + "\n\n"

    readme_content += "### Installing\n\n"
    readme_content += "A step-by-step guide to setting up your development environment.\n\n"
    readme_content += "```bash\n"
    readme_content += "# 1. Clone the repository\n"
    readme_content += f"git clone https://github.com/<username>/{project_name}.git\n"
    readme_content += f"cd {project_name}\n\n"
    readme_content += "# 2. Install dependencies using pixi\n"
    readme_content += "pixi install\n"
    readme_content += "```\n\n"

    readme_content += "## Running the tests\n\n"
    readme_content += "Explain how to run the automated tests for this system. Example using `unittest` or `pytest`.\n\n"
    readme_content += "```bash\n"
    readme_content += "# Example: Run tests with unittest\n"
    readme_content += "python -m unittest discover educational\n"  # Example for unittest
    readme_content += "```\n\n"

    # Built With
    if built_with:
        readme_content += "## Built With\n"
        readme_content += "\n".join([f"- {tool}" for tool in built_with]) + "\n\n"

    readme_content += "## Contributing\n\n"
    readme_content += "Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.\n\n"

    readme_content += "## License\n\n"
    readme_content += "This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.\n\n"

    # --- Write and Confirm ---
    with open(path, "w") as f:
        f.write(readme_content)

    print(f"README.md generated successfully at {path}")


# Example usage
generate_readme("/Users/ryanoates/microarch_lab_conversions/README.md")
