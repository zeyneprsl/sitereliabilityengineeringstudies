# SRE Ödevi - Dockerize ve İzleme Sistemi

Bu proje, Docker containerization ve monitoring konularında pratik yapmak amacıyla geliştirdiğim bir sistemdir. Basit bir Python web servisini Docker ile containerize ettim ve Prometheus + Grafana ile izleme sistemini kurdum.
<img width="1067" height="578" alt="image" src="https://github.com/user-attachments/assets/9a6ffd75-9608-409f-b191-e75a43f1e3f3" />

## Proje Amacı

Bu ödevin amacı,aşağıdaki konularda pratik yapmamı sağlamaktır:

### **Temel Hedefler:**
- **Docker Containerization**: Python web servisini Docker container'ı haline getirmek
- **Monitoring Stack**: Prometheus ile metrik toplama ve alarm kuralları tanımlama
- **Visualization**: Grafana ile metrikleri görselleştirme ve dashboard oluşturma
- **Infrastructure as Code**: Docker Compose ile tüm sistemi yönetme
- **SRE Practices**: Monitoring, alerting ve observability konularında deneyim kazanma

## Gereken Önkoşullar (Docker Kurulumu vb.)

Test edeceğiniz bilgisayarda Docker/Podman ve Docker Compose/Podman Compose yüklü olduğundan emin olun.

### Docker Kurulumu
- **Windows**: Docker Desktop'ı [docker.com](https://www.docker.com/products/docker-desktop) adresinden indirin ve kurun
- **Linux**: `sudo apt-get install docker.io docker-compose` (Ubuntu/Debian) veya `sudo yum install docker docker-compose`
- **macOS**: Docker Desktop'ı [docker.com](https://www.docker.com/products/docker-desktop) adresinden indirin ve kurun

