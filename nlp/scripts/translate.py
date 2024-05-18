
import pandas as pd

from googletrans import Translator

class Translate:
    def __init__(self, df):
        self.df = df

    def translate_columns(self, df, columns_to_translate, chunk_size, src='he', dest='en'):
        # Initialize the Translator object
        translator = Translator()

        # Function to translate text
        def translate_text(text):
            if pd.isna(text):
                return None  # Return None if text is NaN
            try:
                # Split text into chunks with a word count greater than 600
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                translated_chunks = []
                # Translate each chunk
                for chunk in chunks:
                    result = translator.translate(chunk, src=src, dest=dest)
                    translated_chunks.append(result.text)
                # Concatenate translated chunks
                translated_text = ' '.join(translated_chunks)
                return translated_text
            except Exception as e:
                #print(f"Error translating text: '{text}'. Error: {e}")
                return "Translation failed"

        # Translate each specified column
        for column in columns_to_translate:
            # Apply translation to each row in the column
            df[f'{column}_en'] = df[column].apply(translate_text)

        return df

    def translate_dataframe(self, tanslated_path):
        columns_to_translate = ['transcriptAll']
        self.df = self.translate_columns(self.df, columns_to_translate, 600, src='he', dest='en')
        self.df.to_csv(tanslated_path, index=False)
        return self.df