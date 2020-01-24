# habr_google_script_api
Code related to my habr.com article.

## How to use the script:
Put your JSON file with keys in "credentials" directory.
If you want to update script remotely: 

```python update_script.py <config_file_name> <script_id> <script_file_name>```

In this case:

- *config_file_name* — name of JSON config file
- *script_id* — script id
- *script_file_name* — name of .gs file, which will be uploaded to google

If you want to export form: 

```python export_form.py <config_file_name> <result_file_name> <script_id> <google_form_url>```

In this case:

- *config_file_name* — name of JSON config file
- *result_file_name* — name of JSON file where the form will be exported to
- *script_id* — script id
- *google_form_url* — URL of google-form you want to export
