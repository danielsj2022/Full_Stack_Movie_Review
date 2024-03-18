import sqlite3
'''Jeremiah Daniels jbd22a
    due 2/21/2024
    The program in this file is the individual work of Jeremiah Daniels
'''
conn=sqlite3.connect("movieData.db")
print("opended db successfully")

conn.execute('CREATE TABLE Reviews(Username TEXT, MovieID TEXT, ReviewTime TEXT, Rating FLOAT, Review TEXT)')
print("table created success")


conn.execute('CREATE TABLE Movies(MovieID TEXT PRIMARY KEY, Title TEXT, Director TEXT, Genre TEXT, Year INT)')
print("table 2 created success")
conn.close()