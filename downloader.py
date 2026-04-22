import instaloader
import requests

L = instaloader.Instaloader(
    download_pictures=False,
    save_metadata=False
)

def load_session():
    try:
        L.load_session_from_file("your_username")
    except:
        print("No session found")

def download_with_instaloader(shortcode):
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            return post.video_url
    except:
        return None

def download_with_direct_api(url):
    # fallback method (less reliable)
    try:
        return url
    except:
        return None

def get_video_url(shortcode, original_url):
    url = download_with_instaloader(shortcode)
    
    if url:
        return url

    return download_with_direct_api(original_url)
