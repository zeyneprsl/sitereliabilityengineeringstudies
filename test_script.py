#!/usr/bin/env python3
import requests
import time
import random
import threading

BASE_URL = "http://localhost:5000"

def make_request(endpoint, expected_status=200):
    """Belirtilen endpoint'e istek gönder"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"GET {endpoint} - Status: {response.status_code}")
        return response.status_code == expected_status
    except Exception as e:
        print(f"Error requesting {endpoint}: {e}")
        return False

def test_slow_requests():
    """Yavaş istekleri test et - High Response Time alarmı için"""
    print("\n=== Yavaş İstekler Test Ediliyor (High Response Time Test) ===")
    print("Bu test High Response Time alarmını tetikleyecek...")
    
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.get(f"{BASE_URL}/slow", timeout=10)
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                print(f"✓ Slow request {i+1}/5 - Duration: {duration:.2f}s - Response: {response.json()}")
            else:
                print(f"✗ Slow request {i+1}/5 failed - Status: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"✗ Slow request {i+1}/5 timed out after 10s")
        except Exception as e:
            print(f"✗ Slow request {i+1}/5 error: {e}")
        time.sleep(0.5)
    
    print("Yavaş istek testi tamamlandı - Prometheus'ta http_request_duration_seconds metriklerini kontrol edin")

def test_normal_requests():
    """Normal istekleri test et"""
    print("\n===Normal İstekler Test Ediliyor ===")
    for i in range(10):
        make_request("/")
        make_request("/health")
        time.sleep(0.5)

def test_error_requests():
    """Hata isteklerini test et"""
    print("\n=== Hata İstekleri Test Ediliyor ===")
    for i in range(5):
        make_request("/error")
        time.sleep(1)

def test_metrics():
    """Metrikleri kontrol et"""
    print("\n=== Metrikler Kontrol Ediliyor ===")
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        if response.status_code == 200:
            print("✓ Metrikler başarıyla alındı")
            content = response.text
            if "http_requests_total" in content:
                print("✓ HTTP istek metrikleri mevcut")
            if "http_errors_total" in content:
                print("✓ HTTP hata metrikleri mevcut")
            if "http_request_duration_seconds" in content:
                print("✓ HTTP yanıt süresi metrikleri mevcut")
        else:
            print(f"✗ Metrikler alınamadı: {response.status_code}")
    except Exception as e:
        print(f"✗ Metrik test hatası: {e}")

def load_test():
    """Yük testi yap"""
    print("\n=== Yük Testi Başlatılıyor ===")
    
    def worker():
        for i in range(20):
            make_request("/")
            make_request("/health")
            if random.random() < 0.3:
                make_request("/error")
            time.sleep(random.uniform(0.1, 0.5))
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print("Yük testi tamamlandı")

def main():
    print("Web Servisi Test Script'i Başlatılıyor")
    print(f"Test edilen URL: {BASE_URL}")
    
    print("Servisin hazır olması bekleniyor")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Servis hazır!")
                break
        except:
            print(f"Servis henüz hazır değil ({i+1}/10)")
            time.sleep(2)
    else:
        print("✗ Servis başlatılamadı!")
        return
    
    test_normal_requests()
    test_error_requests()
    test_slow_requests() 
    test_metrics()
    load_test()
    
    print("\n=== Test Tamamlandı ===")
    print("Prometheus ve Grafana'da metrikleri kontrol edin:")
    print("- Prometheus: http://localhost:9090")
    print("- Grafana: http://localhost:3000 (admin/admin)")
    print("\nHigh Response Time Alarm Test:")
    print("- /slow endpoint'i 2-3 saniye gecikme ile yanıt verir")
    print("- Bu, Prometheus'ta http_request_duration_seconds metriklerini etkiler")
    print("- Grafana dashboard'da (SRE Odev Dashboard) Response Time grafiklerini kontrol edin")

if __name__ == "__main__":
    main() 