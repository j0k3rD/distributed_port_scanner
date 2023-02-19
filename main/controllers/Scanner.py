#Controller para Scanners
from flask_restful import Resource
from flask import jsonify, request
from ..models.scanner import Scanner as ScannerModel
from .. import db

class Scanner(Resource):
    def get(self, id):
        scanner = ScannerModel.query.get_or_404(id)
        return jsonify(scanner.to_json())

    def put(self, id):
        scanner = ScannerModel.query.get_or_404(id)
        data = request.json
        scanner.ip = data.get('ip', scanner.ip)
        scanner.port = data.get('port', scanner.port)
        db.session.add(scanner)
        db.session.commit()
        return jsonify(scanner.to_json())

    def delete(self, id):
        scanner = ScannerModel.query.get_or_404(id)
        db.session.delete(scanner)
        db.session.commit()
        return jsonify({'message': 'Scanner deleted'})

class Scanners(Resource):
    def get(self):
        scanners = ScannerModel.query.all()
        return jsonify({'scanners': [scanner.to_json() for scanner in scanners]})

    def post(self):
        data = request.json
        scanner = ScannerModel.from_json(data)
        db.session.add(scanner)
        db.session.commit()
        return jsonify(scanner.to_json()), 201