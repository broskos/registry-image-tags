Here is a README.md file tailored for your tool. It includes the preparation steps using the opm CLI and instructions for running your parser.py script.
OLM Catalog Bundle Parser
A lightweight Python utility designed to parse OPM (Operator Package Manager) rendered catalogs. This tool identifies all entries with the olm.bundle schema and extracts their associated sha256 image digests.
Prerequisites
 * Python 3.x: Ensure you have Python installed on your system.
 * opm CLI: Required to extract the catalog metadata from your operator index image.
Preparation
Before running the parser, you must extract the contents of your local or remote index into a JSON format that the script can read.
Use the following command to render the index metadata to a file named catalog.json:
opm render rhel9.lktc7.internal:8443/redhat/redhat-operator-index:v4.18 -o json > catalog.json

Note: Ensure the output file is named catalog.json and is located in the same directory as the script.
How to Run
 * Open your terminal or command prompt.
 * Navigate to the directory containing parser.py and catalog.json.
 * Execute the script:
<!-- end list -->
python parser.py

Expected Output
The script will process the catalog and print a formatted table listing the bundle names and their corresponding SHA256 digests:
BUNDLE NAME                                        | SHA256 DIGEST
---------------------------------------------------------------------------------------------------------------------
advanced-cluster-management.v2.14.1                | dd4a7678648872ea4294b867cdc7bca0ac063b81eaeac9bf5d4fddcaffb96bac
advanced-cluster-management.v2.15.1                | b6506d0e18ee16259c56ae0afcb0db85b854dab69ed420722c928a28e3d0e2dd
cluster-logging.v6.3.2                             | 56ee655fc9fd5aca984a7c552c00112b7314d2e79117f58c469ef91f3cefe640
...

Troubleshooting
 * JSONDecodeError: If you receive an error regarding property names or double quotes, ensure that you used the opm render command correctly. The script is specifically designed to handle the multi-object JSON stream produced by opm.
 * FileNotFoundError: Ensure catalog.json is in the same folder as parser.py.
Would you like me to add a section on how to export this output directly to a CSV file?
