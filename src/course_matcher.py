import os
from typing import Optional, Dict, List
import logging
from config.settings import COURSE_LISTS_DIR, COURSE_LISTS_FILES

class CourseMatcher:
    def __init__(self, courses_dir: str = COURSE_LISTS_DIR):
        self.courses_dir = courses_dir
        self.course_lists: Dict[str, List[str]] = {}
        self.load_all()
    
    def load_all(self):
        for direction, filename in COURSE_LISTS_FILES.items():
            filepath = os.path.join(self.courses_dir, filename)
            try:
                with open(filepath, "r", encoding="UTF-8") as f:
                    courses = [line.strip() for line in f if line.strip()]
                self.course_lists[direction] = courses
                logging.info(f"Loaded {len(courses)} courses for {direction}")
            except FileNotFoundError:
                logging.warning(f"Course list file not found: {filepath}")
                self.course_lists[direction] = []
    
    def get_direction(self, course_name: str) -> Optional[str]:
        if not course_name:
            return None
        for direction, courses in self.course_lists.items():
            if course_name in courses:
                return direction
        return None