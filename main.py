import dropbox
from dropbox.files import SearchV2Result, CreateFolderResult, FileMetadata, DeleteResult, RelocationResult

from config import API_TOKEN

# авторизация приложения
dropbox_client = dropbox.Dropbox(API_TOKEN)


# загрузка файла на dropbox
def upload_file(local_file_path: str, dropbox_file_path: str) -> FileMetadata | bool:
    try:
        with open(local_file_path, 'rb') as local_file:
            return dropbox_client.files_upload(f=local_file.read(), path=f'{dropbox_file_path}')
    except Exception as error:
        print(f'''You've got error by uploading the file "{dropbox_file_path}": {error}''')
        return False


# удаление файла из dropbox
def delete_file(dropbox_file_path: str) -> DeleteResult | bool:
    try:
        return dropbox_client.files_delete_v2(path=dropbox_file_path)
    except Exception as error:
        print(f'''You've got error by deleting the file "{dropbox_file_path}": {error}''')
        return False


# переименование файла на dropbox
def rename_file(old_file_path: str, new_file_path: str) -> RelocationResult | bool:
    try:
        return dropbox_client.files_move_v2(from_path=old_file_path, to_path=new_file_path)
    except Exception as error:
        print(f'''You've got error by renaming the file "{old_file_path}" to "{new_file_path}": {error}''')
        return False


# перемещение файла на dropbox
def transport_file(old_path_to_file: str, new_path_to_file: str) -> RelocationResult | bool:
    try:
        return dropbox_client.files_move_v2(from_path=old_path_to_file, to_path=new_path_to_file)
    except Exception as error:
        print(f'''You've got error by transporting the file "{old_path_to_file}" to "{new_path_to_file}": {error}''')
        return False


# создание папки на dropbox
def create_dir(dropbox_dir_path: str, new_dir_name: str) -> CreateFolderResult | bool:
    try:
        return dropbox_client.files_create_folder_v2(path=f'{dropbox_dir_path}/{new_dir_name}')
    except Exception as error:
        print(f'''You've got error by creating the dir "{new_dir_name}" in dir "{dropbox_dir_path}": {error}''')
        return False


# поиск файла на dropbox по названию по всему хранилищу
def full_search_by_name(dropbox_file_path: str) -> SearchV2Result | bool:
    try:
        return dropbox_client.files_search_v2(query=f'/{dropbox_file_path}')
    except Exception as error:
        print(f'''You've got error by searching the file "{dropbox_file_path}" in full dropbox: {error}''')
        return False


# поиск файла на dropbox по названию в определённой директории
def current_search_by_name(dropbox_file_path: str, dropbox_dir_path: str) -> SearchV2Result | bool:
    try:
        return dropbox_client.files_search_v2(query=f'{dropbox_dir_path}/{dropbox_file_path}')
    except Exception as error:
        print(f'''You've got error by searching the file "{dropbox_file_path}" in dir "{dropbox_dir_path}": {error}''')
        return False


# вывод списка файлов текущей директории на dropbox
def get_files_list(dropbox_dir_path: str) -> SearchV2Result | bool:
    try:
        pass
        return True
    except Exception as error:
        print(f'''You've got error by getting all content from "{dropbox_dir_path}": {error}''')
        return False


def main() -> None:
    # загрузка файла на dropbox
    # print(upload_file(local_file_path='./local_files/new_python_file.py', dropbox_file_path='/sample/new_python_file.py'), '\n\n')

    # удаление файла из dropbox
    # print(delete_file(dropbox_file_path='/sample/new_python_file.py'), '\n\n')

    # переименование файла на dropbox
    # print(rename_file(old_file_path='/sample/ggg2.txt', new_file_path='/sample/ggg2_renamed.txt'), '\n\n')

    # перемещение файла на dropbox
    # print(transport_file(old_path_to_file='/new_python_file.py', new_path_to_file='/sample/new_dir/new_python_file.py'), '\n\n')

    # создание папки на dropbox
    # print(create_dir(dropbox_dir_path='/sample', new_dir_name='new_dir2'), '\n\n')

    # поиск файла на dropbox по названию по всему хранилищу
    a = full_search_by_name(dropbox_file_path='new_python_file.py')


if __name__ == '__main__':
    main()
    a = full_search_by_name(dropbox_file_path='new_python_file.py')


"""
for elem in a.matches:
...     meta = elem.metadata
...     print(type(meta))
...     print(meta.path_display, '\n\n')


for elem in a.matches:
...     print(elem, '\n\n')
... 
SearchMatchV2(
highlight_spans=NOT_SET, 
match_type=SearchMatchTypeV2('filename', None), 

metadata=MetadataV2('metadata', FileMetadata(client_modified=datetime.datetime(2023, 6, 7, 19, 24, 23), 
content_hash='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 
export_info=NOT_SET, file_lock_info=NOT_SET, has_explicit_shared_members=NOT_SET, 
id='id:xAspLRS2F3MAAAAAAAAADQ', is_downloadable=True, media_info=NOT_SET, name='new_python_file.py', 
parent_shared_folder_id=NOT_SET, path_display='/sample/new_dir/new_python_file.py', 
path_lower='/sample/new_dir/new_python_file.py', preview_url=NOT_SET, property_groups=NOT_SET, 
rev='5fd8f30260e4efe010ba1', server_modified=datetime.datetime(2023, 6, 7, 19, 31, 53), 
sharing_info=NOT_SET, size=91, symlink_info=NOT_SET))) 
"""
