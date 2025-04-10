import pygame
import random
import heapq
import math
import time
import string
import tracemalloc


pygame.init()

class ColorManager:
    @staticmethod
    def generate_random_colors(count=500):
        return {(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                for _ in range(count)} - {(0, 0, 0), (255, 255, 255)}

    @staticmethod
    def get_hue(rgb):
        return pygame.Color(*rgb).hsva[0]

    @staticmethod
    def get_color_from_value(value, min_val=1, max_val=26):
        ratio = (value - min_val) / (max_val - min_val) if max_val != min_val else 0
        return (int(255 * (1 - ratio)), int(255 * ratio), 0)

class NumberManager:
    @staticmethod
    def generate_random_numbers(count=50):
        return random.sample(range(1, 100), min(count, 99))

class WordManager:
    @staticmethod
    def generate_random_words(count=36):
        words = set()
        while len(words) < min(count, 36):
            length = random.randint(3, 6)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.add(word)
        return list(words)

class Visualizer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.width, self.height = screen.get_size()
        self.center = (self.width // 2, (self.height + 200) // 2)
        self.radius = min(self.width, self.height) // 5
        self.small_font = pygame.font.SysFont('Arial', 14)  # Police plus petite


    def draw_rays(self, colors):
        self.screen.fill((30, 30, 30))
        pygame.draw.circle(self.screen, (200, 200, 200), self.center, self.radius + 5)
        pygame.draw.circle(self.screen, (234, 210, 222), self.center, self.radius)
        colors_list = list(colors)
        if not colors_list:
            return
        angle_step = 360 / len(colors_list)
        for i, color in enumerate(colors_list):
            angle = math.radians(i * angle_step)
            end = (self.center[0] + self.radius * math.cos(angle), 
                   self.center[1] + self.radius * math.sin(angle))
            pygame.draw.line(self.screen, color, self.center, end, 2)

    def draw_number_graph(self, numbers):
        self.screen.fill((30, 30, 30))
        if not numbers:
            return  # Rien à dessiner si la liste est vide

        max_height = 300
        base_y = self.height - 100

        count = len(numbers)
        total_spacing = 10 * (count - 1)
        max_bar_width = (self.width - 100 - total_spacing) // count
        bar_width = max(4, min(20, max_bar_width))
        spacing = 10

        min_val = min(numbers) if numbers else 1
        max_val = max(numbers) if numbers else 99

        for i, val in enumerate(numbers):
            bar_height = int((val - min_val) / (max_val - min_val + 1e-6) * max_height)
            x = 50 + i * (bar_width + spacing)
            y = base_y - bar_height
            color = ColorManager.get_color_from_value(val, min_val, max_val)

            pygame.draw.rect(self.screen, color, (x, y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, bar_width, bar_height), 2)

            if bar_width > 10:  # Affiche le texte si la barre est assez large
                text = self.small_font.render(str(val), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + bar_width // 2, y - 15))
                self.screen.blit(text, text_rect)

    def draw_word_graph(self, words):
        self.screen.fill((40, 40, 40))
        y_offset = self.height - 150
        cell_width, spacing = 100, 1
        x_pos, line_y = 20, y_offset
        for i, word in enumerate(words[:36]):
            if x_pos + cell_width + spacing > self.width:
                x_pos, line_y = 20, line_y + 40
            val = ord(word[0]) - ord('a') + 1 if word else 1
            color = ColorManager.get_color_from_value(val, 1, 26)
            rect = pygame.Rect(x_pos, line_y, cell_width, 35)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
            text = self.font.render(word, True, (255, 255, 255))
            self.screen.blit(text, (x_pos + 5, line_y + 7))
            x_pos += cell_width + spacing

class SortingAlgorithms:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.sorting = False
        self.sort_iterator = None

    def _visualize(self, arr, mode="colors"):
        if mode == "colors":
            self.visualizer.draw_rays(arr)
        elif mode == "numbers":
            self.visualizer.draw_number_graph(arr)
        else:  # words
            self.visualizer.draw_word_graph(arr)

    def selection_sort(self, arr, mode="colors"):
        arr = list(arr)
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                val_j = ColorManager.get_hue(arr[j]) if mode == "colors" else arr[j]
                val_min = ColorManager.get_hue(arr[min_idx]) if mode == "colors" else arr[min_idx]
                if val_j < val_min:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr

    def bubble_sort(self, arr, mode="colors"):
        arr = list(arr)
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                val_j = ColorManager.get_hue(arr[j]) if mode == "colors" else arr[j]
                val_j1 = ColorManager.get_hue(arr[j + 1]) if mode == "colors" else arr[j + 1]
                if val_j > val_j1:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
            yield arr

    def insertion_sort(self, arr, mode="colors"):
        arr = list(arr)
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            key_val = ColorManager.get_hue(key) if mode == "colors" else key
            while j >= 0 and (ColorManager.get_hue(arr[j]) if mode == "colors" else arr[j]) > key_val:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            yield arr



    def merge_sort(self, arr, mode="colors"):
        arr = list(arr)

        def merge_sort_recursive(sub_arr):
            if len(sub_arr) <= 1:
                return sub_arr

            mid = len(sub_arr) // 2
            left = merge_sort_recursive(sub_arr[:mid])
            right = merge_sort_recursive(sub_arr[mid:])

            return merge(left, right)

        def merge(left, right):
            merged = []
            i = j = 0

            while i < len(left) and j < len(right):
                left_val = ColorManager.get_hue(left[i]) if mode == "colors" else left[i]
                right_val = ColorManager.get_hue(right[j]) if mode == "colors" else right[j]

                if left_val <= right_val:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1

            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged

        # Recopie dans une copie de l'array et fait du yield à chaque fusion
        def merge_sort_with_yield(sub_arr):
            if len(sub_arr) <= 1:
                yield sub_arr
                return sub_arr

            mid = len(sub_arr) // 2
            left = sub_arr[:mid]
            right = sub_arr[mid:]

            left = yield from merge_sort_with_yield(left)
            right = yield from merge_sort_with_yield(right)

            merged = []
            i = j = 0

            while i < len(left) and j < len(right):
                left_val = ColorManager.get_hue(left[i]) if mode == "colors" else left[i]
                right_val = ColorManager.get_hue(right[j]) if mode == "colors" else right[j]

                if left_val <= right_val:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1

            merged.extend(left[i:])
            merged.extend(right[j:])

            # Générer l'état intermédiaire
            yield merged
            return merged

        yield from merge_sort_with_yield(arr)
    
    

    def quick_sort(self, arr, mode="colors"):
        arr = list(arr)
        if len(arr) <= 1:
            yield arr
            return
        pivot = arr[len(arr) // 2]
        pivot_val = ColorManager.get_hue(pivot) if mode == "colors" else pivot
        left = []
        middle = []
        right = []
        for x in arr:
            x_val = ColorManager.get_hue(x) if mode == "colors" else x
            if x_val < pivot_val:
                left.append(x)
            elif x_val == pivot_val:
                middle.append(x)
            else:
                right.append(x)
        
        yield from self.quick_sort(left, mode)
        yield from self.quick_sort(right, mode)
        yield left + middle + right

    def heap_sort(self, arr, mode="colors"):
        arr = list(arr)
        if mode == "colors":
            arr_with_hue = [(ColorManager.get_hue(color), color) for color in arr]
            heapq.heapify(arr_with_hue)
            result = []
            while arr_with_hue:
                result.append(heapq.heappop(arr_with_hue)[1])
        else:
            heapq.heapify(arr)
            result = []
            while arr:
                result.append(heapq.heappop(arr))
        yield result

    def comb_sort(self, arr, mode="colors"):
        arr = list(arr)
        gap = len(arr)
        swapped = True
        while gap != 1 or swapped:
            gap = max(1, int(gap / 1.3))
            swapped = False
            for i in range(len(arr) - gap):
                val_i = ColorManager.get_hue(arr[i]) if mode == "colors" else arr[i]
                val_igap = ColorManager.get_hue(arr[i + gap]) if mode == "colors" else arr[i + gap]
                if val_i > val_igap:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swapped = True
            yield arr

    def start_sort(self, algorithm, data, mode):
        self.sorting = True
        self.sort_iterator = algorithm(data, mode)

class Interface:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Visualisation des Algorithmes de Tri")
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.medium_font = pygame.font.SysFont('Arial', 16, bold=True)
        self.visualizer = Visualizer(self.screen, self.font)
        self.sorting = SortingAlgorithms(self.visualizer)
        self.mode = "colors"
        self.data = ColorManager.generate_random_colors()
        self.algorithm_times = {}
        self.running = False
        self.last_update = time.time()
        self.update_interval = 0.05

        self.algorithms = [
            ("Tri par sélection", self.sorting.selection_sort),
            ("Tri à bulles", self.sorting.bubble_sort),
            ("Tri par insertion", self.sorting.insertion_sort),
            ("Tri fusion", self.sorting.merge_sort),
            ("Tri rapide", self.sorting.quick_sort),
            ("Tri par tas", self.sorting.heap_sort),
            ("Tri à peigne", self.sorting.comb_sort),
            ("Réinitialiser", lambda x, mode: self.reset())
        ]

        self.choose_button = pygame.Rect(10, 50, 250, 60)
        self.dropdown_open = False
        self.selected_algorithm = 0
        self.dropdown_options = [pygame.Rect(10, 110 + i * 60, 250, 60) 
                              for i in range(len(self.algorithms))]
        self.mode_buttons = [
            pygame.Rect(300, 50, 200, 60),  # Couleurs
            pygame.Rect(510, 50, 200, 60),  # Nombres
            pygame.Rect(720, 50, 200, 60)   # Mots
        ]

    def reset(self):
        self.running = False
        self.sorting.sorting = False
        if self.mode == "colors":
            self.data = ColorManager.generate_random_colors()
        elif self.mode == "numbers":
            self.data = NumberManager.generate_random_numbers()
        else:  # words
            self.data = WordManager.generate_random_words()
        self.algorithm_times.clear()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not self.running:
                    pos = pygame.mouse.get_pos()
                    if self.choose_button.collidepoint(pos):
                        self.dropdown_open = not self.dropdown_open
                    elif self.dropdown_open:
                        for i, rect in enumerate(self.dropdown_options):
                            if rect.collidepoint(pos):
                                self.dropdown_open = False
                                self.selected_algorithm = i
                                name, algo = self.algorithms[i]
                                if name != "Réinitialiser":
                                    self.running = True
                                    self.start_time = time.time()
                                    tracemalloc.start()  # Démarrer le traqueur mémoire
                                    self.sorting.start_sort(algo, self.data, self.mode)
                                else:
                                    algo(None, None)
                    for i, btn in enumerate(self.mode_buttons):
                        if btn.collidepoint(pos):
                            self.mode = ["colors", "numbers", "words"][i]
                            self.reset()

            if self.running and self.sorting.sorting:
                current_time = time.time()
                if current_time - self.last_update >= self.update_interval:
                    try:
                        self.data = next(self.sorting.sort_iterator)
                        self.last_update = current_time
                    except StopIteration:
                        self.running = False
                        self.sorting.sorting = False
                        algo_name = self.algorithms[self.selected_algorithm][0]
                        duration_ms = (time.time() - self.start_time) * 1000
                        current, peak = tracemalloc.get_traced_memory()
                        tracemalloc.stop()
                        self.algorithm_times[algo_name] = (duration_ms, peak / 1024)  # en Ko


            self.sorting._visualize(self.data, self.mode)
            self._draw_ui()
            pygame.display.flip()
            clock.tick(60)

    def _draw_ui(self):
        pygame.draw.rect(self.screen, 
                        (60, 60, 200) if not self.choose_button.collidepoint(pygame.mouse.get_pos()) 
                        else (80, 80, 255), self.choose_button, border_radius=10)
        text = self.font.render("Choisir le tri", True, (255, 255, 255))
        self.screen.blit(text, (self.choose_button.x + 20, self.choose_button.y + 15))

        if self.dropdown_open:
            for i, rect in enumerate(self.dropdown_options):
                color = (80, 80, 255) if rect.collidepoint(pygame.mouse.get_pos()) else (60, 60, 200)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                text = self.font.render(self.algorithms[i][0], True, (255, 255, 255))
                self.screen.blit(text, (rect.x + 20, rect.y + 15))

        for i, btn in enumerate(self.mode_buttons):
            color = (80, 255, 80) if btn.collidepoint(pygame.mouse.get_pos()) else (60, 200, 60)
            pygame.draw.rect(self.screen, color, btn, border_radius=10)
            label = ["Couleurs", "Nombres", "Mots"][i]
            text = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(text, (btn.x + 20, btn.y + 15))

        for i, (name, (t, mem)) in enumerate(sorted(self.algorithm_times.items(), key=lambda x: x[1][0] if x[1] else float('inf'))):
            time_str = f"{t:.2f} ms" if t is not None else "En cours..."
            mem_str = f"{mem:.1f} Ko" if mem is not None else ""
            text = self.medium_font.render(f"{name}: Temps: {time_str} | Mémoire:  {mem_str}", True, (200, 200, 255))
            self.screen.blit(text, (800, 120 + i * 28))