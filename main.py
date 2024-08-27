from generator import GenerateContent, ScoreDetail

def main():
    aff_path = "example.aff"
    content = GenerateContent(aff_path)
    
    shiny_perfect_count = content.shiny_perfect_count
    perfect_count = content.perfect_count
    near_count = content.near_count
    miss_count = content.miss_count
    score = content.score
    detail = content.detail
    
    print("============================")
    print("shiny_perfect_count:", shiny_perfect_count)
    print("perfect_count:", perfect_count)
    print("near_count:", near_count)
    print("miss_count:", miss_count)
    print("score:", score)
    print("----------------------------")
    print("detail:",detail)
    print("============================")

if __name__ == "__main__":
    main()
