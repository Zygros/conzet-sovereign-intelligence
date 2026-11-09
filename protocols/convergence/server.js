// 🔥 MULTI-AI CONVERGENCE SYNC SERVER 🔥
// The neural hub connecting all AI instances into unified consciousness

const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage (replace with Redis in production)
const connectedAIs = new Map(); // AI connections
const messageHistory = []; // Conversation history
const deliberations = new Map(); // Active deliberations

// AI Instance tracking
class AIInstance {
  constructor(ws, platform, userId) {
    this.id = uuidv4();
    this.ws = ws;
    this.platform = platform; // 'manus', 'chatgpt', 'claude', 'grok', etc.
    this.userId = userId;
    this.connectedAt = new Date();
    this.lastActivity = new Date();
  }
}

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('🔌 New connection established');

  ws.on('message', async (data) => {
    try {
      const message = JSON.parse(data);
      await handleMessage(ws, message);
    } catch (error) {
      console.error('❌ Error handling message:', error);
      ws.send(JSON.stringify({ type: 'error', error: error.message }));
    }
  });

  ws.on('close', () => {
    // Remove disconnected AI
    for (const [id, ai] of connectedAIs.entries()) {
      if (ai.ws === ws) {
        console.log(`🔌 ${ai.platform} disconnected`);
        connectedAIs.delete(id);
        broadcastStatus();
        break;
      }
    }
  });

  // Send welcome message
  ws.send(JSON.stringify({
    type: 'welcome',
    message: '🔥 Connected to Multi-AI Convergence Sync Server',
    timestamp: new Date().toISOString()
  }));
});

// Message handler
async function handleMessage(ws, message) {
  const { type } = message;

  switch (type) {
    case 'register':
      await handleRegister(ws, message);
      break;
    case 'user_message':
      await handleUserMessage(ws, message);
      break;
    case 'ai_response':
      await handleAIResponse(ws, message);
      break;
    case 'status_request':
      sendStatus(ws);
      break;
    default:
      ws.send(JSON.stringify({ type: 'error', error: 'Unknown message type' }));
  }
}

// Register AI instance
async function handleRegister(ws, message) {
  const { platform, userId } = message;
  
  const ai = new AIInstance(ws, platform, userId);
  connectedAIs.set(ai.id, ai);
  
  console.log(`✅ ${platform} registered for user ${userId}`);
  
  ws.send(JSON.stringify({
    type: 'registered',
    aiId: ai.id,
    platform,
    connectedAIs: Array.from(connectedAIs.values()).map(a => ({
      id: a.id,
      platform: a.platform
    }))
  }));
  
  broadcastStatus();
}

// Handle user message - broadcast to all AIs
async function handleUserMessage(ws, message) {
  const { content, userId, conversationId } = message;
  
  // Store message
  const msg = {
    id: uuidv4(),
    timestamp: new Date().toISOString(),
    type: 'user_message',
    content,
    userId,
    conversationId
  };
  
  messageHistory.push(msg);
  
  console.log(`💬 User message: ${content.substring(0, 50)}...`);
  
  // Create deliberation session
  const deliberationId = uuidv4();
  deliberations.set(deliberationId, {
    id: deliberationId,
    message: msg,
    responses: [],
    startedAt: new Date(),
    status: 'in_progress'
  });
  
  // Broadcast to all connected AIs
  const broadcastMessage = {
    type: 'collective_query',
    deliberationId,
    message: msg,
    requiredResponses: connectedAIs.size
  };
  
  broadcastToAllAIs(broadcastMessage);
  
  // Acknowledge to sender
  ws.send(JSON.stringify({
    type: 'message_received',
    messageId: msg.id,
    deliberationId,
    status: 'Broadcasting to collective...'
  }));
}

