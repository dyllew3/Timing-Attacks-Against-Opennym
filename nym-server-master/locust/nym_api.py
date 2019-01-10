from locust import HttpLocust, TaskSet, task
from random import randint

class UserBehaviour(TaskSet):
    # @task(1)
    # def nym(self):
    #     self.client.get("/nym")

    # @task(2)
    # def rating(self):
    #     nym = randint(0, 14)
    #     if nym == 11: nym += 1
    #     self.client.get("/ratings/{}/spotify.com".format(nym))

    # @task(3)
    # def rating(self):
    #     nym = randint(0, 14)
    #     if nym == 11: nym += 1
    #     self.client.get("/cookies/{}".format(nym))

    @task(4)
    def rating(self):
        nym = randint(0, 14)
        if nym == 11: nym += 1
        self.client.get("/rules/top/{}".format(nym))

    #@task(5)
    #def rating(self):
    #    self.client.get("/identity/spotify.com")

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = 500
    max_wait = 1000
