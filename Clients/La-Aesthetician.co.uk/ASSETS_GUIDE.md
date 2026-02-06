# Image Assets Integration Guide

## 📁 Where to Place Images

Place your images in: `website/public/images/`

### Required Images

#### 1. **Libby's Profile Photo** (for About section)
- **Filename:** `libby-profile.jpg` or `libby-profile.webp`
- **Location:** `website/public/images/libby-profile.jpg`
- **Recommended size:** 800x1000px (portrait)
- **Format:** JPG or WebP
- **Usage:** Main practitioner photo in "Meet Your Practitioner" section

#### 2. **Treatment Room Photos** (optional)
- **Filename:** `treatment-room.jpg`
- **Location:** `website/public/images/treatment-room.jpg`
- **Recommended size:** 1200x800px
- **Format:** JPG or WebP

#### 3. **Certifications/Awards** (optional)
- **Filename:** `awards.jpg`
- **Location:** `website/public/images/awards.jpg`
- **Recommended size:** 800x600px
- **Format:** JPG or WebP

---

## 🔄 After Adding Images

Once you've placed images in `website/public/images/`, run:

```powershell
# 1. Build the site
cd website
npm run build

# 2. Deploy to Hostinger
cd ..
python execution/deploy_ssh.py
```

---

## ✅ Current Status

- [x] Instagram embeds - Fixed with fallback UI
- [ ] Libby's profile photo - **Awaiting from client**
- [ ] Treatment room photos - **Awaiting from client**
- [ ] Awards/certificates - **Awaiting from client**

---

## 📝 Notes

The website is **ready to accept** these images. Once you provide them:
1. I'll update the `page.tsx` to reference the correct image paths
2. Rebuild and redeploy
3. The placeholder will be replaced with real photos

**Where to get images:**
- Instagram profile: https://www.instagram.com/la.aesthetics_rn/
- Direct from client: Libby's phone/camera
- Professional photoshoot (recommended for best quality)
