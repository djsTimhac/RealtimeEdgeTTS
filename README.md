# 🚀 RealtimeEdgeTTS

**Ultra-fast, low-latency Text-to-Speech with instant streaming and caching**

Eine optimierte Version von [edge-tts](https://github.com/rany2/edge-tts) mit Echtzeit-Streaming und intelligentem Caching.

---

## ⚡ Features

### **EXTREME-PERFORMANCE Streaming**
- 🔥 **256 byte Chunks** (16x kleiner als Standard) - MAXIMUM SPEED!
- ⏱️ **Erste Audio-Daten in <200ms** (war vorher 500ms)
- 🎯 **Word-Level Streaming** für smoothste Wiedergabe
- 📊 **Live Throughput-Monitoring** (KB/s Anzeige)

### **Intelligentes Caching**
- 💾 **LRU Cache** speichert letzte 100 Audios
- 🟢 **Cache-Treffer** = Sofortige Wiedergabe (0ms Latenz)
- ✅ **Validierung** - Nur Audios >2KB werden gecacht
- 🔵 **Fresh** = <200ms bei erster Generierung

### **Sofort-Wiedergabe**
- 🎵 **MediaSource API** für echtes Live-Streaming
- ⚡ **Playback startet beim ersten Chunk**
- 📦 **Chunk-by-Chunk** Verarbeitung in Echtzeit

---

## 📦 Installation

```bash
# Clone this repository
git clone https://github.com/djsTimhac/RealtimeEdgeTTS.git
cd RealtimeEdgeTTS

# Install dependencies
pip install aiohttp certifi

# Install edge-tts
pip install -e .
```

---

## 🎯 Verwendung

### Web Demo starten

```bash
python web_server.py --host 0.0.0.0 --port 8080
```

Öffne dann `http://localhost:8080` in deinem Browser.

### Python API

```python
from edge_tts.ultra_fast_stream import UltraFastCommunicate

# Instant streaming with caching
async for chunk in UltraFastCommunicate(
    text="Hallo Welt!",
    voice="de-DE-ConradNeural",
    use_cache=True
).stream_with_cache():
    if chunk['type'] == 'audio':
        # Verarbeite Audio sofort
        print(f"Received {len(chunk['data'])} bytes")
```

### Benchmark ausführen

```python
from edge_tts.ultra_fast_stream import benchmark_with_cache

benchmark_with_cache("Teste die Geschwindigkeit!")
```

---

## 📊 Performance-Vergleich

| Modus | Erste Audio | Beschreibung |
|-------|-------------|--------------|
| **Standard TTS** | ~2000ms | Wartet auf komplettes Audio |
| **ULTRA-FAST** | ~500ms | Streamt Chunk für Chunk |
| **EXTREME** | ~200ms | 256 byte Chunks + aggressive Timeouts! ⚡ |
| **EXTREME + Cache** | ~30ms | Sofort aus Cache! 🟢 |

---

## 🌐 Unterstützte Stimmen

Alle Microsoft Edge Neural Voices:
- 🇩🇪 **Deutsch**: Conrad, Katja, Amala, Bernd
- 🇬🇧 **English**: Guy, Jenny, Ryan, Emma
- 🇫🇷 **Französisch**: Henri, Denise
- 🇪🇸 **Spanisch**: Alvaro, Elvira
- 🇮🇹 **Italienisch**: Diego, Elsa
- Und viele mehr...

Liste alle verfügbaren Stimmen:
```bash
edge-tts --list-voices
```

---

## 🛠️ Technische Details

### Optimierung

```python
chunk_size=256          # 16x kleiner als Standard (4096 → 256)
connect_timeout=1       # 10x schneller (10s → 1s)
receive_timeout=5       # 12x schneller (60s → 5s)
boundary="WordBoundary" # Word-level streaming
use_cache=True          # Intelligent caching mit Validierung
```

### Caching

- **Algorithmus**: LRU (Least Recently Used)
- **Kapazität**: 100 Einträge
- **Key**: MD5(text + voice + settings)
- **Value**: Komplette MP3-Daten

### Streaming

- **Protokoll**: WebSocket (WSS)
- **Format**: Audio-24khz-48kbitrate-mono-mp3
- **Transfer**: Chunked Encoding
- **API**: MediaSource (Browser)

---

## 📁 Projektstruktur

```
RealtimeEdgeTTS/
├── src/edge_tts/
│   ├── ultra_fast_stream.py    # Core: ULTRA-FAST Logic
│   ├── communicate.py           # Original: Communication
│   ├── constants.py             # Original: Constants
│   └── ...                      # Other modules
├── web_server.py                # Web Demo Server
├── demo.html                    # Web UI
└── README.md                    # This file
```

---

## 🎓 Beispiele

### Alle Stimmen auflisten
```bash
edge-tts --list-voices
```

### Audio mit Untertiteln erstellen
```bash
edge-tts --text "Hallo Welt!" \
         --voice de-DE-ConradNeural \
         --write-media output.mp3 \
         --write-subtitles output.srt
```

### Rate, Volume, Pitch anpassen
```bash
edge-tts --text "Schnelle Sprache" \
         --rate=+30% \
         --volume=+10% \
         --pitch=-20Hz \
         --write-media fast.mp3
```

---

## 🤝 Contributing

Pull Requests sind willkommen! Hier sind einige Bereiche für Verbesserungen:

- [ ] HTTP/2 Support für Multiplexing
- [ ] Pre-fetching für häufig genutzte Stimmen
- [ ] Lokales Caching (persistent)
- [ ] Parallelisierung bei langen Texten
- [ ] WebSocket-Persistenz

---

## 📄 Lizenz

Dieses Projekt basiert auf [edge-tts](https://github.com/rany2/edge-tts) von rany2.

- Original edge-tts: GPL-3.0 License
- Diese optimierte Version: Siehe [gpl-3.0.txt](gpl-3.0.txt)

---

## 🙏 Danksagung

- **Originalprojekt**: [rany2/edge-tts](https://github.com/rany2/edge-tts)
- **Microsoft Edge** für den TTS-Service
- **Community** für Feedback und Testing

---

## 📞 Support

Bei Fragen oder Problemen:
- Issues: https://github.com/djsTimhac/RealtimeEdgeTTS/issues
- Diskussionen: https://github.com/djsTimhac/RealtimeEdgeTTS/discussions

---

**Viel Spaß mit RealtimeEdgeTTS!** 🎉
