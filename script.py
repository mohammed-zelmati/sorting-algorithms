# script.py
import pygame
import random
import heapq
import math
import time
import string
import tracemalloc
import os
import json # Added for history logging
from datetime import datetime # Added for history timestamp

# Attempt to import psutil for live memory usage
try:
    import psutil
    psutil_available = True
except ImportError:
    psutil_available = False
    print("--------------------------------------------------------------")
    print("Warning: 'psutil' library not found. Live memory usage unavailable.")
    print("         Install it using: pip install psutil")
    print("--------------------------------------------------------------")

pygame.init()
pygame.mixer.init()

# --- Asset Paths & History Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
HISTORY_DIR = os.path.join(BASE_DIR, 'history') # For JSON logs
COMPARISON_SUMMARY_FILE = os.path.join(HISTORY_DIR, 'comparison_summary.json') # <<< New comparison file path

# --- Helper Functions ---
# (Keep get_font and load_sound as defined previously)
def get_font(font_path, size, default_sys_font='Arial'):
    """Loads a font from path or falls back to system font."""
    try:
        if font_path and os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
        else:
            return pygame.font.SysFont(default_sys_font, size)
    except Exception as e:
        print(f"Error loading font {font_path}: {e}. Using default SysFont.")
        return pygame.font.SysFont(default_sys_font, size)

def load_sound(sound_path):
    """Loads a sound file, handling errors."""
    if not sound_path or not os.path.exists(sound_path): return None
    try: return pygame.mixer.Sound(sound_path)
    except pygame.error as e: print(f"Error loading sound {sound_path}: {e}"); return None

# --- Theme Definitions ---
# (Keep the THEMES dictionary as defined previously)
THEMES = {
    'dark': { 'id': 'dark', 'background': (30, 30, 30), 'text': (230, 230, 230), 'stats_text': (200, 200, 255), 'button_idle': (60, 60, 180), 'button_hover': (80, 80, 220), 'button_text': (255, 255, 255), 'accent': (80, 255, 80), 'accent_hover': (120, 255, 120), 'slider_bar': (50, 50, 50), 'slider_knob': (80, 255, 80), 'tooltip_bg': (240, 240, 240), 'tooltip_text': (10, 10, 10), 'graph_outline': (180, 180, 180), 'help_overlay_bg': (0, 0, 0, 180), 'help_modal_bg': (50, 50, 70), 'help_modal_border': (150, 150, 180), 'font_path': None },
    'light': { 'id': 'light', 'background': (230, 230, 230), 'text': (20, 20, 20), 'stats_text': (0, 0, 100), 'button_idle': (180, 180, 240), 'button_hover': (200, 200, 255), 'button_text': (10, 10, 10), 'accent': (60, 180, 60), 'accent_hover': (80, 220, 80), 'slider_bar': (190, 190, 190), 'slider_knob': (60, 180, 60), 'tooltip_bg': (40, 40, 40), 'tooltip_text': (240, 240, 240), 'graph_outline': (50, 50, 50), 'help_overlay_bg': (200, 200, 200, 180), 'help_modal_bg': (245, 245, 255), 'help_modal_border': (100, 100, 120), 'font_path': None }
}

# --- Data Managers ---
# (Keep ColorManager, NumberManager, WordManager, LetterManager as defined previously)
class ColorManager:
    @staticmethod
    def generate_random_colors(count=100): # Reduced default for better vis
        colors = set(); c=count
        while len(colors) < c: colors.add((random.randint(10, 245), random.randint(10, 245), random.randint(10, 245)))
        return list(colors)
    @staticmethod
    def get_hue(rgb):
        try: return pygame.Color(*rgb).hsva[0]
        except ValueError: return 0

class NumberManager:
    @staticmethod
    def generate_random_numbers(count=50):
        max_val = max(100, count * 2); min_val_gen = 1
        if count == 1: max_val = max(max_val, min_val_gen + 1)
        if count <= 0: return [] # Handle zero count
        safe_count = min(count, max_val) # Prevent sampling more than range allows
        return random.sample(range(min_val_gen, max_val + 1), safe_count)

class WordManager:
    @staticmethod
    def generate_random_words(count=30):
        words = set(); safe_count = min(count, 1000)
        if safe_count <= 0: return []
        while len(words) < safe_count: words.add(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7))))
        return list(words)

class LetterManager:
    @staticmethod
    def generate_random_letters(count=52):
        if count <= 0: return []
        if count <= 26: return random.sample(string.ascii_lowercase, count)
        else: return random.choices(string.ascii_lowercase, k=count)


