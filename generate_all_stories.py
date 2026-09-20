import json
import os
from model_rawi import RAWI


LANDMARKS = [
    "Ajloun_Castle",
    "Al_Maghtas",
    "Dead_Sea",
    "Jerash",
    "Karak_Castle",
    "Petra",
    "Qasr_Amra",
    "Um_AL_Jimal",
    "Um_Qais",
    "Wadi_Mujib",
    "wadi_Rum"
]

LANGUAGES = [
    "English",
    "العربية",
    "Français"
]

STORY_LENGTHS = [
    "Short",
    "Medium",
    "Long"
]

CACHE_PATH = "stories_cache.json"


def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}

    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    cache = load_cache()

    rawi = RAWI()

    total = len(LANDMARKS) * len(LANGUAGES) * len(STORY_LENGTHS)
    completed = len(cache)

    print(f"Existing stories: {completed}/{total}")

    for landmark in LANDMARKS:
        for language in LANGUAGES:
            for story_length in STORY_LENGTHS:

                cache_key = f"{landmark}_{language}_{story_length}"

                if cache_key in cache:
                    print(f"SKIP: {cache_key}")
                    continue

                print(f"GENERATING: {cache_key}")

                try:
                    rawi.generate_story(
                        landmark,
                        language,
                        story_length
                    )

                    print(f"SUCCESS: {cache_key}")

                except Exception as e:
                    print(f"ERROR: {cache_key}")
                    print(e)

                    print("Stopping. Run the script again later to continue.")
                    return

    print("Finished generating all stories.")


if __name__ == "__main__":
    main()