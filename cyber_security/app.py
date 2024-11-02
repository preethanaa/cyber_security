from flask import Flask, jsonify, request
import threading
from vulnerability_scanner import VulnerabilityScanner

app = Flask(_name_)

scanner = VulnerabilityScanner()

@app.route('/start_scan', methods=['POST'])
def start_scan():
    target_url = request.json.get('url')
    if not target_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    scan_id = scanner.start_scan(target_url)
    return jsonify({'scan_id': scan_id}), 200

@app.route('/scan_status/<scan_id>', methods=['GET'])
def scan_status(scan_id):
    status = scanner.get_scan_status(scan_id)
    return jsonify({'status': status}), 200

@app.route('/report/<scan_id>', methods=['GET'])
def get_report(scan_id):
    report = scanner.generate_report(scan_id)
    return jsonify(report), 200

if _name_ == '_main_':
    app.run(debug=True)