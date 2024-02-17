import json
import random


class BasicPromptFetcher:
    def __init__(self):
        self.items = [""]
        self.current_item_index = 0

    def get_random_prompt(self):
        """返回一个随机项。"""
        if not self.items:
            return ""
        return random.choice(self.items)

    def get_next_prompt(self):
        """按顺序返回下一个项，并循环列表。"""
        if not self.items:
            return ""
        item = self.items[self.current_item_index]
        self.current_item_index = (self.current_item_index + 1) % len(self.items)
        return item

    def generate_prompt(self, random_mode=True):
        """生成并返回最终的提示文本。

        Args:
            prefix (str): 在 item 前面添加的文本。
            suffix (str): 在 item 后面添加的文本。
            random_mode (bool): 是否随机选择 item。True 为随机模式，False 为顺序模式。

        Returns:
            str: 生成的提示文本。
        """
        item = self.get_random_prompt() if random_mode else self.get_next_prompt()
        return f"{item}, ".strip()


class PromptFetcher(BasicPromptFetcher):
    def __init__(self, filepath,  random_mode=False):
        super().__init__()
        self.filepath = filepath
        self.items = self.load_prompts()
        self.current_item_index = 0
        self.random_mode = random_mode

    def load_prompts(self):
        """从指定路径加载数据项。"""
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                # 假设文件中的主要内容在一个名为 "items" 的键下
                return data["items"]
        except FileNotFoundError:
            print(f"文件 {self.filepath} 未找到。")
            return []
        except json.JSONDecodeError:
            print(f"文件 {self.filepath} 格式错误。")
            return []

    def get_random_prompt(self):
        """返回一个随机项。"""
        if not self.items:
            return ""
        return random.choice(self.items)

    def get_next_prompt(self):
        """按顺序返回下一个项，并循环列表。"""
        if not self.items:
            return ""
        item = self.items[self.current_item_index]
        self.current_item_index = (self.current_item_index + 1) % len(self.items)
        return item

    def generate_prompt(self, prefix="", suffix=""):
        """生成并返回最终的提示文本。

        Args:
            prefix (str): 在 item 前面添加的文本。
            suffix (str): 在 item 后面添加的文本。
            random_mode (bool): 是否随机选择 item。True 为随机模式，False 为顺序模式。

        Returns:
            str: 生成的提示文本。
        """
        item = self.get_random_prompt() if self.random_mode else self.get_next_prompt()
        return f"{prefix} {item}, {suffix}".strip()


class SingleItemFetcher(BasicPromptFetcher):
    def __init__(self, item):
        super().__init__()  # 调用父类的初始化方法
        self.items = [item]  # 将传入的字符串设置为items列表的唯一元素


class EmptyFetcher(BasicPromptFetcher):
    def generate_prompt(self, random_mode=True):
        """生成并返回一个空的提示文本。

        Returns:
            str: 空字符串。
        """
        return ""
