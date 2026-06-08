import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { TrendingUp, Send, LogOut, Loader2, DollarSign, PieChart, Activity } from 'lucide-react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai' | 'system';
}

const ChatDashboard: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', text: 'Hello! I am your FinSense Financial Assistant. Ask me anything about finance, market trends, or stock insights.', sender: 'system' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: Message = { id: Date.now().toString(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.post('/chat', { query: userMsg.text });
      const aiMsg: Message = { 
        id: (Date.now() + 1).toString(), 
        text: response.data.advice || 'No response received', 
        sender: 'ai' 
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err: any) {
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
      } else {
        const errorMsg: Message = { 
          id: (Date.now() + 1).toString(), 
          text: err.response?.data?.error || 'Failed to communicate with AI', 
          sender: 'system' 
        };
        setMessages(prev => [...prev, errorMsg]);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-slate-200 hidden md:flex flex-col shadow-sm z-10">
        <div className="p-6 flex items-center gap-3 border-b border-slate-100">
          <div className="h-10 w-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-md shadow-blue-600/20">
            <TrendingUp className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">FinSense</h1>
        </div>
        
        <div className="p-4 flex-1">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">Capabilities</h3>
          <ul className="space-y-2">
            <li className="flex items-center gap-3 text-sm text-slate-600 p-2 rounded-lg hover:bg-slate-50 transition-colors">
              <Activity className="h-4 w-4 text-blue-500" /> Real-time Market Data
            </li>
            <li className="flex items-center gap-3 text-sm text-slate-600 p-2 rounded-lg hover:bg-slate-50 transition-colors">
              <PieChart className="h-4 w-4 text-purple-500" /> Portfolio Analysis
            </li>
            <li className="flex items-center gap-3 text-sm text-slate-600 p-2 rounded-lg hover:bg-slate-50 transition-colors">
              <DollarSign className="h-4 w-4 text-emerald-500" /> Investment Advice
            </li>
          </ul>
        </div>

        <div className="p-4 border-t border-slate-100">
          <button 
            onClick={handleLogout}
            className="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-red-600 p-2 w-full rounded-lg hover:bg-red-50 transition-colors"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full relative">
        {/* Mobile Header */}
        <div className="md:hidden p-4 bg-white border-b border-slate-200 flex justify-between items-center z-10 shadow-sm">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-blue-600" />
            <h1 className="text-lg font-bold text-slate-800">FinSense</h1>
          </div>
          <button onClick={handleLogout} className="text-slate-500 hover:text-red-600">
            <LogOut className="h-5 w-5" />
          </button>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 chat-scroll bg-slate-50 relative">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 fade-in duration-300`}
              >
                <div 
                  className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 shadow-sm 
                    ${msg.sender === 'user' 
                      ? 'bg-blue-600 text-white rounded-br-sm' 
                      : msg.sender === 'system'
                        ? 'bg-slate-100 text-slate-600 border border-slate-200 text-sm'
                        : 'bg-white text-slate-800 border border-slate-200 rounded-bl-sm'
                    }
                  `}
                >
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start animate-in fade-in duration-300">
                <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-sm px-5 py-4 shadow-sm flex items-center gap-3 text-slate-500">
                  <Loader2 className="h-5 w-5 animate-spin text-blue-500" />
                  <span className="text-sm font-medium">Analyzing markets...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-slate-200 p-4 sm:p-6 shadow-[0_-4px_6px_-1px_rgb(0,0,0,0.05)] z-10 relative">
          <div className="max-w-3xl mx-auto">
            <form onSubmit={handleSend} className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about stocks, bonds, or market trends..."
                className="w-full pl-5 pr-14 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-inner text-slate-800 placeholder-slate-400"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="absolute right-2 p-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors shadow-md shadow-blue-600/20"
              >
                <Send className="h-5 w-5" />
              </button>
            </form>
            <p className="text-center text-xs text-slate-400 mt-3">
              FinSense can make mistakes. Consider verifying important financial information.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatDashboard;
