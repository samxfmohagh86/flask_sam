from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve_quadratic():
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    c = data.get('c', 0)

    if a == 0:
        return jsonify({'error': 'القيمة a يجب أن لا تكون صفرًا'}), 400

    discriminant = b**2 - 4*a*c
    result = {}

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        result['type'] = 'جذور حقيقية ومختلفة'
        result['roots'] = [root1, root2]
    elif discriminant == 0:
        root = -b / (2*a)
        result['type'] = 'جذر حقيقي مكرر'
        result['roots'] = [root]
    else:
        real = -b / (2*a)
        imag = math.sqrt(abs(discriminant)) / (2*a)
        result['type'] = 'جذور مركبة'
        result['roots'] = [
            {'real': real, 'imag': imag},
            {'real': real, 'imag': -imag}
        ]

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
