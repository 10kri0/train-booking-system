# -*- coding: utf-8 -*-
"""
RailBook -- Database Setup Helper
Run: python setup_db.py
"""
import subprocess, sys, os, getpass

MYSQL_BIN = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"


def try_connect(password):
    import pymysql
    try:
        conn = pymysql.connect(host='localhost', user='root',
                               password=password, connect_timeout=5)
        conn.close()
        return True
    except Exception:
        return False


def update_env(password):
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    lines = []
    if os.path.exists(env_path):
        with open(env_path) as f:
            lines = f.readlines()

    updated, new_lines = False, []
    for line in lines:
        if line.startswith('DB_PASSWORD='):
            new_lines.append(f'DB_PASSWORD={password}\n')
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f'DB_PASSWORD={password}\n')

    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print("  [OK] Updated .env with DB_PASSWORD")


def create_database(password):
    import pymysql
    try:
        conn = pymysql.connect(host='localhost', user='root', password=password)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS train_booking_db "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    print("=" * 55)
    print("  RailBook -- MySQL Database Setup")
    print("=" * 55)

    try:
        import pymysql
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymysql'])
        import pymysql

    # Step 1: Connection test
    print("\n[1/3] Testing MySQL connection with no password...")
    if try_connect(''):
        print("  [OK] Connected! (root has no password)")
        password = ''
    else:
        print("  [FAIL] Root requires a password.")
        print()
        password = None
        for attempt in range(3):
            pwd = getpass.getpass(f"  Enter MySQL root password (attempt {attempt+1}/3): ")
            if try_connect(pwd):
                print("  [OK] Connected successfully!")
                password = pwd
                break
            else:
                print("  [FAIL] Wrong password. Try again.")
        if password is None:
            print("\n  [ERROR] Could not connect after 3 attempts.")
            print("  Make sure MySQL Server is running and try again.")
            sys.exit(1)

    # Step 2: Update .env
    print("\n[2/3] Updating .env...")
    update_env(password)

    # Step 3: Create database
    print("\n[3/3] Creating database 'train_booking_db'...")
    if create_database(password):
        print("  [OK] Database ready!")
    else:
        print("  [ERROR] Could not create database. Check permissions.")
        sys.exit(1)

    print("\n" + "=" * 55)
    print("  Setup complete! Now run:  python app.py")
    print("=" * 55)


if __name__ == '__main__':
    main()
