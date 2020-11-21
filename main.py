import os

import discordbot
import mypath

file_status = mypath.data_folder / "status.txt"


def main():
    discordbot.welcome()
    discordbot.await_message_gg()
    # discordbot.ping_role()
    discordbot.run_bot()


if __name__ == "__main__":
    main()
