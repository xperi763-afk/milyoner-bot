import requests
import time
import telebot

# --- AYARLAR ---
BOT_TOKEN = "8350998442:AAEYGk3aDegQojlxS6Zi7wmVhCARrsZK1ns"
API_KEY = "70a5a59689msh144b836941f5d43p17449ajsn586c190a6bb7"
GROUP_ID = -1003804275122

bot = telebot.TeleBot(BOT_TOKEN)
sent_scores = {}

def score_check():
    url = "https://sofascore.p.rapidapi.com/matches/get-live"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "sofascore.p.rapidapi.com"}
    try:
        response = requests.get(url, headers=headers, timeout=15).json()
        matches = response.get('data', [])
        for match in matches:
            m_id = str(match['id'])
            h_score = match.get('homeScore', {}).get('display', 0)
            a_score = match.get('awayScore', {}).get('display', 0)
            score_now = f"{h_score}-{a_score}"
            
            if m_id not in sent_scores or sent_scores[m_id] != score_now:
                h_name = match['homeTeam']['name']
                a_name = match['awayTeam']['name']
                text = f"⚽ **GOL HABERİ**\n\n🏆 {h_name} {h_score} - {a_score} {a_name}\n\n💎 @milyonerlersohbet"
                bot.send_message(GROUP_ID, text, parse_mode="Markdown")
                sent_scores[m_id] = score_now
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    # Render'da botun başladığını anlamak için gruba mesaj atıyoruz
    bot.send_message(GROUP_ID, "✅ Milyonerler Skor Sistemi Sistem aktif, bol şans")
    while True:
        score_check()
        time.sleep(60)
