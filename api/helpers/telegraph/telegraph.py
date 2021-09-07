from telegraph import Telegraph
from jinja2 import Environment, FileSystemLoader


class TelegraphPost:
    def __init__(self, short_name, author_name):
        self.telegraph = Telegraph()
        self.__SHORT_NAME = short_name
        self.__AUTHOR_NAME = author_name
        self.__TELEGRAPH_TOKEN = self.create_acc()
        self.__TEMPLATE_ENV = Environment(
            loader=FileSystemLoader(searchpath="api/templates")
        )

    def create_acc(self):
        self.telegraph.create_account(
            short_name=self.__SHORT_NAME, author_name=self.__AUTHOR_NAME
        )
        telegraph_token = self.telegraph.get_access_token()
        return telegraph_token

    def create_post(self, rom_name, device, changelog, rom_pic):
        template = self.__TEMPLATE_ENV.get_template("template.html")
        html_content = template.render(
            rom_pic=rom_pic, rom_name=rom_name, changelog=changelog, device=device
        )
        title = f"{rom_name} for {device}"
        response = Telegraph(access_token=self.__TELEGRAPH_TOKEN).create_page(
            title=title, html_content=html_content, author_name=self.__AUTHOR_NAME
        )

        return f'https://telegra.ph/{response["path"]}'
