import os, sys, subprocess
from PIL import Image
from PIL.ExifTags import TAGS

VALID_COMMANDS = ["--output", "-o", "--printconsole", "-pc"]

file = 404
output_location = None
print_to_console = False

default_exif_save = "exported.exif"
default_text_editor = "nano"
default_config_location = "~/.config/echo-utils/exif-viewer/config.json"

if not os.path.exists(default_config_location):
    with open (default_config_location, "w") as f:
        // TODO: get default config from github and write it.

for i in range (0, len(sys.argv)):
    arg = sys.argv[i]
    if arg == "config":
        subprocess.run
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
        
