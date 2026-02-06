#!/usr/bin/env python3
"""
Download Instagram assets using instaloader
"""

import instaloader
from pathlib import Path
import sys

def download_profile_assets(username, output_dir):
    """Download profile picture and recent posts"""
    
    # Create loader instance
    L = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern='',
    )
    
    try:
        print(f"Fetching profile: @{username}")
        
        # Get profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Download profile picture
        print(f"Downloading profile picture...")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        L.download_profilepic(profile, target=str(output_path / "profile"))
        print(f"✓ Profile picture saved")
        
        # Get recent posts (first 6)
        print(f"\nDownloading recent posts...")
        count = 0
        for post in profile.get_posts():
            if count >= 6:
                break
            
            try:
                # Download post
                L.download_post(post, target=str(output_path))
                count += 1
                print(f"✓ Downloaded post {count}/6")
            except Exception as e:
                print(f"✗ Failed to download post: {e}")
                continue
        
        print(f"\n✓ Successfully downloaded {count} posts")
        print(f"📁 Assets saved to: {output_path}")
        
        return True
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"✗ Profile @{username} does not exist")
        return False
    except instaloader.exceptions.ConnectionException as e:
        print(f"✗ Connection error: {e}")
        print("\nInstagram may be rate-limiting. Try again later or use a different method.")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    username = "la.aesthetics_rn"
    output_dir = Path(__file__).parent.parent / "assets" / "instagram"
    
    success = download_profile_assets(username, str(output_dir))
    sys.exit(0 if success else 1)
