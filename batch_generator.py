import os
import string
import random
import time
from requests.exceptions import RequestException, SSLError
import zipfile


def save_image_from_binary(image_data, folder_path, base_file_name):
    file_id = 1
    file_name = f"{base_file_name}_{file_id:04d}.png"
    file_path = os.path.join(folder_path, file_name)

    # 检查文件是否存在，如果存在则递增id直到找到一个唯一的文件名
    while os.path.exists(file_path):
        file_id += 1
        file_name = f"{base_file_name}_{file_id:04d}.png"
        file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, "wb") as file:
            file.write(image_data)
        print("图像已保存到：", file_path)
    except IOError as e:
        print("保存图像时出错：", e)


class BatchImageGenerator:
    def __init__(self, image_generator, prompt_builder,
                 folder_path=r".\output", num_images=500, batch_size=10, sleep_time=10, retry_delay=10):
        """
        初始化批量图像生成器。

        :param image_generator: 用于生成图像的生成器实例。
        :param prompt_builder: 用于构建提示文本的PromptBuilder实例。
        :param folder_path: 图像保存的文件夹路径。
        :param num_images: 要生成的图像总数。
        :param batch_size: 每批次生成的图像数量。
        :param sleep_time: 每批次生成后的休眠时间（秒）。
        :param retry_delay: 因错误重试前的延迟时间（秒）。
        """
        self.generator = image_generator
        self.prompt_builder = prompt_builder  # 修改 prompt_template 为 prompt_builder
        self.folder_path = folder_path
        self.num_images = num_images
        self.batch_size = batch_size
        self.sleep_time = sleep_time
        self.retry_delay = retry_delay

    def generate_batch(self):
        """执行批量生成图像的循环逻辑。"""
        for i in range(0, self.num_images):
            retry_attempts = 5  # 设定重试次数
            prompt, file_name = self.prompt_builder.build_prompt()  # 修改 generate_prompt 为 build_prompt
            while retry_attempts > 0:
                try:
                    # 使用 prompt_builder 生成提示文本
                    image_data = self.generator.generate_image(prompt)

                    if not image_data:
                        raise ValueError("生成的图像数据为空，将重试...")

                    # 假设这是一个函数用于从二进制数据保存图像
                    save_image_from_binary(image_data, self.folder_path, file_name)  # 添加示例文件名
                    print(f"图像 #{i + 1} 保存成功。")

                    if (i + 1) % self.batch_size == 0:
                        print(f"已生成 {i + 1} 张图像，休眠 {self.sleep_time} 秒...")
                        time.sleep(self.sleep_time)
                    break  # 图像数据非空，跳出重试循环

                except (SSLError, RequestException, ValueError) as e:
                    print("发生错误:", e)
                    retry_attempts -= 1
                    if retry_attempts > 0:
                        print(f"尝试重新生成图像，剩余重试次数: {retry_attempts}")
                        time.sleep(self.retry_delay)
                    else:
                        print("达到最大重试次数，继续下一张图像生成。")
                        break  # 退出重试循环，继续下一张图像
                except zipfile.BadZipFile as e:
                    print("发生错误:", e)
                    print("忽略此错误，继续脚本运行")
                    break  # 不对此类错误重试，直接继续
