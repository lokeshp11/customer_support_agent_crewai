
APP_CSS = """
/* General Resets and Fonts */
body {
    font-family: 'Inter', sans-serif;
    background-color: #f0f2f5;
    margin: 0;
    padding: 0;
}

/* Navigation Header */
.nav-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-header img {
    height: 40px;
}

#app-logo button, #app-logo .download-button, #app-logo .maximize-button, #app-logo .share-button {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    z-index: -100 !important;
    pointer-events: none !important;
}

#app-logo {
    border: none !important;
    background: transparent !important;
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%);
    color: white;
    padding: 4rem 2rem;
    text-align: center;
    border-radius: 0 0 20px 20px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.hero-section h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    font-weight: 800;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.hero-section p {
    font-size: 1.5rem;
    opacity: 0.9;
}

/* Service Cards Container */
.cards-container {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding: 2rem;
    flex-wrap: wrap;
}

/* Individual Card Styling */
.service-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    width: 300px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.05);
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.service-card h2 {
    color: #333;
    margin-bottom: 10px;
    font-size: 1.8rem;
}

.service-card p {
    color: #666;
    line-height: 1.6;
}

.service-card .icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

/* Floating Chat Widget */
.floating-chat-container {
    position: fixed;
    bottom: 90px;
    right: 25px;
    width: 420px;
    height: 650px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px) saturate(180%);
    border-radius: 28px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
    z-index: 9999;
    border: 1px solid rgba(255, 255, 255, 0.4);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    opacity: 1;
    transform: translateY(0) scale(1);
    transform-origin: bottom right;
}

.floating-chat-container.chat-hidden {
    opacity: 0 !important;
    transform: translateY(20px) scale(0.9) !important;
    pointer-events: none !important;
    visibility: hidden !important;
    display: none !important; /* Force complete removal from layout */
}

/* Toggle Button */
.chat-toggle-btn {
    position: fixed !important;
    bottom: 25px !important;
    right: 25px !important;
    width: 60px !important;
    height: 60px !important;
    border-radius: 30px !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    box-shadow: 0 10px 25px rgba(118, 75, 162, 0.4) !important;
    z-index: 10000 !important;
    cursor: pointer !important;
    border: none !important;
    font-size: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}

.chat-toggle-btn:hover {
    transform: scale(1.1) rotate(5deg);
}

#chat-header {
    padding: 16px 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#chat-header span {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}

#btn-minimize, #btn-close {
    background: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    min-width: 36px !important;
    height: 36px !important;
    padding: 0 !important;
    margin-left: 8px !important;
    cursor: pointer !important;
    font-size: 1.1rem !important;
    transition: all 0.2s !important;
}

#btn-minimize:hover, #btn-close:hover {
    background: rgba(255, 255, 255, 0.35) !important;
    transform: translateY(-1px);
}

#chat-input-area {
    padding: 20px;
    background: #ffffff;
    border-top: 1px solid rgba(0,0,0,0.06);
    display: flex !important;
    gap: 12px !important;
    align-items: center !important;
}

#msg-input {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 16px !important;
    background: #f8fafc !important;
    padding: 8px !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    transition: all 0.2s ease !important;
}

#msg-input:focus-within {
    border-color: #667eea !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
}

#send-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    min-width: 48px !important;
    height: 48px !important;
    font-size: 1.2rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 12px rgba(118, 75, 162, 0.2) !important;
    transition: all 0.2s !important;
}

#send-btn:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
}

/* Simple Plans Page Styling */
.plans-header {
    background: #333;
    color: white;
    padding: 3rem 1rem;
    text-align: center;
}

.plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.plan-card {
    border: 1px solid #eee;
    padding: 2rem;
    border-radius: 10px;
    background: white;
    text-align: center;
}

.plan-price {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2a9d8f;
    margin: 1rem 0;
}
"""
