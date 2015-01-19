import os

from qubell.api.testing import *

@environment({
    "default": {},
    "AmazonEC2_CentOS_63": {
        "policies": [{
            "action": "provisionVms",
            "parameter": "imageId",
            "value": "us-east-1/ami-eb6b0182"
        }, {
            "action": "provisionVms",
            "parameter": "vmIdentity",
            "value": "root"
        }]
    }
})
class JenkinsDevComponentTestCase(BaseComponentTestCase):
    name = "component-jenkins"
    apps = [{
        "name": name,
        "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name))
    }]
    @classmethod
    def timeout(cls):
        return 60
    @instance(byApplication=name)
    @values({"output.jenkins-server-host": "hosts"})
    def test_port(self, instance, hosts, port=8080):
        import socket
        import time
        time.sleep(60)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hosts, int(port)))

        assert result == 0

@environment({
    "AmazonEC2_Ubuntu_1204": {
        "policies": [{
            "action": "provisionVms",
            "parameter": "imageId",
            "value": "us-east-1/ami-d0f89fb9"
        }, {
            "action": "provisionVms",
            "parameter": "vmIdentity",
            "value": "ubuntu"
        }]
    }
})
class JenkinsDevUbuntuComponentTestCase(BaseComponentTestCase):
    name = "component-jenkins"
    apps = [{
        "name": name,
        "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name)),
        "parameters": {
          "configuration.jenkins-version": "1.572",
          "configuration.install-method": "war"
        }
    }]
    @classmethod
    def timeout(cls):
        return 60
    @instance(byApplication=name)
    @values({"output.jenkins-server-host": "hosts"})
    def test_port(self, instance, hosts, port=8080):
        import socket
        import time
        time.sleep(60)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hosts, int(port)))

        assert result == 0
