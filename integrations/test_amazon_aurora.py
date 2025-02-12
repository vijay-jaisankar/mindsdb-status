import unittest
import mysql.connector
from mysql.connector import errorcode
from utils.query_generator import QueryGenerator as query
from utils.config import get_value_from_json_env_var, generate_random_db_name
from utils.log import setup_logger
from utils.instatus import InstatusClient as ins
from utils.template import IncidentTemplate as template

class TestAmazonAuroraConnection(unittest.TestCase):
    """
    Test class for testing the Amazon Aurora datasource (for both MySQL and PostgreSQL) using the MindsDB SQL API.
    """

    def setUp(self):
        """
        Set up the test environment by establishing a connection
        to the MindsDB SQL API.
        """
        self.incident = ins()
        self.template = template()
        self.query_generator = query()
        self.logger = setup_logger(__name__)
        try:
            config = get_value_from_json_env_var('INTEGRATIONS_CONFIG', 'mindsdb_cloud')
            self.connection = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            cloud_temp = self.template.get_cloud_sql_api_template()
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.incident.report_incident("cl8nll9f7106187olof1m17eg17", cloud_temp)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                self.incident.report_incident("cl8nll9f7106187olof1m17eg17", cloud_temp)

    def tearDown(self):
        """
        Clean up the test environment by closing the connection to the MindsDB SQL API.
        """
        if self.connection.is_connected():
            self.connection.close()

    def test_connection_established(self):
        """
        Test that the connection to the MindsDB SQL API is established.
        """
        if not self.connection.is_connected():
            cloud_temp = self.template.get_cloud_sql_api_template()
            self.incident.report_incident("cl8nll9f7106187olof1m17eg17", cloud_temp)

    def test_execute_query_for_mysql(self):
        """
        Create a new Amazon Aurora MySQL Datasource.
        """
        try:
            cursor = self.connection.cursor()
            random_db_name = generate_random_db_name("aurora_mysql_datasource")
            aws_mysql_config = get_value_from_json_env_var("INTEGRATIONS_CONFIG", 'aws_mysql')
            query = self.query_generator.create_database_query(
                        random_db_name,
                        "aurora",
                         aws_mysql_config
                    )
            cursor.execute(query)
            cursor.close()
        except Exception as err:
            cloud_temp = self.template.get_integration_template("Amazon Aurora MySQL", "clktp2ulb175778c1oqbp0rev8j")
            self.incident.report_incident("cl8nll9f7106187olof1m17eg17", cloud_temp)

    def test_execute_query_for_postgresql(self):
        """
        Create a new Amazon Aurora PostgreSQL Datasource.
        """
        try:
            cursor = self.connection.cursor()
            random_db_name = generate_random_db_name("aurora_mysql_datasource")
            aws_postgresql_config = get_value_from_json_env_var("INTEGRATIONS_CONFIG", 'aws_postgresql')
            query = self.query_generator.create_database_query(
                        random_db_name,
                        "aurora",
                         aws_postgresql_config
                    )
            cursor.execute(query)
            cursor.close()
        except Exception as err:
            cloud_temp = self.template.get_integration_template("Amazon Aurora MySQL", "clktp3jrv174405c8oqfjwvunwh")
            self.incident.report_incident("cl8nll9f7106187olof1m17eg17", cloud_temp)


if __name__ == "__main__":
    unittest.main()
