import os

import discordbot
import mypath

file_status = mypath.data_folder / "status.txt"


def main():
    discordbot.welcome()
    discordbot.await_message_gg()
    create_status_file()
    # discordbot.ping_role()
    discordbot.run_client()


def create_status_file():
    f = open(file_status, "w+")


if __name__ == "__main__":
    main()
