
# SETUP

## Steps:

1. Install Python 3.10.9  (or 3.11.1)
2. Install Docker and Docker Compose
3. Install VS Code with Python Plugin + Pylance + Docker Plugin
4. In project folder run ``` python -m venv .venv ```
5. In project folder create settings file ``` .vscode/settings.json```
6. Import project into VS Code
7. Open the integrated terminal and execute: ``` python -m ./.venv/bin/pip install -r ./requirements.txt ```
8. Open the integrated terminal and execute: ``` docker-compose up ```

## settings.json example:
```
{
    "python.analysis.extraPaths": [
        "lib",
        "${workspaceFolder}"
    ],
    "python.envFile": "${workspaceFolder}/.env",
    "python.analysis.typeCheckingMode": "basic",
    "python.autoComplete.extraPaths": [
        "./lib"
    ],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": false,
    "python.linting.pycodestyleEnabled": false,
    "python.linting.pylintPath": ".venv/bin/pylint",
    "python.linting.pylintArgs": [
        "--disable=C0111"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "/Users/martinkutscher/projects/dhbw/docker_workshop/sensor_data_subscriber/tests",
        "-vv"
    ],
    "workbench.tree.indent": 20,
    "files.exclude": {
        "**/*.pyc": {
            "when": "$(basename).py"
        },
        "**/__pycache__": true,
        "**/.pytest_cache": true
    },
    "python.formatting.provider": "black"
}

```