"""
YOLO ile Gerçek Zamanlı Webcam Nesne Algılama
==============================================
Bu script webcam'den görüntü alarak YOLO modeli ile
tespit edilen nesneleri ekranda gösterir.

Çıkış: 'q' tuşuna basın.
"""

import cv2
from ultralytics import YOLO

# ── Model Yükleme ─────────────────────────────────────────────
# İlk çalıştırmada model otomatik indirilir (~6 MB)
model = YOLO("yolo11n.pt")  # nano model – hızlı ve hafif

# ── Webcam Başlat ─────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam açılamadı! Kameranın bağlı olduğundan emin olun.")
    exit(1)

print("✅ Webcam açıldı. Nesne algılama başlıyor...")
print("ℹ️  Çıkmak için 'q' tuşuna basın.\n")

# ── Ana Döngü ─────────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Kare okunamadı, çıkılıyor...")
        break

    # YOLO ile tahmin yap
    results = model(frame, verbose=False)

    # Tespit edilen nesneleri terminale yazdır
    detections = results[0].boxes
    if len(detections) > 0:
        detected_names = []
        for box in detections:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            name = model.names[cls_id]
            detected_names.append(f"{name} (%{conf*100:.1f})")

        print(f"🔍 Algılanan: {', '.join(detected_names)}")

    # Sonuçları görüntü üzerine çiz
    annotated_frame = results[0].plot()

    # Ekranda göster
    cv2.imshow("YOLO Nesne Algilama", annotated_frame)

    # 'q' ile çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ── Temizlik ──────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
print("\n👋 Program sonlandırıldı.")
