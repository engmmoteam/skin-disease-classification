# 🩺 AI-Powered Skin Disease Classification System

نظام تشخيص مبدئي للأمراض الجلدية يعتمد على التعلم العميق (Deep Learning) مع واجهة ويب تفاعلية.

## 🚀 المميزات الرئيسية
- **نموذج تصنيف احترافي:** يعتمد على معمارية **MobileNetV2** المجهزة بالتعلم المنقول (Transfer Learning).
- **معالجة عدم توازن البيانات:** استخدام أوزان الفئات (`Class Weights`) مع توليد الصور (`Data Augmentation`) لرفع دقة تصنيف الأمراض النادرة.
- **عرض أعلى 3 احتمالات:** إرجاع نتائج الفحص بنسب مئوية لأعلى 3 أمراض مرشحة مع بطاقة إرشادات طبية لكل مرض.
- **خلفية برمجية سريعة:** سيرفر **Flask REST API** لمعالجة الصور وفحصها فورياً.
- **واجهة مستخدم تفاعلية:** تصميم responsive باستخدام JavaScript (Async/Await & Fetch API) يوفر معاينة مسبقة للصورة ومؤشر تحميل متفاعل.

## 🛠️ التقنيات المستخدمة (Tech Stack)
- **AI / ML:** Python, TensorFlow, Keras, OpenCV, NumPy, Scikit-learn
- **Backend:** Flask
- **Frontend:** HTML5, CSS3, JavaScript (ES6, Fetch API)

## 📁 هيكل المشروع (Project Structure)
```text
skinpro/
├── app.py                  # سيرفر Flask والـ API Routes
├── skin_disease_model.h5   # نموذج الذكاء الاصطناعي المدرب
├── model_training.ipynb    # ملف Notebook لتجميع الداتا وتدريب الموديل
├── requirements.txt        # مكتبات المشروع
├── templates/
│   └── index.html          # واجهة المستخدم
└── uploads/                # مجلد مؤقت للصور

⚙️ كيفية التشغيل محلياً
تفعيل البيئة الافتراضية وتثبيت المكتبات:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
تشغيل السيرفر:

Bash
python app.py
فتح الواجهة:
افتح المتصفح على http://127.0.0.1:5000

⚠️ تنويه طبي: هذا المشروع مصمم لأغراض تعليمية وأكاديمية فقط، ولا يعتبر بديلاً عن التشخيص الطبي المتخصص.