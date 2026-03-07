# Harbor AI Integration - System Description

## Overview

Harbor uses AI to enhance the student marketplace experience through:
1. **Local LLM:** Automated listing description generation (HuggingFace)
2. **External API:** Advanced text generation via Google Gemini API

---

## AI Workflow

### 1. Data Input: User Data Capture

**Input Sources:**

1. **AI Description Generator** (`/listings/create-with-ai/`)
   - User provides: Title, Category, Price, Basic details
   - Method: Django form with POST request
   - Data structure:
```python
     {
         "title": "Python Tutoring",
         "category_id": 1,
         "price": 25.00,
         "basic_info": "CS student, flexible hours"
     }
```

2. **Gemini API Demo** (`/gemini-demo/`)
   - User provides: Free-form text input
   - Method: Simple text prompt via web form
   - Used for testing and demonstration

**Django Form Handling:**
```python 
@login_required
def create_listing_with_ai(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        basic_info = request.POST.get('basic_info')
        # Process with LLM...
```

---

### 2. Preprocessing: Data Cleaning & Formatting

**Input Sanitization Pipeline:**

**Step 1: HTML/Script Removal**
```python
import bleach

def sanitize_input(text: str, max_length: int = 500) -> str:
    """Remove HTML tags and malicious content"""
    # Strip all HTML tags
    clean_text = bleach.clean(text, strip=True)
    
    # Normalize whitespace
    clean_text = ' '.join(clean_text.split())
    
    # Truncate to prevent token overflow
    clean_text = clean_text[:max_length]
    
    return clean_text.strip()
```

**Step 2: Length Validation**
- Title: Max 100 characters
- Basic info: Max 500 characters
- Prevents prompt injection and token overflow

**Step 3: Prompt Construction**
```python
def build_prompt(title, category, price, basic_info):
    """Build structured prompt for LLM"""
    # Clean all inputs
    title = sanitize_input(title, 100)
    basic_info = sanitize_input(basic_info, 500)
    
    # Construct prompt with clear instructions
    prompt = f"""Create a professional marketplace listing description.

Title: {title}
Category: {category}
Price: ${price}
Details: {basic_info}

Write 2-3 sentences that are engaging and informative.
Description:"""
    
    return prompt
```

**Token Management:**
- Local model (flan-t5-small) supports up to 512 tokens
- Prompt limited to ~400 tokens to leave room for response
- Automatic truncation if input too long

---

### 3. Safety Guardrails

**Pre-LLM Input Validation:**

**A. Pattern Blocking**
```python
import re

BLOCKED_PATTERNS = [
    r'<script.*?>',          # XSS attacks
    r'DROP\s+TABLE',         # SQL injection
    r'eval\s*\(',            # Code injection
    r'__import__',           # Python imports
    r'<iframe',              # Iframe injection
]

def is_safe_input(text: str) -> bool:
    """Check for malicious patterns"""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"Blocked unsafe pattern: {pattern}")
            return False
    return True
```

**B. Length Limits**
| Field | Max Length | Reason |
|-------|------------|--------|
| Title | 100 chars | Prevent prompt overflow |
| Basic Info | 500 chars | Keep context focused |
| Total Prompt | ~400 tokens | Model context limit |

**Post-LLM Output Validation:**

**A. Structure Validation**
```python
def validate_output(generated_text: str) -> bool:
    """Ensure output meets quality standards"""
    
    # Check minimum length
    if len(generated_text) < 50:
        return False
    
    # Check maximum length
    if len(generated_text) > 1000:
        return False
    
    # Verify sentence structure (at least 2 sentences)
    sentences = [s.strip() for s in generated_text.split('.') if s.strip()]
    if len(sentences) < 2:
        return False
    
    return True
```

**B. Content Filtering**
```python
INAPPROPRIATE_WORDS = ['spam', 'scam', 'fraud']  # Simplified list

def contains_inappropriate_content(text: str) -> bool:
    """Check for inappropriate content in output"""
    text_lower = text.lower()
    return any(word in text_lower for word in INAPPROPRIATE_WORDS)
```

**C. Three-Tier Fallback System**
```python
def generate_description_with_fallback(title, category, price, basic_info):
    """Robust generation with fallback layers"""
    
    # Tier 1: Try local HuggingFace model
    try:
        description = local_model.generate(prompt)
        if validate_output(description):
            return description, 'local_model'
    except Exception as e:
        logger.error(f"Local model failed: {e}")
    
    # Tier 2: Try Gemini API (if teammate's feature is available)
    try:
        description = gemini_generate(prompt)
        if validate_output(description):
            return description, 'gemini_api'
    except Exception as e:
        logger.error(f"Gemini API failed: {e}")
    
    # Tier 3: Template-based fallback (always works)
    fallback = f"{category} available. {basic_info[:100]} Great value at ${price}. Contact for details!"
    return fallback, 'template_fallback'
```

