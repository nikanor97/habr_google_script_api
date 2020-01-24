from pprint import pprint
import socket
import json
import sys

from googleapiclient import errors

from google_habr_login import login


socket.setdefaulttimeout(120)


# Get JSON, which is returned by script
def get_json(service, file_name, script_id, form_url):
    pprint('Exporting form...')
    body = {
        "function": "main",
        "devMode": True,
        "parameters": form_url
    }
    # Get JSON from script
    resp = service.scripts().run(scriptId=script_id, body=body).execute()

    # Write out JSON to file
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(resp['response']['result'], f, ensure_ascii=False, indent=4)

    pprint('Form was successfully exported')


def main():

    try:

        args = sys.argv
        if len(args) != 5:
            raise TypeError('Wrong number of arguments. Four arguments required:  <config_file_name>, '
                            '<result_file_name>, <script_id> and <google_form_url>')
        config_file_name = args[1]
        file_name = args[2]
        script_id = args[3]
        form_url = args[4]

        with open(config_file_name, "r") as f:
            config = json.load(f)

        service = login(config)

        get_json(service, file_name, script_id, form_url)

    except (errors.HttpError, ) as error:
        # The API encountered a problem.
        pprint(error.content.decode('utf-8'))


if __name__ == '__main__':
    main()
