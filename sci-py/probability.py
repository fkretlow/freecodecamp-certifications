import copy
import random

class Hat(object):
    def __init__(self, **balls):
        self.contents = []
        for color, count in balls.items():
            for _ in range(count):
                self.contents.append(color)

    def draw(self, count):
        drawn = []
        if count > len(self.contents):
            drawn += self.contents
            self.contents = []
        else:
            for _ in range(count):
                ball = random.choice(self.contents)
                drawn.append(ball)
                self.contents.remove(ball)
        return drawn


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    num_successes = 0
    for _ in range(num_experiments):
        new_hat = copy.deepcopy(hat)
        sample = new_hat.draw(num_balls_drawn)
        if all(sample.count(color) >= count for color, count in expected_balls.items()):
            num_successes += 1
    return num_successes / num_experiments
