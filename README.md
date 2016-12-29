# sdk-endpoint-test

**Description:**

This script is meant to provide a simple example test script that uses the Globus SDK for Python to test basic endpoint functionality.

The script will attempt to transfer the contents of a configurable source directory on a configurable source endpoint to a configurable destination directory on a configurable destination endpoint.

The script requires that the user have current activations on both endpoints being used. If the endpoints to be used are not activated, the script will attempt to auto-activate them. If auto-activation should fail, the script will prompt the user to activate the endpoints.

If considerable automated transfer testing is desired, then it would best to use shared endpoints so as to avoid issues with activation. More details on sharing and shared endpoints can be found here:

https://docs.globus.org/resource-provider-guide/#sharing_section

**Requirements:**

Use of this script requires that the Globus SDK for Python be installed and configured on the system where the script will be run. The Globus SDK for Python can be found here:

https://github.com/globus/globus-sdk-python

**Use:**

The script has two mutually exclusive switches: --test and --login. When run with the --login switch, the script will direct the user through the appropriate OAuth flow to get a token from Globus to allow the script to perform operations on the user's behalf. When run with the --test switch, the script will use the token previously obtained to run the defined tests, which include only a basic transfer test as described above for now.
