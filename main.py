import sys
import random
import itertools
import numpy as np
import cv2 as cv


# map
MAP_FILE = "cape_python.png"

# search areas
SEARCH_AREA1 = (130, 265, 180, 315)
SEARCH_AREA2 = (80, 255, 130, 305)
SEARCH_AREA3 = (105, 205, 155, 255)


class Search:
    """
    shipwreck search simulation game
    """
    def __init__(self, name):
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print(f"There is no map {MAP_FILE}", file=sys.stderr)
            sys.exit(1)

        self.area_actual = 0
        # sailors location
        self.sailor_actual = [0, 0]
        # search area coordinates
        self.sa1 = self.img[SEARCH_AREA1[1]: SEARCH_AREA1[3], SEARCH_AREA1[0]: SEARCH_AREA1[2]]
        self.sa2 = self.img[SEARCH_AREA2[1]: SEARCH_AREA2[3], SEARCH_AREA2[0]: SEARCH_AREA2[2]]
        self.sa3 = self.img[SEARCH_AREA3[1]: SEARCH_AREA3[3], SEARCH_AREA3[0]: SEARCH_AREA3[2]]

        # probability for areas
        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        # probability of successful search
        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0

    def draw_map(self, last_known):
        """show map"""
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.img, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50 mil morskich', (71, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv.rectangle(self.img, (SEARCH_AREA1[0], SEARCH_AREA1[1]), (SEARCH_AREA1[2], SEARCH_AREA1[3]), (0, 0, 0), 1)
        cv.putText(self.img, '1', (SEARCH_AREA1[0] + 3, SEARCH_AREA1[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.rectangle(self.img, (SEARCH_AREA2[0], SEARCH_AREA2[1]), (SEARCH_AREA2[2], SEARCH_AREA2[3]), (0, 0, 0), 1)
        cv.putText(self.img, '2', (SEARCH_AREA2[0] + 3, SEARCH_AREA2[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.rectangle(self.img, (SEARCH_AREA3[0], SEARCH_AREA3[1]), (SEARCH_AREA3[2], SEARCH_AREA3[3]), (0, 0, 0), 1)
        cv.putText(self.img, '3', (SEARCH_AREA3[0] + 3, SEARCH_AREA3[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, 0)

        cv.putText(self.img, '+', last_known, cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        cv.putText(self.img, '+ = ostatnia znana lokalizacja', (240, 355), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '* = rzeczywista lokalizacja', (242, 370), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        cv.imshow('Obszar do przeszukania', self.img)
        cv.moveWindow('Obszar do przeszukania', 750, 10)
        cv.waitKey(500)

    def final_sailor_location(self, num_search_areas):
        """return random sailor location  x and y"""
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1], 1)
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0], 1)

        area = int(random.triangular(1, num_search_areas + 1))

        if area == 1:
            x = self.sailor_actual[0] + SEARCH_AREA1[0]
            y = self.sailor_actual[1] + SEARCH_AREA1[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SEARCH_AREA2[0]
            y = self.sailor_actual[1] + SEARCH_AREA2[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SEARCH_AREA3[0]
            y = self.sailor_actual[1] + SEARCH_AREA3[1]
            self.area_actual = 3
        return x, y

    def calc_search_effectiveness(self):
        """sets a value that represents the effectiveness of the search"""
        self.sep1 = random.uniform(0.2, 0.9)
        self.sep2 = random.uniform(0.2, 0.9)
        self.sep3 = random.uniform(0.2, 0.9)

    def conduct_search(self, area_num, area_array, effectiveness_prob):
        """returns the search result and a list of coordinates"""
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        coords = list(itertools.product(local_x_range, local_y_range))
        random.shuffle(coords)
        coords = coords[:int((len(coords) * effectiveness_prob))]
        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_num == self.area_actual and loc_actual in coords:
            return f"Znaleziono w obszarze nr {area_num}", coords
        else:
            return f"Nie znaleziono", coords

    def revise_target_probs(self):
        """method updates probability for each area (bayes theorem)"""
        denomination = self.p1 * (1 - self.sep1) + self.p2 * (1 - self.sep2) + self.p3 * (1 - self.sep3)
        self.p1 = self.p1 * (1 - self.sep1) / denomination
        self.p2 = self.p2 * (1 - self.sep2) / denomination
        self.p3 = self.p3 * (1 - self.sep3) / denomination


def draw_menu(search_num):
    """print menu with choices"""
    print(f"\nPodejście numer {search_num}")
    print(
        """
        Wybierz następne obszary do przeszukania:

        0 - Wyjdź z programu
        1 - Przeszukaj dwukrotnie obszar pierwszy
        2 - Przeszukaj dwukrotnie obszar drugi
        3 - Przeszukaj dwukrotnie obszar trzeci
        4 - Przeszukaj obszary pierwszy i drugi
        5 - Przeszukaj obszary pierwszy i trzeci
        6 - Przeszukaj obszary drugi i trzeci
        7 - Zacznij od początku
        """
    )


def main():

    app = Search("cape_python")
    app.draw_map(last_known=(160, 290))
    sailor_x, sailor_y = app.final_sailor_location(num_search_areas=3)
    print("=" * 65)
    print(f"Początkowe prawdopodobieństwo (P):")
    print(f"P1 = {app.p1}, P2 = {app.p2}, P3 = {app.p3}")
    search_num = 1

    while True:
        app.calc_search_effectiveness()
        draw_menu(search_num)
        choice = input("Wybierz opcję: >")

        if choice == "0":
            sys.exit()

        elif choice == "1":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1)
            results_2, coords_2 = app.conduct_search(1, app.sa1, app.sep1)
            app.sep1 = (len(set(coords_1 + coords_2))) / (len(app.sa1)**2)
            app.sep2 = 0
            app.sep3 = 0

        elif choice == "2":
            results_1, coords_1 = app.conduct_search(2, app.sa2, app.sep2)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2)
            app.sep1 = 0
            app.sep2 = (len(set(coords_1 + coords_2))) / (len(app.sa2)**2)
            app.sep3 = 0

        elif choice == "3":
            results_1, coords_1 = app.conduct_search(3, app.sa3, app.sep3)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3)
            app.sep1 = 0
            app.sep2 = 0
            app.sep3 = (len(set(coords_1 + coords_2))) / (len(app.sa3) ** 2)

        elif choice == "4":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2)
            app.sep3 = 0

        elif choice == "5":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3)
            app.sep2 = 0

        elif choice == "6":
            results_1, coords_1 = app.conduct_search(2, app.sa2, app.sep2)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3)
            app.sep1 = 0

        elif choice == "7":
            main()

        else:
            print("zły wybór", file=sys.stderr)
            continue

        app.revise_target_probs()
        print(f"Podejście nr {search_num} - wynik 1: {results_1}", file=sys.stderr)
        print(f"Podejście nr {search_num} - wynik 2: {results_2}", file=sys.stderr)
        print(f"Skuteczność poszukiwań (E) dla podejścia nr {search_num}")
        print(f"E1 = {app.sep1}, E2 = {app.sep2}, E3 = {app.sep3}")

        if results_1 == "Nie znaleziono" and results_2 == "Nie znaleziono":
            print(f"Nowe oszacowanie Prawdopodobieństwa (P)"
                  f"dla podejścia nr. {search_num + 1}")
            print(f"P1 = {app.p1}, P2 = {app.p2}, P3 = {app.p3}")

        else:
            cv.circle(app.img, (sailor_x[0], sailor_y[0]), 3, (255, 0, 0), -1)
            cv.imshow("Obszar do przeszukania", app.img)
            cv.waitKey(1500)
            main()

        search_num += 1


if __name__ == "__main__":
    main()