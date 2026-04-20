"""
OpenAI API 调用工具
"""
import sys


def call_api(client, system_prompt, user_prompt, temperature=0.4, max_tokens=30000, model=None):
    """调用 OpenAI API"""
    try:
        model_name = model or "claude-opus-4-6"
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n  API 调用失败: {e}")
        return None
