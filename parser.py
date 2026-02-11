import json
import re

def get_bundle_info(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            decoder = json.JSONDecoder()
            pos = 0
            
            print(f"{'BUNDLE NAME':<50} | {'SHA256 DIGEST'}")
            print("-" * 117)

            while pos < len(content):
                content = content.lstrip()
                if not content:
                    break
                
                try:
                    obj, end_pos = decoder.raw_decode(content)
                    
                    # Filter for 'olm.bundle'
                    if obj.get("schema") == "olm.bundle":
                        name = obj.get("name", "N/A")
                        image_url = obj.get("image", "")
                        
                        # Extract digest following 'sha256:'
                        # We look for the part after the colon in 'sha256:...'
                        digest = "N/A"
                        if "sha256:" in image_url:
                            digest = image_url.split("sha256:")[-1]
                        
                        print(f"{name:<50} | {digest}")
                    
                    content = content[end_pos:].lstrip()
                    pos = 0 
                    
                except json.JSONDecodeError:
                    break

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

if __name__ == "__main__":
    get_bundle_info('catalog.json')
