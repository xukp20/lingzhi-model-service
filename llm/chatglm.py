# online or offline model
ONLINE=1
if ONLINE:
    from zhipuai import ZhipuAI
    import os
    # load api_key from env
    api_key = os.environ.get('ZHIPUAI_API')
    client = ZhipuAI(api_key=api_key) # 填写您自己的APIKey

    def chatglm(messages, model="glm-3-turbo", temperature=0.01, top_p=0.7, max_tokens=512):
        response = client.chat.completions.create(
            model=model,
            messages=messages, 
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def chatglm_once(prompt, input_str, model="glm-3-turbo", temperature=0.01, top_p=0.7, max_tokens=512):
        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": input_str
            }
        ]

        return chatglm(messages, model, temperature, top_p, max_tokens)

else:
    # Local, consider using VLLM TODO
    pass