# --- Visualizer Class ---
# (Keep Visualizer class largely as defined previously, ensuring it uses self.theme)
class Visualizer:
    def __init__(self, screen, fonts, theme):
        self.screen = screen; self.fonts = fonts; self.theme = theme
        self.width, self.height = screen.get_size()
        self.center = (self.width // 2, (self.height + 150) // 2)
        self.radius = min(self.width, self.height - 200) // 3
        self.current_vis_state = []

    def update_theme(self, new_theme): self.theme = new_theme

    def _get_color_from_item(self, item, mode, min_val=None, max_val=None, index=0, total_items=1):
        color = pygame.Color(self.theme.get('text', (200, 200, 200)))
        try:
            if mode == "colors": hue = pygame.Color(*item).hsva[0]; color.hsva = (hue, 100, 100, 100)
            elif mode == "numbers" and min_val is not None and max_val is not None:
                val_range = (max_val - min_val) if max_val != min_val else 1; norm_val = (item - min_val) / val_range
                hue = norm_val * 300; color.hsva = (hue % 360, 90, 95, 100)
            elif mode == "letters":
                char_ord = ord(item.lower()); min_char, max_char = ord('a'), ord('z')
                val_range = (max_char - min_char) if max_char != min_char else 1; norm_val = (char_ord - min_char) / val_range
                hue = norm_val * 360; color.hsva = (hue % 360, 85, 90, 100)
            elif mode == "words" and item:
                char_ord = ord(item[0].lower()); min_char, max_char = ord('a'), ord('z')
                val_range = (max_char - min_char) if max_char != min_char else 1; norm_val = (char_ord - min_char) / val_range
                hue = norm_val * 360; color.hsva = (hue % 360, 75, 85, 100)
        except Exception: pass
        return color

    def _visualize(self, data, mode="colors", theme=None):
        if theme: self.update_theme(theme)
        self.screen.fill(self.theme['background'])
        self.current_vis_state = list(data)
        if not self.current_vis_state: return
        min_val, max_val = None, None
        if mode == "numbers" and self.current_vis_state:
            try:
                numeric_data = [item for item in self.current_vis_state if isinstance(item, (int, float))]
                if numeric_data: min_val, max_val = min(numeric_data), max(numeric_data)
            except TypeError: pass
        if mode == "colors": self.draw_rays(self.current_vis_state, mode)
        elif mode == "numbers": self.draw_number_graph(self.current_vis_state, mode, min_val, max_val)
        elif mode == "words": self.draw_word_graph(self.current_vis_state, mode)
        elif mode == "letters": self.draw_number_graph(self.current_vis_state, mode, is_letters=True)

    def draw_rays(self, data_list, mode):
        n = len(data_list); angle_step = 360 / n
        pygame.draw.circle(self.screen, self.theme.get('graph_outline'), self.center, self.radius + 5, 2)
        pygame.draw.circle(self.screen, self.theme.get('background'), self.center, self.radius)
        for i, item in enumerate(data_list):
            angle = math.radians(i * angle_step - 90); end_x = self.center[0] + self.radius * math.cos(angle); end_y = self.center[1] + self.radius * math.sin(angle)
            line_color = self._get_color_from_item(item, mode, index=i, total_items=n)
            pygame.draw.line(self.screen, line_color, self.center, (end_x, end_y), 2)

    def draw_number_graph(self, data_list, mode, min_val=None, max_val=None, is_letters=False):
        n = len(data_list); graph_area_y_start = 150; graph_area_height = self.height - graph_area_y_start - 100; base_y = graph_area_y_start + graph_area_height
        graph_area_width = self.width - 100; graph_area_x_start = 50; spacing = max(1, int(8 - n * 0.05)); total_spacing = spacing * (n - 1)
        bar_width = (graph_area_width - total_spacing) / n if n > 0 else 10; bar_width = max(2, int(bar_width))
        if is_letters: local_min_val, local_max_val, values = ord('a'), ord('z'), [ord(item.lower()) for item in data_list]
        elif min_val is not None and max_val is not None: local_min_val, local_max_val, values = min_val, max_val, data_list
        else: local_min_val, local_max_val, values = 0, 1, [0] * n
        val_range = (local_max_val - local_min_val) if local_max_val != local_min_val else 1
        for i, value in enumerate(values):
            norm_val = max(0.0, min(1.0, (value - local_min_val) / val_range)); bar_height = max(1, int(norm_val * (graph_area_height - 5)))
            x = graph_area_x_start + i * (bar_width + spacing); y = base_y - bar_height; item = data_list[i]
            color_min = local_min_val if mode == "numbers" else None; color_max = local_max_val if mode == "numbers" else None
            color = self._get_color_from_item(item, mode, color_min, color_max, i, n)
            rect = pygame.Rect(x, y, bar_width, bar_height); pygame.draw.rect(self.screen, color, rect); pygame.draw.rect(self.screen, self.theme.get('graph_outline'), rect, 1)
            if bar_width > 15:
                text = self.fonts['small'].render(str(item), True, self.theme['text']); text_rect = text.get_rect(midbottom=(x + bar_width / 2, y - 3))
                self.screen.blit(text, text_rect)

    def draw_word_graph(self, data_list, mode):
        n = len(data_list); cols = max(1, int(math.sqrt(n * self.width / self.height) * 0.8)); rows = math.ceil(n / cols)
        padding = 20; available_width = self.width - 2 * padding; available_height = self.height - 170 - padding
        cell_width = max(60, (available_width - (cols - 1)) // cols); cell_height = max(30, (available_height - (rows - 1)) // rows)
        start_x = padding + (available_width - cols * cell_width - (cols - 1)) // 2; start_y = 150
        for i, item in enumerate(data_list):
            row = i // cols; col = i % cols; x = start_x + col * (cell_width + 1); y = start_y + row * (cell_height + 1)
            color = self._get_color_from_item(item, mode, index=i, total_items=n); rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(self.screen, color, rect); pygame.draw.rect(self.screen, self.theme.get('graph_outline'), rect, 1)
            text = self.fonts['medium'].render(str(item), True, self.theme['text']); text_rect = text.get_rect(center=rect.center)
            self.screen.set_clip(rect); self.screen.blit(text, text_rect); self.screen.set_clip(None)

# --- Sorting Algorithms Class ---
# (Keep SortingAlgorithms class as defined previously)
class SortingAlgorithms:
    def __init__(self, visualizer): self.visualizer = visualizer; self.sorting = False; self.sort_iterator = None
    def _get_compare_value(self, item, mode):
        try:
            if mode == "colors": return ColorManager.get_hue(item)
            elif mode == "letters": return item.lower()
            return item
        except Exception: return item
    def selection_sort(self, arr, mode="colors"):
        arr = list(arr); n = len(arr)
        for i in range(n):
            min_idx = i; val_min = self._get_compare_value(arr[min_idx], mode)
            for j in range(i + 1, n):
                val_j = self._get_compare_value(arr[j], mode)
                if val_j < val_min: min_idx = j; val_min = self._get_compare_value(arr[min_idx], mode)
            if i != min_idx: arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr
    def bubble_sort(self, arr, mode="colors"):
        arr = list(arr); n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                val_j = self._get_compare_value(arr[j], mode); val_j1 = self._get_compare_value(arr[j + 1], mode)
                if val_j > val_j1: arr[j], arr[j + 1] = arr[j + 1], arr[j]; swapped = True; yield arr
            if not swapped: break
        yield arr
    def insertion_sort(self, arr, mode="colors"):
        arr = list(arr)
        for i in range(1, len(arr)):
            key = arr[i]; key_val = self._get_compare_value(key, mode); j = i - 1
            val_j = self._get_compare_value(arr[j], mode) if j >= 0 else None
            while j >= 0 and val_j > key_val: arr[j + 1] = arr[j]; yield arr; j -= 1; val_j = self._get_compare_value(arr[j], mode) if j >= 0 else None
            arr[j + 1] = key; yield arr
        yield arr
    def merge_sort(self, arr, mode="colors"): arr = list(arr); yield from self._merge_sort_recursive_yield(arr, 0, len(arr), mode)
    def _merge_sort_recursive_yield(self, arr, start, end, mode):
        if end - start <= 1: return arr[start:end]
        mid = start + (end - start) // 2
        left_sorted = yield from self._merge_sort_recursive_yield(arr, start, mid, mode)
        right_sorted = yield from self._merge_sort_recursive_yield(arr, mid, end, mode)
        merged = []; l_idx, r_idx = 0, 0
        while l_idx < len(left_sorted) and r_idx < len(right_sorted):
            left_val = self._get_compare_value(left_sorted[l_idx], mode); right_val = self._get_compare_value(right_sorted[r_idx], mode)
            if left_val <= right_val: merged.append(left_sorted[l_idx]); l_idx += 1
            else: merged.append(right_sorted[r_idx]); r_idx += 1
        merged.extend(left_sorted[l_idx:]); merged.extend(right_sorted[r_idx:])
        arr[start:end] = merged; yield arr; return merged
    def quick_sort(self, arr, mode="colors"): arr = list(arr); yield from self._quick_sort_recursive_yield(arr, 0, len(arr) - 1, mode)
    def _quick_sort_recursive_yield(self, arr, low, high, mode):
        if low < high:
            pi = yield from self._partition_yield(arr, low, high, mode)
            yield from self._quick_sort_recursive_yield(arr, low, pi - 1, mode); yield from self._quick_sort_recursive_yield(arr, pi + 1, high, mode)
    def _partition_yield(self, arr, low, high, mode):
        pivot = arr[high]; pivot_val = self._get_compare_value(pivot, mode); i = low - 1
        for j in range(low, high):
            val_j = self._get_compare_value(arr[j], mode)
            if val_j <= pivot_val: i += 1; arr[i], arr[j] = arr[j], arr[i]; yield arr
        arr[i + 1], arr[high] = arr[high], arr[i + 1]; yield arr; return i + 1
    def heap_sort(self, arr, mode="colors"):
        arr = list(arr); n = len(arr)
        for i in range(n // 2 - 1, -1, -1): yield from self._heapify_yield(arr, n, i, mode)
        for i in range(n - 1, 0, -1): arr[i], arr[0] = arr[0], arr[i]; yield arr; yield from self._heapify_yield(arr, i, 0, mode)
        yield arr
    def _heapify_yield(self, arr, n, i, mode):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        val_largest = self._get_compare_value(arr[largest], mode)
        
        if left < n:
            val_left = self._get_compare_value(arr[left], mode)
            if val_left > val_largest:
                largest = left
                val_largest = self._get_compare_value(arr[largest], mode)
        
        if right < n:
            val_right = self._get_compare_value(arr[right], mode)
            if val_right > val_largest:
                largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr
            yield from self._heapify_yield(arr, n, largest, mode)
    def comb_sort(self, arr, mode="colors"):
        arr = list(arr); n = len(arr); gap = n; shrink = 1.3; swapped = True
        while gap > 1 or swapped:
            gap = max(1, int(gap / shrink)); swapped = False
            for i in range(n - gap):
                val_i = self._get_compare_value(arr[i], mode); val_igap = self._get_compare_value(arr[i + gap], mode)
                if val_i > val_igap: arr[i], arr[i + gap] = arr[i + gap], arr[i]; swapped = True; yield arr
        yield arr
    def start_sort(self, algorithm, data, mode):
        self.sorting = True; data_copy = list(data)
        self.sort_iterator = algorithm(data_copy, mode)
        return self.sort_iterator

# --- Interface Class (Main Application Logic) ---
class Interface:
    def __init__(self):
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Enhanced Sorting Visualizer - Python/Pygame")

        # History Setup
        self.history_folder = HISTORY_DIR
        self.comparison_summary_file = COMPARISON_SUMMARY_FILE # <<< Path to summary file
        if not os.path.exists(self.history_folder):
             try: os.makedirs(self.history_folder); print(f"Created history folder: {self.history_folder}")
             except OSError as e: print(f"Error creating history folder {self.history_folder}: {e}"); self.history_folder = None

        # Theme
        self.current_theme = 'dark'; self.theme = THEMES[self.current_theme]
        # Fonts
        self.fonts = { 'large': get_font(self.theme.get('font_path'), 30, 'Segoe UI'), 'medium': get_font(self.theme.get('font_path'), 20, 'Segoe UI'), 'small': get_font(self.theme.get('font_path'), 16, 'Segoe UI'), 'tooltip': get_font(self.theme.get('font_path'), 14, 'Segoe UI'), 'help_title': get_font(self.theme.get('font_path'), 24, 'Segoe UI Bold'), 'help_text': get_font(self.theme.get('font_path'), 16, 'Segoe UI') }
        # Sounds
        self.sounds = { 'click': load_sound(os.path.join(SOUNDS_DIR, 'click.wav')), 'complete': load_sound(os.path.join(SOUNDS_DIR, 'done.mp3')), 'step': load_sound(os.path.join(SOUNDS_DIR, 'compare.wav')) }
        if self.sounds['click']: self.sounds['click'].set_volume(0.4)
        if self.sounds['complete']: self.sounds['complete'].set_volume(0.6)
        if self.sounds['step']: self.sounds['step'].set_volume(0.2)

        # Core Components
        self.visualizer = Visualizer(self.screen, self.fonts, self.theme)
        self.sorting_handler = SortingAlgorithms(self.visualizer)
        # State Variables
        self.mode = "numbers"; self.data = NumberManager.generate_random_numbers(); self.original_data = list(self.data)
        self.algorithm_times = {}; self.running = False; self.paused = False; self.step_mode = False
        self.current_sort_iterator = None; self.start_time = 0; self.last_update_time = time.time(); self.live_time_ms = 0
        # Speed Control
        self.update_interval = 0.05; self.min_interval = 0.001; self.max_interval = 0.5; self.dragging_slider = False
        # Live Stats
        self.process = psutil.Process(os.getpid()) if psutil_available else None; self.live_memory_usage_kb = 0; self.fps = 0; self.clock = pygame.time.Clock()
        # UI Elements & State
        self.dropdown_open = False; self.hover_rect_id = None; self.hover_start_time = 0; self.tooltip_delay = 600
        self.active_tooltip_text = None; self.ui_elements = {}; self.dropdown_option_rects = []
        self.show_help = False # <<< State for help modal
        self._setup_ui_elements()
        # Algorithms
        self.algorithms = [
            ("Selection Sort", self.sorting_handler.selection_sort, "O(n^2) Time | O(1) Space | Unstable"),
            ("Bubble Sort", self.sorting_handler.bubble_sort, "O(n^2) Time | O(1) Space | Stable"),
            ("Insertion Sort", self.sorting_handler.insertion_sort, "O(n^2) Time | O(1) Space | Stable"),
            ("Merge Sort", self.sorting_handler.merge_sort, "O(n log n) Time | O(n) Space | Stable"),
            ("Quick Sort", self.sorting_handler.quick_sort, "O(n log n) Avg | O(log n) Space | Unstable"),
            ("Heap Sort", self.sorting_handler.heap_sort, "O(n log n) Time | O(1) Space | Unstable"),
            ("Comb Sort", self.sorting_handler.comb_sort, "O(n log n) Avg | O(1) Space | Unstable"),
        ]
        self.selected_algorithm_index = 0

    def _setup_ui_elements(self):
        self.ui_elements['algo_dropdown_btn'] = {'rect': pygame.Rect(10, 10, 250, 40), 'tooltip': "Select Sorting Algorithm"}
        mode_btn_width, mode_btn_height, mode_start_x, mode_spacing = 120, 40, 280, 10
        modes = ["Colors", "Numbers", "Words", "Letters"]
        mode_tooltips = ["Sort RGB colors by Hue", "Sort numbers", "Sort words alphabetically", "Sort letters alphabetically"]
        self.mode_buttons = []
        for i, mode_label in enumerate(modes):
            btn_id = f'mode_btn_{mode_label.lower()}'
            rect = pygame.Rect(mode_start_x + i * (mode_btn_width + mode_spacing), 10, mode_btn_width, mode_btn_height)
            self.ui_elements[btn_id] = {'rect': rect, 'tooltip': mode_tooltips[i], 'label': mode_label}
            self.mode_buttons.append(btn_id)

        # Help Button ('?') - Top Right
        self.ui_elements['help_btn'] = {'rect': pygame.Rect(self.width - 55, 10, 40, 40), 'tooltip': "Help / Info"}
        # Theme Toggle Button - Moved Left slightly
        self.ui_elements['theme_btn'] = {'rect': pygame.Rect(self.ui_elements['help_btn']['rect'].left - 130 - 10, 10, 130, 40), 'tooltip': "Toggle Dark/Light Theme", 'label': "Toggle Theme" }

        # Bottom row controls
        slider_y = 65; bottom_row_y = self.height - 55 # Y position for bottom controls
        self.ui_elements['speed_slider'] = {'rect': pygame.Rect(10, bottom_row_y, 300, 15), 'tooltip': "Adjust visualization speed (Log Scale)"}
        self.ui_elements['speed_knob'] = {'rect': pygame.Rect(0, 0, 12, 25), 'tooltip': "Drag to change speed"}
        self.ui_elements['speed_knob']['rect'].centery = self.ui_elements['speed_slider']['rect'].centery

        self.ui_elements['step_btn'] = {'rect': pygame.Rect(self.ui_elements['speed_slider']['rect'].right + 20, bottom_row_y - 12, 150, 40), 'tooltip': "Toggle Step-by-Step Mode"}
        self.ui_elements['next_step_btn'] = {'rect': pygame.Rect(self.ui_elements['step_btn']['rect'].right + 10, bottom_row_y - 12, 140, 40), 'tooltip': "Advance one sort step (Right Arrow)"}
        self.ui_elements['restart_btn'] = {'rect': pygame.Rect(self.ui_elements['next_step_btn']['rect'].right + 10, bottom_row_y - 12, 120, 40), 'tooltip': "Restart sort with new data (R)"}

        # Help Modal Close Button (relative position, calculated in draw)
        self.ui_elements['help_close_btn'] = {'rect': pygame.Rect(0, 0, 100, 35), 'tooltip': "Close Help"}

        self._update_knob_pos() # Set initial knob position

    # (Keep _update_knob_pos, _update_interval_from_knob, _play_sound, toggle_theme)
    def _update_knob_pos(self):
        slider_rect = self.ui_elements['speed_slider']['rect']; knob_rect = self.ui_elements['speed_knob']['rect']
        safe_interval = max(self.min_interval, min(self.update_interval, self.max_interval))
        log_min = math.log(self.min_interval); log_max = math.log(self.max_interval); log_current = math.log(safe_interval)
        ratio = (log_current - log_min) / (log_max - log_min) if (log_max - log_min) != 0 else 0
        ratio = max(0.0, min(1.0, ratio)); knob_rect.centerx = slider_rect.left + ratio * slider_rect.width
    def _update_interval_from_knob(self):
        slider_rect = self.ui_elements['speed_slider']['rect']; knob_rect = self.ui_elements['speed_knob']['rect']
        ratio = max(0.0, min(1.0, (knob_rect.centerx - slider_rect.left) / slider_rect.width))
        log_min = math.log(self.min_interval); log_max = math.log(self.max_interval)
        log_current = log_min + ratio * (log_max - log_min)
        self.update_interval = max(self.min_interval, min(math.exp(log_current), self.max_interval))
    def _play_sound(self, sound_key):
        if sound_key in self.sounds and self.sounds[sound_key]: self.sounds[sound_key].play()
    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'; self.theme = THEMES[self.current_theme]
        self.fonts = { 'large': get_font(self.theme.get('font_path'), 30, 'Segoe UI'), 'medium': get_font(self.theme.get('font_path'), 20, 'Segoe UI'), 'small': get_font(self.theme.get('font_path'), 16, 'Segoe UI'), 'tooltip': get_font(self.theme.get('font_path'), 14, 'Segoe UI'), 'help_title': get_font(self.theme.get('font_path'), 24, 'Segoe UI Bold'), 'help_text': get_font(self.theme.get('font_path'), 16, 'Segoe UI') }
        self.visualizer.update_theme(self.theme); self._play_sound('click')


    def reset_data(self, play_sound=True): # Added optional sound flag
        """Generates new data based on the current mode and stops sorting."""
        print(f"Resetting data for mode: {self.mode}")
        if self.mode == "colors": self.data = ColorManager.generate_random_colors(count=100)
        elif self.mode == "numbers": self.data = NumberManager.generate_random_numbers(count=50)
        elif self.mode == "words": self.data = WordManager.generate_random_words(count=30)
        elif self.mode == "letters": self.data = LetterManager.generate_random_letters(count=52)
        else: self.data = []
        self.original_data = list(self.data)
        self.stop_sorting_process(clear_times=True)
        if play_sound: self._play_sound('click')

    def stop_sorting_process(self, clear_times=False):
         self.running = False; self.paused = False; self.sorting_handler.sorting = False
         self.current_sort_iterator = None; self.live_time_ms = 0
         if tracemalloc.is_tracing(): tracemalloc.stop()
         if clear_times: self.algorithm_times.clear()

    def start_sorting_process(self):
        if not self.data: print("No data to sort."); return
        self.stop_sorting_process(clear_times=False)
        algo_name, algo_func, _ = self.algorithms[self.selected_algorithm_index]
        print(f"Starting sort: {algo_name} ({self.mode})")
        self.original_data = list(self.data)
        tracemalloc.start()
        self.start_time = time.time(); self.live_time_ms = 0; self.last_update_time = self.start_time
        self.current_sort_iterator = self.sorting_handler.start_sort(algo_func, self.data, self.mode)
        self.running = True; self.paused = self.step_mode
        # Don't play click sound here, it's played by the action triggering this

    def restart_current_sort(self):
        print("Restarting sort...")
        self.stop_sorting_process(clear_times=True)
        self.reset_data(play_sound=False) # Generate new data without click sound
        self.start_sorting_process() # Start same algorithm
        self._play_sound('click') # Play sound after restart initiated

    # --- History Logging ---
    def _save_history(self, algo_name, duration_ms, peak_mem_kb):
        """Saves the sort result to an individual JSON file."""
        if not self.history_folder: return

        timestamp_obj = datetime.now()
        timestamp_str = timestamp_obj.strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"sort_{algo_name.replace(' ', '_')}_{self.mode}_{timestamp_str}.json"
        filepath = os.path.join(self.history_folder, filename)

        data_repr = { "count": len(self.original_data), "first_5": self.original_data[:5], "last_5": self.original_data[-5:] }
        history_entry = {
            "timestamp_iso": timestamp_obj.isoformat(), # Store ISO format too
            "algorithm": algo_name, "data_type": self.mode, "data_details": data_repr,
            "time_ms": round(duration_ms, 3), "memory_peak_kb": round(peak_mem_kb, 2)
        }
        try:
            with open(filepath, 'w') as f: json.dump(history_entry, f, indent=4)
            print(f"Saved history to: {filename}")
            # --- Trigger summary update ---
            self._update_comparison_summary(history_entry) # <<< Call summary update
        except Exception as e: print(f"Error saving history to {filepath}: {e}")

    def _update_comparison_summary(self, history_entry): # <<< New method
        """Reads, updates, and writes the comparison_summary.json file."""
        if not self.history_folder: return

        summary_data = {}
        try:
            # Read existing summary file if it exists
            if os.path.exists(self.comparison_summary_file):
                with open(self.comparison_summary_file, 'r') as f:
                    summary_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Warning: Could not read or decode {self.comparison_summary_file}. Starting fresh. Error: {e}")
            summary_data = {} # Start fresh if file is corrupted or doesn't exist

        # Ensure the structure is a dictionary
        if not isinstance(summary_data, dict):
            print(f"Warning: {self.comparison_summary_file} does not contain a dictionary. Starting fresh.")
            summary_data = {}

        # Prepare the new record for the summary (subset of history_entry)
        summary_record = {
            "algorithm": history_entry['algorithm'],
            "time_ms": history_entry['time_ms'],
            "memory_kb": history_entry['memory_peak_kb'],
            "timestamp": history_entry['timestamp_iso'] # Use ISO timestamp
        }

        # Get the list for the current data type, creating it if it doesn't exist
        data_type_key = history_entry['data_type']
        if data_type_key not in summary_data:
             summary_data[data_type_key] = []
        elif not isinstance(summary_data[data_type_key], list):
             print(f"Warning: Data type key '{data_type_key}' in summary is not a list. Replacing.")
             summary_data[data_type_key] = [] # Replace if not a list


        # Append the new record
        summary_data[data_type_key].append(summary_record)

        # Write the updated data back to the summary file
        try:
            with open(self.comparison_summary_file, 'w') as f:
                json.dump(summary_data, f, indent=2) # Use indent 2 for summary
        except Exception as e:
            print(f"Error writing updated summary to {self.comparison_summary_file}: {e}")


    def advance_sort_step(self):
        if not self.running or not self.current_sort_iterator: return False
        try:
            next_data = next(self.current_sort_iterator)
            if next_data is not None: self.data = next_data
            self.last_update_time = time.time()
            self._play_sound('step')
            return True
        except StopIteration:
            duration_ms = (time.time() - self.start_time) * 1000
            peak_mem_kb = 0
            try:
                if tracemalloc.is_tracing(): current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop(); peak_mem_kb = peak / 1024
            except ValueError: pass
            finally:
                 if tracemalloc.is_tracing(): tracemalloc.stop()
            algo_name = self.algorithms[self.selected_algorithm_index][0]
            self.algorithm_times[algo_name] = (duration_ms, peak_mem_kb)
            print(f"Sort {algo_name} finished: {duration_ms:.2f} ms, Peak Mem: {peak_mem_kb:.1f} Ko")
            self._save_history(algo_name, duration_ms, peak_mem_kb) # <<< Saves history & updates summary
            self._play_sound('complete')
            self.running = True; self.paused = True; self.sorting_handler.sorting = False; self.current_sort_iterator = None
            return False
        except Exception as e:
            print(f"Error during sort step: {e}")
            self.stop_sorting_process()
            return False

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        current_hover_id = None; tooltip_candidate = None

        # --- Check Hover ---
        # Prioritize help modal close button if help is shown
        if self.show_help:
            close_btn_info = self.ui_elements['help_close_btn']
            if close_btn_info['rect'].collidepoint(mouse_pos):
                 current_hover_id = 'help_close_btn'
                 tooltip_candidate = close_btn_info.get('tooltip')
        # Check other elements only if help is not shown or close wasn't hovered
        if not current_hover_id:
            element_ids_in_draw_order = list(self.ui_elements.keys())
            element_ids_in_draw_order.reverse()
            for element_id in element_ids_in_draw_order:
                if element_id == 'help_close_btn': continue # Already checked
                # Skip irrelevant buttons based on state
                if element_id == 'restart_btn' and not self.running: continue
                if element_id == 'next_step_btn' and not (self.step_mode and self.running and self.sorting_handler.sorting): continue
                if element_id in self.ui_elements: # Check if key exists
                    info = self.ui_elements[element_id]
                    if info['rect'].collidepoint(mouse_pos):
                        current_hover_id = element_id; tooltip_candidate = info.get('tooltip', ''); break
            if not current_hover_id and self.dropdown_open:
                for i, rect in enumerate(self.dropdown_option_rects):
                    if rect.collidepoint(mouse_pos): current_hover_id = f'dropdown_opt_{i}'; tooltip_candidate = self.algorithms[i][2]; break

        # --- Tooltip Timing ---
        now = pygame.time.get_ticks()
        if current_hover_id is not None and current_hover_id == self.hover_rect_id:
            if now - self.hover_start_time >= self.tooltip_delay: self.active_tooltip_text = tooltip_candidate
            else: self.active_tooltip_text = None
        elif current_hover_id is not None: self.hover_rect_id = current_hover_id; self.hover_start_time = now; self.active_tooltip_text = None
        else: self.hover_rect_id = None; self.active_tooltip_text = None

        # --- Event Loop ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # --- Handle Help Modal Click ---
                    if self.show_help:
                         close_btn_info = self.ui_elements['help_close_btn']
                         if close_btn_info['rect'].collidepoint(mouse_pos):
                              self.show_help = False # Close help modal
                              self.paused = False # Unpause sorting if it was paused by help
                              self._play_sound('click')
                         # Ignore other clicks when help is shown
                         continue # Skip rest of click handling

                    # --- Find clicked element (if help not shown) ---
                    # (Keep the logic for finding clicked_element_id as before)
                    clicked_element_id = None
                    if self.dropdown_open: # Check dropdown first
                         for i, rect in enumerate(self.dropdown_option_rects):
                              if rect.collidepoint(mouse_pos): clicked_element_id = f'dropdown_opt_{i}'; break
                    if not clicked_element_id: # Check other elements
                        for element_id in element_ids_in_draw_order:
                             if element_id == 'help_close_btn': continue # Skip
                             if element_id == 'restart_btn' and not self.running: continue
                             if element_id == 'next_step_btn' and not (self.step_mode and self.running and self.sorting_handler.sorting): continue
                             if element_id in self.ui_elements:
                                  info = self.ui_elements[element_id]
                                  if info['rect'].collidepoint(mouse_pos): clicked_element_id = element_id; break


                    # --- Handle Clicks ---
                    if clicked_element_id == 'algo_dropdown_btn': self.dropdown_open = not self.dropdown_open; self._play_sound('click')
                    elif clicked_element_id and clicked_element_id.startswith('dropdown_opt_'):
                        index = int(clicked_element_id.split('_')[-1])
                        if self.selected_algorithm_index != index: # <<< Auto-reset only if changed
                             self.selected_algorithm_index = index; self.dropdown_open = False
                             self.reset_data(play_sound=False) # Reset without sound
                             self.start_sorting_process() # Start new algo
                             self._play_sound('click') # Play sound now
                        else:
                             self.dropdown_open = False # Just close if same selected
                    elif clicked_element_id and clicked_element_id.startswith('mode_btn_'):
                        mode_label = self.ui_elements[clicked_element_id]['label']; new_mode = mode_label.lower()
                        if self.mode != new_mode: # <<< Auto-reset only if changed
                             self.mode = new_mode
                             self.reset_data() # Reset for new mode (plays sound)
                             # Optional: Automatically start the current algorithm in the new mode?
                             # self.start_sorting_process() # Uncomment to auto-start on mode change
                        # If clicking current mode, maybe reset? Or do nothing. Currently does nothing if same mode.
                    elif clicked_element_id == 'theme_btn': self.toggle_theme()
                    elif clicked_element_id == 'help_btn': # <<< Handle Help Button Click
                         self.show_help = True
                         if self.running and not self.paused: # Pause sorting if running
                              self.paused = True
                         self._play_sound('click')
                    elif clicked_element_id == 'speed_knob': self.dragging_slider = True; self._play_sound('click')
                    elif clicked_element_id == 'step_btn':
                        self.step_mode = not self.step_mode; self.paused = self.step_mode and self.running; self._play_sound('click'); print(f"Step mode: {'ON' if self.step_mode else 'OFF'}")
                    elif clicked_element_id == 'next_step_btn':
                        if self.step_mode and self.running: self.advance_sort_step()
                    elif clicked_element_id == 'restart_btn':
                         if self.running: self.restart_current_sort()
                    elif self.dropdown_open and not clicked_element_id: self.dropdown_open = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: self.dragging_slider = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_slider: slider_rect = self.ui_elements['speed_slider']['rect']; knob_rect = self.ui_elements['speed_knob']['rect']; knob_rect.centerx = max(slider_rect.left, min(mouse_pos[0], slider_rect.right)); self._update_interval_from_knob()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_help: self.show_help = False; self.paused = False # Close help, unpause
                    else: return False # Quit on Escape if help not shown
                elif event.key == pygame.K_SPACE:
                    if not self.show_help and self.running and not self.step_mode: self.paused = not self.paused; self._play_sound('click')
                elif event.key == pygame.K_RIGHT:
                    if not self.show_help and self.step_mode and self.running: self.advance_sort_step()
                elif event.key == pygame.K_r:
                     if not self.show_help and self.running: self.restart_current_sort()
                elif event.key == pygame.K_h: # Add H key for help
                     self.show_help = not self.show_help
                     if self.show_help and self.running and not self.paused: self.paused = True # Pause on opening help
                     elif not self.show_help and self.paused and not self.step_mode: self.paused = False # Unpause on closing help
                     self._play_sound('click')


        return True # Continue running

    def update(self):
        # --- Do not update sorting if help is shown ---
        if self.show_help:
             # Keep updating FPS maybe, but not sorting or live time
             self.fps = self.clock.get_fps()
             return # Skip sorting updates

        self.fps = self.clock.get_fps()
        if self.process:
            try: self.live_memory_usage_kb = self.process.memory_info().rss / 1024
            except (psutil.NoSuchProcess, psutil.AccessDenied): self.process = None

        # Advance sort only if running, not paused, not step mode, and handler active
        if self.running and self.sorting_handler.sorting and not self.paused and not self.step_mode:
            current_time = time.time()
            time_since_last_update = current_time - self.last_update_time
            safe_interval = max(0.0001, self.update_interval)
            steps_to_take = int(time_since_last_update / safe_interval)
            if steps_to_take > 0:
                for _ in range(steps_to_take):
                    if not self.advance_sort_step(): break
                self.last_update_time += steps_to_take * safe_interval

        if self.running and self.sorting_handler.sorting:
            self.live_time_ms = (time.time() - self.start_time) * 1000

    def draw(self):
        self.visualizer._visualize(self.data, self.mode, self.theme)
        self._draw_ui_elements()
        self._draw_tooltip()
        # --- Draw Help Modal if active ---
        if self.show_help:
            self._draw_help_modal()
        pygame.display.flip()

    def _draw_ui_elements(self):
        # (Keep drawing logic for buttons, slider, stats as before)
        # Helper function to draw buttons
        def draw_button(element_id, default_text=None):
             # Skip drawing irrelevant buttons based on state
             if element_id == 'restart_btn' and not self.running: return
             if element_id == 'next_step_btn' and not (self.step_mode and self.running and self.sorting_handler.sorting): return

             info = self.ui_elements[element_id]
             rect = info['rect']
             label = info.get('label', default_text)
             is_hovering = (self.hover_rect_id == element_id and not self.show_help) # Disable hover if help shown
             is_active = False

             # Determine active state
             if element_id.startswith('mode_btn_') and self.mode == label.lower(): is_active = True
             elif element_id == 'step_btn' and self.step_mode: is_active = True
             elif element_id == 'step_btn' and self.paused and not self.step_mode: is_active = True # Reuse rect for pause
             elif element_id == 'help_btn' and self.show_help: is_active = True # Highlight help btn if modal open

             idle_color = self.theme['button_idle']; hover_color = self.theme['button_hover']
             active_color = self.theme['accent']; active_hover_color = self.theme['accent_hover']
             text_color = self.theme['button_text']; outline_color = self.theme['accent']

             if is_active: btn_color = active_hover_color if is_hovering else active_color; outline_color = self.theme['text']
             else: btn_color = hover_color if is_hovering else idle_color

             pygame.draw.rect(self.screen, btn_color, rect, border_radius=5)
             if is_hovering or is_active: pygame.draw.rect(self.screen, outline_color, rect, 1, border_radius=5)

             # Adjust label for dynamic buttons (Pause/Step, Help)
             if element_id == 'step_btn': label = "Step Mode: ON" if self.step_mode else "Step Mode: OFF"
             if element_id == 'step_btn' and self.running and not self.step_mode: label = "PAUSED (SPACE)" if self.paused else "Pause (SPACE)"
             if element_id == 'help_btn': label = "?" # Always show '?'

             if label:
                  font_key = 'medium' if rect.height >= 40 else 'small'
                  # Special larger font for help '?' button
                  if element_id == 'help_btn': font_key = 'large'
                  text = self.fonts[font_key].render(str(label), True, text_color) # Use str() for safety
                  text_rect = text.get_rect(center=rect.center)
                  # Adjust text position slightly for help '?' button
                  if element_id == 'help_btn': text_rect.centery -= 2
                  self.screen.blit(text, text_rect)

        # --- Draw All UI Elements ---
        # Draw elements that should be below dropdown
        for btn_id in self.mode_buttons: draw_button(btn_id)
        draw_button('theme_btn')
        draw_button('help_btn') # <<< Draw help button
        # Speed Slider (as before)
        slider_info = self.ui_elements['speed_slider']; knob_info = self.ui_elements['speed_knob']; is_hovering_slider = self.hover_rect_id in ['speed_slider', 'speed_knob'] and not self.show_help
        pygame.draw.rect(self.screen, self.theme['slider_bar'], slider_info['rect'], border_radius=4); pygame.draw.rect(self.screen, self.theme['text'] if is_hovering_slider else self.theme['graph_outline'], slider_info['rect'], 1, border_radius=4)
        knob_color = self.theme['accent_hover'] if self.dragging_slider else self.theme['slider_knob']; pygame.draw.rect(self.screen, knob_color, knob_info['rect'], border_radius=3)
        speed_label_text = f"{1.0/max(0.001, self.update_interval):.0f}x"; speed_label = self.fonts['small'].render(speed_label_text, True, self.theme['text'])
        self.screen.blit(speed_label, speed_label.get_rect(midright=(slider_info['rect'].left - 10, slider_info['rect'].centery)))

        # Bottom row buttons
        draw_button('step_btn'); draw_button('next_step_btn'); draw_button('restart_btn')

        # Draw Dropdown Button & Options (draw last to be on top)
        draw_button('algo_dropdown_btn', self.algorithms[self.selected_algorithm_index][0])
        base_rect = self.ui_elements['algo_dropdown_btn']['rect']
        arrow_points = [(base_rect.right - 15, base_rect.centery - 3), (base_rect.right - 5, base_rect.centery - 3), (base_rect.right - 10, base_rect.centery + 3)]
        if self.dropdown_open: arrow_points = [(base_rect.right - 15, base_rect.centery + 3), (base_rect.right - 5, base_rect.centery + 3), (base_rect.right - 10, base_rect.centery - 3)]
        pygame.draw.polygon(self.screen, self.theme['button_text'], arrow_points)
        if self.dropdown_open:
             self.dropdown_option_rects = []
             for i, (name, _, _) in enumerate(self.algorithms):
                  opt_rect = pygame.Rect(base_rect.left, base_rect.bottom + i * (base_rect.height + 2), base_rect.width, base_rect.height)
                  self.dropdown_option_rects.append(opt_rect)
                  opt_id = f'dropdown_opt_{i}'; is_hovering_opt = (self.hover_rect_id == opt_id and not self.show_help)
                  opt_color = self.theme['button_hover'] if is_hovering_opt else self.theme['button_idle']; pygame.draw.rect(self.screen, opt_color, opt_rect, border_radius=5)
                  if is_hovering_opt: pygame.draw.rect(self.screen, self.theme['accent'], opt_rect, 1, border_radius=5)
                  opt_text = self.fonts['medium'].render(name, True, self.theme['button_text']); self.screen.blit(opt_text, opt_text.get_rect(center=opt_rect.center))

        self._draw_stats_info()

    def _draw_stats_info(self):
        # (Keep implementation from previous response)
        y_offset_completed = 120 ; max_stats_height = self.height - y_offset_completed - 20; stat_line_height = 25 ; visible_stats_count = max_stats_height // stat_line_height
        sorted_times = sorted(self.algorithm_times.items(), key=lambda item: item[1][0] if item[1] and item[1][0] is not None else float('inf'))
        for i, (name, stats) in enumerate(sorted_times):
            if i >= visible_stats_count: break
            if stats: t, mem = stats; time_str = f"{t:.1f} ms" if t is not None else "N/A"; mem_str = f"{mem:.1f} Ko" if mem is not None else "N/A"
            else: time_str, mem_str = "N/A", "N/A"
            text_content = f"{name}: {time_str} | Mem(Peak): {mem_str}"; text = self.fonts['small'].render(text_content, True, self.theme['stats_text'])
            self.screen.blit(text, text.get_rect(topright=(self.width - 10, y_offset_completed + i * stat_line_height)))
        y_offset_live = self.height - 30 ; live_stats_texts = []; x_pos_live = 10
        live_stats_texts.append(f"FPS: {self.fps:.1f}")
        if self.running and self.sorting_handler.sorting: live_stats_texts.append(f"Time: {self.live_time_ms:.0f} ms")
        if self.process: live_stats_texts.append(f"Mem(Live): {self.live_memory_usage_kb:.1f} Ko")
        for i, stat_text in enumerate(live_stats_texts):
            text = self.fonts['small'].render(stat_text, True, self.theme['stats_text']); text_rect = text.get_rect(midleft=(x_pos_live, y_offset_live)); self.screen.blit(text, text_rect)
            x_pos_live += text_rect.width + 20


    def _draw_tooltip(self):
         # (Keep implementation from previous response, checking self.show_help)
         if self.active_tooltip_text and not self.show_help: # Don't show tooltip if help is open
            mouse_x, mouse_y = pygame.mouse.get_pos(); tooltip_surface = self.fonts['tooltip'].render(self.active_tooltip_text, True, self.theme['tooltip_text'])
            tooltip_rect = tooltip_surface.get_rect(topleft=(mouse_x + 15, mouse_y + 10))
            if tooltip_rect.right > self.width - 5: tooltip_rect.right = self.width - 5
            if tooltip_rect.bottom > self.height - 5: tooltip_rect.bottom = self.height - 5
            bg_rect = tooltip_rect.inflate(8, 6); pygame.draw.rect(self.screen, self.theme['tooltip_bg'], bg_rect, border_radius=3)
            pygame.draw.rect(self.screen, self.theme.get('graph_outline', self.theme['text']), bg_rect, 1, border_radius=3)
            self.screen.blit(tooltip_surface, tooltip_rect)

    # --- Help Modal Drawing --- <<< New Method
    def _draw_help_modal(self):
        """Draws the help overlay and modal window."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(self.theme.get('help_overlay_bg', (0, 0, 0, 180)))
        self.screen.blit(overlay, (0, 0))

        # Modal dimensions and position
        modal_width = self.width * 0.7
        modal_height = self.height * 0.9
        modal_x = (self.width - modal_width) // 2
        modal_y = (self.height - modal_height) // 2
        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)

        # Draw modal background and border
        pygame.draw.rect(self.screen, self.theme.get('help_modal_bg', (50, 50, 70)), modal_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.theme.get('help_modal_border', (150, 150, 180)), modal_rect, 2, border_radius=10)

        # --- Help Text Content ---
        help_content = [
            ("Sorting Visualizer Help", self.fonts['help_title'], self.theme['accent']),
            ("", None, None), # Spacer
            ("Controls:", self.fonts['medium'], self.theme['text']),
            ("- Algorithm Dropdown: Select which sorting algorithm to visualize.", self.fonts['help_text'], self.theme['text']),
            ("- Mode Buttons (Colors, Numbers, etc.): Choose the type of data to sort and visualize.", self.fonts['help_text'], self.theme['text']),
            ("  - Colors: Sorts RGB by Hue, shown as rainbow rays.", self.fonts['help_text'], self.theme['text']),
            ("  - Numbers: Sorts numbers, shown as bars.", self.fonts['help_text'], self.theme['text']),
            ("  - Words: Sorts words alphabetically, shown in a grid.", self.fonts['help_text'], self.theme['text']),
            ("  - Letters: Sorts letters alphabetically, shown as bars.", self.fonts['help_text'], self.theme['text']),
            ("- Speed Slider: Adjust the animation speed (steps per second).", self.fonts['help_text'], self.theme['text']),
            ("- Step Mode Button: Toggle manual step-by-step sorting.", self.fonts['help_text'], self.theme['text']),
            ("- Next Step Button / Right Arrow: Advance one step when Step Mode is ON.", self.fonts['help_text'], self.theme['text']),
            ("- Pause Button / Spacebar: Pause/Resume automatic sorting.", self.fonts['help_text'], self.theme['text']),
            ("- Restart Button / R Key: Restart the current algorithm with new data.", self.fonts['help_text'], self.theme['text']),
            ("- Theme Button: Toggle between Dark and Light themes.", self.fonts['help_text'], self.theme['text']),
            ("- ? Button / H Key: Show/Hide this help window.", self.fonts['help_text'], self.theme['text']),
            ("- ESC Key: Close help window or quit the application.", self.fonts['help_text'], self.theme['text']),
            ("", None, None), # Spacer
            ("Algorithms:", self.fonts['medium'], self.theme['text']),
            # Add brief descriptions from README or algorithm tooltips
            *[(f"- {name}: {tooltip}", self.fonts['help_text'], self.theme['text']) for name, _, tooltip in self.algorithms]
        ]

        # --- Render Help Text ---
        text_x = modal_x + 20
        text_y = modal_y + 20
        line_height = 25 # Adjust as needed

        for content, font, color in help_content:
            if font and color:
                try:
                     text_surface = font.render(content, True, color)
                     self.screen.blit(text_surface, (text_x, text_y))
                     text_y += int(font.get_height() * 1.1) # Move down based on font height
                except Exception as e:
                     print(f"Error rendering help text line '{content}': {e}") # Handle font render errors
                     text_y += line_height # Fallback spacing
            else:
                text_y += line_height // 2 # Spacer


        # --- Draw Close Button ---
        close_btn_info = self.ui_elements['help_close_btn']
        # Position near bottom-right corner of modal
        close_btn_rect = close_btn_info['rect']
        close_btn_rect.width = 100
        close_btn_rect.height = 35
        close_btn_rect.bottomright = (modal_rect.right - 15, modal_rect.bottom - 15)

        is_hovering_close = (self.hover_rect_id == 'help_close_btn')
        close_color = self.theme['button_hover'] if is_hovering_close else self.theme['button_idle']
        pygame.draw.rect(self.screen, close_color, close_btn_rect, border_radius=5)
        if is_hovering_close:
            pygame.draw.rect(self.screen, self.theme['accent'], close_btn_rect, 1, border_radius=5)

        close_text = self.fonts['medium'].render("Close (ESC)", True, self.theme['button_text'])
        close_text_rect = close_text.get_rect(center=close_btn_rect.center)
        self.screen.blit(close_text, close_text_rect)


    def run_app(self):
        app_running = True
        while app_running:
            app_running = self.handle_input()
            if not app_running: break
            self.update()
            self.draw()
            self.clock.tick(60)
        if tracemalloc.is_tracing(): tracemalloc.stop()
        pygame.quit()
        print("Visualizer closed.")

# --- Main execution ---
# (This part is typically in main.py, but included here if running script.py directly)
# if __name__ == "__main__":
#     app = Interface()
#     app.run_app()