import sqlite3


class SqliteDB:
    """Create database instance."""

    def __init__(self, path):
        self.path = path
        try:
            self.conn = sqlite3.connect(self.path)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            print('Could not perform database operation: ', e)
            self.conn = None
            self.cursor = None

    def g(self, query):
        """Query database for single row.

        Args:
            query (str): SQLite query

        Returns:
            result (dict): Query result
        """
        self.cursor.execute(query)
        columns = [description[0] for description in self.cursor.description]
        result = dict(zip(columns, self.cursor.fetchone()))
        return result

    def q(self, query):
        """Query database for multiple rows.

        Args:
            query (string): SQLite query

        Returns:
            results (list): Query results
        """
        results = []
        self.cursor.execute(query)
        columns = [description[0] for description in self.cursor.description]
        for row in self.cursor.fetchall():
            result = dict(zip(columns, row))
            results.append(result)
        return results
