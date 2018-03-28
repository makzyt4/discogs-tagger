import discogstagger.crawler


class Search:
    def __init__(self):
        self.base_url = discogstagger.crawler.WebCrawler().base_url

    def ask_if_continue(self, text):
        while True:
            choice = input(text + " (Y/n): ")
            if choice == "Y":
                return True
            elif choice == "n":
                return False
            else:
                print("Wrong input. Enter uppercase 'Y' or lowercase 'n'.")
