import requests
import os


def send_quickstatements(username, api_token, commands, batchname, format="v1"):
    """
    Upload QuickStatements commands via the QS API

    To effectively use this function you must have uploaded a batch server-side
    command before, see further details at <https://quickstatements.toolforge.org/#/user>.

    Args:
        username (str): Wikimedia username.
        api_token (str): QuickStatements API token, you can find yours at
            <https://quickstatements.toolforge.org/#/user> (If you're logged in).
        commands (str): QuickStatements commands.
        batchname (str): Name of the batch.
        format (str): One of either 'v1' or 'csv', specifying which syntax the
            QS commands are using. Defaults to v1.

    """

    data = {
        "action": "import",
        "submit": "1",
        "username": username,
        "token": api_token,
        "format": "v1",
        "data": commands,
        "batchname": batchname,
    }

    r = requests.post(
        url="https://tools.wmflabs.org/quickstatements/api.php", data=data
    )

    r.raise_for_status()

    response = r.json()

    if r.status_code == 200:
        print(f"Batch {batchname} uploaded!\nBatch ID:{response['batch_id']}")


def main():

    test_qs = """Q18270892|P594|"ENSMUSG00000041303"|S248|Q99936939|S854|"https://github.com/oscar-franzen/PanglaoDB"|S813|+2020-09-09T00:00:00Z/11
    Q18270918|P594|"ENSMUSG00000042229"|S248|Q99936939|S854|"https://github.com/oscar-franzen/PanglaoDB"|S813|+2020-09-09T00:00:00Z/11
    Q18270972|P594|"ENSMUSG00000027134"|S248|Q99936939|S854|"https://github.com/oscar-franzen/PanglaoDB"|S813|+2020-09-09T00:00:00Z/11
    Q18270976|P594|"ENSMUSG00000026645"|S248|Q99936939|S854|"https://github.com/oscar-franzen/PanglaoDB"|S813|+2020-09-09T00:00:00Z/11
    Q18270979|P594|"ENSMUSG00000037740"|S248|Q99936939|S854|"https://github.com/oscar-franzen/PanglaoDB"|S813|+2020-09-09T00:00:00Z/11
    Q18271073|P594|"ENSMUSG00000027848"|S248|Q99936939|S854|"https://github.com/oscar-franzen/PanglaoDB"|S813|+2020-09-09T00:00:00Z/11
    """

    username = "Jvcavv"
    token = os.environ.get("TOKEN")

    send_quickstatements(username, token, test_qs, "API_test_batch3")


if __name__ == "__main__":
    main()