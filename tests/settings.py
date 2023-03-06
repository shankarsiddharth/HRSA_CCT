"""
Skip all the tests that require a connection to the cloud.
This is useful if you are running the tests on a machine that does not have an internet connection.
or if you are running the tests on a machine that does not have the required credentials
or if you are running the tests, and you do not want to incur the cost of using the cloud services.
"""
SKIP_CLOUD_CONNECT_TESTS = False

"""
Skip all the tests that incur considerable cost for using the cloud services.
"""
SKIP_CLOUD_CONNECT_TESTS_WITH_HIGH_COST = True

"""
Skip tests that require a connection to the cloud, but only if the cost of the operation is negligible.
This is useful to test the cloud connection, the services, the credentials, and the application APIs. 
"""
SKIP_CLOUD_CONNECT_TESTS_WITH_NEGLIGIBLE_COST = False
