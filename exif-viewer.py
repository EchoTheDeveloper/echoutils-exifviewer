import os, sys, subprocess, requests, json
from PIL import Image
from PIL.ExifTags import TAGS

VALID_COMMANDS = ["--output", "-o", "--printconsole", "-pc"]

input_file = None
output_location = None
print_to_console = False

url = "https://raw.githubusercontent.com/EchoTheDeveloper/echoutils-exifviewer/refs/heads/main/default-config.json"
default_config_location = os.path.expanduser("~/.config/echo-utils/exif-viewer/config.json")
os.makedirs(os.path.dirname(default_config_location), exist_ok=True)

if not os.path.exists(default_config_location):
    response = requests.get(url)
    if response.status_code == 200:
        with open(default_config_location, "wb") as f:
            f.write(response.content)
    else:
        print("Config file not found and failed to fetch default config over wifi")
        print(response.status_code)

with open(default_config_location, "r") as f:
    config = json.load(f)

config_editor = config["default-editor"]
default_exif_save = config["default-exif-out"]

i = 0
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == "config":
        subprocess.run([config_editor, default_config_location])
    elif arg in VALID_COMMANDS:
        if i + 1 < len(sys.argv):
            content = sys.argv[i + 1]
            if arg in ("--output", "-o"):
                output_location = content
            elif arg in ("--printconsole", "-pc"):
                print_to_console = content.lower() in ("true", "t")
            i += 1
    elif arg.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        input_file = arg
    i += 1

if not input_file:
    print("ERROR: NO IMAGE SUBMITTED")
    sys.exit()

if not output_location and not print_to_console:
    output_location = default_exif_save

image = Image.open(input_file)
exif_data = {TAGS.get(tag, tag): value for tag, value in image.getexif().items()}

if print_to_console:
    print(json.dumps(exif_data, indent=2))

if output_location:
    if os.path.exists(output_location):
        print("ERROR: OUTPUT FILE EXISTS")
        sys.exit()
    with open(output_location, "w") as f:
        json.dump(exif_data, f, indent=2)

