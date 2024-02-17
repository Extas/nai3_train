import json

from generator.basic_novelai_image_generator import BasicNovelaiImageGenerator
from prompter.fetcher.chara_prompt_fetcher import CharacterPromptFetcher
from prompter.fetcher.basic_prompt_fetcher import EmptyFetcher, SingleItemFetcher
from prompter.fetcher.quality_prompt_fetcher import QualityPromptFetcher
from prompter.fetcher.setting.solo_prompt_fetcher import SoloPromptFetcher
from prompter.fetcher.state.wardrobe_malfunction import WardrobeMalfunctionPromptFetcher

from prompter.prompt_builder import PromptBuilder

from batch_generator import BatchImageGenerator

characters_path = r".\json\role\base_role.json"


def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)


config_path = r'.\config.json'  # 配置文件路径
config = load_config(config_path)
token = config.get('token', '')  # 如果配置文件中没有token，返回空字符串
# 生成多张图像并保存

generator = BasicNovelaiImageGenerator(token)
chara_fetcher = CharacterPromptFetcher(filepath=characters_path, random_mode=False)
quality_fetcher = QualityPromptFetcher()
solo_fetcher = SoloPromptFetcher()
empty_fetcher = EmptyFetcher()
shouukun = SingleItemFetcher("{fukuro_daizi},[naga_u,henreader],[[ask_(askzy),ama_mitsuki]],mikozin,{kaede_(sayappa),goldowl},[wlop,nekojira],[[ke-ta,mignon]],{{teranekosu,gin00}},year_2023,")
wardrobe_malfunction = WardrobeMalfunctionPromptFetcher()

# 人物词+风格词+镜头词/环境词+人物特征描写+动作词+质量词
prompt_builder = PromptBuilder([chara_fetcher], [shouukun], [solo_fetcher],
                               [wardrobe_malfunction], [empty_fetcher], [quality_fetcher])

batch_generator = BatchImageGenerator(
    image_generator=generator,
    prompt_builder=prompt_builder
)

batch_generator.generate_batch()
