from bs4 import BeautifulSoup

import sys
import urllib.request


# pass first argument as your url
url = sys.argv[1]

def remove_punctuation(s):
    """Strip all punctuation, except "_", "/" , "-"from s."""

    punctuation = "!\"#$%&'()*+,/.:;<=>?@[\\]^`{|}~"

    s_sans_punct = ""
    for letter in s:
        if letter not in punctuation:
            s_sans_punct += letter
    return s_sans_punct


def myreplace(old, new, s):
    """Replace all occurrences of old with new in s."""

    result = " ".join(s.split())  # firsly remove any multiple spaces " ".

    return new.join(result.split(old))


def build_file(url, urlfile):
    """ """
    myfile = open(urlfile, "w")
    myfile.write("[InternetShortcut]\n")
    myfile.write('''URL="{0}"'''.format(url))
    myfile.close()

def main() -> None:

    # Encode urlfile, to ignore non ascii characters.

    # Use beautiful soup to find url title
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(strip=True)
    dtitle = soup.title.text

    # limit length of title
    title = dtitle[0:83]

    # encode url title
    encoded = title.encode("ascii", "ignore")
    #  encoded = urlfile.encode("ascii", "replace")

    # Decode now to utf-8.
    urlfileutf8 = encoded.decode("utf-8")

    # Strip any punctuation, excluding "_"
    clean = remove_punctuation(urlfileutf8)

    # Replace spaces with underscore.
    spaces = myreplace(" ", "_", clean)

    # Constuct output location and filename.
    # convert urlfile to utf-8

    urlfile2 = "/home/live/Dropbox/bookmarks/" + spaces + ".url"

    # Text to display.
    print("\n    New file created at....\n")
    print("    " + urlfile2 + "\n")

    # Build the output file.
    build_file(url, urlfile2)

# --------------------------------------------------
if __name__ == "__main__":
    main()
