
import nltk
from datetime import datetime, timedelta
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import markdown
from weasyprint import HTML

nltk.download('punkt')
nltk.download('stopwords')

class Espresso:
    def __init__(self, discord_embeds=[]):
        self.news_data = [{'title': embed.title, 'description': embed.description, 'url': embed.url, 'timestamp': embed.timestamp} for embed in discord_embeds]

    def daily_digest(self):
        today = datetime.now().date()
        return [news for news in self.news_data if news['timestamp'].date() == today]

    def weekly_digest(self):
        today = datetime.now().date()
        a_week_ago = today - timedelta(days=7)
        return [news for news in self.news_data if a_week_ago <= news['timestamp'].date() <= today]

    def extract_keywords(self, text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [w for w in word_tokens if not w.lower() in stop_words]
        keywords = Counter(filtered_text)
        return keywords.most_common(10)  # returns top 10 keywords

    def daily_keywords(self):
        daily_news = self.daily_digest()
        text = ' '.join([news['title'] + ' ' + news['description'] for news in daily_news])
        return self.extract_keywords(text)

    def weekly_keywords(self):
        weekly_news = self.weekly_digest()
        text = ' '.join([news['title'] + ' ' + news['description'] for news in weekly_news])
        return self.extract_keywords(text)

    def output_markdown(self, news_data):
        md_content = "\n".join([f"## [{news['title']}]({news['url']})\n{news['description']}" for news in news_data])
        return md_content

    def export_html(self, md_content):
        return markdown.markdown(md_content)

    def export_pdf(self, html_content, output_filename="news_digest.pdf"):
        HTML(string=html_content).write_pdf(output_filename)
