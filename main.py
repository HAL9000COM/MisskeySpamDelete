import argparse
import logging

import requests


class MisskeyNote:
    def __init__(self, user_id, username, name, host, text, created_at):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.host = host
        self.text = text
        self.created_at = created_at


def process_search_results(data):
    notes = []
    for note in data:
        user_id = note["user"]["id"]
        username = note["user"]["username"]
        name = note["user"]["name"]
        host = note["user"]["host"]
        text = note["text"]
        created_at = note["createdAt"]
        notes.append(MisskeyNote(user_id, username, name, host, text, created_at))
    return notes


class ApiAccess:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def search_post(self, query: str):
        search_url = f"{self.base_url}/api/notes/search"
        search_response = requests.post(
            search_url, headers=self.headers, json={"query": query}
        )
        if search_response.status_code == 200:
            data = search_response.json()
            return data
        else:
            logging.error(f"Note Search Error: {search_response.status_code}")
            return None

    def delete_user(self, user_id: str):
        delete_url = f"{self.base_url}/api/admin/accounts/delete"
        delete_response = requests.post(
            delete_url, headers=self.headers, json={"userId": user_id}
        )
        if delete_response.status_code == 204:
            return True
        else:
            logging.error(f"User Delete Error: {delete_response.status_code}")
            return False

    def suspend_user(self, user_id: str):
        suspend_url = f"{self.base_url}/api/admin/suspend-user"
        suspend_response = requests.post(
            suspend_url, headers=self.headers, json={"userId": user_id}
        )
        if suspend_response.status_code == 204:
            return True
        else:
            logging.error(f"User Suspend Error: {suspend_response.status_code}")
            return False

    def batch_delete_user(self, notes: list[MisskeyNote]):
        for note in notes:
            if self.delete_user(note.user_id):
                logging.info(f"User {note.username}@{note.host} deleted.")
            else:
                logging.error(f"User {note.username} delete failed.")

    def batch_suspend_user(self, notes: list[MisskeyNote]):
        for note in notes:
            if self.suspend_user(note.user_id):
                logging.info(f"User {note.username}@{note.host} suspended.")
            else:
                logging.error(f"User {note.username} suspend failed.")

    def manual_decision(self, notes: list[MisskeyNote]):
        for note in notes:
            print("\n")
            print(f"User {note.username}@{note.host} created at {note.created_at}")
            print(f"Text:\n{note.text}")
            print("\n")
            action = input(
                "Enter 'd' to delete user, 's' to suspend user,'q' to quit, others to skip:"
            )
            if action == "d":
                res = self.delete_user(note.user_id)
                if res:
                    logging.info(f"User {note.username}@{note.host} deleted.")
                else:
                    logging.error(f"User {note.username} delete failed.")
            elif action == "s":
                self.suspend_user(note.user_id)
                if res:

                    logging.info(f"User {note.username}@{note.host} suspended.")
                else:
                    logging.error(f"User {note.username} suspend failed.")
            elif action == "q":
                logging.info(f"Program quit.")
                break
            else:
                logging.info(f"User {note.username}@{note.host} skipped.")
                continue


def main(base_url: str, api_key: str, query: str, action: str):
    api = ApiAccess(base_url, api_key)
    data = api.search_post(query)
    if data:
        notes = process_search_results(data)
    else:
        logging.info(f"No post found for keyword '{query}'")
        return
    if action is None:
        logging.getLogger().setLevel(logging.INFO)
        api.manual_decision(notes)
        logging.info(f"Manual decision completed for keyword '{query}'")
        return
    if action == "delete":
        api.batch_delete_user(notes)
    elif action == "block":
        api.batch_suspend_user(notes)
    logging.info(f"Action {action} completed for keyword '{query}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Misskey Spam Delete", description="Misskey Spam delete using API."
    )
    parser.add_argument(
        "-u",
        "--url",
        help="Misskey instance URL",
        required=True,
        default="https://misskey.example",
    )
    parser.add_argument("-t", "--token", help="Bearer token", required=True)
    parser.add_argument("-k", "--keyword", help="keyword to search", required=True)
    parser.add_argument(
        "-a",
        "--action",
        help="Action to perform, if not provided, default to manual input.",
        choices=["delete", "suspend"],
    )
    parser.add_argument("-l", "--log", help="log to filepath")
    args = parser.parse_args()
    if args.log is not None:
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(
            filename="args.log",
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    main(args.url, args.token, args.keyword, args.action)
