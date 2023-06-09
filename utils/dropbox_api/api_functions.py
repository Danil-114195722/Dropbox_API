from dropbox import Dropbox
from dropbox.files import CreateFolderResult, DeleteResult, RelocationResult, FileMetadata, FolderMetadata


# загрузка файла на dropbox
def upload_file(dropbox_client: Dropbox, local_file_path: str, dropbox_file_path: str) -> FileMetadata | bool:
    try:
        with open(local_file_path, 'rb') as local_file:
            return dropbox_client.files_upload(f=local_file.read(), path=f'{dropbox_file_path}')
    except Exception as error:
        print(f'''You've got error by uploading the file "{dropbox_file_path}": {error}''')
        return False


# удаление файла из dropbox
def delete_file(dropbox_client: Dropbox, dropbox_file_path: str) -> DeleteResult | bool:
    try:
        return dropbox_client.files_delete_v2(path=dropbox_file_path)
    except Exception as error:
        print(f'''You've got error by deleting the file "{dropbox_file_path}": {error}''')
        return False


# переименование файла на dropbox
def rename_file(dropbox_client: Dropbox, old_file_path: str, new_file_path: str) -> RelocationResult | bool:
    try:
        return dropbox_client.files_move_v2(from_path=old_file_path, to_path=new_file_path)
    except Exception as error:
        print(f'''You've got error by renaming the file "{old_file_path}" to "{new_file_path}": {error}''')
        return False


# перемещение файла на dropbox
def transport_file(dropbox_client: Dropbox, old_path_to_file: str, new_path_to_file: str) -> RelocationResult | bool:
    try:
        return dropbox_client.files_move_v2(from_path=old_path_to_file, to_path=new_path_to_file)
    except Exception as error:
        print(f'''You've got error by transporting the file "{old_path_to_file}" to "{new_path_to_file}": {error}''')
        return False


# создание папки на dropbox
def create_dir(dropbox_client: Dropbox, dropbox_dir_path: str, new_dir_name: str) -> CreateFolderResult | bool:
    try:
        return dropbox_client.files_create_folder_v2(path=f'{dropbox_dir_path}/{new_dir_name}')
    except Exception as error:
        print(f'''You've got error by creating the dir "{new_dir_name}" in dir "{dropbox_dir_path}": {error}''')
        return False


# поиск файла на dropbox по названию по всему хранилищу
def full_search_by_name(dropbox_client: Dropbox, dropbox_file_name: str) -> list:
    return_list = []

    try:
        all_matches = dropbox_client.files_search_v2(query=f'/{dropbox_file_name}')
        for match in all_matches.matches:
            file_metadata = match.metadata._value
            return_list.append(file_metadata.path_display)
    except Exception as error:
        print(f'''You've got error by searching the file "{dropbox_file_name}" in full dropbox: {error}''')

    return return_list


# вывод содержимого текущей директории на dropbox
def get_files_list(dropbox_client: Dropbox, dropbox_dir_path: str) -> list:
    dir_content = []

    try:
        all_entities = dropbox_client.files_list_folder(path=dropbox_dir_path)
        for entity in all_entities.entries:
            entity_type = 'файл'
            if isinstance(entity, FolderMetadata):
                entity_type = 'папка'
            dir_content.append((entity_type, entity.name))
    except Exception as error:
        print(f'''You've got error by getting all content from "{dropbox_dir_path}": {error}''')

    return dir_content


def main() -> None:
    # загрузка файла на dropbox
    # print(upload_file(local_file_path='./local_files/test_python_file.py', dropbox_file_path='/sample/test_python_file.py'), '\n\n')

    # удаление файла из dropbox
    # print(delete_file(dropbox_file_path='/sample/test_python_file.py'), '\n\n')

    # переименование файла на dropbox
    # print(rename_file(old_file_path='/sample/ggg2.txt', new_file_path='/sample/ggg2_renamed.txt'), '\n\n')

    # перемещение файла на dropbox
    # print(transport_file(old_path_to_file='/test_python_file.py', new_path_to_file='/sample/new_dir/test_python_file.py'), '\n\n')

    # создание папки на dropbox
    # print(create_dir(dropbox_dir_path='/sample', new_dir_name='new_dir2'), '\n\n')

    # поиск файла на dropbox по названию по всему хранилищу
    # all_matches = full_search_by_name(dropbox_file_name='test_python_file.py')

    # вывод списка файлов текущей директории на dropbox
    # all_matches = get_files_list(dropbox_dir_path='/sample')

    # for match in all_matches:
    #     print(match)
    pass


if __name__ == '__main__':
    main()
