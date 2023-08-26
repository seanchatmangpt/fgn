from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from chat import chat

# Create a Flask application
app = Flask(__name__)
CORS(app)  # Enables Cross Origin Resource Sharing for the application

@app.route('/api/chat', methods=['POST'])
def interact():
    """Endpoint for interacting with AI through the chat function"""
    data = request.get_json()
    prompt = data['prompt']
    response = chat(prompt=prompt)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

import React, { useState } from 'react';
import axios from 'axios';

const ChatComponent = () => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  const sendPrompt = async () => {
    try {
      const result = await axios.post('/api/chat', { prompt });
      setResponse(result.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
      <button onClick={sendPrompt}>Send</button>
      <p>{response}</p>
    </div>
  );
};

export default ChatComponent;
