from dropbox import Dropbox

from data.config import API_TOKEN


# авторизация приложения
dropbox_client = Dropbox(API_TOKEN)


if __name__ == '__main__':
    pass
