# RedXTools

RedXTools, Discord otomasyonu, hesap kontrolleri ve ilgili yardımcı işlemler için Windows terminal aracıdır.

## Gereksinimler

- Windows
- Python 3.11 veya daha yeni

## Kurulum

1. `.env.example` dosyasını `.env` olarak kopyalayın.
2. Kendi Discord uygulama kimliğinizi, davet metninizi ve isteğe bağlı bağlantıları girin. Kullanmayacağınız alanı boş bırakın.
3. Bağımlılıkları kurup programı başlatın.

```
copy .env.example .env
pip install -r requirements.txt
python main.py
```

Windows üzerinde `start.bat` dosyasını da çalıştırabilirsiniz. Betik Python kurulumunu kontrol eder, bağımlılıkları yükler ve programı açar.

## Yapılandırma

`.env` içindeki değerler başlangıçta okunur. `.env` dosyasını depoya eklemeyin.

| Degisken | Amac |
| --- | --- |
| `APP_NAME` | Discord Rich Presence üzerinde görünen ad |
| `APP_VERSION` | Arayüzde görünen sürüm |
| `APP_AUTHOR` | Bannerlarda yazdırılan ad |
| `DISCORD_CLIENT_ID` | Rich Presence için Discord uygulama kimliği |
| `DISCORD_INVITE` | Ana bannerda görünen davet metni |
| `RPC_LARGE_IMAGE` | Rich Presence görsel anahtarı |
| `RPC_DOWNLOAD_URL` | İsteğe bağlı indirme düğmesi adresi |
| `RPC_YOUTUBE_URL` | İsteğe bağlı YouTube düğmesi adresi |
| `DEFAULT_WEBHOOK_URL` | Bir araç webhook sorduğunda ve giriş boş bırakıldığında kullanılan adres |

`DISCORD_CLIENT_ID` boşsa Rich Presence kapalı kalır.

`config.json` ilk çalıştırmada oluşur. İş parçacığı sayısı, istek gecikmesi, proxy kullanımı ve benzeri çalışma ayarlarını tutar. `proxies.txt` her satırda bir proxy içerir. Bu iki dosya yerelde kalır.

## Menu

```
[1] Discord Tools
[2] More Tools
[3] Settings
[4] Statistics
[0] Exit
```

Discord araçları token üretimi ve kontrolü, sunucuya katılma ve ayrılma, mesaj, durum, token bilgisi, proxy ayarı ve token ile giriş işlemlerini kapsar.

Diğer araçlar Hotmail, Zula, Valorant ve Steam kontrollerini, ayrıca tekrar temizleme, log arama, SMS otomasyonu ve kaynak indirme işlemlerini kapsar.

## Proje yapisi

```
RedXTools/
├── main.py
├── start.bat
├── requirements.txt
├── .env.example
├── modules/
│   ├── settings.py
│   └── rpc_manager.py
└── tools/
    ├── discord/
    ├── hotmail/
    ├── steam/
    ├── valorant/
    ├── zula/
    ├── smsbomber/
    └── other/
```

## Sorumluluk reddi

Bu proje eğitim amacıyla yayımlanmıştır. Discord kurallarına ve bulunduğunuz yerdeki yasalara uymak sizin sorumluluğunuzdadır. Sahibi olmadığınız veya test izniniz olmayan hesap ve servislerde kullanmayın.
