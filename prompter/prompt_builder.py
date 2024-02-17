class PromptBuilder:
    def __init__(self, character_fetchers=None, style_fetchers=None, setting_fetchers=None, feature_fetchers=None,
                 action_fetchers=None, quality_fetchers=None):
        # 初始化各种fetchers
        self.character_fetchers = character_fetchers or []
        self.style_fetchers = style_fetchers or []
        self.setting_fetchers = setting_fetchers or []
        self.feature_fetchers = feature_fetchers or []
        self.action_fetchers = action_fetchers or []
        self.quality_fetchers = quality_fetchers or []

    def build_prompt(self):
        prompt = ""
        file_name_parts = []

        # 处理字符和风格fetchers以构建文件名
        for fetcher_list in [self.character_fetchers, self.style_fetchers]:
            for fetcher in fetcher_list:
                generated_prompt = fetcher.generate_prompt()
                if generated_prompt:
                    prompt += generated_prompt + " "
                    file_name_parts += generated_prompt.split(", ")

        # 按顺序遍历其他fetcher列表并生成prompt
        for fetcher_list in [self.setting_fetchers, self.feature_fetchers, self.action_fetchers, self.quality_fetchers]:
            for fetcher in fetcher_list:
                generated_prompt = fetcher.generate_prompt()
                if generated_prompt:
                    prompt += generated_prompt + " "

        # 构建文件名
        file_name = ("_".join(file_name_parts).replace(" ", "_").replace(",", "_")
                     .replace("__", "_").replace(":", "_") + ".png")

        print("Prompt generated:", prompt.strip())
        print("File name:", file_name)
        # 返回生成的提示和文件名
        return prompt.strip(), file_name
