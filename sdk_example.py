import argparse
import json
import globus_sdk
import example_libs

CONFIG_FILE = "clientid.cfg"
TOKEN_FILE = "token.cfg"

def parse_arguments():
    p = argparse.ArgumentParser()

    p.add_argument("-t", "--test", action="store_true",
                   help="run tests")
    p.add_argument("-l", "--login", action="store_true",
                   help="log in to Globus Auth and get tokens")

    a = p.parse_args()

    if not a.test and not a.login:
        p.print_help()
        exit(0)

    return a

def login(auth_client):
    auth_client.oauth2_start_flow_native_app(refresh_tokens=True)

    print('Please go to this URL and login: {0}'
          .format(auth_client.oauth2_get_authorize_url()))

    get_input = getattr(__builtins__, 'raw_input', input)
    auth_code = get_input('Please enter the code here: ').strip()
    token_response = auth_client.oauth2_exchange_code_for_tokens(auth_code)

    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
    transfer_rt = globus_transfer_data['refresh_token']
    token_cfg = dict(REFRESH_TOKEN = transfer_rt)

    with open(TOKEN_FILE, "w") as tf:
        json.dump(token_cfg, tf)

    print("Token saved to: " + TOKEN_FILE + "\n")

def run_tests(auth_client):
    with open(TOKEN_FILE, "r") as tf:
        token_cfg = json.load(tf)

    transfer_rt = token_cfg['REFRESH_TOKEN']

    authorizer = globus_sdk.RefreshTokenAuthorizer(transfer_rt, auth_client)
    transfer_client = globus_sdk.TransferClient(authorizer=authorizer)

    transfer_test = example_libs.TransferTest(transfer_client,
                                              source_endpoint="ddb59aef-6d04-11e5-ba46-22000b92c6ec",
                                              destination_endpoint="ddb59af0-6d04-11e5-ba46-22000b92c6ec",
                                              source_path="/~/",
                                              destination_path="/~/",
                                              recursive=True
                                              )

    transfer_test.run_test()

def read_clientid_cfg():
    with open(CONFIG_FILE, "r") as cf:
        config = json.load(cf)
    if config['APP_CLIENT_ID'] == "":
        print("App client ID could not be found in: " + CONFIG_FILE + "\n")
        exit(1)
    return config['APP_CLIENT_ID']

def main():
    client_id = read_clientid_cfg()
    auth_client = globus_sdk.NativeAppAuthClient(client_id)
    args = parse_arguments()

    if args.login and args.test:
        print("Please use only one of the --login or --test switches.")
    elif args.login:
        login(auth_client)
        exit(0)
    elif args.test:
        run_tests(auth_client)
        exit(0)
    else:
        print("Problem parsing arguments.")
        exit(1)

if __name__ == "__main__":
    main()
    
