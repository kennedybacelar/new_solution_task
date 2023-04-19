import yaml

MANDATORY_KEYS = ["input_path", "output_path"]

def load_config() -> dict:
    with open('settings.yml', 'r') as file:
        settings = yaml.safe_load(file) or {}
    
    for key in MANDATORY_KEYS:
        if not key in settings:
            raise Exception(f"Setting.yml is missing mandatory keys: {key}")
    return settings