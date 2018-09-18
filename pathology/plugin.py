"""
Plugin definition for the pathology Opal plugin
"""
from opal.core import plugins

from pathology.urls import urlpatterns

class PathologyPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our Opal application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.pathology': [
            # 'js/pathology/app.js',
            # 'js/pathology/controllers/larry.js',
            # 'js/pathology/services/larry.js',
        ]
    }

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {}

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}