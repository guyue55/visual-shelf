#!/usr/bin/env python3
"""Local preview lifecycle. POSIX only (macOS/Linux), Python stdlib."""
import argparse
import fcntl
import functools
import http.server
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime'
STATE = RUNTIME / 'service.json'
LOG = RUNTIME / 'service.log'


def load_state():
    if not STATE.exists():
        return None
    try:
        state = json.loads(STATE.read_text())
        if not isinstance(state['pid'], int) or state['pid'] <= 1:
            raise ValueError('invalid pid')
        if not isinstance(state['port'], int) or not 1024 <= state['port'] <= 65535:
            raise ValueError('invalid port')
        if not isinstance(state['token'], str) or len(state['token']) != 48:
            raise ValueError('invalid token')
        return state
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(f'状态文件损坏，未执行进程操作：{STATE}') from exc


def owned(state):
    if not state:
        return False
    result = subprocess.run(['ps', '-ww', '-p', str(state['pid']), '-o', 'args='], capture_output=True, text=True)
    command = result.stdout.strip()
    # Check full script path plus per-start random token, not PID alone.
    return result.returncode == 0 and str(Path(__file__).resolve()) in command and '--serve' in command and state['token'] in command


def healthy(state):
    if not owned(state):
        return False
    try:
        request = urllib.request.Request(f'http://127.0.0.1:{state["port"]}/__visual_shelf_health__')
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(request, timeout=0.5) as response:
            return json.load(response) == {'token': state['token']}
    except (OSError, ValueError):
        return False


def serve(port, token):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/__visual_shelf_health__':
                data = json.dumps({'token': token}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                super().do_GET()
    handler = functools.partial(Handler, directory=str(ROOT / 'dist'))
    with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as server:
        server.serve_forever()


def stop():
    state = load_state()
    if not state:
        print('STOPPED：没有受管服务')
        return
    if not owned(state):
        STATE.unlink(missing_ok=True)
        print('STOPPED：已清理过期状态；未向其他进程发送信号')
        return
    os.kill(state['pid'], signal.SIGTERM)
    for _ in range(50):
        if not owned(state):
            STATE.unlink(missing_ok=True)
            print('STOPPED：服务已停止')
            return
        time.sleep(0.1)
    raise RuntimeError('停止超时，保留状态供排查；没有强制 kill')


def start(port):
    state = load_state()
    if owned(state):
        if not healthy(state):
            raise RuntimeError('受管进程存在但健康检查失败；请查看 logs 后 restart')
        if port is not None and port != state['port']:
            raise RuntimeError('已有服务运行在其他端口；使用 restart --port 切换')
        print(f'RUNNING：已启动 http://127.0.0.1:{state["port"]}/ PID={state["pid"]}')
        return
    STATE.unlink(missing_ok=True)
    port = port or 4173
    # Preflight avoids rebuilding when an unrelated service already owns the port.
    with socket.socket() as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('127.0.0.1', port))
        except OSError as exc:
            raise RuntimeError(f'端口 {port} 不可用，未停止任何进程；请使用 --port 指定空闲端口') from exc
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'library.py'), 'build'], cwd=ROOT, check=True)
    token = secrets.token_hex(24)
    with LOG.open('ab') as log:
        process = subprocess.Popen([sys.executable, '-u', str(Path(__file__).resolve()), '--serve', str(port), token],
                                   cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                   start_new_session=True, close_fds=True)
    state = {'pid': process.pid, 'port': port, 'token': token}
    try:
        for _ in range(50):
            if process.poll() is not None:
                raise RuntimeError(f'启动进程提前退出，查看 {LOG}')
            if healthy(state):
                temporary = RUNTIME / 'service.json.tmp'
                temporary.write_text(json.dumps(state) + '\n')
                temporary.replace(STATE)
                print(f'RUNNING：http://127.0.0.1:{port}/ PID={process.pid}\n日志：{LOG}')
                return
            time.sleep(0.1)
        raise RuntimeError(f'健康检查超时，查看 {LOG}')
    except BaseException:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        raise


def main():
    if len(sys.argv) == 4 and sys.argv[1] == '--serve':
        serve(int(sys.argv[2]), sys.argv[3])
        return 0
    parser = argparse.ArgumentParser(description='Visual Shelf 本地预览管理（macOS/Linux）')
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'status', 'logs'])
    parser.add_argument('--port', type=int, help='start/restart 使用，默认 4173；restart 未指定时沿用受管端口')
    args = parser.parse_args()
    if args.port is not None and (args.command not in ('start', 'restart') or not 1024 <= args.port <= 65535):
        parser.error('--port 仅用于 start/restart，范围 1024～65535')
    if sys.version_info < (3, 11):
        parser.error('需要 Python 3.11+')
    RUNTIME.mkdir(mode=0o700, exist_ok=True)
    # Kernel lock releases on exit, including interruption; no stale mkdir locks.
    with (RUNTIME / 'service.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.command == 'start':
            start(args.port)
        elif args.command == 'stop':
            stop()
        elif args.command == 'restart':
            previous = load_state()
            port = args.port or (previous['port'] if previous else 4173)
            stop()
            start(port)
        elif args.command == 'logs':
            print('\n'.join(LOG.read_text(errors='replace').splitlines()[-80:]) if LOG.exists() else '暂无日志')
        else:
            state = load_state()
            if healthy(state):
                print(f'RUNNING：http://127.0.0.1:{state["port"]}/ PID={state["pid"]}')
                return 0
            print('UNHEALTHY：进程存在，HTTP 健康检查失败' if owned(state) else 'STOPPED：没有存活的受管服务（不代表端口空闲）')
            return 1
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BlockingIOError:
        print('失败：另一个管理命令正在执行，请稍后重试', file=sys.stderr)
        sys.exit(2)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f'失败：{exc}', file=sys.stderr)
        sys.exit(2)
