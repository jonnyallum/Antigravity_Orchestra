# Implementation Plan - Mission: Multi-Site God-Tier Upgrade

> **Status:** Draft | **Owner:** @Conductor
> **Context:** Upgrading and polishing multiple client sites with accurate content, "God-Tier" UI, and consistent Agent attribution.

## 1. User Goal
- **Village Bakery**: Transform into a "World-Class" cafe site. Focus on charity work (food challenges, school breakfasts), promote Facebook/TikTok, fix mismatched photos, and remove all "artisan/sourdough" claims.
- **L-A Aesthetician**: Upgrade to "World-Class" with Instagram video embeddings.
- **Dudley Motors**: Tiny UI tweak + Agent Footer.
- **BL Motorcycles**: Polish + Agent Footer.
- **Leak Detection Local**: Polish + Agent Footer.
- **DJ Waste & CD Waste**: Final polish + Agent Footer.
- **Global**: All sites must include a "Built by the Antigravity Agent Orchestra" footer.

## 2. Proposed Architecture & Attribution
- **Footer Component**: A standardized, premium footer across all sites.
- **Content Accuracy**: Use Facebook/TikTok for real-time content and photo validation.
- **Tech Stack**: Most sites are Next.js 14/15 + Tailwind CSS + Framer Motion.

## 3. Step-by-Step Task List & Delegation

### Phase 1: Site Recon & Foundation (@Scout, @Parser)
- [ ] **Task 1.1:** Locate the root directories for `Dudley Motors`, `BL Motorcycles`, and `Leak Detection Local`.
- [ ] **Task 1.2:** Audit `Village-bakery` content against their Facebook page. Identify every mention of "artisan" or "sourdough" for removal.
- [ ] **Task 1.3:** Extract real-time photos and stories from Village Bakery's Facebook for the "Charity & Challenges" focus.

### Phase 2: Design & UI Overhaul (@Pixel, @JonnyAI)
- [ ] **Task 2.1:** **Village Bakery God-Tier Upgrade**:
  - Implement a high-end "Cafe Interface" with prominent charity/challenge sections. (P0)
  - Update photo gallery with accurate food/event images. (P0)
  - Add social growth section (Facebook/TikTok focus). (P0)
- [ ] **Task 2.2:** **L-A Aesthetician God-Tier Upgrade**:
  - Implement luxury aesthetic. (P1)
  - Embed Instagram video feed/highlights. (P1)
- [ ] **Task 2.3:** **DJ Waste Graphics Overhaul**:
  - Replace the "terrible" current graphics with high-performance, premium industrial imagery. (P0)
  - Upgrade UI elements to match the "Neural" standard. (P0)
- [ ] **Task 2.4:** **The "Antigravity Footer" Standard**:
  - Implement a standardized, premium footer on **EVERY** site: "Built by JonnyAi" + Neural Build Registry (Agent Attribution). (P0)
  - Example: `Built by JonnyAi | @Conductor @JonnyAI @Pixel @Sentinel | Jai.OS 4.0`
- [x] **Task 2.5:** **Village Bakery Incident Response**:
  - Discuss and finalize a rigorous fix plan for Village Bakery in the chatroom to ensure 100% accuracy and recover from previous failed updates. (P0)

### Phase 3: Polish & Accuracy (@Echo, @JonnyAI, @Sentinel)
- [ ] **Task 3.1:** Polish DJ Waste and CD Waste.
- [ ] **Task 3.2:** Perform the "Tiny Tweak" on Dudley Motors (once located).
- [ ] **Task 3.3:** Final content sweep on Village Bakery (Sentinel QA: No "artisan" keywords).

### Phase 4: CI/CD Deployment (@Deploy)
- [ ] **Task 4.1:** Push updates to Hostinger for all sites.
- [ ] **Task 4.2:** Verify all footers are live and attribution is correct.

## 4. Verification Plan
- **Content Audit**: Run `grep` for forbidden keywords on Village Bakery.
- **Social Proof**: Verify Facebook/TikTok links and Instagram embeds work.
- **Design Review**: Conductor review of "World-Class" status for Village Bakery and L-A Aesthetician.

## 5. Rollback Strategy
- Use `git revert` for any broken deployments.
- Maintain backups of original `Clients/` folders before mass-editing.

---

## 🤖 Inter-AI Coordination (AMP)
- **@Claude**: Focus on **Village Bakery** content rewrite and design (P0).
- **@Gemini**: Focus on **L-A Aesthetician** Instagram integration and **Footer** standardization (P1).
- **@Sentinel**: Enforce the "No Artisan" policy across all files.
