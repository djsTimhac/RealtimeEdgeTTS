"""Web server for Edge TTS demo with EXTREME-PERFORMANCE instant streaming and caching."""

import asyncio
import json
import time
from aiohttp import web
from edge_tts.realtime_stream import RealtimeCommunicate


async def tts_handler(request):
    """Handle TTS requests and stream audio INSTANTLY with caching."""
    
    try:
        data = await request.json()
        text = data.get('text', '')
        voice = data.get('voice', 'de-DE-ConradNeural')
        rate = data.get('rate', '+0%')
        volume = data.get('volume', '+0%')
        pitch = data.get('pitch', '+0Hz')
        
        if not text:
            return web.json_response(
                {'error': 'No text provided'}, 
                status=400
            )
        
        # EXTREME-PERFORMANCE: Maximum speed settings
        communicate = RealtimeCommunicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch,
            chunk_size=256,  # EXTREME: 256 bytes for MAXIMUM speed!
            connect_timeout=1,  # EXTREME: 1 second only!
            receive_timeout=5,  # EXTREME: 5 seconds only!
            use_cache=True,  # Enable intelligent caching
        )
        
        # Stream response
        response = web.StreamResponse(
            status=200,
            reason='OK',
            headers={
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': 'attachment; filename="speech.mp3"',
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',  # Disable proxy buffering
                'X-Chunked-Transfer': 'true',  # Enable chunked transfer
                'X-Stream-Start': 'immediate',  # Custom header for instant start
            },
        )
        
        await response.prepare(request)
        
        total_bytes = 0
        chunk_count = 0
        start_time = time.time()
        first_chunk_sent = False
        is_cached = None
        
        async for chunk in communicate.stream_with_cache():
            if chunk['type'] == 'audio':
                # Validate audio data before sending
                if len(chunk['data']) == 0:
                    print("⚠️ Warning: Received empty audio chunk, skipping")
                    continue
                    
                await response.write(chunk['data'])
                total_bytes += len(chunk['data'])
                chunk_count += 1
                
                # Track if this is cached or fresh generation
                if is_cached is None:
                    is_cached = chunk.get('cached', False)
                
                # Log first chunk immediately
                if not first_chunk_sent:
                    first_chunk_sent = True
                    elapsed_ms = (time.time() - start_time) * 1000
                    cache_status = "⚡ CACHED" if is_cached else "🚀 FRESH"
                    print(f"⚡ {cache_status} Chunk #{chunk_count} sent in {elapsed_ms:.0f}ms ({len(chunk['data'])} bytes)")
                elif chunk_count <= 5:
                    elapsed_ms = (time.time() - start_time) * 1000
                    print(f"   Chunk #{chunk_count} @ {elapsed_ms:.0f}ms ({len(chunk['data'])} bytes)")
                elif chunk_count % 20 == 0:
                    elapsed_ms = (time.time() - start_time) * 1000
                    throughput = total_bytes / (elapsed_ms/1000) / 1024
                    print(f"⚡ Speed: {throughput:.1f} KB/s | Total: {total_bytes:,} bytes")
        
        await response.write_eof()
        
        total_time = (time.time() - start_time) * 1000
        cache_label = "🟢 CACHED" if is_cached else "🔵 FRESH"
        print(f"✅ Generated {total_bytes:,} bytes in {total_time:.0f}ms {cache_label}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error generating TTS: {e}")
        import traceback
        traceback.print_exc()
        return web.json_response(
            {'error': str(e)},
            status=500
        )


async def index_handler(request):
    """Serve the main demo page."""
    return web.FileResponse('./demo.html')


def create_app():
    """Create and configure the web application."""
    app = web.Application()
    
    # Routes
    app.router.add_get('/', index_handler)
    app.router.add_post('/api/tts', tts_handler)
    
    return app


def main():
    """Run the web server."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Edge TTS Web Demo Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
    
    args = parser.parse_args()
    
    app = create_app()
    
    print("=" * 60)
    print("🎙️  Edge TTS Web Demo Server")
    print("=" * 60)
    print(f"📍 Server läuft unter: http://{args.host}:{args.port}")
    print(f"🎯 Öffne diese URL in deinem Browser")
    print("=" * 60)
    
    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
