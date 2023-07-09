import os
import subprocess

# download database file
def get_file():
    link = input("لطفا لینک فایل دیتابیس را وارد کنید: \n ")
    dbfile = link.rpartition("/")[2]
    subprocess.run(["wget", link])

    if os.path.exists(dbfile):
        print("فایل دریافت شد.")
        extract_users(dbfile)
    else:
        print("مشکل در دریافت فایل.")




# Extract users
def extract_users(dbfile):
    try:
        with open(dbfile, "r") as file:
            database = file.read()
            users = str(database.split("""INSERT INTO `users` VALUES""")[1].split(";")).split('),(')
            print("استخراج اطلاعات با موفقیت انجام شد.")
            create_users(users)

    except:
        print(f"مشکل در استخراج اطلاعات.")


#Create users and register in Dragon
def create_users(users):
    try:
        for user in users:
            values = user.split(',')
            username = values[1][1:-1]
            password = values[2][1:-1]
            encpassword = subprocess.getoutput(f"""perl -e 'print crypt($ARGV[0], "password")' {password}""")
            expiry = values[7][1:-1]
            limit = values[5][1:-1]
            os.system(f"useradd -e {expiry} -M -s /bin/false -p {encpassword} {username} >/dev/null 2>&1 &")
            os.system(f'echo "{password}" >/etc/VPSManager/senha/{username}')
            os.system(f'echo "{username} {limit}" >>/root/usuarios.db')
        print("انتقال کاربران با موفقیت انجام شد.")
    except:
        print("مشکل در انتقال کاربران.")


get_file()


