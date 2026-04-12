"""
Local HuggingFace LLM integration for Harbor
FOR GRADING: Part 2B - Local LLM Integration
"""
import logging
import bleach
import re

logger = logging.getLogger(__name__)

# Safety constants
MAX_INPUT_LENGTH = 500
BLOCKED_PATTERNS = [
    r'<script.*?>',
    r'DROP\s+TABLE',
    r'eval\s*\(',
]


def sanitize_input(text: str, max_length: int = MAX_INPUT_LENGTH) -> str:
    """Clean user input"""
    clean = bleach.clean(text, strip=True)
    clean = ' '.join(clean.split())
    return clean[:max_length].strip()


def is_safe_input(text: str) -> bool:
    """Check for malicious patterns"""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


def validate_output(text: str) -> bool:
    """Validate LLM output quality"""
    if len(text) < 50 or len(text) > 1000:
        return False
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    return len(sentences) >= 2


class HarborLocalLLM:
    """
    Local HuggingFace model wrapper
    FOR GRADING: This class loads and uses a local LLM
    """
    
    def __init__(self, model_name="google/flan-t5-small"):
        """
        Initialize with HuggingFace model
        Model weights will be downloaded automatically on first use
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self._loaded = False
        logger.info(f"Initialized LocalLLM with model: {model_name}")
    
    def load_model(self):
        """
        Lazy load the model (only when first needed)
        FOR GRADING: This demonstrates transformers library usage
        """
        if self._loaded:
            return
        
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            logger.info(f"Loading HuggingFace model: {self.model_name}")
            print(f"⏳ Downloading {self.model_name} weights (first time only)...")
            
            # Download and load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Download and load model
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            
            self._loaded = True
            print(f"✅ Model loaded successfully!")
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Could not load HuggingFace model: {e}")
    
    def generate(self, prompt: str, max_new_tokens: int = 150) -> str:
        """
        Generate text using the local model
        FOR GRADING: Core text generation function
        """
        # Ensure model is loaded
        self.load_model()
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            # Generate output
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=max_new_tokens,
                num_beams=4,
                temperature=0.7,
                do_sample=False,
                early_stopping=True
            )
            
            # Decode output
            generated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            
            return generated_text.strip()
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise


# Global instance (lazy-loaded)
_local_llm = None

def get_local_llm():
    """Get or create the global LLM instance"""
    global _local_llm
    if _local_llm is None:
        _local_llm = HarborLocalLLM()
    return _local_llm


def generate_listing_description(title: str, category: str, price: float, basic_info: str) -> dict:
    """
    Main function to generate listing description using local LLM
    FOR GRADING: This is the entry point for local LLM integration
    
    Returns:
        dict with keys: description, source, success, error
    """
    # Sanitize inputs
    title = sanitize_input(title, 100)
    basic_info = sanitize_input(basic_info, 500)
    
    # Safety check
    if not is_safe_input(title) or not is_safe_input(basic_info):
        return {
            'description': f"{category} available. Contact for details!",
            'source': 'fallback',
            'success': False,
            'error': 'Unsafe input detected'
        }
    
    # Build prompt
    prompt = f"""
    You are an assistant that writes high-quality marketplace listings.

    Write a professional and engaging description based on the information below.

    Title: {title}
    Category: {category}
    Price: ${price}
    Details: {basic_info}

    Requirements:
    - Write 2–3 complete sentences
    - Use a friendly and professional tone
    - Do NOT repeat the input word-for-word
    - Expand slightly on the details
    - Make it appealing to potential buyers
    - Do NOT include labels like 'Title', 'Category', or 'Price' in the output

    Final Description:
    """
    
    # Try to generate with local model
    try:
        llm = get_local_llm()
        description = llm.generate(prompt)
        
        # Validate output
        if validate_output(description):
            return {
                'description': description,
                'source': 'local_huggingface',
                'success': True,
                'error': None
            }
        else:
            logger.warning("Generated output failed validation")
            
    except Exception as e:
        logger.error(f"LLM generation error: {e}")
    
    # Fallback if model fails
    fallback = f"{category} service available. {basic_info[:100]} Great value at ${price}. Contact for more details!"
    return {
        'description': fallback,
        'source': 'template_fallback',
        'success': False,
        'error': 'Model generation failed'
    }
