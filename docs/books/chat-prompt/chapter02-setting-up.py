# Import necessary modules
import os
import venv

# Create a virtual environment
venv_dir = "./venv"
venv.create(venv_dir, with_pip=True)

# Activate the virtual environment
activate_script = os.path.join(venv_dir, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_dir, "bin", "activate")
activate_cmd = f"source {activate_script}"

# Print the activation command to the console (this is necessary because you cannot activate the virtual environment from within a Python script)
print(f"Virtual environment created. Activate it by entering the following command in your shell or command prompt: \n{activate_cmd}")

# Assuming that `requirements.txt` exists in the current directory...
pip_cmd = f"{os.path.join(venv_dir, 'bin', 'pip' if os.name != 'nt' else 'Scripts\\pip.exe')} install -r requirements.txt"
os.system(pip_cmd)  # Execute the pip command to install dependencies

# Now you can start your development!
