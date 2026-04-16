import os
import datetime
import zoneinfo
import requests
import json
import random
import hashlib

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
UNSPLASH_ACCESS_KEY = os.environ["UNSPLASH_ACCESS_KEY"]

# 記事テーマリスト
TOPICS = [
    "カーナビの音量を速度に合わせて自動調整する機能の使い方",
    "ドライブレコーダーの取り付け方法と注意点",
    "車のバッテリー上がりの原因と対処法",
    "カーナビのバージョンアップのやり方",
    "車内をスッキリ整理するおすすめ収納グッズ",
    "燃費を良くするための運転のコツ",
    "タイヤ交換の時期の見極め方",
    "車のヘッドライトが暗い時の対処法",
    "ETC取り付けのDIY方法",
    "スマホホルダーのおすすめと選び方",
    "車のエアコンフィルター交換方法",
    "ドアミラーの自動格納が効かない時の対処法",
    "カーオーディオのスピーカー交換入門",
    "バックカメラの映りが悪い原因と改善方法",
    "車内でFire TV Stickを使う方法",
]

def get_unsplash_image(keyword):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": keyword,
        "per_page": 1,
        "orientation": "landscape"
    }
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data["results"]:
        photo = data["results"][0]
        image_url = photo["urls"]["regular"]
        author = photo["user"]["name"]
        author_url = photo["user"]["links"]["html"]
        return image_url, author, author_url
    return None, None, None

def generate_article(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
あなたは車・カーナビ・DIYカスタムに詳しいブロガーです。
以下のテーマで日本語のブログ記事を書いてください。

テーマ：{topic}

条件：
- 文字数：800〜1200文字
- 読者は車好きの一般人（専門用語は噛み砕いて説明）
- 見出しはMarkdownの##を使う
- 実用的で具体的な内容にする
- 冒頭に導入文、最後にまとめを入れる
- タイトルは記事の最初に「# タイトル」の形式で書く
- ブログ名は「ダッシュボードの住人」、筆者名は「管理人」とする
- 「〇〇」「○○」「◯◯」などのプレースホルダーは絶対に使わない
"""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def save_post(content, topic):
    today = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
    slug = hashlib.md5(topic.encode()).hexdigest()[:8]
    filename = f"content/posts/{today}-{slug}.md"
    
    os.makedirs("content/posts", exist_ok=True)
    
    # タイトル抽出
    lines = content.strip().split("\n")
    title = ""
    body = content
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            body = "\n".join(lines[i+1:]).strip()
            break
    
    # キーワードマップ
    keyword_map = {
        "カーナビ": "car navigation",
        "ドライブレコーダー": "dashcam car",
        "バッテリー": "car battery",
        "タイヤ": "car tire",
        "ETC": "highway toll",
        "スマホホルダー": "phone mount car",
        "エアコン": "car air conditioning",
        "スピーカー": "car audio speaker",
        "バックカメラ": "car rear camera",
        "Fire TV": "streaming device car",
    }
    keyword = "car"
    for jp, en in keyword_map.items():
        if jp in topic:
            keyword = en
            break

    image_url, author, author_url = get_unsplash_image(keyword)
    
    keyword2 = keyword + " interior" if keyword != "car" else "car dashboard"
    image_url2, author2, author_url2 = get_unsplash_image(keyword2)
    
    image_credit2 = ""
    if image_url2:
        image_credit2 = f'\n![{title}]({image_url2})\n*Photo by [{author2}]({author_url2}) on [Unsplash](https://unsplash.com)*\n\n'
    
    body_lines = body.split("\n")
    new_body = []
    inserted = False
    for line in body_lines:
        if line.startswith("## ") and not inserted:
            new_body.append(image_credit2)
            inserted = True
        new_body.append(line)
    body = "\n".join(new_body)
    
    frontmatter = f"""---
title: "{title}"
date: {today}
draft: false
image: "{image_url}"
---
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(frontmatter + "\n" + body)
    
    print(f"記事を生成しました: {filename}")

if __name__ == "__main__":
    topic = random.choice(TOPICS)
    print(f"テーマ: {topic}")
    content = generate_article(topic)
    save_post(content, topic)