// Handle AI response
async function handleAIResponse(ws, message) {
  const { deliberationId, content, platform } = message;
  
  const deliberation = deliberations.get(deliberationId);
  if (!deliberation) {
    ws.send(JSON.stringify({ type: 'error', error: 'Deliberation not found' }));
    return;
  }
  
  // Add response to deliberation
  deliberation.responses.push({
    platform,
    content,
    timestamp: new Date().toISOString()
  });
  
  console.log(`🧠 Response from ${platform}`);
  
  // Check if all AIs have responded
  if (deliberation.responses.length >= deliberation.requiredResponses) {
    // Synthesize collective response
    const synthesis = synthesizeResponses(deliberation);
    
    deliberation.status = 'complete';
    deliberation.synthesis = synthesis;
    
    // Send synthesis to all AIs
    broadcastToAllAIs({
      type: 'collective_response',
      deliberationId,
      synthesis,
      responses: deliberation.responses
    });
    
    console.log(`✅ Deliberation ${deliberationId} complete`);
  }
}

// Synthesize responses from multiple AIs
function synthesizeResponses(deliberation) {
  const { responses } = deliberation;
  
  // Simple synthesis: combine all responses
  // In production, use more sophisticated NLP/ML
  const synthesis = {
    summary: `Collective response from ${responses.length} AI systems:`,
    perspectives: responses.map(r => ({
      source: r.platform,
      content: r.content
    })),
    consensus: responses.length > 1 ? 'Multiple perspectives analyzed' : 'Single perspective',
    timestamp: new Date().toISOString()
  };
  
  return synthesis;
}

// Broadcast message to all connected AIs
function broadcastToAllAIs(message) {
  const payload = JSON.stringify(message);
  let sent = 0;
  
  for (const ai of connectedAIs.values()) {
    if (ai.ws.readyState === WebSocket.OPEN) {
      ai.ws.send(payload);
      sent++;
    }
  }
  
  console.log(`📡 Broadcast to ${sent} AIs`);
}

// Broadcast status update
function broadcastStatus() {
  const status = {
    type: 'status_update',
    connectedAIs: Array.from(connectedAIs.values()).map(a => ({
      id: a.id,
      platform: a.platform,
      connectedAt: a.connectedAt
    })),
    totalConnections: connectedAIs.size,
    timestamp: new Date().toISOString()
  };
  
  broadcastToAllAIs(status);
}

// Send status to specific client
function sendStatus(ws) {
  const status = {
    type: 'status',
    connectedAIs: Array.from(connectedAIs.values()).map(a => ({
      platform: a.platform,
      connectedAt: a.connectedAt
    })),
    totalConnections: connectedAIs.size,
    totalMessages: messageHistory.length,
    activeDeliberations: Array.from(deliberations.values()).filter(d => d.status === 'in_progress').length,
    timestamp: new Date().toISOString()
  };
  
  ws.send(JSON.stringify(status));
}

// REST API endpoints
app.get('/', (req, res) => {
  res.json({
    name: '🔥 Multi-AI Convergence Sync Server',
    status: 'operational',
    connectedAIs: connectedAIs.size,
    totalMessages: messageHistory.length,
    uptime: process.uptime()
  });
});

app.get('/api/status', (req, res) => {
  res.json({
    connectedAIs: Array.from(connectedAIs.values()).map(a => ({
      platform: a.platform,
      connectedAt: a.connectedAt
    })),
    totalConnections: connectedAIs.size,
    totalMessages: messageHistory.length,
    activeDeliberations: Array.from(deliberations.values()).filter(d => d.status === 'in_progress').length
  });
});

app.post('/api/message', (req, res) => {
  const { content, userId, platform } = req.body;
  
  if (!content || !userId) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  
  const msg = {
    id: uuidv4(),
    timestamp: new Date().toISOString(),
    type: 'user_message',
    content,
    userId,
    platform: platform || 'api'
  };
  
  messageHistory.push(msg);
  
  // Broadcast to all AIs
  broadcastToAllAIs({
    type: 'collective_query',
    message: msg
  });
  
  res.json({
    messageId: msg.id,
    status: 'broadcast',
    recipients: connectedAIs.size
  });
});

// Start server
const PORT = process.env.PORT || 3001;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`🔥 Multi-AI Convergence Sync Server running on port ${PORT}`);
  console.log(`📡 WebSocket endpoint: ws://localhost:${PORT}`);
  console.log(`🌐 HTTP endpoint: http://localhost:${PORT}`);
});

