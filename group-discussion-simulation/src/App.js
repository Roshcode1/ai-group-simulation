import React, { useState, useEffect } from 'react';
import APIKeyInput from './components/APIKeyInput';
import Character from './components/Character';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import './App.css';

const characters = [
  { id: 1, name: 'Alice', avatar: 'https://i.pravatar.cc/150?img=1', voiceId: '21m00Tcm4TlvDq8ikWAM' },
  { id: 2, name: 'Bob', avatar: 'https://i.pravatar.cc/150?img=2', voiceId: 'GBv7mTt0atIp3Br8iCZE' },
  { id: 3, name: 'Charlie', avatar: 'https://i.pravatar.cc/150?img=3', voiceId: 'IKne3meq5aSn9XLyUdCD' },
];

function App() {
  const [geminiApiKey, setGeminiApiKey] = useState('');
  const [elevenLabsApiKey, setElevenLabsApiKey] = useState('');
  const [messages, setMessages] = useState([]);
  const [currentThread, setCurrentThread] = useState(0);

  const playAudio = (audioData) => {
    const audio = new Audio(URL.createObjectURL(audioData));
    audio.play();
  };

  const handleSendMessage = async (message) => {
    if (!geminiApiKey) {
      alert('Please enter your Gemini API key.');
      return;
    }
    if (!elevenLabsApiKey) {
      alert('Please enter your ElevenLabs API key.');
      return;
    }

    const userMessage = { sender: 'user', text: message };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);

    const nextCharacter = characters[currentThread];

    const prompt = `
      You are in a group discussion with multiple AI characters.
      The characters are: ${characters.map(c => c.name).join(', ')}.
      The current conversation is:
      ${newMessages.map(m => `${m.sender}: ${m.text}`).join('\n')}

      It is now ${nextCharacter.name}'s turn to speak.
      Generate a response for ${nextCharacter.name}.
      The response should be a single message from ${nextCharacter.name}.
    `;

    try {
      // Get text response from Gemini
      const geminiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${geminiApiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
        }),
      });

      if (!geminiResponse.ok) {
        throw new Error('Failed to fetch from Gemini API');
      }

      const geminiData = await geminiResponse.json();
      const aiText = geminiData.candidates[0].content.parts[0].text;
      const aiMessage = { sender: nextCharacter.name, text: aiText };
      setMessages([...newMessages, aiMessage]);
      setCurrentThread((currentThread + 1) % characters.length);

      // Get audio from ElevenLabs
      const elevenLabsResponse = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${nextCharacter.voiceId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'xi-api-key': elevenLabsApiKey,
        },
        body: JSON.stringify({
          text: aiText,
          model_id: 'eleven_multilingual_v2',
        }),
      });

      if (!elevenLabsResponse.ok) {
        throw new Error('Failed to fetch from ElevenLabs API');
      }

      const audioData = await elevenLabsResponse.blob();
      playAudio(audioData);

    } catch (error) {
      console.error(error);
      alert('An error occurred while fetching from the APIs.');
    }
  };

  return (
    <div className="app-container">
      <h1>Group Discussion Simulation</h1>
      <APIKeyInput apiKey={geminiApiKey} setApiKey={setGeminiApiKey} placeholder="Enter your Gemini API Key" />
      <APIKeyInput apiKey={elevenLabsApiKey} setApiKey={setElevenLabsApiKey} placeholder="Enter your ElevenLabs API Key" />
      <div className="characters-container">
        {characters.map(character => (
          <Character key={character.id} character={character} />
        ))}
      </div>
      <ChatWindow messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
