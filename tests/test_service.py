import json
import fcntl
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='visual shelf ')
        self.root = Path(self.tmp.name)
        for name in ('scripts', 'site', 'catalog', 'assets'):
            shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns('__pycache__'))
        self.command = ['bash', str(self.root / 'scripts' / 'service.sh')]

    def run_service(self, *args, expected=0):
        result = subprocess.run([*self.command, *args], cwd='/', capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def tearDown(self):
        subprocess.run([*self.command, 'stop'], capture_output=True, timeout=15)
        self.tmp.cleanup()

    def test_lifecycle_idempotence_restart_and_http(self):
        port = free_port()
        self.run_service('status', expected=1)
        self.run_service('start', '--port', str(port))
        state = self.root / '.runtime' / 'service.json'
        first = json.loads(state.read_text())
        self.run_service('start')
        self.assertEqual(json.loads(state.read_text())['pid'], first['pid'])
        self.run_service('status')
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/catalog.json', timeout=2) as response:
            self.assertEqual(len(json.load(response)), len(list((self.root / 'catalog').glob('*.json'))))
        self.run_service('restart')
        second = json.loads(state.read_text())
        self.assertEqual(second['port'], port)
        self.assertNotEqual(second['token'], first['token'])
        self.run_service('logs')
        self.run_service('stop')
        self.run_service('stop')
        self.run_service('status', expected=1)

    def test_unrelated_port_owner_is_not_stopped(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0)); sock.listen()
            port = sock.getsockname()[1]
            self.run_service('start', '--port', str(port), expected=2)
            self.assertEqual(sock.getsockname()[1], port)
            self.assertFalse((self.root / '.runtime' / 'service.json').exists())

    def test_stale_state_never_signals_unrelated_pid(self):
        runtime = self.root / '.runtime'
        runtime.mkdir()
        (runtime / 'service.json').write_text(json.dumps({'pid': os.getpid(), 'port': 4173, 'token': 'a' * 48}))
        self.run_service('stop')
        self.assertFalse((runtime / 'service.json').exists())
        os.kill(os.getpid(), 0)

    def test_concurrent_command_rejected(self):
        runtime = self.root / '.runtime'; runtime.mkdir()
        with (runtime / 'service.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.run_service('start', '--port', str(free_port()), expected=2)
        self.run_service('status', expected=1)

    def test_build_failure_does_not_leave_service(self):
        (self.root / 'catalog' / 'broken.json').write_text('{}')
        self.run_service('start', '--port', str(free_port()), expected=2)
        self.assertFalse((self.root / '.runtime' / 'service.json').exists())

    def test_malformed_state_and_bad_port_fail_explicitly(self):
        runtime = self.root / '.runtime'; runtime.mkdir()
        (runtime / 'service.json').write_text('{broken')
        self.run_service('stop', expected=2)
        (runtime / 'service.json').unlink()
        self.run_service('start', '--port', '0', expected=2)


if __name__ == '__main__':
    unittest.main()
