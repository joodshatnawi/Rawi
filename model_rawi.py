from ultralytics import YOLO
from PIL import Image, ImageDraw
from groq import Groq
import edge_tts
import asyncio
import json
import streamlit as st
import os
from dotenv import load_dotenv
import random
from rag import retrieve_context as rag_retrieve_context


load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
facts_path = os.path.join(BASE_DIR, "data","facts.json")
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")
STORY_PROMPT_PATH = os.path.join(PROMPT_DIR, "story_generation.md")
QUERY_REWRITING_PROMPT_PATH=os.path.join(PROMPT_DIR,"query_rewriting.md")
ANSWER_GENERATION_PROMPT_PATH=os.path.join(PROMPT_DIR,"answer_generation.md")

class RAWI:
    def __init__(self):
        self.model=self.load_model()
        self.facts=self.load_facts()
        self.client=self.load_client()
        self.story_prompt = self.load_story_prompt()
        
    # ---------------- Load Model ----------------
    @staticmethod
    @st.cache_resource
    def load_model():
        return YOLO(os.path.join(BASE_DIR,"best.pt"))
        
        # ---------------- Load Facts ----------------
    @staticmethod
    @st.cache_data
    def load_facts():
        with open(facts_path,"r",encoding="utf-8")as f:
            return json.load(f)

        # ---------------- Load Story Prompt ----------------
    @staticmethod
    def load_story_prompt():
        with open(STORY_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
                
        # ---------------- Detect Landmark ----------------
    def detect_landmark(self,image_path):
        results =self.model(image_path,
                            conf=0.25,
                            iou=0.45,
                            verbose=False)
        predictions=[]
        for box in results[0].boxes:
            x1,y1,x2,y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name=self.model.names[class_id]
            predictions.append({
                "class":class_name,
                "confidence": confidence,
                "x":(x1+x2)/2,
                "y":(y1+y2)/2,
                "width":x2-x1,
                "height":y2-y1
                })
        return{"predictions":predictions}
        
    # ---------------- Draw Boxes ----------------
    @staticmethod
    def draw_boxes(image_path,results):
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        for de in results["predictions"]:
            x1 = de["x"] - de["width"] / 2
            y1 = de["y"] - de["height"] / 2
            x2 = de["x"] + de["width"] / 2
            y2 = de["y"] + de["height"] / 2
            label = de["class"]
            confidence=de["confidence"]
            text=f"{label} {confidence*100:0.1f}%"
            draw.rectangle([(x1,y1),(x2,y2)],outline="red",width=4)
            text_x=x1
            text_y=max(0,y1-25)
            bbox=draw.textbbox((text_x, text_y),text)
            draw.rectangle(bbox,fill="red")
            draw.text((text_x,text_y),text,fill="white")
        return img
        
    # ---------------- Load Groq Client ----------------
   
    @staticmethod
    def load_client():
        return Groq(api_key=os.getenv("GROQ_API_KEY"))

    # ---------------- Story Cache ----------------
    def load_story_cache(self):
        cache_path = "stories_cache.json"

        if not os.path.exists(cache_path):
            return {}

        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_story_cache(self, cache):
        cache_path = "stories_cache.json"

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)
    
    # ---------------- Generate Story ----------------
    def generate_story(self, detected_class, language, story_length):

        # ---------------- Cache  ----------------
        cache = self.load_story_cache()
        cache_key = f"{detected_class}_{language}_{story_length}"

        if cache_key in cache:
            return cache[cache_key]["story"]
        # ---------------- Load Facts ----------------
        landmark = self.facts[detected_class]

        landmark_name = landmark["name"][language]
        welcome = landmark["welcome"][language]

        facts = landmark["story_facts"]

        facts_text = "\n".join(
            f"- {fact}" for fact in facts
        )

        # ---------------- Length Instructions ----------------
        length_instruction = {
            "العربية": {
                "Short": (
                    "اكتب قصة قصيرة بين 70 و80 كلمة، ويفضل أن تكون قريبة من 75 كلمة. "
                    "يشمل عدد الكلمات المقدمة والخاتمة. "
                    "اختر فقط المعلومات التي يمكن عرضها بشكل طبيعي ضمن هذا النطاق. "
                    "إذا تجاوزت المعلومات المختارة الحد الأعلى، احذف المعلومات الأقل أهمية بدلًا من تجاوز 80 كلمة."
                ),
                "Medium": (
                    "اكتب قصة متوسطة بين 110 و130 كلمة، ويفضل أن تكون قريبة من 120 كلمة. "
                    "يشمل عدد الكلمات المقدمة والخاتمة. "
                    "اختر فقط المعلومات التي يمكن عرضها بشكل طبيعي ضمن هذا النطاق. "
                    "إذا تجاوزت المعلومات المختارة الحد الأعلى، احذف المعلومات الأقل أهمية بدلًا من تجاوز 130 كلمة."
                ),
                "Long": (
                    "اكتب قصة طويلة بين 160 و190 كلمة، ويفضل أن تكون قريبة من 175 كلمة. "
                    "يشمل عدد الكلمات المقدمة والخاتمة. "
                    "استخدم عددًا أكبر من المعلومات المهمة المتاحة، لكن لا تحاول تضمين جميع المعلومات. "
                    "إذا تجاوزت المعلومات المختارة 190 كلمة، احذف المعلومات الأقل أهمية بدلًا من تجاوز الحد الأعلى. "
                    "لا تضف أي معلومات غير موجودة في الحقائق."
                )
            },

            "English": {
                "Short": (
                    "Write a short story between 70 and 80 words, preferably close to 75 words. "
                    "The word count includes the opening and closing. "
                    "Select only facts that can fit naturally within this range. "
                    "If the selected information exceeds the upper limit, remove the least important facts instead of exceeding 80 words."
                ),
                "Medium": (
                    "Write a medium-length story between 110 and 130 words, preferably close to 120 words. "
                    "The word count includes the opening and closing. "
                    "Select only facts that can fit naturally within this range. "
                    "If the selected information exceeds the upper limit, remove the least important facts instead of exceeding 130 words."
                ),
                "Long": (
                    "Write a long story between 160 and 190 words, preferably close to 175 words. "
                    "The word count includes the opening and closing. "
                    "Use more important provided facts, but do not try to include all available facts. "
                    "If the selected information exceeds 190 words, remove the least important facts instead of exceeding the upper limit. "
                    "Do not add any information that is not supported by the facts."
                )
            },

            "Français": {
                "Short": (
                    "Écrivez une histoire courte entre 70 et 80 mots, de préférence proche de 75 mots. "
                    "Le nombre de mots comprend l'introduction et la conclusion. "
                    "Sélectionnez uniquement les informations qui peuvent être présentées naturellement dans cette limite. "
                    "Si les informations sélectionnées dépassent la limite supérieure, supprimez les informations les moins importantes au lieu de dépasser 80 mots."
                ),
                "Medium": (
                    "Écrivez une histoire de longueur moyenne entre 110 et 130 mots, de préférence proche de 120 mots. "
                    "Le nombre de mots comprend l'introduction et la conclusion. "
                    "Sélectionnez uniquement les informations qui peuvent être présentées naturellement dans cette limite. "
                    "Si les informations sélectionnées dépassent la limite supérieure, supprimez les informations les moins importantes au lieu de dépasser 130 mots."
                ),
                "Long": (
                    "Écrivez une histoire longue entre 160 et 190 mots, de préférence proche de 175 mots. "
                    "Le nombre de mots comprend l'introduction et la conclusion. "
                    "Utilisez davantage d'informations importantes fournies, mais n'essayez pas d'inclure toutes les informations disponibles. "
                    "Si les informations sélectionnées dépassent 190 mots, supprimez les informations les moins importantes au lieu de dépasser la limite supérieure. "
                    "N'ajoutez aucune information qui ne soit pas confirmée par les faits."
                )
            }
        }
        selected_length_instruction = length_instruction[language][story_length]

        # ---------------- Select Language Prompt ----------------
        if language == "العربية":
            start = self.story_prompt.index("## Arabic Prompt")
            end = self.story_prompt.index("## English Prompt")
            prompt_template = self.story_prompt[start:end]

        elif language == "English":
            start = self.story_prompt.index("## English Prompt")
            end = self.story_prompt.index("## French Prompt")
            prompt_template = self.story_prompt[start:end]

        else:
            start = self.story_prompt.index("## French Prompt")
            prompt_template = self.story_prompt[start:]

        # ---------------- Fill Prompt ----------------
        prompt_text = prompt_template.format(
            landmark_name=landmark_name,
            welcome=welcome,
            facts_text=facts_text,
            length_instruction=selected_length_instruction
        )

        # ---------------- System Prompt ----------------
        system_start = self.story_prompt.index("## System Prompt")
        system_end = self.story_prompt.index("## Arabic Prompt")
        system_prompt = self.story_prompt[system_start:system_end]

        # ---------------- Groq ----------------
        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            temperature=0.2,
            max_tokens=2000,
            reasoning_effort="low"
        )
        story_text = completion.choices[0].message.content

        if story_text is None or not story_text.strip():
            raise ValueError("Groq returned an empty story.")
        story_text = story_text.strip()

        cache[cache_key] = {
            "landmark": detected_class,
            "language": language,
            "length": story_length,
            "story": story_text,
            "model": "openai/gpt-oss-120b"
        }

        self.save_story_cache(cache)

        return story_text
    
    # ---------------- Generate Audio ----------------
    @staticmethod
    def generate_audio(story_text, language):

        voice_settings = {
            "العربية": "ar-JO-SanaNeural",
            "English": "en-US-JennyNeural",
            "Français": "fr-FR-DeniseNeural"
        }

        voice = voice_settings[language]
        audio_file = "live_narrator_voice.mp3"

        async def generate():
            communicate = edge_tts.Communicate(
                story_text,
                voice
            )
            await communicate.save(audio_file)

        asyncio.run(generate())

        return audio_file

    # ---------------- Generate Fun Fact ----------------
    def generate_fun_fact(self, detected_class,language):
        fun_facts = self.facts[detected_class]["fun_facts"][language]
        return random.choice(fun_facts)           

    # ---------------- Rewrite Question ----------------
    def rewrite_question(
        self,
        detected_class,
        language,
        question,
        history=None
    ):
        if history is None:
            history = []

        history_text = ""

        for item in history[-5:]:
            if any(x in item["answer"] for x in [
                "لا أملك معلومات كافية",
                "don't have enough information",
                "pas suffisamment d'informations"
            ]):
                continue

            history_text += (
                f"المستخدم: {item['question']}\n"
                f"المساعد: {item['answer']}\n\n"
            )

        with open(
            QUERY_REWRITING_PROMPT_PATH,
            "r",
            encoding="utf-8"
        ) as f:
            system_prompt = f.read()

        prompt_text = f"""
    Conversation History:

    {history_text}

    Current Detected Landmark:

    {detected_class}

    Current User Question:

    {question}
    """
        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            temperature=0,
            max_tokens=200,
            reasoning_effort="low"
        )

        rewritten_question = completion.choices[0].message.content
        if rewritten_question:
            rewritten_question = rewritten_question.strip()

        if not rewritten_question:
            return question

        return rewritten_question

    # ---------------- Retrieve Context ----------------
    def retrieve_context(self, detected_class, question, k=8):
        return rag_retrieve_context(
                detected_class,
                question,
                k=k
            )    

    # ---------------- Generate Answer ----------------
    def generate_answer(self, detected_class, language, question, history=None):

        landmark = self.facts[detected_class]
        landmark_name = landmark["name"][language]

        if history is None:
            history = []

        history_text = ""

        for item in history[-5:]:
            history_text += (
                f"المستخدم: {item['question']}\n"
                f"المساعد: {item['answer']}\n\n"
            )
        needs_rewrite = False

        if history:
            follow_up_words = [
                "هو", "هي", "هذا", "هذه", "ذلك", "تلك",
                "له", "لها", "هناك",
                "شو", "وشو", "وين", "كيف", "ليش", "متى", "مين",
                "it", "he", "she", "they", "this", "that", "its",
                "what about", "where is", "how", "why", "when"
            ]

            needs_rewrite = any(
                word in question.lower()
                for word in follow_up_words
            )

        if needs_rewrite:
            rewritten_question = self.rewrite_question(
                detected_class,
                language,
                question,
                history
            )
        else:
            rewritten_question = question
        
        # ---------------- Retrieve Context ----------------

        context_list = self.retrieve_context(
            detected_class,
            rewritten_question,
            k=4
        )

        # ---------------- No Context ----------------

        if not context_list:

            if language == "العربية":
                return "عذرًا، لا أملك معلومات كافية للإجابة."

            elif language == "English":
                return "Sorry, I don't have enough information to answer this question."

            else:
                return "Désolé, je n'ai pas suffisamment d'informations pour répondre."

        context = "\n\n".join(
            f"- {chunk['text']}"
            for chunk in context_list
        )

        # ---------------- System Prompt ----------------

        with open(
            ANSWER_GENERATION_PROMPT_PATH,
            "r",
            encoding="utf-8"
        ) as f:
            system_prompt = f.read()

        # ---------------- User Prompt ----------------

        prompt = f"""
        Current landmark:
        {landmark_name}

        Retrieved information:
        {context}

        Requested language:
        {language}

        User question:
        {rewritten_question}
        """
        # ---------------- Generate Answer ----------------
        completion = self.client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=500,
        reasoning_effort="low"
    )

        answer = completion.choices[0].message.content

        if not answer:
            return "عذرًا، لا أملك معلومات كافية للإجابة."
        answer = answer.strip()
        return answer

    def analyze(self, image_path, language, story_length):
        # Detect landmark
        result = self.detect_landmark(image_path)
        # No landmark detected
        if len(result["predictions"]) == 0:
            return (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            )

        # Get prediction
        detected_class = result["predictions"][0]["class"]
        confidence = float(result["predictions"][0]["confidence"])
        
        # Load landmark data
        landmark = self.facts[detected_class]
        landmark_name = landmark["name"][language]
        info = landmark["info"]
        latitude = landmark["location"]["lat"]
        longitude = landmark["location"]["lon"]

        # Draw detection box
        image = self.draw_boxes(image_path, result)

        # Generate story
        story = self.generate_story(
            detected_class,
            language,
            story_length
        )

        # Generate Fun Fact
        fun_fact = self.generate_fun_fact(detected_class,language)

        # Generate audio narration
        audio = self.generate_audio(story, language)

        return (
            image,
            story,
            audio,
            confidence,
            landmark_name,
            latitude,
            longitude,
            info,
            detected_class,
            fun_fact
        )
