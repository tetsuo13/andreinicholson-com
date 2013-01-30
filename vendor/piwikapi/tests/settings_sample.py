class Settings:
    """
    This class contains settings for the unit tests
    """
    #: The ID of the site you want to send the test tracking requests to
    PIWIK_SITE_ID = 1

    #: This must contain the URL to your Piwik install's /piwik.php, something
    #: like 'http://example.com/piwik.php'
    PIWIK_TRACKING_API_URL = '<Your Piwik tracker API URL>'

    #: This must contain the URL to your Piwik install's root
    PIWIK_ANALYTICS_API_URL = '<Your Piwik API URL>'

    #: The auth token of an admin user for the site defined in PIWIK_SITE_ID
    PIWIK_TOKEN_AUTH = '<Your Piwik auth token>'

    #: The ID of the goal that will be used for unit tests.
    #: If set to ``None`` a goal will be created automatically for each goal
    #: test and deleted after the test has completed successfully.
    PIWIK_GOAL_ID = None
