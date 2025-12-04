import os

import google.generativeai as genai

# 利用可能なモデルをキャッシュ
_available_model = None


def get_available_model():
    """
    利用可能なGemini APIモデルを取得する

    Returns:
        str: 利用可能なモデル名

    Raises:
        ValueError: 利用可能なモデルが見つからない場合
    """
    global _available_model

    if _available_model is not None:
        return _available_model

    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEYが設定されていません")

        genai.configure(api_key=api_key)

        # generateContentをサポートするモデルを取得
        models = genai.list_models()
        available_models = [
            m.name
            for m in models
            if "generateContent" in m.supported_generation_methods
        ]

        if not available_models:
            raise ValueError("利用可能なモデルが見つかりません")

        # 優先順位: gemini-1.5-pro > gemini-1.5-flash > gemini-pro > その他
        for preferred in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]:
            for model_name in available_models:
                if preferred in model_name:
                    _available_model = model_name.replace("models/", "")
                    print(f"使用するGemini APIモデル: {_available_model}")
                    return _available_model

        # 優先モデルが見つからない場合は最初のモデルを使用
        _available_model = available_models[0].replace("models/", "")
        print(f"使用するGemini APIモデル: {_available_model}")
        return _available_model

    except Exception as e:
        print(f"モデル取得エラー: {str(e)}")
        # フォールバック: 一般的なモデル名を試す
        _available_model = "gemini-pro"
        print(f"フォールバックモデルを使用: {_available_model}")
        return _available_model


def improve_text(original_text):
    """
    Gemini APIを使用して文章を改善する

    Args:
        original_text (str): 元の文章

    Returns:
        str: 改善された文章

    Raises:
        Exception: API呼び出しに失敗した場合
    """
    try:
        # APIキーを設定
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEYが設定されていません")

        genai.configure(api_key=api_key)

        # 利用可能なモデルを取得
        model_name = get_available_model()
        model = genai.GenerativeModel(model_name)

        # プロンプトを作成
        prompt = f"""以下の文章をより客観的で端的な表現に改善してください。
改善のポイント:
- 主観的な表現を客観的に
- 冗長な部分を簡潔に
- 曖昧な表現を明確に
- 感情的な表現を中立的に

元の文章:
{original_text}

改善された文章のみを出力してください。説明や前置きは不要です。"""

        # テキスト生成
        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("APIからの応答が空です")

        return response.text.strip()

    except Exception as e:
        # エラーメッセージを詳細に表示
        raise Exception(f"文章の改善に失敗しました: {str(e)}")
