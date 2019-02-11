class Anime:
    title=""
    latest_ep=""
    previous_ep =""
    latest_ep_link=""
    updated = False
    
    def __init__(self):
        self.previous_ep = self.latest_ep

    def __str__(self):
        return self.title + ":\n" + self.latest_ep + "\n" + self.latest_ep_link + '\n'