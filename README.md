# Skopeo Image Tag Wrapper

A Python utility to list, filter, and sort container image tags from a remote registry using `skopeo`. This tool helps track new releases by comparing versions against a defined minimum threshold.

In a private registry scenario, it can also be used to check for the existence of images newer than the desired version.

## Purpose
This script automates the discovery of new image tags by:
1. Connecting to a specified container registry.
2. Fetching all available tags for a list of images.
3. Filtering tags based on a "minimum version" using semantic versioning logic.
4. Sorting the results in descending order (newest versions first).

## Prerequisites
- **Python 3.x**
- **Skopeo**: Must be installed and available in your system `$PATH`.
- **Packaging Library**: Required for robust version comparison.
  ```bash
  pip install packaging
  ```

## Usage
Run the script from the directory containing your configuration file:
```bash
python skopeo_wrapper.py
```

## Configuration: images.txt
The script reads image data from a file named `images.txt` located in the same directory.

### Format
*   **Line 1**: The base URL of the container registry (e.g., `docker.io` or `quay.io`).
*   **Subsequent Lines**: The image path and the minimum version tag, separated by a colon (`image_path:min_tag`).

### Sample `images.txt`
```text
docker.io
library/alpine:3.15.0
library/ubuntu:20.04
library/redis:8.0.0
```
## Technical Details
- **Registry Handling**: The script automatically concatenates the registry from the first line with each image path (e.g., `docker.io/library/alpine`).
- **Semantic Versioning**: It uses `packaging.version` to ensure accurate comparisons (e.g., recognizing that `1.10.0` is newer than `1.2.0`).
- **JSON Integration**: It interfaces with `skopeo list-tags` and parses the JSON output to retrieve the tag list safely.

// ... existing code ...
- **Semantic Versioning**: It uses `packaging.version` to ensure accurate comparisons (e.g., recognizing that `1.10.0` is newer than `1.2.0`).
- **JSON Integration**: It interfaces with `skopeo list-tags` and parses the JSON output to retrieve the tag list safely.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.