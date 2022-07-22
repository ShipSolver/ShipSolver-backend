import requests
from clint.textui.progress import Bar as ProgressBar  # Library to monitor the upload
from requests_toolbelt.multipart.encoder import (
    MultipartEncoder,
    MultipartEncoderMonitor,
)


def test_image_post():
    # Optional callback to monitor the upload
    def create_callback(encoder):
        encoder_len = encoder.len
        bar = ProgressBar(expected_size=encoder_len, filled_char="■")

        def callback(monitor):
            bar.show(monitor.bytes_read)
            return callback

    file_path = "/home/stefan/Pictures/Selection_001.png"  # file path

    try:
        file = open(file_path, "rb")

        # Sample Payload
        e = MultipartEncoder(
            {
                "upload[file]": (file.name, file, "application/octet-stream"),
            }
        )

        callback = create_callback(e)
        payload = MultipartEncoderMonitor(e, callback)
        url = "http://localhost:6767/api/blob_storage/"

        r = requests.post(
            url,
            data=payload,
            headers={
                "Content-Type": payload.content_type,
                "Authorized": "eyJraWQiOiJoQU9HMERlWjE1dXQ3Mkp4d1wvRHFTSjduSHU0d1A1c00xdVVQUTFGRUU3OD0iLCJhbGciOiJSUzI1NiJ9",
            },
        )
    except Exception as x:
        print("Status: Error ", x)
    else:
        print("Status: Success ", r.status_code, r.text)


def test_image_get():
    try:
        url = "http://localhost:6767/api/blob_storage/"

        r = requests.get(
            url, {"uploaded_file_name": "images/43401294-e65c-44a3-8d88-9708d4a72024"}
        )
    except Exception as x:
        print("Status: Error ", x)
    else:
        print("Status: Success ", r.status_code, r.text)


# test_image_post()
# test_image_get()


res = requests.get("http://localhost:6767/api/ticket/7")

print(res.status_code, res.text)
