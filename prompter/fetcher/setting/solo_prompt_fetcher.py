from ..basic_prompt_fetcher import BasicPromptFetcher

class SoloPromptFetcher(BasicPromptFetcher):
    def generate_prompt(self, random_mode=True):
        """生成并返回一个单人的提示文本。

        Returns:
            str: 包含单人描述的字符串。
        """
        return "solo, "
