from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # تفعيل CORS للسماح بالاتصال من تطبيق React Native

def solve_quadratic(a, b, c):
    """
    حل معادلة من الدرجة الثانية: ax² + bx + c = 0
    """
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        
        # حساب المميز
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            # حلين حقيقين مختلفين
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return {
                "status": "success",
                "solutions": [x1, x2],
                "discriminant": discriminant,
                "type": "حلين حقيقين مختلفين",
                "equation": f"{a}x² + {b}x + {c} = 0"
            }
        elif discriminant == 0:
            # حل حقيقي واحد
            x = -b / (2*a)
            return {
                "status": "success",
                "solutions": [x],
                "discriminant": discriminant,
                "type": "حل حقيقي واحد",
                "equation": f"{a}x² + {b}x + {c} = 0"
            }
        else:
            # حلين مركبين
            real_part = -b / (2*a)
            imaginary_part = math.sqrt(-discriminant) / (2*a)
            return {
                "status": "success",
                "solutions": [
                    f"{real_part} + {imaginary_part}i",
                    f"{real_part} - {imaginary_part}i"
                ],
                "discriminant": discriminant,
                "type": "حلين مركبين",
                "equation": f"{a}x² + {b}x + {c} = 0"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"خطأ في الحساب: {str(e)}"
        }

@app.route('/')
def home():
    return jsonify({
        "message": "مرحبًا بك في API حل المعادلات التربيعية",
        "endpoints": {
            "solve_quadratic": "/solve",
            "method": "POST",
            "parameters": {"a": "number", "b": "number", "c": "number"}
        }
    })

@app.route('/solve', methods=['POST'])
def api_solve():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "يجب إرسال البيانات بصيغة JSON"
            }), 400
        
        a = data.get('a')
        b = data.get('b')
        c = data.get('c')
        
        if a is None or b is None or c is None:
            return jsonify({
                "status": "error",
                "message": "يجب إرسال جميع المعاملات: a, b, c"
            }), 400
        
        if float(a) == 0:
            return jsonify({
                "status": "error",
                "message": "المعامل a لا يمكن أن يكون صفرًا في معادلة تربيعية"
            }), 400
        
        result = solve_quadratic(a, b, c)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"خطأ في الخادم: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
