import sqlite3
from sqlite3 import Error

class_a=0
class_b=0
class_c=0
class_d=0

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' REPLACE INTO person(name,passwd,amount)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' REPLACE INTO trash(id,class_a,class_b,class_c,class_d)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def update_data(class_a_add,class_b_add,class_c_add,class_d_add):
    database = r"/home/baicaitong/trashbin_project_webapi/pythonsqlite.db"
    global class_a
    global class_b
    global class_c
    global class_d

    class_a+=class_a_add
    class_b+=class_b_add
    class_c+=class_c_add
    class_d+=class_d_add
    sum=class_a + class_b +class_c+class_d
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        # project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        # project_id = create_project(conn, project)

        # tasks
        task_1 = ('baicaitong',123456,sum)
        task_2 = (1,class_a,class_b,class_c,class_d)

        # create tasks
        create_project(conn, task_1)
        create_task(conn, task_2)


def query_person():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    database = r"/home/baicaitong/trashbin_project_webapi/pythonsqlite.db"
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM person")

        rows = cur.fetchall()

        # for row in rows:
        #     print(row)
    return rows[0]
def query_trash():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    database = r"/home/baicaitong/trashbin_project_webapi/pythonsqlite.db"
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM trash")

        rows = cur.fetchall()

        # for row in rows:
        #     print(row)
    return rows[0]
# t=query_person()
# print(t[0])

# q=query_trash()
# print(q[2])












# def select_task_by_priority(conn, priority):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(row)







