import os
import getpass
import hashlib
import re

BASE_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# STRONG PASSWORD CHECK
# =========================
def is_strong_password(password):
    if len(password) < 8:
        return False, "Min 8 chars"
    if not re.search(r"[A-Z]", password):
        return False, "Need uppercase"
    if not re.search(r"[a-z]", password):
        return False, "Need lowercase"
    if not re.search(r"[0-9]", password):
        return False, "Need number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Need special char"
    return True, "Strong"

# =========================
# CREATE FOLDER
# =========================
def create_folder():
    folder = input("Enter folder name: ")
    path = os.path.join(BASE_PATH, folder)

    if not os.path.exists(path):
        os.mkdir(path)
        print(f"📁 Created at {path}")
    else:
        print("⚠️ Folder already exists")

# =========================
# SAVE PASSWORD
# =========================
def save_password(path, folder, pwd):
    with open(os.path.join(path, f"{folder}_pass.txt"), "w") as f:
        f.write(hash_password(pwd))

def verify_password(path, folder, pwd):
    try:
        with open(os.path.join(path, f"{folder}_pass.txt"), "r") as f:
            return f.read() == hash_password(pwd)
    except:
        return False

# =========================
# LOCK CORE FUNCTION
# =========================
def perform_lock(path, folder):
    if folder.endswith("_LOCKED"):
        print("⚠️ Already locked!")
        return

    locked_name = folder + "_LOCKED"
    locked_path = os.path.join(path, locked_name)
    original_path = os.path.join(path, folder)

    if os.path.exists(locked_path):
        print("❌ Locked folder already exists!")
        return

    os.rename(original_path, locked_path)
    os.system(f'attrib +h "{locked_path}"')

    print(f"\n🔒 '{locked_name}' LOCKED")

# =========================
# LOCK INTERNAL
# =========================
def lock_folder():
    folder = input("Enter folder name: ")
    path = BASE_PATH

    full_path = os.path.join(path, folder)

    if not os.path.exists(full_path):
        print("❌ Folder not found")
        return

    while True:
        pwd = getpass.getpass("Set password: ")
        valid, msg = is_strong_password(pwd)

        if valid:
            print("✅ Strong password")
            break
        else:
            print("❌", msg)

    save_password(path, folder, pwd)
    perform_lock(path, folder)

# =========================
# LOCK EXTERNAL 🔥
# =========================
def lock_external_folder():
    full_path = input("Enter full folder path: ").strip()

    if not os.path.exists(full_path):
        print("❌ Folder not found!")
        return

    folder = os.path.basename(full_path)
    path = os.path.dirname(full_path)

    if folder.endswith("_LOCKED"):
        print("⚠️ Already locked!")
        return

    while True:
        pwd = getpass.getpass("Set password: ")
        valid, msg = is_strong_password(pwd)

        if valid:
            print("✅ Strong password")
            break
        else:
            print("❌", msg)

    save_password(path, folder, pwd)
    perform_lock(path, folder)

# =========================
# FILE MANAGER
# =========================
def manage_files(path, folder):
    folder_path = os.path.join(path, folder)

    while True:
        print("\n--- File Manager ---")
        print("1. Create File")
        print("2. Edit File")
        print("3. View Files")
        print("4. Exit & Lock")

        ch = input("Choice: ")

        if ch == '1':
            name = input("File name: ")
            with open(os.path.join(folder_path, name), "w") as f:
                f.write(input("Enter content: "))
            print("✅ File created")

        elif ch == '2':
            name = input("File name: ")
            file_path = os.path.join(folder_path, name)

            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write("\n" + input("Add content: "))
                print("✅ Updated")
            else:
                print("❌ File not found")

        elif ch == '3':
            files = os.listdir(folder_path)
            print("\n📂 Files:")
            for f in files:
                print(" -", f)

        elif ch == '4':
            perform_lock(path, folder)
            break

        else:
            print("Invalid")

# =========================
# UNLOCK (WORKS FOR BOTH)
# =========================
def unlock_folder():
    full_path = input("Enter full locked folder path: ").strip()

    if not os.path.exists(full_path):
        print("❌ Locked folder not found")
        return

    folder = os.path.basename(full_path)
    path = os.path.dirname(full_path)

    if not folder.endswith("_LOCKED"):
        print("❌ Not a locked folder")
        return

    original = folder.replace("_LOCKED", "")

    pwd = getpass.getpass("Enter password: ")

    if verify_password(path, original, pwd):
        original_path = os.path.join(path, original)

        os.system(f'attrib -h "{full_path}"')
        os.rename(full_path, original_path)

        print(f"\n🔓 '{original}' UNLOCKED")

        os.startfile(original_path)

        # 🔥 Auto File Manager
        manage_files(path, original)

    else:
        print("❌ Wrong password")

# =========================
# MENU
# =========================
def main():
    while True:
        print("\n===== Secure Folder System =====")
        print("1. Create Folder")
        print("2. Lock Folder (Desktop)")
        print("3. Lock External Folder 🔥")
        print("4. Unlock Folder")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            create_folder()
        elif choice == '2':
            lock_folder()
        elif choice == '3':
            lock_external_folder()
        elif choice == '4':
            unlock_folder()
        elif choice == '5':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