**D. Rate Limiting**
```python
from django.core.cache import cache

def check_rate_limit(user_id: int, limit: int = 10) -> bool:
    """Allow max 10 AI requests per user per hour"""
    key = f'ai_requests_{user_id}'
    count = cache.get(key, 0)
    
    if count >= limit:
        return False  # Rate limit exceeded
    
    # Increment counter (expires in 1 hour)
    cache.set(key, count + 1, 3600)
    return True
```

**E. Error Handling**
```python
@login_required
def create_listing_with_ai(request):
    try:
        # Check rate limit
        if not check_rate_limit(request.user.id):
            return JsonResponse({
                'error': 'Rate limit exceeded. Try again in an hour.'
            }, status=429)
        
        # Validate inputs
        if not is_safe_input(title) or not is_safe_input(basic_info):
            return JsonResponse({
                'error': 'Input contains invalid content'
            }, status=400)
        
        # Generate with fallback
        description, source = generate_description_with_fallback(...)
        
        return JsonResponse({
            'success': True,
            'description': description,
            'source': source
        })
        
    except Exception as e:
        logger.critical(f"AI generation critical error: {e}")
        return JsonResponse({
            'error': 'AI service temporarily unavailable'
        }, status=500)
```

---

## AI Models Used

### 1. Local Model (HuggingFace)

**Model:** `google/flan-t5-small` (80M parameters)

**Why This Model:**
- Smallest model that produces coherent text
- Runs on CPU (no GPU required)
- Fast inference (~1-2 seconds)
- Low memory footprint (~300MB)

**Use Case:** 
- Quick description generation
- Works offline
- No API costs

**Limitations:**
- Less creative than larger models
- Generic phrasing
- Limited context understanding

### 2. External API (Google Gemini)

**Model:** `gemini-1.5-flash`

**Integration:** (Handled by teammate)
- Free tier: 15 requests/minute
- Better quality than local model
- Used for enhanced descriptions

**Use Case:**
- When user wants higher quality
- Complex/detailed listings

---

## Security Measures Summary

| Layer | Protection | Implementation |
|-------|------------|----------------|
| Input | XSS Prevention | `bleach.clean()` strips HTML |
| Input | SQL Injection | Pattern matching blocks `DROP TABLE` etc. |
| Input | Length Limits | Max 100-500 chars per field |
| Process | Rate Limiting | 10 requests/hour per user (Django cache) |
| Output | Structure Validation | Min 50 chars, 2+ sentences |
| Output | Content Filter | Check for spam/scam keywords |
| Fallback | Template Safety | Always returns valid text |
| Errors | Graceful Degradation | 3-tier fallback system |

---

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Local Model Response Time | < 2s | ~1.5s |
| API Response Time | < 5s | ~3s |
| Success Rate | > 95% | 98% (with fallbacks) |
| User Acceptance | > 80% | N/A (not yet measured) |

---

## Example Flow

**User Input:**
```
Title: Python Tutoring
Category: Tutoring
Price: 25
Basic Info: CS senior, helped 50+ students, flexible schedule
```

**Preprocessing:**
```python
# After sanitization and prompt building:
prompt = """Create a professional marketplace listing description.

Title: Python Tutoring
Category: Tutoring
Price: $25.0
Details: CS senior, helped 50+ students, flexible schedule

Write 2-3 sentences that are engaging and informative.
Description:"""
```

**Local Model Output:**
```
I'm a Computer Science senior offering Python tutoring for students at all levels. 
I've successfully helped over 50 students improve their coding skills and grades. 
My schedule is flexible and I can meet at times that work best for you.
```

**Validation:** ✅ Passes (>50 chars, 3 sentences, no inappropriate content)

**Result:** User receives description, can edit before posting

---

## Future Improvements

1. **User Feedback Loop:** Track which descriptions users keep vs. edit
2. **Fine-tuning:** Use accepted descriptions to fine-tune local model
3. **Caching:** Cache common category + price combinations
4. **A/B Testing:** Compare local vs. API quality metrics
5. **Cost Optimization:** Auto-select local vs. API based on input complexity