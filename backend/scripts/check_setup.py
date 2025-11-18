"""
Diagnostic script to check backend setup
Run this from the backend directory: python scripts/check_setup.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("=" * 60)
    print("1. CHECKING .ENV FILE")
    print("=" * 60)

    env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        print("❌ ERROR: .env file not found!")
        print(f"   Expected location: {env_path}")
        print("\n   To fix:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and add your API keys")
        return False

    print(f"✅ .env file exists at {env_path}")

    # Check for required variables
    required_vars = ['GEMINI_API_KEY']
    optional_vars = ['QDRANT_URL', 'QDRANT_API_KEY', 'QDRANT_HOST']

    from dotenv import load_dotenv
    load_dotenv(env_path)

    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f"your-{var.lower().replace('_', '-')}-here":
            missing.append(var)
            print(f"❌ {var} is not set or using example value")
        else:
            # Mask the key for security
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var} is set: {masked}")

    # Check Qdrant configuration
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_key = os.getenv('QDRANT_API_KEY')
    qdrant_host = os.getenv('QDRANT_HOST', 'localhost')

    if qdrant_url:
        print(f"✅ Using Qdrant Cloud: {qdrant_url[:30]}...")
        if not qdrant_key or qdrant_key == "your-qdrant-api-key-here":
            print(f"❌ QDRANT_API_KEY is not set!")
            missing.append('QDRANT_API_KEY')
        else:
            print(f"✅ QDRANT_API_KEY is set")
    else:
        print(f"ℹ️  Using local Qdrant at {qdrant_host}:6333")

    return len(missing) == 0


def check_gemini_connection():
    """Test Gemini API connection"""
    print("\n" + "=" * 60)
    print("2. TESTING GEMINI API CONNECTION")
    print("=" * 60)

    try:
        from app.services.gemini_service import gemini_service

        # Test embedding generation
        print("Testing embedding generation...")
        embedding = gemini_service.generate_embedding("test")
        print(f"✅ Gemini API is working! Embedding size: {len(embedding)}")
        return True

    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        print("\n   To fix:")
        print("   1. Get API key from: https://makersuite.google.com/app/apikey")
        print("   2. Add it to backend/.env as GEMINI_API_KEY=your-key-here")
        return False


def check_qdrant_connection():
    """Test Qdrant connection and check for documents"""
    print("\n" + "=" * 60)
    print("3. TESTING QDRANT VECTOR DATABASE")
    print("=" * 60)

    try:
        from app.services.vector_store import vector_store

        # Test connection
        print("Testing Qdrant connection...")
        # Try to search with dummy embedding
        dummy_embedding = [0.1] * 768
        results = vector_store.search(dummy_embedding, top_k=1)

        if not results:
            print("⚠️  Qdrant is connected but NO DOCUMENTS FOUND!")
            print("\n   To fix:")
            print("   Run: python scripts/initialize_documents.py")
            return False
        else:
            print(f"✅ Qdrant is working! Found {len(results)} document(s)")
            print(f"   Sample document: {results[0].get('subset', 'Unknown')}")
            return True

    except Exception as e:
        print(f"❌ Qdrant connection error: {e}")
        print("\n   To fix:")
        print("   Option 1 (Recommended): Use Qdrant Cloud")
        print("   1. Sign up at: https://cloud.qdrant.io/")
        print("   2. Create a cluster")
        print("   3. Add QDRANT_URL and QDRANT_API_KEY to .env")
        print("\n   Option 2: Use local Docker")
        print("   1. Run: docker-compose up -d qdrant")
        print("   2. Initialize: python scripts/initialize_documents.py")
        return False


def check_documents():
    """Check if PDF documents exist"""
    print("\n" + "=" * 60)
    print("4. CHECKING PDF DOCUMENTS")
    print("=" * 60)

    from app.core.config import settings
    docs_dir = Path(settings.DOCUMENTS_DIR)

    if not docs_dir.exists():
        print(f"❌ Documents directory not found: {docs_dir}")
        return False

    pdf_files = list(docs_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDF files found in {docs_dir}")
        print("\n   To fix:")
        print("   1. Place ETCS PDF documents in backend/documents/")
        print("   2. Run: python scripts/initialize_documents.py")
        return False

    print(f"✅ Found {len(pdf_files)} PDF document(s):")
    for pdf in pdf_files[:5]:  # Show first 5
        print(f"   - {pdf.name}")
    if len(pdf_files) > 5:
        print(f"   ... and {len(pdf_files) - 5} more")

    return True


def main():
    """Run all diagnostic checks"""
    print("\n" + "🔍 ETCS DOCUMENTATION ASSISTANT - SETUP DIAGNOSTICS" + "\n")

    checks = [
        ("Environment file", check_env_file),
        ("Gemini API", check_gemini_connection),
        ("Qdrant database", check_qdrant_connection),
        ("PDF documents", check_documents),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = all(result for _, result in results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    if all_passed:
        print("\n🎉 All checks passed! Your backend should be working.")
        print("\nNext steps:")
        print("1. Restart the backend server")
        print("2. Try asking a question in the frontend")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nFor help, check the documentation or run:")
        print("python scripts/initialize_documents.py")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
