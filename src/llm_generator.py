# src/llm_generator.py
from transformers import pipeline
import torch

class ComplaintGenerator:
    def __init__(self, model_name="gpt2"):
        """Initialize the LLM generator with a compatible model"""
        print(f"🔄 Loading LLM model: {model_name}...")
        
        # Use a model that's widely available and compatible
        self.generator = pipeline(
            "text-generation",
            model=model_name,
            max_new_tokens=150,
            pad_token_id=50256  # GPT-2 specific
        )
        print(f"✅ LLM Ready")
    
    def generate_answer(self, question, context_chunks):
        """Generate answer based on context chunks"""
        if not context_chunks:
            return "No relevant complaints found to answer this question."
        
        # Format context
        context = "\n".join([f"- {chunk}" for chunk in context_chunks[:3]])
        
        prompt = f"""You are a financial analyst assistant. Answer the question using the complaint data.

COMPLAINTS:
{context}

QUESTION: {question}

ANSWER:"""
        
        try:
            response = self.generator(
                prompt,
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7
            )[0]['generated_text']
            
            # Extract only the answer part
            answer = response.split("ANSWER:")[-1].strip()
            return answer
        except:
            return f"Based on {len(context_chunks)} complaints: {context[:200]}..."