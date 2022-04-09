# "http://www.google.com", "https://www.apple.com", "https://mackenty.org"


class CrawlerStorage:
    def __init__(self):
        self.visited = set({})
        self.raw_link_component_to_code = {
            "https://": "1.",
            "http://": "2."
        }
        self.code_to_raw_link_component = {}

        for key, value in self.raw_link_component_to_code.items():
            self.code_to_raw_link_component[value] = key
        return

    def compress_url(self, url):
        encoded_url = ""
        for key in self.raw_link_component_to_code:
            if url[:len(key)] == key:
                print(key, "in url")
            encoded_url += self.raw_link_component_to_code.get(key)
        return encoded_url

    def expand_encoded_url(self, encoded_url):
        url = ""
        for key in self.code_to_raw_link_component:
            if encoded_url[:len(key)] == key:
                print(key, "in url")
            encoded_url += self.code_to_raw_link_component.get(key)
        return url