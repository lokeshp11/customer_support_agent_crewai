import gradio as gr
import os
from src.crew import CustomerSupportCrew
from src.logger import setup_logging
from src.css import APP_CSS
import base64

logger = setup_logging()

# Function to encode image to base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

logo_base64 = get_base64_image("logo.png")
logo_img_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else "/file=logo.png"

# Greeting Message
INITIAL_GREETING = """👋 **Hi there! I'm PulseAI.**
To get started, are you an existing customer? If so, please share your **Name and Email** so I can access your account.
"""

def run_customer_support(message, history):
    if not message:
        return "", history
        
    if not os.environ.get("OPENAI_API_KEY"):
        history.append({"role": "assistant", "content": "Error: OPENAI_API_KEY not found."})
        return "", history
    
    history.append({"role": "user", "content": message})
    
    try:
        # Construct context from history
        context_str = ""
        # Get last 5 exchanges to avoid token limits, excluding the current user message which is already in 'message'
        recent_history = history[-10:] if history else []
        for msg in recent_history:
            role = msg.get("role")
            content = msg.get("content")
            
            # Handle Gradio 5+ content format (can be a list of dicts)
            if isinstance(content, list):
                text_content = ""
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_content += item.get("text", "")
                content = text_content
            
            if role == "user":
                context_str += f"User: {content}\n"
            elif role == "assistant":
                context_str += f"Assistant: {content}\n"
        
        full_query = f"""
Previous Conversation History:
{context_str}

Current User Query:
{message}
"""
        logger.info(f"Received query: {message}")
        crew = CustomerSupportCrew(full_query)
        result = crew.run()
        history.append({"role": "assistant", "content": str(result)})
    except Exception as e:
        logger.error(f"UI Error: {str(e)}")
        history.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})
        
    return "", history

def toggle_chat(visible):
    return not visible

def navigate(target_page):
    # Returns (home_vis, mobile_vis, broadband_vis)
    if target_page == "home":
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    elif target_page == "mobile":
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    elif target_page == "broadband":
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

# HTML Content using the classes defined in CSS
HOME_HTML = """
<div class="hero-section">
    <h1>Experience the Speed of Pulse</h1>
    <p>Seamless connectivity for your home and mobile life.</p>
</div>
<div class="cards-container">
    <div class="service-card" onclick="document.getElementById('nav-btn-mobile').click()">
        <span class="icon">📱</span>
        <h2>Mobile Plans</h2>
        <p>Unbeatable 5G speeds with unlimited data options starting from $20/mo.</p>
    </div>
    <div class="service-card" onclick="document.getElementById('nav-btn-broadband').click()">
        <span class="icon">🌐</span>
        <h2>Broadband</h2>
        <p>Ultra-fast fibre broadband for your smart home. 1Gbps and 2Gbps plans available.</p>
    </div>
</div>
"""

MOBILE_HTML = """
<div class="plans-header">
    <h1>Mobile Plans</h1>
    <p>Choose the perfect plan for you</p>
</div>
<div class="plan-grid">
    <div class="plan-card">
        <h3>Starter 4G</h3>
        <p class="plan-price">$15<small>/mo</small></p>
        <ul style="list-style: none; padding: 0;">
            <li>20GB Data</li>
            <li>100 Mins Talktime</li>
            <li>Free Caller ID</li>
        </ul>
    </div>
    <div class="plan-card" style="border: 2px solid #764ba2; transform: scale(1.05);">
        <div style="background: #764ba2; color: white; padding: 5px; border-radius: 5px; margin-bottom: 10px;">BSES SELLER</div>
        <h3>Power 5G</h3>
        <p class="plan-price">$25<small>/mo</small></p>
        <ul style="list-style: none; padding: 0;">
            <li>100GB Data</li>
            <li>Unlimited Talktime</li>
            <li>Free Roaming (APAC)</li>
        </ul>
    </div>
    <div class="plan-card">
        <h3>Unlimited 5G</h3>
        <p class="plan-price">$45<small>/mo</small></p>
        <ul style="list-style: none; padding: 0;">
            <li>Unlimited Data</li>
            <li>Unlimited Talktime</li>
            <li>Global Roaming</li>
        </ul>
    </div>
</div>
"""

BROADBAND_HTML = """
<div class="plans-header">
    <h1>Home Broadband</h1>
    <p>Reliable fibre for the whole family</p>
</div>
<div class="plan-grid">
    <div class="plan-card">
        <h3>1Gbps Fibre</h3>
        <p class="plan-price">$39<small>/mo</small></p>
        <p>Perfect for HD streaming and gaming.</p>
    </div>
    <div class="plan-card">
        <h3>2Gbps Gamer</h3>
        <p class="plan-price">$59<small>/mo</small></p>
        <p>Dedicated gaming bandwidth + Free Router.</p>
    </div>
</div>
"""

