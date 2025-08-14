// HolySheet - Real-time WebSocket Client
class HolySheetApp {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.currentSheetData = null;
        this.init();
    }

    init() {
        this.setupWebSocket();
        this.setupEventListeners();
        this.updateConnectionStatus('Connecting...', 'gray');
    }

    setupWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            this.isConnected = true;
            this.updateConnectionStatus('Connected', 'green');
            console.log('WebSocket connected');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            this.isConnected = false;
            this.updateConnectionStatus('Disconnected', 'red');
            console.log('WebSocket disconnected');
            // Attempt to reconnect after 3 seconds
            setTimeout(() => this.setupWebSocket(), 3000);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('Error', 'red');
        };
    }

    setupEventListeners() {
        // Chat functionality
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-chat');
        
        const sendMessage = () => {
            const message = chatInput.value.trim();
            if (message && this.isConnected) {
                this.sendChatMessage(message);
                chatInput.value = '';
            }
        };
        
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Load sheet functionality
        document.getElementById('load-sheet').addEventListener('click', () => {
            this.loadSheet();
        });

        // Quick actions
        document.querySelectorAll('.quick-action').forEach(button => {
            button.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                this.performQuickAction(action);
            });
        });

        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }
    }

    updateConnectionStatus(status, color) {
        const statusEl = document.getElementById('connection-status');
        statusEl.textContent = status;
        statusEl.className = `px-3 py-1 rounded-full text-sm bg-${color}-100 text-${color}-700`;
    }

    sendChatMessage(message) {
        // Add user message to chat
        this.addChatMessage(message, 'user');
        
        // Send to WebSocket
        if (this.ws && this.isConnected) {
            this.ws.send(JSON.stringify({
                type: 'chat',
                message: message,
                sheet_data: this.currentSheetData
            }));
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case 'chat_response':
                this.addChatMessage(data.message, 'assistant');
                break;
            case 'sheet_loaded':
                this.displaySheetData(data.data);
                break;
            case 'error':
                this.showError(data.message);
                break;
        }
    }

    addChatMessage(message, sender) {
        const chatContainer = document.getElementById('chat-container');
        
        // Remove empty state if present
        if (chatContainer.children.length === 1 && chatContainer.children[0].classList.contains('text-center')) {
            chatContainer.innerHTML = '';
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-4 ${sender === 'user' ? 'text-right' : 'text-left'}`;
        
        const bubble = document.createElement('div');
        bubble.className = `inline-block max-w-xs lg:max-w-md px-4 py-3 rounded-xl font-medium ${
            sender === 'user' 
                ? 'bg-black text-white' 
                : 'bg-gray-50 text-gray-900 border border-gray-200'
        }`;
        bubble.textContent = message;
        
        messageDiv.appendChild(bubble);
        chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    loadSheet() {
        const sheetUrl = document.getElementById('sheet-url').value.trim();
        if (!sheetUrl) {
            this.showError('Please enter a Google Sheets URL');
            return;
        }

        // Show loading state
        this.showLoading('Loading sheet...');
        
        // For now, simulate loading (you'll implement actual Google Sheets API)
        setTimeout(() => {
            this.showQuickActions();
            this.showSuccess('Sheet loaded successfully!');
        }, 1000);
    }

    performQuickAction(action) {
        const actions = {
            analyze: 'Analyze this financial data. What patterns, trends, or insights do you see?',
            clean: 'Help me clean up this data. Identify duplicates, formatting issues, missing values, or inconsistencies.',
            trends: 'What financial trends can you identify in this data over time? Any concerning patterns or opportunities?',
            formulas: 'Suggest useful Excel/Google Sheets formulas for this financial data. Include specific cell references.'
        };
        
        if (actions[action]) {
            this.sendChatMessage(actions[action]);
        }
    }

    showQuickActions() {
        document.getElementById('quick-actions').classList.remove('hidden');
    }

    showLoading(message) {
        // Implement loading UI
        console.log('Loading:', message);
    }

    showSuccess(message) {
        // Implement success notification
        console.log('Success:', message);
    }

    showError(message) {
        // Implement error notification
        console.error('Error:', message);
    }

    displaySheetData(data) {
        const dataContainer = document.getElementById('data-container');
        // Implement data table display
        dataContainer.innerHTML = '<div class="text-green-600">Sheet data loaded!</div>';
        this.currentSheetData = data;
    }
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', () => {
    new HolySheetApp();
});
