from random import random

MAX_CITIES = 20
MAX_TIME = 500 * MAX_CITIES
INIT_PHEROMONE = 1.0 / MAX_CITIES

MAX_ANTS = MAX_CITIES * MAX_CITIES
ALPHA = 1  # Вес фермента
BETA = 5  # Коэффициент эвристики
RHO = 0.5  # Интенсивность
QVAL = 100  # Кол-во феромонов на один проход


class Ant(object):

    def __init__(self, start_city):
        self.cur_city = start_city
        self.path = [start_city]
        self.tour_length = 0.

    def move_to_city(self, city):
        global DISTANCE, MAX_CITIES
        self.path.append(city)
        self.tour_length += int(DISTANCE[self.cur_city][city])
        if len(self.path) == MAX_CITIES:
            self.tour_length += int(DISTANCE[self.path[-1]][self.path[0]])
        self.cur_city = city

    def can_move(self):
        global MAX_CITIES
        return len(self.path) < MAX_CITIES

    def reset(self, city):
        self.cur_city = city
        self.path = [city]
        self.tour_length = 0.


def get_random(l):
    r = random()
    cur_probability = 0
    cur_val = None

    for val, probability in l:
        cur_val = val
        cur_probability += probability
        if r <= cur_probability:
            break

    return cur_val


ANTS = []
DISTANCE = []
PHEROMONE = []
BEST = 1000
BEST_ANT = None


def init():
    global DISTANCE, PHEROMONE, ANTS

    for i in range(MAX_CITIES):
        DISTANCE.append([0.] * MAX_CITIES)
        PHEROMONE.append([INIT_PHEROMONE] * MAX_CITIES)

    # получаем расстояния
    for i in range(MAX_CITIES):
        DISTANCE[i] = input().split(' ')

    # создаем муравьев
    to = 0
    for i in range(MAX_ANTS):
        ANTS.append(Ant(to))
        to += 1
        to = to % MAX_CITIES


def ant_product(from_city, to_city, ph=None):
    global DISTANCE, PHEROMONE, ALPHA, BETA
    ph = ph or PHEROMONE[from_city][to_city]
    return (ph ** ALPHA) * \
           ((1. / int(DISTANCE[from_city][to_city])) ** BETA)


def select_next_city(ant):
    global MAX_CITIES, PHEROMONE, DISTANCE
    denom = 0.
    not_visited = []

    for to in range(MAX_CITIES):
        if to not in ant.path:
            ap = ant_product(ant.cur_city, to)
            not_visited.append((to, ap))
            denom += ap

    assert not_visited
    not_visited = [(val, ap / denom) for (val, ap) in not_visited]
    to = get_random(not_visited)
    return to


def simulate_ants():  # пускаем муравьев
    global ANTS, MAX_CITIES
    moving = 0

    for ant in ANTS:
        if ant.can_move():
            ant.move_to_city(select_next_city(ant))
            moving += 1

    return moving


def update_trails():
    global MAX_CITIES, PHEROMONE, RHO, INIT_PHEROMONE, ANTS

    # Добавляем новые ферменты
    for ant in ANTS:
        pheromove_amount = QVAL / ant.tour_length

        for i in range(MAX_CITIES):
            if i == MAX_CITIES - 1:
                from_city = ant.path[i]
                to_city = ant.path[0]
            else:
                from_city = ant.path[i]
                to_city = ant.path[i + 1]
            assert from_city != to_city
            PHEROMONE[from_city][to_city] = PHEROMONE[from_city][to_city] * (1 - RHO) + pheromove_amount
            PHEROMONE[to_city][from_city] = PHEROMONE[from_city][to_city]


def restart_ants():
    global ANTS, BEST, BEST_ANT, MAX_CITIES
    to = 0

    for ant in ANTS:
        if ant.tour_length < BEST:
            BEST = ant.tour_length
            BEST_ANT = ant

        ant.reset(to)
        to += 1
        to = to % MAX_CITIES


if __name__ == '__main__':
    init()
    cur_time = 0
    while cur_time < MAX_TIME:
        cur_time += 1

        if simulate_ants() == 0:
            update_trails()
            cur_time != MAX_TIME and restart_ants()

    print(int(BEST_ANT.tour_length))