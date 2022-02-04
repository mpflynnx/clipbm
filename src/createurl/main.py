import subprocess
from pathlib import Path, PosixPath

import regex
import requests
import validus
from bs4 import BeautifulSoup
from colorama import Fore
from unidecode import unidecode


def paste_xsel():
    p = subprocess.Popen(["xsel", "-b", "-o"], stdout=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    return stdout.decode("utf-8")


def remove_punctuation(s):
    """Strip all punctuation."""

    regularExpression = r"[\p{C} \p{M} \p{P} \p{S} \p{Z}]+"

    remove = regex.compile(regularExpression)

    return remove.sub(" ", s).strip()


def myreplace(old, new, s):
    """Replace all occurrences of old with new in s."""

    result = " ".join(s.split())  # firsly remove any multiple spaces " ".

    return new.join(result.split(old))


def build_file(url, urlfile):
    """ """
    with open(urlfile, mode="w", encoding="utf-8") as myfile:
        myfile.write("[InternetShortcut]\n")
        myfile.write(f'''URL="{url}"''')


def get_title(reg_url):
    """Use beautiful soup to find url title."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
    }
    res = requests.get(url=reg_url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup.title.text


def main() -> None:

    try:
        print(Fore.LIGHTCYAN_EX + "\n    Reading url from clipboard...", flush=True)

        # Get url from clipboard
        dreg_url = paste_xsel()

        # Remove trailing newlines from string dreg_url
        reg_url = dreg_url.rstrip()

        # Validate reg_url
        if not validus.isurl(reg_url):
            print(Fore.LIGHTRED_EX + "    ⚠️   ERROR: No url available in clipboard. 😢")
            return

        print(Fore.LIGHTCYAN_EX + "\n    Getting title for url...", flush=True)

        dtitle = get_title(reg_url)

        # limit length of title
        title = dtitle[0:83]

        # Strip any punctuation, excluding "_"
        clean = remove_punctuation(title)

        # Replace spaces with underscore.
        spaces = myreplace(" ", "_", clean)

        # transliterate any Unicode text in title
        utf8title = unidecode(spaces)

        # define the destination path
        dest_path = PosixPath("~/Dropbox/bookmarks/")

        # define the filename suffix
        Path.suffix = ".url"

        # Constuct output location and filename.
        urlfile2 = dest_path.expanduser() / (utf8title + Path.suffix)

        # Build the output file.
        build_file(reg_url, urlfile2)

        # Text to display.
        print(Fore.LIGHTYELLOW_EX + "\n    New file created at....\n")
        print(Fore.LIGHTGREEN_EX + f"{urlfile2}\n")

    except Exception as x:
        print(Fore.LIGHTRED_EX + f"⚠️⚠️⚠️⚠️   Error: Unexpected crash: {x}.")


# --------------------------------------------------
if __name__ == "__main__":
    main()
