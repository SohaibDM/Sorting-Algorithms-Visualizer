import math
import pygame
import random
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = BLACK

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Algorithm Visualization')
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD )/ len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, ((draw_info.width - title.get_width()) / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.WHITE)
    draw_info.window.blit(controls, ((draw_info.width - controls.get_width())/2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Q - Quick Sort", 1,draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - ( val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color,(x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num2 > num1 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_idx = i
        if (ascending):
            for j in range(i + 1, len(lst)):
                if lst[j] < lst[min_idx]:
                    min_idx = j
        if (not ascending):
            for j in range(i + 1, len(lst)):
                if lst[j] > lst[min_idx]:
                    min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
        yield True

    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    low = 0
    high = len(lst) - 1
    yield from quick_sort_recursive(lst, low, high, draw_info, ascending)

def quick_sort_recursive( lst, low, high, draw_info, ascending):
        if low < high:
            gen = partition(lst, low, high, draw_info, ascending)
            while True:
                try:
                    pi = next(gen)
                except StopIteration as e:
                    pi = e.value
                    break
                yield True

            yield from quick_sort_recursive( lst, low, pi-1, draw_info, ascending)
            yield from quick_sort_recursive(lst, pi+1, high, draw_info, ascending)
            yield True


def partition(lst, low, high, draw_info, ascending = True):
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
    yield True

    return i + 1


def main():
    run = True
    clock = pygame.time.Clock()

    n= 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    low = 0
    high = len(lst) - 1
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_gen = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sorting_algorithm_gen)
                pygame.time.delay(20)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_gen = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and sorting == False:
                ascending = True

            elif event.key == pygame.K_d and sorting == False:
                ascending = False

            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"

            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"

            elif event.key == pygame.K_s and sorting == False:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

            elif event.key == pygame.K_q and sorting == False:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick Sort"
    pygame.quit()

if __name__ == '__main__':
    main()