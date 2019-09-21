from bs4 import BeautifulSoup
import requests


class page():
    def __init__(self, soup):
        self.page = soup.find(class_="inner-content clearfix")

    def name(self):
        return str(self.page.a).split('">')[-1][:-4]

    def date(self):
        return str(self.page.find(itemprop="dateCreated")).split('"')[1]

    def question(self):
        qu = self.page.find(class_="postcell post-layout--right")
        question = qu.find(class_="post-text")
        if question.find_all('a') != []:
            for link in question.find_all('a'):
                link.replace_with(str(link))
        return question.text

    def anses(self):
        right_answer = self.page.find(class_="answer accepted-answer")
        ansList = []
        if None != right_answer:
            answers = self.page.find(id='answers')
            answers = answers.find_all(class_="answer")
            for answer_ in answers:
                post_text_ = answer_.find(class_="post-text")
                if post_text_.find_all('a') != []:
                    for link in post_text_.find_all("a"):
                        link.replace_with(str(link))
                ansList.append(post_text_.text)
        return ansList


def scrapper(urlfile):
    cnt = -1
    MainDict = {}
    with open(f"{urlfile}", "r") as file:
        urls_count = file.readlines()
        print(f"{len(urls_count)} urls found in file.")
        for url in urls_count:
            cnt += 1
            soup = BeautifulSoup(requests.get(f"https://ru.stackoverflow.com/questions/{url[:-1]}").text, "html.parser")
            pg = page(soup)
            if pg.anses() != []:
                MainDict[cnt] = [pg.anses(), pg.name(), f"https://ru.stackoverflow.com/questions/{url[:-1]}",
                                 pg.question(), pg.date()]
            print(f"{round((cnt * 100) / len(urls_count), 3)} %")
    return MainDict
