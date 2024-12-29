with open("create_db.sql") as arq:
    import mariadb
    from sys import argv

    if len(argv) < 5 or not argv[2].isnumeric():
        print("WRONG USAGE!")
        print("create_db.py ip port user password")
        print(
            "ip, port, user and password are commonly "
            "127.0.0.1, 3306, root, password respectively."
        )
    else:
        conn = mariadb.connect(
            host=argv[1],
            port=int(argv[2]),
            user=argv[3],
            password=argv[4],
        )
        cur = conn.cursor()
        commands = [
            cmd.replace("\n", "") for cmd in arq.read().split(";") if cmd.strip()
        ]
        for command in commands:
            if command:
                try:
                    cur.execute(command)
                except Exception as e:
                    print(command)
                    print("Error:", e)
        conn.commit()
        conn.close()
