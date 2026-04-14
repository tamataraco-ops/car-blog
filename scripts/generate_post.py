import os
import datetime
import requests
import json
import random

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

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

def generate_article(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
あなたは車・カーナビ・DIYカスタムに詳しいブロガーです。
以下のテーマで日本語のブログ記事を書いてください。

テーマ：{topic}

条件：
- 文字数：800〜1200文字
- 読者は車好きの一般人（専門用語は噛み砕いて説明）
- 見出しはMarkdownの##を使う