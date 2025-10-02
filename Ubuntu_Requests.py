import requests
import os
from urllib.parse import urlparse
from pathlib import Path

def create_directory(directory_name):
    """Create directory in the spirit of Ubuntu community - preparing a shared space"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"✓ Community directory '{directory_name}' is ready")
        return True
    except Exception as e:
        print(f"✗ Could not create community directory: {e}")
        return False

def extract_filename(url):
    """Extract filename from URL with respect to the resource's identity"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    # Get filename from URL path
    if path:
        filename = os.path.basename(path)
        if filename and '.' in filename:
            return filename
    
    # Generate meaningful filename if none found
    domain = parsed_url.netloc.replace('www.', '').split('.')[0]
    return f"image_from_{domain}.jpg"

def fetch_image(url, directory="Fetched_Images"):
    """
    Fetch image from the global community with Ubuntu principles:
    - Respect for the resource
    - Graceful error handling
    - Community sharing preparation
    """
    print(f"\n🌍 Connecting to the global community at: {url}")
    
    try:
        # Respectful connection with timeout
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Check if content is actually an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print("✗ The resource is not an image. Please provide an image URL.")
            return False
        
        # Create community directory
        if not create_directory(directory):
            return False
        
        # Determine filename with respect to original identity
        filename = extract_filename(url)
        filepath = os.path.join(directory, filename)
        
        # Ensure unique filename to respect existing community resources
        counter = 1
        original_filepath = filepath
        while os.path.exists(filepath):
            name, ext = os.path.splitext(original_filepath)
            filepath = f"{name}_{counter}{ext}"
            counter += 1
        
        # Save the shared resource with care
        print(f"📥 Receiving shared resource: {filename}")
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        file_size = os.path.getsize(filepath) / 1024  # Size in KB
        print(f"✓ Successfully received and stored: {filename} ({file_size:.1f} KB)")
        print(f"📍 Community archive location: {os.path.abspath(filepath)}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"✗ Community responded with an error: {e}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to the community. Please check the URL and your connection.")
    except requests.exceptions.Timeout:
        print("✗ Connection timeout. The community is not responding.")
    except requests.exceptions.RequestException as e:
        print(f"✗ Unexpected connection issue: {e}")
    except IOError as e:
        print(f"✗ Cannot save the shared resource: {e}")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")
    
    return False

def main():
    """Main function embodying Ubuntu philosophy - 'I am because we are'"""
    print("=" * 60)
    print("       UBUNTU-INSPIRED IMAGE FETCHER")
    print("=" * 60)
    print("Embracing the wisdom: 'I am because we are'")
    print("Connecting to the global community with respect...")
    print("-" * 60)
    
    while True:
        url = input("\n🌐 Please share the community resource URL (or 'quit' to exit): ").strip()
        
        if url.lower() in ['quit', 'exit', '']:
            print("\n🙏 Thank you for participating in our global community!")
            print("May we continue to share and grow together.")
            break
        
        if not url.startswith(('http://', 'https://')):
            print("⚠️  Please provide a complete URL starting with http:// or https://")
            continue
        
        # Fetch the image with Ubuntu principles
        fetch_image(url)
        
        print("\n" + "-" * 60)
        print("Ready to receive another community resource...")

if __name__ == "__main__":
    main()