### Podman Kurulumu (Alternatif)
- **Windows**: `winget install RedHat.Podman` veya [podman.io](https://podman.io/getting-started/installation) adresinden indirin
- **Linux**: `sudo apt-get install podman podman-compose` (Ubuntu/Debian) veya `sudo yum install podman podman-compose` 
- **macOS**: `brew install podman` veya [podman.io](https://podman.io/getting-started/installation) adresinden indirin

### Kurulum Sonrası Kontrol
```bash
# Docker için
docker --version
docker-compose --version

# Podman için
podman --version
podman-compose --version
```

## Proje Yapısı
```
sreödev/
├── app.py                          # Flask web servisi
├── requirements.txt                # Python bağımlılıkları
├── Dockerfile                     # Web servisi Docker imajı
├── docker-compose.yml             # Tüm servislerin konfigürasyonu
├── prometheus.yml                 # Prometheus konfigürasyonu
├── rules.yml                      # Prometheus alarm kuralları
├── grafana/                       # Grafana konfigürasyonları
│   ├── Dockerfile                 # Grafana Docker imajı
│   └── provisioning/              # Grafana provisioning
│       ├── dashboards/            # Dashboard provisioning
│       │   ├── dashboard.yml      # Dashboard config
│       │   └── sre-odev-dashboard.json # Ana dashboard
│       └── datasources/           # Datasource provisioning
│           └── prometheus.yml     # Prometheus datasource
├── test_script.py                 # Test script'i
└── README.md                      # Bu dosya
```

## Kurulum ve Çalıştırma

### 1. Projeyi Hazırlayın
- Zip dosyasını açın
- `sreödev` klasörüne gidin

### 2. Docker Servislerini Başlatın
#### **Windows PowerShell:**
```powershell
docker-compose up -d
docker-compose logs -f
```
#### **Linux/macOS Terminal:**
```bash
docker-compose up -d
docker-compose logs -f
```
**2. Container Durumları:**
```bash
docker ps
```
**Beklenen Çıktı:**
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED        STATUS                             PORTS                    NAMES
ea7990ad5f74   grafana/grafana:latest   "/run.sh"                4 hours ago    Up 52 seconds                      0.0.0.0:3000->3000/tcp   sredev-grafana-1
18b54d8056c3   prom/prometheus:latest   "/bin/prometheus --c…"   4 hours ago    Up 52 seconds                      0.0.0.0:9090->9090/tcp   sredev-prometheus-1
140d131d904f   sredev-web-service       "python app.py"          29 hours ago   Up 52 seconds (health: starting)   0.0.0.0:5000->5000/tcp   sredev-web-service-1
```
**3. Health Check Durumu:**
```bash
# Web servisi health check
curl http://localhost:5000/health

# Beklenen çıktı:
#StatusCode        : 200
#StatusDescription : OK
#Content           : {"status":"healthy","timestamp":1755176009.6239808}
```

##  Erişim Noktaları

| Servis | URL | Port | Açıklama |
|--------|-----|------|----------|
| **Web Servisi** | http://localhost:5000 | 5000 | Ana uygulama |
| **Prometheus** | http://localhost:9090 | 9090 | Metrik toplama ve alarmlar |
| **Grafana** | http://localhost:3000 | 3000 | Metrik görselleştirme |

### Grafana Giriş Bilgileri
- **Kullanıcı Adı**: `admin`
- **Şifre**: `admin`

## Prometheus Kullanım Kılavuzu

### **Prometheus Nedir?**
Prometheus, sistemlerinizi izlemek ve alarm vermek için kullanılan açık kaynaklı bir monitoring ve alerting sistemidir. 
Web servisimden metrikleri toplar ve bu verileri analiz etmenizi sağlar.

### **Prometheus Arayüzüne Erişim:**
1. Tarayıcınızda `http://localhost:9090` adresine gidin
2. Prometheus ana sayfası açılacak

### **Temel Kullanım:**
#### **1. Hedefleri Kontrol Etme:**
- **"Status"** → **"Targets"** tıklayın
- **"web-service"** hedefinin durumunu görün:
  - **UP**: Servis çalışıyor ve metrikler toplanıyor
  - **DOWN**: Servis çalışmıyor veya erişilemiyor

#### **2. Metrikleri Görme:**
- **"Graph"** tıklayın
- **Query** alanına metrik adını yazın:
  ```
  http_requests_total
  ```
- **Execute** tıklayın
- Grafik ve tablo formatında verileri görün

#### **3. Popüler Metrikler:**
```promql
# Toplam istek sayısı
http_requests_total

# Hata oranı (son 5 dakika)
sum(rate(http_requests_total{status=~"4..|5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Yanıt süresi (95. persentil)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# İstek/saniye oranı
sum(rate(http_requests_total[1m]))
```
#### **4. Zaman Aralığı Seçimi:**
- Sağ üstte **"Last 15 minutes"** yazan yere tıklayın
- **"Last 1 hour"**, **"Last 6 hours"** gibi seçeneklerden birini seçin

#### **5. Alarm Durumunu Kontrol Etme:**
- **"Alerts"** tıklayın
- Tanımladığım alarmların durumunu görün:
  - **Inactive**: Alarm koşulu sağlanmamış
  - **Pending**: Alarm koşulu sağlandı, beklemede
  - **Firing**: Alarm aktif ve tetiklendi

#### **6. Metrik İsimlerini Kontrol Etme:**
**ÖNEMLİ: Python'da tanımladığım metrik isimleri ile Prometheus'ta görünen metrik isimleri aynı olmalı!**

## Grafana Kullanım Kılavuzu

### **Grafana Nedir?**
Grafana, Prometheus'tan gelen verileri güzel grafikler ve paneller halinde görselleştirmemizi sağlayan bir dashboard platformudur.

### **Grafana Arayüzüne Erişim:**
1. Tarayıcınızda `http://localhost:3000` adresine gidin
2. **admin/admin** ile giriş yapın

### **Temel Kullanım:**

**🎉 Dashboard Otomatik Yükleniyor!**

**Dashboard Provisioning Aktif:**
- **"SRE Odev Dashboard"** otomatik olarak yükleniyor
- Manuel import yapmaya gerek yok
- Grafana açıldığında dashboard hazır

**4 Panel Otomatik Yükleniyor:**
- Total Requests
- Error Rate  
- Response Time
- Requests per Second

**ÖNEMLİ: Eğer manuel yapılıcaksa Dashboard import etmeden önce Prometheus data source eklemelisiniz!**
**MANUEL KULLANIM**
**Prometheus Data Source Ekleme**
- Sol menüden  **"Data sources"** tıklayın
- **"Add data source"** tıklayın
- **"Prometheus"** seçin
- **URL**: `http://prometheus:9090` yazın
- **"Save & Test"** tıklayın
- ✅ **"Successfully queried the Prometheus API."** mesajını görün

#### **Adım 1: hazır Dashboard Import Etme(bu hazır dashboardu önce grafana ile manuel oluşturup sonra json dosyası ile export ettim)**
- Sol menüden **"Dashboards"** → **"Import"** tıklayın
- **"Upload JSON file"** seçin
- `grafana/dashboards/working-dashboard.json` dosyasını yükleyin
- **"Import"** tıklayın
- **4 panel otomatik olarak yüklenecek:**
  - Total Requests
  - Error Rate
  - Response Time 
  - Requests per Second 

#### **2. Hazır dashboard yerine Manuel Panel Oluşturma:**
- **"new"** → **"newDashboard"** tıklayın
- **"Add visulation"** tıklayın
- **Data source**: Prometheus seçin
- **Query A** alanına metrik yazın:
  ```
  sum(http_requests_total)
  ```
- **Panel title**: "Total Requests" yazın
- **run queries** tıklayın

#### **3. Mevcut Dashboard'a Panel Ekleme:**
- **"Back to dashboard"** butonuna tıkla
- **Panel Ekleme:**
  - Dashboard'da **"Add"** butonuna tıkla
  - **"visulation"** tıkla
- **Panel Konfigürasyonu:**
  - **Query A** alanına metrik yazın:
    ```
    sum(rate(http_requests_total[1m]))
    ```
  - **Panel title**: "Requests per Second" yazın
  - **Visualization Seçimi :**
    - **"Time series"** seçersen: Sadece grafik görünür, zaman ekseni var
    - **"Stat"** seçersen: Büyük sayı + altında mini grafik görünür
  - **"run queries"** tıklayın
- **Dashboard'ı Kaydet:**
  - **"Save dashboard"** tıklayın

#### **4. Dashboard Düzenleme:**
- Dashboard'da **"Edit"** düğmesine tıklayın
- Panelleri sürükleyip bırakarak yerleştirin
- Panel boyutlarını ayarlayın
- **"Save"** tıklayın

## Alarm Kuralları ve Test Etme

### **Tanımladığım Alarm Kuralları:**

#### **1. HighErrorRate**
- **Ne İzleniyor**: Web servisindeki hata oranı
- **Alarm Koşulu**: Son 5 dakikada hata oranı %10'un üzerinde
- **Alarm Seviyesi**: Warning
- **Bekleme Süresi**: 10 saniye
- **Ne Anlama Geliyor**: Çok fazla hata oluyorsa sistemde bir sorun var demektir

#### **2. ServiceDown**
- **Ne İzleniyor**: Web servisinin erişilebilirliği
- **Alarm Koşulu**: Web servisi 30 saniyeden fazla erişilemez
- **Alarm Seviyesi**: Kritik
- **Bekleme Süresi**: 30 saniye
- **Ne Anlama Geliyor**: Web servisi tamamen çökmüş olabilir

#### **3. HighResponseTime**
- **Ne İzleniyor**: Web servisinin yanıt süresi
- **Alarm Koşulu**: 95. persentil yanıt süresi 1 saniyenin üzerinde
- **Alarm Seviyesi**: Warning
- **Bekleme Süresi**: 2 dakika
- **Ne Anlama Geliyor**: Servis yavaş çalışıyor, performans sorunu var

### **Alarmları Test Etme:**

#### **Test Script ile Otomatik Test:**
**Python script ile otomatik yük testi:**

**Windows PowerShell:**
```powershell
# Test script'i çalıştır
python test_script.py
```
**Test script ne yapar:**
- 300 hata isteği gönderir
- Her 200ms'de bir istek
- Toplam 1 dakika sürer
- Hata oranını %10'un üzerine çıkarır

#### **Hata Oranını Artırmak İçin:**
Web servisine bilerek hatalı istekler göndererek alarmı tetikleyebilirsiniz:

**Windows PowerShell:**
```powershell
# Hata tetikleme endpoint'i
Invoke-WebRequest -Uri "http://localhost:5000/error" -UseBasicParsing

# Çok sayıda hata üretmek için
for ($i=1; $i -le 50; $i++) { 
    Invoke-WebRequest -Uri "http://localhost:5000/error" -UseBasicParsing 
    Start-Sleep -Milliseconds 100 
}

**Linux/macOS:**
```bash
curl http://localhost:5000/error

for i in {1..50}; do curl http://localhost:5000/error; sleep 0.1; done
```

#### **Test Sonrası Kontrol:**
1. **Prometheus'ta**: `http://localhost:9090/alerts` sayfasına gidin
2. **HighErrorRate** alarmının **"Firing"** olduğunu görün
3. **Grafana'da**: Dashboard'da hata oranının arttığını görün

### **Alarm Durumları:**
- **Inactive**: Alarm koşulu sağlanmamış
- **Pending**: Alarm koşulu sağlandı, beklemede (for süresi)
- **Firing**: Alarm aktif ve tetiklendi

**Sistem performans kontrolü:**
```bash
# Container'ların RAM ve CPU kullanımı
docker stats --no-stream

# Disk kullanımı
docker system df

# Image boyutları
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Volume boyutları
docker volume ls
docker volume inspect sredev_prometheus_data
```

### **Troubleshooting Checklist**

**Docker Desktop Sorunları:**
- [ ] Docker Desktop çalışıyor mu?
- [ ] Docker Engine başladı mı? (`docker ps`)
- [ ] Port'lar açık mı? (`netstat -an`)

**Container Sorunları:**
- [ ] Container'lar başladı mı? (`docker-compose ps`)
- [ ] Log'larda hata var mı? (`docker-compose logs`)
- [ ] Network bağlantısı var mı? (`docker network ls`)
- [ ] Volume'lar mount edildi mi? (`docker volume ls`)

**Monitoring Sorunları:**
- [ ] Prometheus targets UP mı?
- [ ] Grafana data source bağlandı mı?
- [ ] Metrikler geliyor mu? (`curl /metrics`)
- [ ] Alarm kuralları yüklendi mi? 

### Servisleri Durdur : docker-compose down

## Ek Kaynaklar

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
