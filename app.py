from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

    
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print("جاري تحميل الموديل...")
model = load_model('skin_disease_model.h5')
print("تم تحميل الموديل بنجاح!")

# قائمة الفئات مرتبة أبجديًا
classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

# قاموس المعلمات والمعلومات الطبية المبسطة
disease_info = {
    'akiec': {'ar': 'التقران السفعي (AKIEC)', 'desc': 'بقع قشرية تظهر غالباً بسبب التعرض لشمس الصيف، وتتطلب متابعة دورية.'},
    'bcc': {'ar': 'سرطان الخلايا القاعدية (BCC)', 'desc': 'أكثر أورام الجلد شيوعاً، ينمو ببطء شديد وقابل للشفاء التام عند الاكتشاف المبكر.'},
    'bkl': {'ar': 'التقران المثي (BKL)', 'desc': 'نمو جلدي حميد شائع جداً وغير ضار إطلاقاً.'},
    'df': {'ar': 'الورم الليفي الجلدي (DF)', 'desc': 'عقدة جلدية صلبة وحميدة تظهر غالباً في الأطراف.'},
    'mel': {'ar': 'الميلانوما (MEL)', 'desc': 'نوع يستوجب العرض الفوري على طبيب أمراض جلدية للتقييم الدقيق.'},
    'nv': {'ar': 'الشامة الحميدة (NV)', 'desc': 'شامة أو حسنة طبيعية وحميدة تماماً.'},
    'vasc': {'ar': 'الآفات الوعائية (VASC)', 'desc': 'تغيرات حميدة في الأوعية الدموية الجلدية.'}
}

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 128))
    img = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(img, axis=0)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'لم يتم اختيار صورة'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'اسم الملف فارغ'}), 400

    # حفظ الصورة مرة واحدة فقط
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        # معالجة الصورة والتنبؤ
        processed_img = preprocess_image(filepath)
        predictions = model.predict(processed_img)[0]
        
        # مسح الصورة بعد ما الموديل يخلص
        if os.path.exists(filepath):
            os.remove(filepath)
            
    except Exception as e:
        # في حالة حدوث أي خطأ، نمسح الصورة برضه
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'حدث خطأ داخلي أثناء معالجة الصورة.'}), 500

    # استخراج أعلى 3 احتمالات
    top3_indices = np.argsort(predictions)[-3:][::-1]
    top3_results = []

    for idx in top3_indices:
        code = classes[idx]
        top3_results.append({
            'code': code,
            'name': disease_info[code]['ar'],
            'desc': disease_info[code]['desc'],
            'confidence': float(f"{predictions[idx] * 100:.2f}")
        })

    return jsonify({'results': top3_results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)