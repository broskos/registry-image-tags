import json
import re
import argparse
import sys

def parse_catalog(input_file):
    # Regex to capture exactly 64 characters of a hex sha256 digest
    digest_pattern = re.compile(r"sha256:([a-fA-F0-9]{64})")
    output_filename = "bundle_digests.txt"
    
    try:
        with open(input_file, 'r') as f:
            content = f.read()
            
        decoder = json.JSONDecoder()
        pos = 0
        found_bundles = 0
        
        # Prepare the output content
        header = f"{'BUNDLE NAME':<55} | {'SHA256 DIGEST'}"
        separator = "-" * 125
        output_lines = [header, separator]
        
        # Print to console for immediate feedback
        print(header)
        print(separator)
        
        while pos < len(content):
            content = content.lstrip()
            if not content:
                break
            
            try:
                obj, end_pos = decoder.raw_decode(content)
                
                if obj.get("schema") == "olm.bundle":
                    name = obj.get("name", "Unknown")
                    image = obj.get("image", "")

                    # Extract digest using regex
                    match = digest_pattern.search(image)
                    digest = match.group(1) if match else "No Digest Found"
                    
                    line = f"{name:<55} | {digest}"
                    print(line)
                    output_lines.append(line)
                    found_bundles += 1
                
                content = content[end_pos:].lstrip()
                pos = 0
            except json.JSONDecodeError:
                break
        
        summary = f"\nParsing complete. Total bundles found: {found_bundles}"
        print(summary)
        output_lines.append(summary)

        # Write to file
        with open(output_filename, 'w') as out_file:
            out_file.write("\n".join(output_lines))
        print(f"Results have been saved to: {output_filename}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse OLM catalog for bundle digests.")
    parser.add_argument("-f", "--file", default="catalog.json", help="Input JSON file (default: catalog.json)")
    args = parser.parse_args()
    
    parse_catalog(args.file)
