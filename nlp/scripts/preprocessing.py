import re


class Preprocessing:
    def __init__(self, df):
        self.df = df

    def remove_only_timestamps(self, text):
        # Define a regular expression pattern to match only the timestamps at the start of each line
        pattern = r'\d{2}:\d{2}:\d{2}-'
        # Remove the matched patterns
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text

    def remove_specific_phrases(self, text):
        # Define the exact phrases you want to remove
        phrases_to_remove = [
            re.escape("agent: שלום, הגעת לווטסאפ של מרכזי הסיוע לנפגעות ונפגעי תקיפה מינית"),
            re.escape("agent: שלום, הגעת לקו הווטסאפ של מרכזי הסיוע לנפגעות ונפגעי תקיפה מינית."),
            re.escape("agent: סייעת תשוחח איתך בקרוב"),
            re.escape("agent: הצ'אט שלנו בווטסאפ *לא פעיל* כעת ואין ביכולתנו לראות או לקבל את הודעתך"),
            re.escape("agent: שעות המענה בווטסאפ:\nבימים א'-ה' ושבת בין השעות 17:00-23:00"),
            re.escape(
                "agent: אם הנך זקוק/ה כרגע לסיוע, ניתן לפנות ל:\n✳️ קו סיוע טלפוני זמין 24/7:\n 1202 מענה ע\"י אישה, \n 1203 מענה ע\"י גבר\n 2511* תהל- סיוע לנשים וילדים דתיים  \n ✳️ צ'אט אנונימי באתר 1202kolmila.org.il בימים א'-ה' ובשבת, בין השעות 17:00-24:00"),
            re.escape("agent: מוזמנות ומוזמנים לפנות אלינו בשעות הפעילות"),
            re.escape("agent: בשל עומס פניות, אני מתנצלת על זמן ההמתנה למענה"),
            re.escape("במידה והנך זקוק/ה כרגע לסיוע, ניתן לפנות ל:"),
            re.escape("* קו סיוע 1202 אשר זמין 24/7"),
            re.escape("* צ'אט אנונימי באתר kolmila.org.il  בימים א'-ה' ובשבת, בין השעות 17:00-24:00"),
            re.escape("אשלח לך הודעה מיד כשאסיים לטפל בפניות הקודמות"),
            re.escape("הסיוע בווטסאפ פועל:"),
            re.escape("ביום א' בין השעות 10:00-13:00 ו- 17:00-23:00,"),
            re.escape("בימים ב'-ה' וביום שבת בין השעות 17:00-23:00."),
            re.escape("אם הנך זקוק/ה כרגע לסיוע, ניתן לפנות ל:"),
            re.escape("✳️ קו סיוע טלפוני זמין 24/7:"),
            re.escape('1202 מענה ע"י אישה,'),
            re.escape('1203 מענה ע"י גבר'),
            re.escape("2511* תהל- סיוע לנשים וילדים דתיים"),
            re.escape("✳️ צ'אט אנונימי באתר 1202kolmila.org.il בימים א'-ה' ובשבת, בין השעות 17:00-24:00"),
            re.escape("* 	קו סיוע 1202 אשר זמין 24/7"),
            re.escape("*	צ'אט אנונימי באתר kolmila.org.il  בימים א'-ה' ובשבת, בין השעות 17:00-24:00"),
            re.escape("agent: שעות המענה בווטסאפ:"),
            re.escape(" בימים ב'-ה' ושבת בין השעות 17:00-23:00")
        ]

        # Use regular expressions to remove the phrases
        '''
        for phrase in phrases_to_remove:
            text = re.sub(re.escape(phrase), '', text)
    
        text = re.sub(r'\n+', '\n', text).strip()
    '''
        for phrase in phrases_to_remove:
            text = re.sub(phrase, '', text, flags=re.MULTILINE)

        # Clean up excessive newlines left after removing phrases
        text = re.sub(r'\n+', '\n', text).strip()

        return text

    def remove_empty_lines(self, text):
        # Regex pattern to match lines that only contain whitespace
        pattern = r'^\s*$'
        # Replace the matched patterns with an empty string and use re.MULTILINE to apply the pattern to each line
        cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
        # Remove extra newline characters left after removing lines
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()
        return cleaned_text

    def remove_empty_consumer_lines(self, text):
        # Regex pattern to match "consumer:" lines that are empty or contain only whitespace
        pattern = r'^(consumer:\s*)+\n'
        # Replace the matched patterns with nothing, using re.MULTILINE to apply the pattern to each line
        cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
        # Remove extra newline characters left after removing lines
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()
        return cleaned_text

    def remove_empty_agent_lines(self, text):
        # Regex pattern to match "agent:" lines that are empty or contain only whitespace
        pattern = r'^(agent:\s*)+\n'
        # Replace the matched patterns with nothing, using re.MULTILINE to apply the pattern to each line
        cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
        # Remove extra newline characters left after removing lines
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()
        return cleaned_text

    def remove_emojis(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def clean_text(self, text):
        text = self.remove_only_timestamps(text)
        text = self.remove_specific_phrases(text)
        text = self.remove_empty_lines(text)
        text = self.remove_empty_consumer_lines(text)
        text = self.remove_empty_agent_lines(text)
        text = self.remove_emojis(text)
        text = text.replace('"', '')
        text = text_without_quotes = text.replace("'", "")
        return text

    def process_dataframe(self, column_to_predict):
        self.df = self.df.rename(columns=lambda x: x.strip())
        self.df[column_to_predict] = self.df[column_to_predict].astype(str)
        self.df[column_to_predict] = self.df[column_to_predict].apply(self.clean_text)
        self.df['count'] = self.df[column_to_predict].apply(lambda x: len(x.split()))
        self.df = self.df[self.df['count'] >= 30]
        columns_to_copy = ['count', column_to_predict]
        self.df = self.df[columns_to_copy].copy()
        return self.df
        '''
        classification_mapping = {
            0: 'not relevant', 1: 'Emotional Assistance',
            2: 'Information', 3: 'Information',
            4: 'High Risk', 5: 'High Risk', 6: 'High Risk'
        }
        self.df['category'] = self.df['classification '].map(classification_mapping)

        categories = self.df['category'].unique().tolist()

        NUM_LABELS= len(categories)

        id2label={id:label for id,label in enumerate(categories)}
        label2id={label:id for id,label in enumerate(categories)}'''
