#create new seed_data.py file
"""
Seed data for Harbor RAG Pipeline.
These examples serve as the 'Gold Standard' for the AI to emulate.
"""

reference_listings = [
    # --- CATEGORY: TUTORING/SERVICES ---
    {
        "text": "Expert Physics 212 tutor with 3 years experience. I specialize in electromagnetism and midterm prep. Flexible meeting times at Grainger Library or via Zoom. Helping students master complex concepts with simplified practice problems."
    },
    {
        "text": "Professional essay editing and proofreading for humanities courses. I provide detailed feedback on structure, grammar, and citations. Quick 24-hour turnaround for urgent deadlines."
    },
    {
        "text": "Math 221 (Calculus I) tutoring sessions. Focus on derivative rules and integration techniques. I offer 1-on-1 sessions tailored to your specific syllabus and homework needs."
    },

    # --- CATEGORY: ELECTRONICS/TECH ---
    {
        "text": "Monitor for sale: 27-inch 4K IPS display in excellent condition. Perfect for gaming or creative work. Includes HDMI and Power cables. No scratches or dead pixels."
    },
    {
        "text": "Noise-canceling headphones (Sony WH-1000XM4). Used for one semester, like-new condition. Incredible battery life and sound quality. Includes original carrying case."
    },
    {
        "text": "Graphing Calculator (TI-84 Plus CE). Essential for STEM classes. Bright color screen and comes with a charging cable. Battery holds a charge perfectly."
    },

    # --- CATEGORY: HOUSING/DORM LIFE ---
    {
        "text": "Lightly used mini-fridge for sale. Perfect for dorm rooms, includes a small freezer compartment. Clean, energy-efficient, and runs very quietly. Pickup available at ISR."
    },
    {
        "text": "Memory foam mattress topper (Twin XL). Only used for one semester. High-density foam that makes any dorm bed feel like a luxury mattress. Sanitized and ready for use."
    },
    {
        "text": "Adjustable desk lamp with built-in USB charging port. Three different light warmth settings, perfect for late-night study sessions without straining your eyes."
    },

    # --- CATEGORY: CREATIVE/PHOTOGRAPHY ---
    {
        "text": "Professional graduation photography sessions. 1-hour shoot at up to 3 campus locations (Alma Mater, Quad, etc.). Includes 15 professionally edited high-resolution photos and full printing rights."
    },
    {
        "text": "Custom hand-knit winter scarves. Available in various colors and patterns. Made with high-quality wool-blend yarn to keep you warm during Illinois winters. Great as a gift!"
    },
    {
        "text": "Graphic design services for RSOs and student events. I create eye-catching flyers, logos, and social media assets with a fast turnaround time. Check out my portfolio for examples."
    },

    # --- CATEGORY: APPAREL/GEAR ---
    {
        "text": "Vintage Illinois Basketball jersey, size Large. Rare find in great condition with no fading or stains. Perfect for game days and tailgates."
    },
    {
        "text": "Mountain bike in good condition. 21-speed with front suspension. Recently tuned up and ready for campus commuting. Includes a sturdy U-lock and cable."
    }
]