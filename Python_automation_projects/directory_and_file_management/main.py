import os
import shutil
import stat


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 Folder created: {folder_name}")
    else:
        print(f"⚠️ Folder already exists: {folder_name}")


def create_file(file_name, content=""):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 File created: {file_name}")


def read_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            print(f"📖 File content ({file_name}):\n{f.read()}")
    else:
        print("❌ File not found!")


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"🗑️ File deleted: {file_name}")
    else:
        print("❌ File to delete not found!")


def rename_item(old_name, new_name):
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"✏️ Renamed: {old_name} → {new_name}")
    else:
        print("❌ File or folder not found!")


def move_file(file_name, target_folder):
    if os.path.exists(file_name):
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(file_name, target_folder)
        print(f"📦 {file_name} → moved to {target_folder}")
    else:
        print("❌ File not found!")


def handle_remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name, onerror=handle_remove_readonly)
        print(f"🗑️ Folder deleted: {folder_name}")
    else:
        print("❌ Folder to delete not found!")


def organize_files_by_type(folder_name):
    if not os.path.exists(folder_name):
        print("❌ Folder not found!")
        return
    for file in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file)
        if os.path.isfile(file_path):
            ext = file.split(".")[-1]
            target_folder = os.path.join(folder_name, ext.upper())
            os.makedirs(target_folder, exist_ok=True)
            shutil.move(file_path, target_folder)
            print(f"📂 {file} → moved to {target_folder}")


def clean_empty_folders(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        if not os.listdir(root):
            os.rmdir(root)
            print(f"🗑️ Empty folder removed: {root}")


if __name__ == "__main__":
    test_path = r"C:\Users\lalah\OneDrive\Desktop\EXAMPLE"

    # 1. Create a folder
    # create_folder(test_path)

    # 2. Create and write to a file
    # create_file(os.path.join(test_path, "example.txt"), "Hello World!")

    # 3. Read a file
    # read_file(os.path.join(test_path, "example.txt"))

    # 4. Rename a file
    # rename_item(
    #     os.path.join(test_path, "example.txt"),
    #     os.path.join(test_path, "renamed.txt")
    # )

    # 5. Move a file to another folder
    # move_file(
    #     os.path.join(test_path, "renamed.txt"),
    #     os.path.join(test_path, "MovedFiles")
    # )

    # 6. Organize files by type
    # organize_files_by_type(test_path)

    # 7. Remove empty folders
    # clean_empty_folders(test_path)

    # 8. Delete folder with all contents
    # delete_folder(test_path)
