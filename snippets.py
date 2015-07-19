import logging
import argparse
import sys
import psycopg2

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='ubuntu' password='thinkful' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        command = "insert into snippets values (%s, %s)"
        try:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """Getting a snippet with an associated name"""
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    if not row:
        row = [False]
    return row[0]
    
def catalog():
    """Display catalog of keywords"""
    logging.info("Displaying keywords")
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets")
        row = cursor.fetchall()
    logging.debug("Keywords displayed successfully.")
    return row
    
def main():
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    catalog_parser = subparsers.add_parser("catalog", help="Catalog of keywords")
    
    arguments = parser.parse_args(sys.argv[1:])
    
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        if snippet == False:
            print 'Error: Snippet does not exist'
        else:
            print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        keywords = catalog()
        print keywords
        
if __name__ == "__main__":
    main()