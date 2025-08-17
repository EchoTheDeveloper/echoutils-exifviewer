import os, sys, subprocess
import requests, json
from PIL import Image
from PIL.ExifTags import TAGS

VALID_COMMANDS = ["--output", "-o", "--printconsole", "-pc"]

file = 404
output_location = None
print_to_console = False

url = "https://raw.githubusercontent.com/EchoTheDeveloper/echoutils-exifviewer/refs/heads/main/default-config.json"

default_config_location = "~/.config/echo-utils/exif-viewer/config.json"

if not os.path.exists(default_config_location):
    with open (default_config_location, "w") as f:
        response = requests.get(url)
        if response.status_code == 200:
            f.write(response.content)
        else:
            print("Config file not found and failed to fetch default config over wifi")
            print(response.status_code)

with open(default_config_location, "r") as f:
    config = json.load(f.read())

config_editor = config["default-editor"]

for i in range (0, len(sys.argv)):
    arg = sys.argv[i]
    if arg == "config":
        subprocess.run(f"{config_editor} {default_config_location")
    elif (arg.startswith("--") or arg.startswith("-")) and arg in VALID_COMMANDS:
        command = arg
        content = sys.argv[i+1]
        if arg == "--output" or arg == "-o":
            output_location = content
        elif arg == "--printconsole" or arg == "-pc":
            if content == "true" or content == "t":
                print_to_console = True
            elif content == "false" or content == "f":
                print_to_console = False
            else:
                print("Unrecognised argument for print to console flag, defaulting to False")

    elif arg.endswith((".png", ".jpg", ".jpeg", ".webp")) or arg.endswith("\""):
        file = arg

# Error Cases
if file == 404:
    print("ERROR: NO IMAGE SUBMITTED")
    sys.exit()
if output_location == None and print_to_console == False:
    print(f"Warning: There is no output location and print to console is false, EXIF data will be saved to: {default_exif_save}")
    output_location = default_exif_save


image = Image.open(file)

exif_data = image.getexif()

if print_to_console:
    print(exif_data)
        
