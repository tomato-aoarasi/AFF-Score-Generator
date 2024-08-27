from element import *
from aff.decoder import *
from utils import read_file
import random

PM_SCORE = 10000000 

def calculate_score(shiny_pure, pure, far, lost, single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score):
    return (shiny_pure * single_shiny_pure_score +
            pure * single_pure_score +
            far * single_far_score +
            lost * single_lost_score)

def find_combination(min_score, max_score, max_note, max_tap, max_hold, max_arc, 
                    single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score, attempts=100000):
    for _ in range(attempts):
        note_shiny_pure = random.randint(0, max_note)
        note_pure = random.randint(0, max_note - note_shiny_pure)
        note_far = random.randint(0, max_note - note_shiny_pure - note_pure)
        note_lost = max_note - note_shiny_pure - note_pure - note_far
        
        tap_shiny_pure = random.randint(0, max_tap)
        tap_pure = random.randint(0, max_tap - tap_shiny_pure)
        tap_far = random.randint(0, max_tap - tap_shiny_pure - tap_pure)
        tap_lost = max_tap - tap_shiny_pure - tap_pure - tap_far
        
        hold_shiny_pure = random.randint(0, max_hold)
        hold_lost = max_hold - hold_shiny_pure
        
        arc_shiny_pure = random.randint(0, max_arc)
        arc_lost = max_arc - arc_shiny_pure
        
        total_score = (
            calculate_score(note_shiny_pure, note_pure, note_far, note_lost,
                            single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score) +
            calculate_score(tap_shiny_pure, tap_pure, tap_far, tap_lost,
                            single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score) +
            calculate_score(hold_shiny_pure, 0, 0, hold_lost,
                            single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score) +
            calculate_score(arc_shiny_pure, 0, 0, arc_lost,
                            single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score)
        )
        
        if min_score <= total_score <= max_score:
            return {
                "note_shiny_pure": note_shiny_pure,
                "note_pure": note_pure,
                "note_far": note_far,
                "note_lost": note_lost,
                "tap_shiny_pure": tap_shiny_pure,
                "tap_pure": tap_pure,
                "tap_far": tap_far,
                "tap_lost": tap_lost,
                "hold_shiny_pure": hold_shiny_pure,
                "hold_lost": hold_lost,
                "arc_shiny_pure": arc_shiny_pure,
                "arc_lost": arc_lost,
                "total_score": total_score
            }
            
class ScoreDetail:
    def __init__(self, detail):
        shiny_pure_count = detail['note_shiny_pure'] + detail['tap_shiny_pure'] + detail['hold_shiny_pure'] + detail['arc_shiny_pure']
        pure_count = detail['note_pure'] + detail['tap_pure']
        far_count = detail['note_far'] + detail['tap_far']
        lost_count = detail['note_lost'] + detail['tap_lost'] + detail['hold_lost'] + detail['arc_lost']
        
        score = int(detail["total_score"])
        
        self.shiny_perfect_count = shiny_pure_count
        self.perfect_count = pure_count
        self.near_count = far_count
        self.miss_count = lost_count
        self.score = score
        self.detail = detail

def GenerateContent(aff_path: str, min_score: int = 9800000, max_score: int = 9880000, attempts: int = 100000) -> ScoreDetail:
    chart = parse_aff(read_file(aff_path))
    max_combo = chart.get_total_combo()
    max_note = chart.get_combo_of(Tap) # shiny_pure, pure, far, lost
    max_tap = chart.get_combo_of(ArcTap) # shiny_pure, pure, far, lost
    max_hold = chart.get_combo_of(Hold) # shiny_pure, lost
    max_arc = chart.get_combo_of(Arc) # shiny_pure, lost
    
    single_pure_score = PM_SCORE / max_combo
    single_far_score = single_pure_score / 2
    single_lost_score = 0
    single_shiny_pure_score = single_pure_score + 1
    
    result = find_combination(min_score, max_score, max_note, max_tap, max_hold, max_arc, 
                              single_shiny_pure_score, single_pure_score, single_far_score, single_lost_score, attempts)
    
    return ScoreDetail(result)