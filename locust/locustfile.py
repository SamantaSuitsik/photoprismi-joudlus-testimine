import os
import json
import random
import string
import logging
from locust import HttpUser, task, between, LoadTestShape
logging.basicConfig(filename='locust.log', filemode='w', level=logging.INFO)


class PhotoPrismUser(HttpUser):
    wait_time = between(1, 3)

    with open("fileList.json") as f:
        file_list = json.load(f)

    def generate_upload_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    @task
    def upload_file(self):
        upload_id = self.generate_upload_id()
        file_name = random.choice(self.file_list)
        logging.info("Photo: %s", file_name)
        file_path = os.path.join("/home/samanta/kool/loputoo/locust/photos", file_name)
        url = f"/api/v1/users/usrzn0i6w9iu0075/upload/{upload_id}"

        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"files": (file_name, file_content, "image/jpeg")}

        with self.client.post(url, files=files, catch_response=True) as res:
            if res.status_code != 200:
                res.failure("POST failed")

        put_payload = {"albums": []}
        with self.client.put(url, data=json.dumps(put_payload), catch_response=True) as resPut:
            if resPut.status_code != 200:
                resPut.failure("PUT failed")
                print(resPut.text)


class RampUpDownShape(LoadTestShape):
    steps = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3, 1]
    step_time = 20
    spawn_rate = 1

    def tick(self):
        i = int(self.get_run_time() // self.step_time)
        if i >= len(self.steps):
            return None
        return (self.steps[i], self.spawn_rate)
