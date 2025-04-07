import pygame
import random
import time
import heapq
import math

pygame.init()

class ColorManager:
    @staticmethod
    def generate_random_colors(count=1000):
        return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                for _ in range(count)]

    @staticmethod
    def get_hue(rgb):
        r, g, b = rgb
        color = pygame.Color(r, g, b, 255)
        return color.hsva[0]

    @staticmethod
    def get_color_from_value(value, min_val=1, max_val=99):
        ratio = (value - min_val) / (max_val - min_val)
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        b = 0
        return (r, g, b)

class NumberManager:
    @staticmethod
    def generate_random_numbers(count=30):
        return [random.randint(1, 99) for _ in range(count)]

class Visualizer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_rays(self, colors):
        self.screen.fill((0, 0, 0))
        width, height = self.screen.get_size()
        center_x, center_y = width // 2, (height + 200) // 2
        radius = min(width, height) // 4

        pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), radius + 5)
        pygame.draw.circle(self.screen, (234, 210, 222), (center_x, center_y), radius)

        num_rays = len(colors)
        angle_step = 360 / num_rays

        for i, color in enumerate(colors):
            angle = math.radians(i * angle_step)
            end_x = center_x + radius * math.cos(angle)
            end_y = center_y + radius * math.sin(angle)
            pygame.draw.line(self.screen, color, (center_x, center_y), (end_x, end_y), 2)

        pygame.display.flip()

    def draw_number_graph(self, numbers):
        self.screen.fill((0, 0, 0))
        y_offset = self.screen.get_height() - 150
        case_width, spacing = 80, 1
        max_width = self.screen.get_width()
        x_pos, line_y_offset = 20, y_offset

        for i, val in enumerate(numbers[:30]):
            if x_pos + case_width + spacing > max_width:
                x_pos = 20
                line_y_offset += 40
            color = ColorManager.get_color_from_value(val)
            pygame.draw.rect(self.screen, color, pygame.Rect(x_pos, line_y_offset, case_width, 30))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x_pos, line_y_offset, case_width, 30), 2)
            text = self.font.render(f"{val}", True, (255, 255, 255))
            self.screen.blit(text, (x_pos + 5, line_y_offset + 5))
            x_pos += case_width + spacing

        pygame.display.flip()

