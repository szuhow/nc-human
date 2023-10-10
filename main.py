from nc_py_api import Nextcloud
import requests
from json import dumps
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image  # this example requires `pillow` to be installed
import os
if __name__ == "__main__":
    load_dotenv()
    api_url = os.getenv("API_URL")
    api_login = os.getenv("API_LOGIN")
    api_password = os.getenv("API_PASSWORD")
    # create Nextcloud client instance class
    nc = Nextcloud(nextcloud_url=api_url, nc_auth_user=api_login, nc_auth_pass=api_password)
    buf = BytesIO()
    Image.merge(
        "RGB",
        [
            Image.linear_gradient(mode="L"),
            Image.linear_gradient(mode="L").transpose(Image.ROTATE_90),
            Image.linear_gradient(mode="L").transpose(Image.ROTATE_180),
        ],
    ).save(
        buf, format="PNG"
    )  # saving image to the buffer
    buf.seek(0)  # setting the pointer to the start of buffer
    nc.files.upload_stream("RGB.png", buf)  # uploading file from the memory to the user's root folder
    exit(0)
    # if nc.check_capabilities("files_sharing"):  # check one capability
    #     print("Sharing API is not present.")
    #
    # # check child values in the same call
    # if nc.check_capabilities("files_sharing.api_enabled"):
    #     print("Sharing API is present, but is not enabled.")
    #
    # # check multiply capabilities at one
    # missing_cap = nc.check_capabilities(["files_sharing.api_enabled", "user_status.enabled"])
    # if missing_cap:
    #     print(f"Missing capabilities: {missing_cap}")
    # rgb_image = nc.files.download("RGB.png")
    # Image.open(BytesIO(rgb_image)).show()  # wrap `bytes` into BytesIO for Pillow
    # exit(0)
    # def list_dir(directory):
    #     # usual recursive traversing over directories
    #     for node in nc.files.listdir(directory):
    #         if node.is_dir:
    #             list_dir(node)
    #         else:
    #             print(f"{node.user_path}")
    #
    # print("Files on the instance for the selected user:")
    # list_dir("")
    # exit(0)
