# The tests on repl.it won't succeed with this implementation because they
# expect you to actually change `Hat.contents` while drawing. But then you need
# to create a deep copy of the hat for every run of the experiment, which is
# terribly inefficient. It's way easier (and better) to just delegate the
# drawing to `random.sample`

import random

class Hat(object):
    def __init__(self, **balls):
        self.contents = []
        for color, count in balls.items():
            for _ in range(count):
                self.contents.append(color)

    def draw(self, count):
        if count > len(self.contents):
            return self.contents
        else:
            return random.sample(self.contents, count)

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    num_successes = 0
    for _ in range(num_experiments):
        sample = hat.draw(num_balls_drawn)
        if all(sample.count(color) >= count for color, count in expected_balls.items()):
            num_successes += 1
    return num_successes / num_experiments
