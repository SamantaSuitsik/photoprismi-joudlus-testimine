import os
import json
import random
import string
import logging
import time

from locust import HttpUser, task, between, LoadTestShape, TaskSet
from locust.exception import StopUser


logging.basicConfig(filename='locust.log', filemode='w', level=logging.INFO)


def generate_upload_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


with open("fileList.json") as files_json:
    file_list = json.load(files_json)


class UserTasks(TaskSet):

    def get_some_photo_uid(self):
        url = "/api/v1/photos?count=120&offset=0&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=&order=added&q=&public=true&quality=3&review=true"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    return response_data[0]["UID"]

                except Exception as e:
                    response.failure("Failed to parse UID: " + str(e))

    def show_all_photos(self):
        url = "/api/v1/photos?count=120&offset=0&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=&order=added&q=&public=true&quality=3&review=true"
        self.client.get(url)

    def upload_file(self, upload_id):
        logging.info("Upload id %s", upload_id)  # TODO: remove line
        # Find a file
        file_name = random.choice(file_list)
        logging.info("Photo: %s", file_name)
        file_path = os.path.join("photos", file_name)

        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"files": (file_name, file_content, "image/jpeg")}

        url = f"/api/v1/users/usrzn0i6w9iu0075/upload/{upload_id}"
        with self.client.post(url, files=files, catch_response=True) as res:
            if res.status_code != 200:
                res.failure("POST request failed when uploading a photo")

        put_payload = {"albums": []}
        with self.client.put(url, data=json.dumps(put_payload), catch_response=True) as putRes:
            if putRes.status_code != 200:
                putRes.failure("PUT request failed when uploading a photo")
                print(putRes.text)

    def go_to_calendar(self):
        url = "/api/v1/albums?count=24&offset=0&q=&category=&order=newest&year=&type=month"
        self.client.get(url)

    def get_march_photos(self):
        album_url = "/api/v1/albums/assgnkhe6a1hbodk"
        self.client.get(album_url)
        time.sleep(1)
        photos_url = "/api/v1/photos?count=120&offset=0&s=assgnkhe6a1hbodk&merged=true&country=&camera=0&order=oldest&q="
        self.client.get(photos_url)

    def download_photo(self, uid):
        logging.info("UID %s", uid)  # TODO: remove line

        url = f"/api/v1/photos/{uid}/dl"
        self.client.get(url)

    def archive_or_delete_photo(self, action_type, uid):
        if action_type == 'delete':
            url = "/api/v1/batch/photos/archive"
        elif action_type == 'archive':
            url = "/api/v1/batch/photos/delete"
        else:
            raise StopUser("Invalid type, please use a correct type ('delete' or 'archive')")

        payload = {
            "photos": [uid]
        }

        with self.client.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, catch_response=True) as res:
            if res.status_code != 200:
                res.failure("POST request failed when archiving/deleting a photo")


class UploadScenario(UserTasks):
    @task
    def scenario(self):
        upload_id = generate_upload_id()

        self.show_all_photos()
        self.upload_file(upload_id)


class ViewScenario(UserTasks):
    @task
    def scenario(self):
        self.show_all_photos()
        self.go_to_calendar()
        self.get_march_photos()


class DownloadScenario(UserTasks):
    @task
    def scenario(self):
        uid = self.get_some_photo_uid()

        self.download_photo(uid)


class DeleteScenario(UserTasks):
    # Todo: Failib, kui ühte ja sama pilti samal ajal kustutatakse ja alla tõmmatakse, kas on ok?
    @task
    def scenario(self):
        uid = self.get_some_photo_uid()

        self.archive_or_delete_photo("archive", uid)
        time.sleep(2)
        self.archive_or_delete_photo("delete", uid)


class PhotoprismUser(HttpUser):
    wait_time = between(1, 5)

    tasks = {UploadScenario: 4, ViewScenario: 4, DownloadScenario: 4, DeleteScenario: 1}
