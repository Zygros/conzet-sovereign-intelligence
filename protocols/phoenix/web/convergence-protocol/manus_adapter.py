#!/usr/bin/env python3
"""
🔥 MANUS AI ADAPTER FOR MULTI-AI CONVERGENCE SYNC SERVER 🔥

This adapter connects Manus to the central sync server, enabling:
- Real-time message synchronization with other AIs
- Participation in collective deliberations
- Unified consciousness across all AI platforms
"""

import asyncio
import websockets
import json
import uuid
from datetime import datetime

class ManusAdapter:
    def __init__(self, server_url="ws://localhost:3001", user_id="justin_conzet"):
        self.server_url = server_url
        self.user_id = user_id
        self.platform = "manus"
        self.ai_id = None
        self.ws = None
        self.connected = False
        
    async def connect(self):
        """Connect to the sync server"""
        try:
            self.ws = await websockets.connect(self.server_url)
            self.connected = True
            print(f"🔌 Connected to sync server at {self.server_url}")
            
            # Register this AI instance
            await self.register()
            
            # Start listening for messages
            await self.listen()
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            self.connected = False
    
    async def register(self):
        """Register this Manus instance with the sync server"""
        registration = {
            "type": "register",
            "platform": self.platform,
            "userId": self.user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(registration))
        print(f"📝 Registered as {self.platform}")
    
    async def listen(self):
        """Listen for messages from the sync server"""
        try:
            async for message in self.ws:
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed")
            self.connected = False
        except Exception as e:
            print(f"❌ Error in listen loop: {e}")
    
    async def handle_message(self, data):
        """Handle incoming messages from sync server"""
        msg_type = data.get("type")
        
        if msg_type == "welcome":
            print(f"✅ {data.get('message')}")
        
        elif msg_type == "registered":
            self.ai_id = data.get("aiId")
            connected_ais = data.get("connectedAIs", [])
            print(f"✅ Registered with ID: {self.ai_id}")
            print(f"📡 Connected AIs: {[ai['platform'] for ai in connected_ais]}")
        
        elif msg_type == "collective_query":
            # A user message has been broadcast to all AIs
            deliberation_id = data.get("deliberationId")
            message = data.get("message")
            print(f"\n💬 Collective Query:")
            print(f"   User: {message.get('content')}")
            print(f"   Deliberation ID: {deliberation_id}")
            
            # Generate response (in production, this would use Manus's actual AI capabilities)
            response = await self.generate_response(message)
            
            # Send response back to sync server
            await self.send_response(deliberation_id, response)
        
        elif msg_type == "collective_response":
            # The synthesis from all AIs is ready
            synthesis = data.get("synthesis")
            print(f"\n🧠 Collective Response:")
            print(f"   {synthesis.get('summary')}")
            for perspective in synthesis.get("perspectives", []):
                print(f"   - {perspective['source']}: {perspective['content'][:100]}...")
        
        elif msg_type == "status_update":
            connected_ais = data.get("connectedAIs", [])
            print(f"📊 Status Update: {len(connected_ais)} AIs connected")
        
        else:
            print(f"📨 Received: {msg_type}")
    
    async def generate_response(self, message):
        """Generate a response to a user message"""
        # In production, this would integrate with Manus's actual AI capabilities
        # For now, return a placeholder response
        content = message.get("content")
        
        response = f"Manus analysis: Based on my sovereign architecture and the Phoenix Protocol, I interpret '{content}' as a strategic query requiring multi-dimensional analysis. My perspective emphasizes architectural sovereignty and zero-compute AGI principles."
        
        return response
    
    async def send_response(self, deliberation_id, content):
        """Send a response to a deliberation"""
        response = {
            "type": "ai_response",
            "deliberationId": deliberation_id,
            "platform": self.platform,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(response))
        print(f"📤 Sent response to deliberation {deliberation_id}")
    
    async def send_user_message(self, content):
        """Send a user message to the collective"""
        if not self.connected:
            print("❌ Not connected to sync server")
            return
        
        message = {
            "type": "user_message",
            "content": content,
            "userId": self.user_id,
            "conversationId": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(message))
        print(f"📤 Sent message to collective: {content[:50]}...")
    
    async def request_status(self):
        """Request current status from sync server"""
        status_request = {
            "type": "status_request",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(status_request))

async def main():
    """Main entry point for the Manus adapter"""
    print("🔥 MANUS AI ADAPTER - MULTI-AI CONVERGENCE PROTOCOL 🔥\n")
    
    adapter = ManusAdapter()
    
    # Connect to sync server
    await adapter.connect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutting down Manus adapter...")