with gr.Blocks(title="Pulse Telecom") as demo:
    
    # State to track chat visibility
    chat_visible = gr.State(False)

    # --- Navigation Header ---
    with gr.Row(elem_classes="nav-header"):
        with gr.Column(scale=1, min_width=100):
            gr.HTML(f'<img src="{logo_img_src}" style="height: 50px; border: none; background: transparent;">', elem_id="app-logo")
        with gr.Column(scale=10):
             gr.Markdown(
                """
                # <span style="color: #00FFFF;">Pulse Telecom</span>
                <span style="color: #CCCCCC;">*Connecting your world, one pulse at a time.*</span>
                """
            )
        with gr.Column(scale=4):
            with gr.Row():
                nav_home = gr.Button("Home", variant="secondary")
                nav_mobile = gr.Button("Mobile", variant="secondary", elem_id="nav-btn-mobile")
                nav_broadband = gr.Button("Broadband", variant="secondary", elem_id="nav-btn-broadband")

    # --- Pages ---
    with gr.Group(visible=True) as home_page:
        gr.HTML(HOME_HTML)

    with gr.Group(visible=False) as mobile_page:
        gr.HTML(MOBILE_HTML)
        
    with gr.Group(visible=False) as broadband_page:
        gr.HTML(BROADBAND_HTML)

    # --- Floating Chat Widget ---
    # The toggle button is always visible
    chat_toggle = gr.Button("💬", elem_classes="chat-toggle-btn", elem_id="main-chat-toggle")

    # The chat window container (Starts WITH 'chat-hidden' class)
    with gr.Column(elem_classes="floating-chat-container chat-hidden") as chat_window:
        with gr.Row(elem_id="chat-header"):
            gr.Markdown("<span>PulseAI Support</span>")
            btn_minimize = gr.Button("−", size="sm", elem_id="btn-minimize")
            close_chat = gr.Button("✕", size="sm", elem_id="btn-close")

        # Confirmation Dialog (Centered in chat window)
        with gr.Column(visible=False, elem_id="close-confirmation-area") as close_confirmation:
            gr.Markdown("### End chat session?")
            gr.Markdown("Ending the session will clear your current conversation history.")
            with gr.Row():
                confirm_yes = gr.Button("Yes, end session", variant="primary")
                confirm_no = gr.Button("No, keep chatting", variant="secondary")

        with gr.Group(visible=True) as chat_main_area:
            chatbot = gr.Chatbot(
                value=[{"role": "assistant", "content": INITIAL_GREETING}],
                show_label=False,
                height=450,
                avatar_images=(None, "logo.png")
            )
            with gr.Row(elem_id="chat-input-area"):
                msg_input = gr.Textbox(
                    show_label=False,
                    placeholder="Type your message...",
                    scale=4,
                    container=False,
                    elem_id="msg-input"
                )
                send_btn = gr.Button("➤", size="sm", scale=1, elem_id="send-btn")

        # Chat interaction logic
        def on_user_msg(user_input, history):
            if not user_input:
                return "", history, gr.update(visible=True)
            
            resp_input, resp_history = run_customer_support(user_input, history)
            
            # Check for [CLOSE_CHAT] token
            should_close = False
            if resp_history and resp_history[-1]['role'] == 'assistant':
                last_msg = resp_history[-1]['content']
                if "[CLOSE_CHAT]" in last_msg:
                    should_close = True
                    resp_history[-1]['content'] = last_msg.replace("[CLOSE_CHAT]", "").strip()
            
            if should_close:
                return "", resp_history, gr.update(elem_classes="floating-chat-container chat-hidden"), False
            return "", resp_history, gr.update(), True

        msg_input.submit(on_user_msg, [msg_input, chatbot], [msg_input, chatbot, chat_window, chat_visible])
        send_btn.click(on_user_msg, [msg_input, chatbot], [msg_input, chatbot, chat_window, chat_visible])
        
        # Close button show confirmation
        def show_confirm():
            return gr.update(visible=True), gr.update(visible=False)
        
        def cancel_confirm():
            return gr.update(visible=False), gr.update(visible=True)
            
        close_chat.click(show_confirm, None, [close_confirmation, chat_main_area])
        confirm_no.click(cancel_confirm, None, [close_confirmation, chat_main_area])

        def minimize_chat_fn():
            return False, gr.update(elem_classes="floating-chat-container chat-hidden")

        btn_minimize.click(
            minimize_chat_fn,
            None,
            outputs=[chat_visible, chat_window]
        )

        def handle_confirm_yes():
            logger.info("Session end confirmed. Resetting history and closing.")
            print("[SupportBot] Session Ended by User - Resetting State", flush=True)
            new_history = [{"role": "assistant", "content": INITIAL_GREETING}]
            # returns: chatbots content, chat_visible state, window classes, confirmation visibility, main_area visibility
            return new_history, False, gr.update(elem_classes="floating-chat-container chat-hidden"), gr.update(visible=False), gr.update(visible=True)

        confirm_yes.click(
            handle_confirm_yes, 
            None, 
            outputs=[chatbot, chat_visible, chat_window, close_confirmation, chat_main_area]
        )
        
        # After confirming, we also need to hide the confirmation area for next time
        confirm_yes.click(lambda: gr.update(visible=False), None, close_confirmation)

    # --- Logic Wiring ---
    
    def toggle_chat_fn(visible):
        new_state = not visible
        logger.info(f"Toggle Chat clicked. New visibility: {new_state}")
        print(f"[SupportBot] UI Interaction: Toggle Chat (Show={new_state})", flush=True)
        new_classes = "floating-chat-container" if new_state else "floating-chat-container chat-hidden"
        return new_state, gr.update(elem_classes=new_classes)

    chat_toggle.click(
        toggle_chat_fn,
        inputs=[chat_visible],
        outputs=[chat_visible, chat_window]
    )

        # Navigation
    nav_home.click(lambda: navigate("home"), None, [home_page, mobile_page, broadband_page])
    nav_mobile.click(lambda: navigate("mobile"), None, [home_page, mobile_page, broadband_page])
    nav_broadband.click(lambda: navigate("broadband"), None, [home_page, mobile_page, broadband_page])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, css=APP_CSS, theme=gr.themes.Soft())
