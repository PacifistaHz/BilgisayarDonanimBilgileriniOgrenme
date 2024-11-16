import getmac
import uuid
import socket
import cpuinfo
import wmi

# Temel sistem bilgileri
bilgisayarAdi = socket.gethostname()
ipAdresi = socket.gethostbyname(bilgisayarAdi)
fizikselAdres1 = hex(uuid.getnode())
fizikselAdres = getmac.get_mac_address()
info = cpuinfo.get_cpu_info()

print("Fiziksel Adres (getmac):", fizikselAdres)
print("Fiziksel Adres (uuid):", fizikselAdres1)
print("Bilgisayar Adı:", bilgisayarAdi)
print("IP Adresi:", ipAdresi)
print("İşlemci Bilgileri:", info)

# WMI ile ayrıntılı sistem bilgileri (sadece Windows)
try:
    bilgisayar = wmi.WMI()
    bilgisayarBilgileri = bilgisayar.Win32_ComputerSystem()[0]
    isletimSistemiBilgileri = bilgisayar.Win32_OperatingSystem()[0]
    islemciBilgileri = bilgisayar.Win32_Processor()[0]
    ekranKartiBilgileri = bilgisayar.Win32_VideoController()[0]

    isletimSistemiAdi = isletimSistemiBilgileri.Name.split('|')[0]
    isletimSistemiVersiyon = ''.join([isletimSistemiBilgileri.Version, isletimSistemiBilgileri.BuildNumber])
    ramBellek = float(isletimSistemiBilgileri.TotalVisibleMemorySize) / 1048576

    print("İşletim Sistemi Adı:", isletimSistemiAdi)
    print("İşletim Sistemi Versiyonu:", isletimSistemiVersiyon)
    print("İşlemci Bilgileri:", islemciBilgileri.Name)
    print("RAM (GB):", round(ramBellek, 2))
    print("Ekran Kartı Bilgileri:", ekranKartiBilgileri.Name)
except Exception as e:
    print(f"WMI ile bilgiler alınırken bir hata oluştu: {e}")

# Ekstra bilgi: CPU, bellek ve ağ arayüzleri
try:
    import psutil

    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    memory_info = psutil.virtual_memory()
    net_interfaces = psutil.net_if_addrs()

    print("CPU Çekirdek Sayısı:", cpu_cores)
    print("CPU İş Parçacığı (Thread) Sayısı:", cpu_threads)
    print("Toplam Bellek (GB):", round(memory_info.total / 1024**3, 2))
    print("Ağ Arayüzleri:")
    for interface, addrs in net_interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f" - {interface}: IP Adresi = {addr.address}")
            elif addr.family == socket.AF_PACKET:
                print(f" - {interface}: MAC Adresi = {addr.address}")

except ImportError:
    print("psutil modülü yüklenmemiş. Ekstra bilgiler alınamayacak.")
except Exception as e:
    print(f"Ekstra bilgiler alınırken bir hata oluştu: {e}")
