import os


#open xpanel database file
with open("Database.sql", "r+") as file:
    database = file.read()
    users = database.split("""INSERT INTO `users` VALUES""")
    users = str(users[1].split(";"))

#extract users from database and replicate them in Dragon
pairs = users.split('),(')
for pair in pairs:
    values = pair.split(',')
    username = values[1][1:-1]
    password = values[2][1:-1]
    expiry = values[7][1:-1]
    limit = values[5][1:-1]
    os.system(f"useradd -e {expiry} -M -s /bin/false -p {password} {username} >/dev/null 2>&1 &")
    os.system(f'echo "{password}" >/etc/VPSManager/senha/{username}')
    os.system(f'echo "{username} {limit}" >>/root/usuarios.db')
