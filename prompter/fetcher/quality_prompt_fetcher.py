from .basic_prompt_fetcher import BasicPromptFetcher
import json


class QualityPromptFetcher(BasicPromptFetcher):
    def generate_prompt(self, random_mode=True):
        """生成并返回一个包含质量描述的提示文本。

        Returns:
            str: 包含多个质量描述的字符串。
        """
        return "best quality, amazing quality, very aesthetic, absurdres"
