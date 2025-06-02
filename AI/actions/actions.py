# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ActionAnswerFromPDF(Action):
    def name(self) -> Text:
        return "action_explain_mean"

    def load_pdf_text(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page_num in range(len(doc)):
            page = doc[page_num]
            # Extract normal text
            text = page.get_text()
            full_text += text + "\n"

            # Extract images and OCR text from them
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))

                ocr_text = pytesseract.image_to_string(image)
                full_text += "\n[OCR IMAGE TEXT]:\n" + ocr_text + "\n"

        return full_text

    def find_answer(self, question: str, context: str) -> str:
        # Split context into sentences
        sentences = context.split('.')
        vectorizer = TfidfVectorizer().fit_transform([question] + sentences)
        similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:])
        most_relevant_index = similarity.argmax()
        return sentences[most_relevant_index].strip()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        question = tracker.latest_message.get('text')
        pdf_path = "actions/applied_statistics.pdf"
        pdf_text = self.load_pdf_text(pdf_path)
        answer = self.find_answer(question, pdf_text)

        dispatcher.utter_message(text=answer)
        return []
