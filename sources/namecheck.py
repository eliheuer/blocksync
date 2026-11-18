"""Check the actual app-menu family name once against the live FontData API."""
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from fgtools import project


def main():
    family = project.load().config["familyName"]
    url = "https://namecheck.fontdata.com/api/?" + urlencode({"q": family})
    with urlopen(url, timeout=30) as response:
        data = json.load(response)["data"]
    confidence = data["confidence"]
    if data["query"] != family or not confidence:
        raise ValueError("FontData returned an incomplete result for this family")
    print(json.dumps(data, indent=2))
    return data["trademark"] is not False or any(count != 0 for count in confidence.values())


if __name__ == "__main__":
    raise SystemExit(main())
