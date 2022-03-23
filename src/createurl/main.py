import glob
import subprocess
import sys
from pathlib import Path

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


def validate_clipboard(clip):
    """
    Checks clipboard for a url string.
    Checks clipboard for html containing url and title.
    Returns url and title.
    """

    empty_title = ""
    if validus.isurl(clip):
        return clip, empty_title
    else:
        soup = BeautifulSoup(clip, "html.parser")
        if soup.find(href=True) or soup.find("a") is not None:
            url = soup.find(href=True)["href"]
            raw_title = soup.find("a").contents[0]
            return url, raw_title
        sys.exit(
            Fore.LIGHTRED_EX + "    ⚠️   ERROR: No url available in clipboard. 😢\n"
        )


def main() -> None:

    try:
        print(Fore.LIGHTCYAN_EX + "\n    Reading url from clipboard...", flush=True)

        # Get url from clipboard
        dreg_url, dtitle = validate_clipboard(paste_xsel())

        #  Remove any trailing newlines from string dreg_url
        reg_url = dreg_url.rstrip()

        print(Fore.LIGHTCYAN_EX + "\n    Getting title for url...", flush=True)
        print(Fore.LIGHTCYAN_EX + "     ..." + reg_url, flush=True)

        # if dtitle empty, use requests with url to get title
        if dtitle == "":
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
        dest_path = Path.home() / "Dropbox" / "bookmarks"
        Path.mkdir(dest_path, parents=True, exist_ok=True)

        # define the filename suffix
        Path.suffix = ".url"

        # Constuct filename.
        filename = utf8title + Path.suffix

        # Constuct output location and filename.
        urlfile2 = dest_path / filename

        # check if file name exists
        for file in glob.glob(f"{dest_path}/**/{filename}", recursive=True):
            if file:
                sys.exit(Fore.LIGHTRED_EX + f'\n    "{filename}" exists, exiting!\n')

        # Build the output file.
        build_file(reg_url, urlfile2)

        # Text to display.
        print(Fore.LIGHTYELLOW_EX + "\n    New file created at....\n")
        print(Fore.LIGHTGREEN_EX + f"{urlfile2}\n")

    except Exception as x:
        print(Fore.LIGHTRED_EX + f"⚠️⚠️⚠️⚠️   Error: Unexpected crash: {x}.\n")


# --------------------------------------------------
if __name__ == "__main__":
    main()
