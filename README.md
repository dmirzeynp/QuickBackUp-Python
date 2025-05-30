﻿# QuickBackUp-Python
# 💾 QuickBackUp - Şifreli Otomatik Yedekleme Aracı

QuickBackUp, kullanıcı dostu arayüzü ile klasörlerinizi kolayca şifreli `.zip` formatında yedeklemenizi sağlayan bir Python uygulamasıdır. Uygulama, şifreleme için AES algoritması kullanır ve yedek geçmişinizi yönetmenize de olanak tanır.

## 🛠️ Özellikler

- 📁 Belirtilen klasörü `.zip` formatında yedekleme
- 🔒 AES şifreleme desteği (pyzipper kütüphanesi)
- 🧾 Otomatik yedek isimlendirme (`yedek1.zip`, `yedek2.zip`...)
- 📜 Yedekleme raporu oluşturma
- 🕘 Önceki yedekleri listeleme veya silme
- 🔓 Şifreli yedekleri açma (Extract)
- 🧹 Formu temizleme
- ❌ Tek tıklamayla çıkış

## 📦 Gereksinimler

- Python 3.7+
- Aşağıdaki Python kütüphaneleri:


pip install pyzipper
🚀 Kurulum
Bu projeyi klonlayın:



cd quickbackup
Gereksinimleri yükleyin:


pip install pyzipper
Uygulamayı başlatın:

python quickbackup.py
🖥️ Kullanım
Yedeklenecek klasörü seçin.

Yedeklerin kaydedileceği klasörü seçin.

Bir şifre girin.

Yedekle butonuna tıklayın.

Uygulama otomatik olarak dosyaları şifreli .zip dosyasına dönüştürür.

📁 Önceki Yedekleri Göster ile geçmişe göz atın.

🗑️ Önceki Yedekleri Sil ile eski yedekleri temizleyin.

🔓 Şifreli Yedek Aç ile eski şifreli yedekleri tekrar çıkarın.

📂 Yedekler Nerede?
Yedek dosyalar, seçtiğiniz hedef klasörde yedek1.zip, yedek2.zip, ... şeklinde oluşturulur. Aynı zamanda, oluşturulan yedeklerin listesi backup_history.txt dosyasında tutulur.

📃 Raporlama
Her yedeklemede, aşağıdaki bilgileri içeren bir rapor_YYYYMMDD_HHMMSS.txt dosyası oluşturulur:

Yedek dosyasının adı

Yedeklenen dosya sayısı

Yedeklenen dosya isimleri

🔐 Şifreli Yedek Açma
🔓 Şifreli Yedek Aç butonuna tıklayarak:

Şifreli .zip dosyasını seçin

Şifreyi girin

Dosyaların çıkarılacağı klasörü seçin

📝 Geliştirici Notları
Şifre korumalı .zip dosyalar pyzipper kütüphanesi ile AES-256 şifreleme kullanılarak oluşturulur.

Uygulama çoklu iş parçacığı (threading) kullanarak arayüzün donmasını engeller.

👨‍💻 Katkıda Bulunma
Katkılarınızı memnuniyetle karşılıyoruz! Fork'layın, değişiklik yapın ve pull request gönderin. Hatalar veya öneriler için lütfen issue açın.

📜 Lisans
MIT Lisansı.
