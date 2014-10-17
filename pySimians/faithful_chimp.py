#!/usr/bin/env python
import os.path

from fabric.api import env, execute, run, put
from fabric.context_managers import settings
from fabric.decorators import serial


@serial
def _unleash_simian(simian):
    simian._upload_tools()
    simian._use_tools()


class FaithfulChimp(object):
    """ Will strike every time """

    def __init__(self, server, port, user, passwd=None):
        self._host = "{0}@{1}:{2}".format(user, server, port)
        self._passwd = passwd
        self._tools = []

    def give_tool(self, tool, toolbox="scripts"):
        self._tools.append((toolbox, tool))

    def unleash(self):
        # workaround a small issue with Fabric and key-based-login
        password = "x" if self._passwd is None else self._passwd
        with settings(hosts=[self._host],
                      password=password,
                      connection_attempts=30,
                      disable_known_hosts=True):
            env.use_ssh_config = True
            execute(_unleash_simian, simian=self)

    def _upload_tools(self):
        for toolbox, tool in self._tools:
            tool_path = os.path.join(toolbox, tool)
            put(tool_path, "./{}".format(tool), use_sudo=False, mode=0644)

    def _use_tools(self):
        env.command_timeout = 60 * 3

        # not working due to one shell per call to run
        run("""echo "TODO: use tool in background" """)
        result = run("dtach -n `mktemp -u /tmp/%s.XXXX` sleep 20 & echo $!",
                     pty=True)

        run("""echo "TODO: use tool and wait to complete" """)
        run("sleep 3")

        # kill running background process
        run("kill -9 {} || true".format(result.split("\n")[0]))


if __name__ == '__main__':
    # TODO move this in a test file
    m = FaithfulChimp("localhost", 22, os.environ.get("USER"))

    # A simple tool
    m.give_tool("test_echo_tool", "test_scripts")

    # A nasty tool
    m.give_tool("burnio.sh")
    m.unleash()
