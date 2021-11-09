from django.db import models

class Event(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")

    # def __str__(self):
    #     return self.description