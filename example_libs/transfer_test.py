import globus_sdk
import sys

class TransferTest:
    def __init__(self, transfer_client, source_endpoint,
                 destination_endpoint, source_path, destination_path,
                 recursive):
        self.tc = transfer_client
        self.src_ep = source_endpoint
        self.dst_ep = destination_endpoint
        self.src_path = source_path
        self.dst_path = destination_path
        self.recursive = recursive

    def run_test(self):
        for ep in (self.src_ep,self.dst_ep):
            r = self.tc.endpoint_autoactivate(ep, if_expires_in=3600)
            while r["code"] == "AutoActivationFailed":
                print("Endpoint requires manual activation, please open "
                      "the following URL in a browser to activate the "
                      "endpoint:")
                print("https://www.globus.org/app/endpoints/%s/activate" % ep)
                print("Press ENTER after activating the endpoint:")
                sys.stdin.readline()
                r = self.tc.endpoint_autoactivate(ep, if_expires_in=3600)

        tdata = globus_sdk.TransferData(self.tc, self.src_ep, self.dst_ep)
        tdata.add_item(self.src_path, self.dst_path, recursive=self.recursive)
        transfer_result = self.tc.submit_transfer(tdata)
        print("task_id = %s" % transfer_result["task_id"])
