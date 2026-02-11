# OLM Catalog Bundle Parser

A Python utility designed to parse OPM (Operator Package Manager) rendered catalogs. This tool scans the catalog for entries with the olm.bundle schema, extracts the sha256 image digests, and saves the results to a local text file.

### Prerequisites

 * Python 3.x: Ensure you have Python installed on your system.
 * opm CLI: Required to extract the catalog metadata from your operator index image.

### Preparation

Before running the parser, you must extract the contents of your local registry operator-index into a JSON format file that the script can read.
Use the a modified copy of the following command to render the index metadata to a file named catalog.json:


```opm render rhel9.lktc7.internal:8443/redhat/redhat-operator-index:v4.18 -o json > catalog.json```

Subsitute your local registry, path and tag for the operator-index you want to parse.

This command saves the metadata from the v4.18 index to a file named catalog.json in your current directory.

### How to Run
 * Open your terminal or command prompt.
 * Navigate to the directory containing parser.py and catalog.json.
 * Execute the script:
<!-- end list -->
```python parser.py```

#### Options
If your rendered file has a different name you can specify on the command line:
```
python parser.py -f your-filename.json
```
### Expected Output
The script provides feedback in the terminal and automatically generates a file named bundle_digests.txt containing the results:

```
BUNDLE NAME                                             | SHA256 DIGEST
-----------------------------------------------------------------------------------------------------------------------------
advanced-cluster-management.v2.14.1                     | dd4a7678648872ea4294b867cdc7bca0ac063b81eaeac9bf5d4fddcaffb96bac
cluster-logging.v6.4.2                                  | 442e8ca696eb526c0a933d260d1f50a5d45d57427116f0210f440ac7f1135573
...

Parsing complete. Total bundles found: 12

```

### Troubleshooting
 * JSONDecodeError: If you receive an error regarding property names or double quotes, ensure that you used the opm render command correctly. The script is specifically designed to handle the multi-object JSON stream produced by opm.
 * FileNotFoundError: Ensure catalog.json is in the same folder as parser.py.
