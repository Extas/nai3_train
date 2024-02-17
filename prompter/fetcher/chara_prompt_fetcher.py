from .basic_prompt_fetcher import PromptFetcher
import json


class CharacterPromptFetcher(PromptFetcher):
    def load_prompts(self):
        """专门加载角色列表的逻辑。"""
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                prompts = []
                for role in data["role"]:
                    name = role["name"]
                    work = role["work"]
                    prompt = f"{name}, {work}"
                    prompts.append(prompt)
                return prompts
        except FileNotFoundError:
            print(f"文件 {self.filepath} 未找到。")
            return []
        except json.JSONDecodeError:
            print(f"文件 {self.filepath} 格式错误。")
            return []

    def generate_prompt(self, prefix="", suffix=""):
        """
        生成并返回最终的提示文本，自动在前后添加 "1girl" 和 "solo"。

        :param prefix: 用户定义的额外前缀文本。
        :param suffix: 用户定义的额外后缀文本。
        :param random_mode: 是否随机选择角色。
        :return: 生成的提示文本。
        """
        # 在用户定义的前缀前加上 "1girl"，在后缀后加上 "solo"
        final_prefix = f"1girl, {prefix}".strip()
        # 调用基类的 generate_prompt 方法，传递更新后的前后缀参数
        return super().generate_prompt(prefix=final_prefix)
