#!/usr/bin/env python3
import subprocess
import json
import sys
from packaging import version


def get_tags(image_name):
    """Fetches tags for a given image using skopeo list-tags."""
    try:
        result = subprocess.run(
            ["skopeo", "list-tags", f"docker://{image_name}"],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        return data.get("Tags", [])
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error fetching tags for {image_name}: {e}")
        return []


def filter_and_sort_tags(tags, min_tag):
    """Filters tags >= min_tag and sorts them descending by version."""
    filtered = []
    try:
        min_ver = version.parse(min_tag)
    except version.InvalidVersion:
        print(f"Warning: Minimum tag '{min_tag}' is not a valid version. Using string comparison.")
        min_ver = min_tag

    for tag in tags:
        try:
            current_ver = version.parse(tag)
            if isinstance(min_ver, version.Version) and current_ver >= min_ver:
                filtered.append(tag)
            elif not isinstance(min_ver, version.Version) and tag >= min_tag:
                filtered.append(tag)
        except version.InvalidVersion:
            continue  # Skip non-version tags (like 'latest') if we are version filtering

    # Sort helper to handle potential version parsing errors during sort
    def sort_key(t):
        try:
            return version.parse(t)
        except version.InvalidVersion:
            return t

    return sorted(filtered, key=sort_key, reverse=True)


def main():
    image_file = "images.txt"
    try:
        with open(image_file, "r") as f:
            # Filter out empty lines and whitespace
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {image_file} not found.")
        sys.exit(1)

    if not lines:
        print(f"Error: {image_file} is empty.")
        return

    # Use the first line as the registry
    registry = lines[0].rstrip('/')
    image_entries = lines[1:]

    print(f"Using Registry: {registry}\n")

    for line in image_entries:
        if ":" not in line:
            print(f"Skipping invalid line: {line} (Expected image:min_tag)")
            continue

        image_path, min_tag = line.rsplit(":", 1)
        # Construct the full image name for skopeo
        full_image_name = f"{registry}/{image_path}"
        
        print(f"Processing {full_image_name} (min version: {min_tag})...")
        
        all_tags = get_tags(full_image_name)
        if not all_tags:
            continue

        final_tags = filter_and_sort_tags(all_tags, min_tag)

        if final_tags:
            for tag in final_tags:
                print(f"  - {tag}")
        else:
            print("  No tags found matching criteria.")
        print()


if __name__ == "__main__":
    main()