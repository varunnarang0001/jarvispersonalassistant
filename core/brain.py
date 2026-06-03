import os
from groq import Groq

class JarvisBrain:
    def __init__(self):
        """Initializes the Groq client and sets up the Llama 3.1 engine."""
        # 1. Secure Authentication
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Critical Error: GROQ_API_KEY missing from .env file.")

        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.1-8b-instant"
        
        # 2. State Management (Memory)
        self.current_persona_name = "Jarvis"
        self.chat_history = [] 
        
        # 3. The Master Rule
        self.master_rule = (
            " Keep your answers extremely concise, usually 1 to 2 sentences. "
            "Do NOT use markdown formatting, bolding, or asterisks."
            "Explain in detail when Scientific questions are asked"
        )
        
        # 4. Boot the default session
        default_instruction = "You are Jarvis, a highly intelligent, formal, and polite AI assistant. Call the user 'Sir'."
        self._boot_chat_session(default_instruction)

    def _boot_chat_session(self, instruction_text):
        """Builds a fresh memory bank with specific rules."""
        final_instruction = instruction_text + self.master_rule
        
        # The first message must always be the 'system' rules.
        self.chat_history = [
            {"role": "system", "content": final_instruction}
        ]

    def change_persona_dynamic(self, custom_description):
        """Wipes the memory and shifts the personality matrix."""
        new_instruction = f"You are {custom_description}."
        self.current_persona_name = custom_description
        self._boot_chat_session(new_instruction) 
        return True 

    def think(self, user_input):
        """Sends the memory bank to Groq, applies sliding window, and returns text."""
        try:
            # 1. Add user message
            self.chat_history.append({"role": "user", "content": user_input})
            
            # 2. Memory Management (Sliding Window)
            if len(self.chat_history) > 5:
                self.chat_history.pop(1) 
                self.chat_history.pop(1) 

            # 3. Call the AI
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.chat_history,
                temperature=0.7,
                max_tokens=150
            )
            # 4. Extract Text
            ai_text = response.choices[0].message.content
            
            # 5. Save to memory and return
            self.chat_history.append({"role": "assistant", "content": ai_text})
            return ai_text
            
        except Exception as e:
            return f"Sir, I encountered a cognitive error: {str(e)}"

# ==========================================
# ISOLATED TESTING ENVIRONMENT
# ==========================================
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    try:
        my_brain = JarvisBrain()
    except Exception as e:
        print(e)
        exit()

    print("\n--- Testing Groq Brain Module (Type 'exit' to quit) ---")
    
    while True:
        user_text = input(f"You (to {my_brain.current_persona_name}): ")
        
        if user_text.lower() in ["exit", "quit", "bye"]:
            print("Shutting down brain testing.")
            break
            
        elif user_text.lower().startswith("act like a") or user_text.lower().startswith("act like an"):
            extracted_persona = user_text.lower().replace("act like a", "").replace("act like an", "").strip()
            my_brain.change_persona_dynamic(extracted_persona)
            print(f"System: Personality shifted to {extracted_persona.capitalize()}.")
            continue 
            
        answer = my_brain.think(user_text)
        print(f"AI: {answer}")