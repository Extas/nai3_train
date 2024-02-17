import requests
import zipfile
import io
import random

negative_prompt_default = """lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, 
unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract],
{+_+},{chibi},{animal,doll}, {normal quality},weibo watermark, bad hands, mismatched pupils, heart-shaped pupils, 
glowing eye, bad anatomy, @_@"""


class BasicNovelaiImageGenerator:
    def __init__(self, token):
        self.token = token
        self.api = "https://api.novelai.net/ai/generate-image"
        self.headers = {
            "authorization": f"Bearer {self.token}",
            "referer": "https://novelai.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        self.proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",  # 如果你的API也可能通过HTTPS访问，同样设置HTTPS代理
        }

    def generate_image(self, input_text, width=832, height=1216, scale=5, sampler="k_dpmpp_2s_ancestral", steps=28, seed=-1,
                       negative_prompt=negative_prompt_default):
        if seed is None or seed == -1:
            seed = random.randint(0, 9999999999)

        json_payload = {
            "input": input_text + ", best quality, amazing quality, very aesthetic, absurdres",
            "model": "nai-diffusion-3",
            "action": "generate",
            "parameters": {
                "width": width,
                "height": height,
                "scale": scale,
                "sampler": sampler,
                "steps": steps,
                "seed": seed,
                "n_samples": 1,
                "ucPreset": 3,
                "qualityToggle": "true",
                "sm": "true",
                "sm_dyn": "false",
                "dynamic_thresholding": "false",
                "controlnet_strength": 1,
                "legacy": "false",
                "add_original_image": "false",
                "uncond_scale": 1,
                "cfg_rescale": 0,
                "noise_schedule": "native",
                "negative_prompt": negative_prompt,
            },
        }
        try:
            response = requests.post(self.api, json=json_payload, headers=self.headers)
            response.raise_for_status()  # 如果请求返回的状态码不是 2xx，会抛出异常
            if response.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(response.content), mode="r") as zip:
                    with zip.open("image_0.png") as image:
                        return image.read()

        except requests.exceptions.RequestException as e:
            print("请求出现异常:", e)
        except Exception as e:
            print("捕获到未处理的异常:", e)
        return None
