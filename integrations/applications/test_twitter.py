import unittest
import mysql.connector
from mysql.connector import errorcode
from utils.query_generator import QueryGenerator as query
from utils.config import generate_random_db_name, get_value_from_json_env_var
from utils.log import setup_logger
from utils.instatus import InstatusClient as ins
from utils.template import IncidentTemplate as template


class TestTwitterConnection(unittest.TestCase):
    """
    Test class for testing the Twitter datasource using the MindsDB SQL API.
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
        Clean up the test environment by closing the connection
        to the MindsDB SQL API.
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

    def test_execute_query(self):
        """
        Create a new Twitter Datasource.
        """
        try:
            cursor = self.connection.cursor()
            random_db_name = generate_random_db_name("twitter_datasource")
            twitter_config = get_value_from_json_env_var("INTEGRATIONS_CONFIG", 'twitter')
            query = self.query_generator.create_database_query(
                        random_db_name,
                        "twitter",
                        twitter_config
                    )
            cursor.execute(query)
            cursor.close()
        except Exception as err:
            cloud_temp = self.template.get_integration_template("Twitter", "clkwkimng21735bbocc2j7zguy")
            self.incident.report_incident("cl8nll9f7106187olof1m17eg17", cloud_temp)


if __name__ == "__main__":
    unittest.main()