class SortingAlgorithms:
    def __init__(self, visualizer):
        self.visualizer = visualizer

    # Algorithmes de tri pour les couleurs
    def selection_sort_colors(self, arr):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if ColorManager.get_hue(arr[j]) < ColorManager.get_hue(arr[min_idx]):
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self.visualizer.draw_rays(arr)
            pygame.time.wait(1)
        return arr

    def bubble_sort_colors(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if ColorManager.get_hue(arr[j]) > ColorManager.get_hue(arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            self.visualizer.draw_rays(arr)
            pygame.time.wait(1)
        return arr

    def insertion_sort_colors(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ColorManager.get_hue(key) < ColorManager.get_hue(arr[j]):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            self.visualizer.draw_rays(arr)
            pygame.time.wait(1)
        return arr


    def merge_sort_colors(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort_colors(arr[:mid])
        right = self.merge_sort_colors(arr[mid:])
        return self._merge_colors(left, right)

    def _merge_colors(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if ColorManager.get_hue(left[i]) < ColorManager.get_hue(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        self.visualizer.draw_rays(result)
        pygame.time.wait(1)
        return result

    def quick_sort_colors(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        pivot_hue = ColorManager.get_hue(pivot)
        left = [x for x in arr if ColorManager.get_hue(x) < pivot_hue]
        middle = [x for x in arr if ColorManager.get_hue(x) == pivot_hue]
        right = [x for x in arr if ColorManager.get_hue(x) > pivot_hue]
        result = self.quick_sort_colors(left) + middle + self.quick_sort_colors(right)
        self.visualizer.draw_rays(result)
        pygame.time.wait(1)
        return result

    def heap_sort_colors(self, arr):
        arr_with_hue = [(ColorManager.get_hue(color), color) for color in arr]
        heapq.heapify(arr_with_hue)
        result = [heapq.heappop(arr_with_hue)[1] for _ in range(len(arr_with_hue))]
        self.visualizer.draw_rays(result)
        pygame.time.wait(1)
        return result

    def comb_sort_colors(self, arr):
        gap = len(arr)
        swapped = True
        while gap != 1 or swapped:
            gap = max(1, int(gap / 1.3))
            swapped = False
            for i in range(len(arr) - gap):
                if ColorManager.get_hue(arr[i]) > ColorManager.get_hue(arr[i + gap]):
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swapped = True
            self.visualizer.draw_rays(arr)
            pygame.time.wait(1)
        return arr

    # Algorithmes de tri pour les nombres
    def selection_sort_numbers(self, arr):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self.visualizer.draw_number_graph(arr)
            pygame.time.wait(1000)
        return arr

    def bubble_sort_numbers(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            self.visualizer.draw_number_graph(arr)
            pygame.time.wait(1000)
        return arr

    def insertion_sort_numbers(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            self.visualizer.draw_number_graph(arr)
            pygame.time.wait(1000)
        return arr

    def merge_sort_numbers(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort_numbers(arr[:mid])
        right = self.merge_sort_numbers(arr[mid:])
        merged = self._merge_numbers(left, right)
        self.visualizer.draw_number_graph(merged)
        pygame.time.wait(1000)
        return merged

    def _merge_numbers(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def quick_sort_numbers(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        result = self.quick_sort_numbers(left) + middle + self.quick_sort_numbers(right)
        self.visualizer.draw_number_graph(result)
        pygame.time.wait(1000)
        return result

    def heap_sort_numbers(self, arr):
        heapq.heapify(arr)
        sorted_arr = [heapq.heappop(arr) for _ in range(len(arr))]
        self.visualizer.draw_number_graph(sorted_arr)
        pygame.time.wait(1000)
        return sorted_arr

    def comb_sort_numbers(self, arr):
        gap = len(arr)
        swapped = True
        while gap != 1 or swapped:
            gap = max(1, int(gap / 1.3))
            swapped = False
            for i in range(len(arr) - gap):
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swapped = True
            self.visualizer.draw_number_graph(arr)
            pygame.time.wait(1000)
        return arr

class Interface:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 740))
        pygame.display.set_caption("Tri Interactif")
        self.font = pygame.font.SysFont('Arial', 20)
        self.visualizer = Visualizer(self.screen, self.font)
        self.sorting = SortingAlgorithms(self.visualizer)
        self.mode = "couleurs"
        self.data = ColorManager.generate_random_colors()
        self.algorithm_times = {}
        self.result_text = ""

        self.algorithms = [
            ("Tri par sélection", self.sorting.selection_sort_colors, self.sorting.selection_sort_numbers),
            ("Tri à bulles", self.sorting.bubble_sort_colors, self.sorting.bubble_sort_numbers),
            ("Tri par insertion", self.sorting.insertion_sort_colors, self.sorting.insertion_sort_numbers),
            ("Tri fusion", self.sorting.merge_sort_colors, self.sorting.merge_sort_numbers),
            ("Tri rapide", self.sorting.quick_sort_colors, self.sorting.quick_sort_numbers),
            ("Tri par tas", self.sorting.heap_sort_colors, self.sorting.heap_sort_numbers),
            ("Tri à peigne", self.sorting.comb_sort_colors, self.sorting.comb_sort_numbers),
            ("Réinitialiser", lambda x: self.reset(), lambda x: self.reset())
        ]
        self.rects = [pygame.Rect(10, 20 + i * 60, 200, 50) for i in range(len(self.algorithms))]
        self.mode_rects = [pygame.Rect(320, 20, 150, 50), pygame.Rect(480, 20, 150, 50)]

    def reset(self):
        if self.mode == "couleurs":
            self.data = ColorManager.generate_random_colors()
        else:
            self.data = NumberManager.generate_random_numbers()
        self.result_text = ""
        self.algorithm_times = {}

    def detect_click(self, x, y, width, height, pos):
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            if self.mode == "couleurs":
                self.visualizer.draw_rays(self.data)
            else:
                self.visualizer.draw_number_graph(self.data)

            for i, (name, _, _) in enumerate(self.algorithms):
                pygame.draw.rect(self.screen, (100, 100, 255), self.rects[i])
                text = self.font.render(name, True, (255, 255, 255))
                self.screen.blit(text, (self.rects[i].x + 10, self.rects[i].y + 10))

            pygame.draw.rect(self.screen, (100, 255, 100), self.mode_rects[0])
            pygame.draw.rect(self.screen, (100, 255, 100), self.mode_rects[1])
            text_colors = self.font.render("Tri de couleurs", True, (255, 0, 0))
            text_numbers = self.font.render("Tri de nombres", True, (255, 0, 0))
            self.screen.blit(text_colors, (self.mode_rects[0].x + 10, self.mode_rects[0].y + 10))
            self.screen.blit(text_numbers, (self.mode_rects[1].x + 10, self.mode_rects[1].y + 10))

            if self.algorithm_times:
                sorted_times = sorted(self.algorithm_times.items(), key=lambda x: x[1])
                y_offset = 120
                for name, t in sorted_times:
                    text = self.font.render(f"{name}: {t:.4f} ms", True, (255, 255, 255))
                    self.screen.blit(text, (550, y_offset))
                    y_offset += 20

            if self.result_text:
                text_result = self.font.render(f"Temps d'exécution: {self.result_text} ms", True, (255, 255, 255))
                text_width = self.font.size(f"Temps d'exécution: {self.result_text} ms")[0]
                self.screen.blit(text_result, ((self.screen.get_width() - text_width) // 2, self.screen.get_height() - 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.detect_click(self.mode_rects[0].x, self.mode_rects[0].y, 150, 50, event.pos):
                        self.mode = "couleurs"
                        self.reset()
                    elif self.detect_click(self.mode_rects[1].x, self.mode_rects[1].y, 150, 50, event.pos):
                        self.mode = "nombres"
                        self.reset()
                    for idx, rect in enumerate(self.rects):
                        if self.detect_click(rect.x, rect.y, rect.width, rect.height, event.pos):
                            name, color_sort, num_sort = self.algorithms[idx]
                            algo = color_sort if self.mode == "couleurs" else num_sort
                            if name == "Réinitialiser":
                                self.reset()
                            else:
                                start = time.time()
                                self.data = algo(self.data)
                                elapsed = (time.time() - start) * 1000
                                self.result_text = f"{elapsed:.2f}"
                                self.algorithm_times[name] = elapsed
                            break

            pygame.time.wait(1000)

