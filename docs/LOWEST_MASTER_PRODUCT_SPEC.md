# LOWEST — Master Product, Engineering, Monetization & Launch Specification

## 0. Executive Summary

LOWEST is a camera-first shopping intelligence app for India.

The promise is deliberately simple:

> See it. Snap it. Get it for less.

A user can photograph a product, scan its barcode, paste a link, type a query, or upload an image. LOWEST identifies the exact product or the closest high-confidence match, searches supported commerce sources, normalizes prices and fees, calculates the true delivered cost, ranks offers, and routes the user to the best buying option.

The long-term product is not merely a comparison engine. It becomes a demand-routing marketplace where consumers declare intent and merchants compete to win that demand.

V1 must be realistically shippable by a small team using AI-assisted development. It should prioritize:

1. Camera and barcode product identification
2. Exact-SKU resolution
3. Offer aggregation from approved feeds/APIs/affiliate sources
4. True delivered price calculation
5. Price history and Buy/Wait guidance where data is sufficient
6. Affiliate/deep-link conversion
7. Native advertising and clearly labeled sponsored placements
8. Savings wallet/history
9. Alerts
10. Merchant adapters and future reverse-bid architecture

The app must not depend on brittle, unauthorized scraping of platforms that prohibit automated extraction. Each merchant source should be connected through an adapter with explicit source type, freshness, confidence, legal status, and feature flags.

---

# 1. Product Thesis

Indian commerce is fragmented across quick commerce, marketplaces, retailers, brand-direct stores, local sellers, and emerging network commerce. Users frequently compare the same product across several apps and still fail to know the real cost because sticker price is not the final price.

The core problem is not product discovery. It is purchase optimization.

LOWEST answers one question:

> What is the cheapest trustworthy way for me to obtain this exact product, here, now?

The app should eventually become the operating layer above commerce providers rather than another inventory-heavy marketplace.

---

# 2. Positioning

## 2.1 Consumer positioning

LOWEST is not an ecommerce store.

LOWEST is the price intelligence and buying decision layer above stores.

Tagline candidates:

- NEVER OVERPAY AGAIN
- SEE IT. SNAP IT. GET IT FOR LESS.
- ONE PHOTO. EVERY PRICE.
- FIND THE REAL LOWEST PRICE.
- BEFORE YOU BUY, LOWEST IT.

Preferred launch line:

> NEVER OVERPAY AGAIN.

Secondary descriptor:

> Snap any product. We find the best verified way to buy it.

## 2.2 Brand character

LOWEST should feel:

- Fast
- Intelligent
- Neutral
- Slightly cheeky
- Obsessive about saving money
- Trustworthy enough for high-value purchases
- Premium, not coupon-spammy

Avoid:

- Casino-style discount graphics
- Fake countdowns
- Red flashing sale UI
- Misleading urgency
- Dark patterns
- Paid ranking disguised as organic ranking

---

# 3. Product Scope

## 3.1 V1 category focus

V1 should focus on categories where exact product identification is achievable and pricing changes frequently:

- FMCG
- Beauty and personal care
- Household products
- Packaged food
- Consumer electronics
- Small appliances

Cars, furniture, travel, services, and property should remain architectural extensions, not day-one scope.

## 3.2 Inputs

The user can initiate a search through:

1. Camera photo
2. Gallery upload
3. Barcode scan
4. Text search
5. Product URL paste
6. Share-to-LOWEST extension from another app, if supported

---

# 4. Core User Journey

## Flow A — Photograph a physical product

1. User opens app
2. Camera is primary CTA
3. User photographs product
4. OCR + vision + packaging/logo/model extraction runs
5. Product candidates are generated
6. If confidence > threshold, exact match page opens
7. If confidence is uncertain, show 2–5 candidates
8. User confirms the product
9. LOWEST retrieves offers
10. Offers are normalized
11. App calculates TRUE PRICE
12. Best verified offer is shown first
13. User taps BUY
14. Affiliate/deep link opens merchant
15. Conversion attribution is recorded where supported
16. User returns and sees cumulative savings

## Flow B — Barcode scan

Barcode should be fastest path for packaged products.

1. Scan EAN/UPC/GTIN
2. Resolve canonical product
3. Retrieve offers
4. Display price ranking

## Flow C — Paste product link

1. User copies Amazon/Flipkart/brand link
2. Paste or share into LOWEST
3. Extract canonical title, model, variant, quantity and identifiers
4. Match against product graph
5. Search alternate sellers
6. Return ranked offers

---

# 5. The Killer Screen

The result screen must answer the user's question within one glance.

Example:

DOVE INTENSE REPAIR SHAMPOO
650 ml

BEST VERIFIED PRICE
₹519

Save ₹76 vs next comparable option

Delivery: 24 min
Seller: Example Merchant
Confidence: Exact match

[BUY FOR ₹519]

Then show the comparison table:

| Seller | Item Price | Delivery | Platform Fee | Known Discount | TRUE PRICE | ETA | Verified |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Merchant A | 499 | 20 | 0 | 0 | 519 | 24 min | Yes |
| Merchant B | 525 | 0 | 10 | 0 | 535 | 12 min | Yes |
| Merchant C | 549 | 0 | 0 | 10 | 539 | Tomorrow | Yes |

The comparison table should default to total payable cost, not product sticker price.

---

# 6. TRUE PRICE Engine

## 6.1 Goal

TRUE PRICE is the estimated all-in cost the user will pay to acquire the exact item.

Conceptually:

TRUE_PRICE = item_price + delivery_fee + platform_fee + mandatory_fee + tax_delta - eligible_known_discount - eligible_cashback_value

But V1 should be conservative.

Only include discounts automatically if they are reliably determinable.

Examples:

- Public coupon code valid for everyone: include
- Merchant universal sale: include
- Membership discount if user marks membership as active: include
- Bank-specific discount without knowing user's card: show separately, do not automatically subtract
- Cashback with uncertain redemption: show as optional effective value

## 6.2 Transparency

Each offer must expose a breakdown.

Never rank a seller first because of a hidden ad payment.

Sponsored offers may appear, but must be labeled Sponsored and must not overwrite the organic cheapest result.

---

# 7. Product Identification Engine

## 7.1 Identification hierarchy

Use the strongest available signals in this order:

1. Barcode / GTIN / EAN / UPC
2. Model number
3. Brand + exact product title + pack size
4. OCR from packaging
5. Vision embeddings
6. Merchant identifiers
7. User confirmation

## 7.2 Canonical product model

Every product should resolve to a canonical record:

- product_id
- canonical_name
- brand_id
- category_id
- subcategory_id
- variant
- size_value
- size_unit
- quantity
- model_number
- gtin
- ean
- upc
- isbn if relevant
- mpn
- manufacturer
- canonical_image
- normalized_attributes JSON
- status
- created_at
- updated_at

## 7.3 Product fingerprints

Generate normalized fingerprints based on:

brand + model + size + variant + category

This reduces duplicates.

Example:

"Dove Intense Repair 650ml" and "Dove Intense Repair Shampoo, 650 ML" should resolve to the same canonical product.

---

# 8. Product Graph Moat

The long-term moat is an Indian commerce identity graph.

The graph maps many merchant listings to one canonical product.

Tables/entities:

- canonical_products
- merchant_products
- product_aliases
- product_identifiers
- categories
- brands
- merchants
- merchant_locations
- offers
- offer_snapshots
- coupons
- payment_promotions
- product_images
- product_embeddings
- user_product_confirmations

Over time, every user correction improves matching quality.

---

# 9. Merchant Connector Architecture

Every commerce source must implement a standard adapter.

Interface concept:

MerchantAdapter

- search(query, location)
- getProduct(merchantProductId)
- getOffers(canonicalProduct, location)
- buildDeepLink(offer)
- normalize(rawProduct)
- healthCheck()

Metadata:

- source_type: api | affiliate_feed | merchant_feed | ondc | manual_partner | permitted_public
- freshness_seconds
- geographic_coverage
- attribution_required
- deep_link_supported
- checkout_supported
- status
- legal_review_status

Feature flags must allow any connector to be disabled instantly without app release.

Do not create V1 around prohibited automated extraction.

---

# 10. Data Confidence Model

Every offer needs a confidence score.

Inputs:

- exact identifier match
- title similarity
- pack-size match
- model match
- image similarity
- freshness
- source reliability
- historical consistency

Confidence labels:

- Exact match
- High confidence
- Similar item
- Unverified

Do not mix similar items into the organic exact-product price table unless clearly separated.

---

# 11. Location Architecture

Quick-commerce prices and inventory may vary by locality.

V1 location options:

- User-selected PIN code
- Device location with permission
- Saved home location

Store coarse locality for price relevance.

Do not expose a user's precise location publicly.

Location permission should be optional; PIN code input must work as fallback.

---

# 12. Price History

Create time-series snapshots:

- offer_id
- merchant_id
- canonical_product_id
- location_bucket
- observed_price
- true_price
- availability
- observed_at

Show:

- Current price
- 7-day low
- 30-day low
- 90-day low where sufficient data exists
- Historical median

Do not claim price history where data coverage is inadequate.

---

# 13. BUY NOW or WAIT

Only enable when sufficient historical observations exist.

Signals:

- Current percentile vs 30/90-day history
- Recent price velocity
- Promotion frequency
- Seasonal history where available
- Inventory level where available

Outputs:

BUY NOW
GOOD PRICE
AVERAGE PRICE
WAIT

Examples:

> BUY NOW — This is within 2% of the lowest observed verified price in the last 90 days.

> WAIT — Current price is 11% above the 30-day median.

Avoid false certainty.

---

# 14. Watchlist & Alerts

Users can tap:

[ALERT ME BELOW ₹500]

Alert types:

- Price drops below threshold
- New lowest merchant appears
- Product returns in stock
- New public coupon becomes available
- Price hits recent low

Push frequency limits are essential.

Do not spam.

---

# 15. Savings Wallet

This is the retention loop.

Home card:

YOU SAVED
₹1,842
THIS MONTH

Lifetime:

₹12,419 SAVED WITH LOWEST

Savings should only count where there is a defensible baseline.

Possible baseline:

- Difference between selected LOWEST offer and next comparable verified offer at purchase time
- Difference from user's pasted source price

Label methodology transparently.

---

# 16. Future Reverse Marketplace — MAKE THEM BID

This is the strategic destination.

For high-intent/high-ticket products, users can create a buy request.

Example:

BMW X3
Gurugram
Purchase within 7 days
Preferred color: black
Finance: required
Current best verified quote: ₹X

Participating dealers receive anonymized qualified demand and can submit offers.

Rules:

- Seller identity verified
- User identity protected until consent
- Offer validity required
- No fake bids
- No bait pricing
- Taxes/registration/fees normalized
- Dealer can state conditions

The buyer sees a live reverse-auction style board.

This is not required for V1 but database/event architecture should not prevent it.

---

# 17. Future Demand Aggregation

LOWEST can eventually aggregate demand:

> 1,284 users in NCR want Product X this week.

Merchants can submit bulk offers.

Do not expose private consumer identities.

Potential mechanics:

- Join deal
- Minimum buyer threshold
- Offer expiry
- Group-buy quantity tiers

This transforms comparison into demand-led commerce.

---

# 18. Monetization Strategy

Consumer V1 should remain free.

Revenue layers:

## 18.1 Affiliate commissions

Earn commission on qualified purchases through approved affiliate programs.

Requirements:

- Merchant-specific attribution
- Deep-link generation
- Click IDs
- Conversion reporting
- Refund/cancellation reconciliation where available

## 18.2 Display/native advertising

Use ads conservatively.

Potential inventory:

- Native ad in discovery feed
- Native sponsored result after organic top result
- Banner on non-transactional screens
- App-open ad only after product/retention validation, not at first launch
- Interstitial only at natural pauses, never while scanning or before showing the cheapest price

Never place an ad over the camera shutter or Buy button.

Never disguise ads as price results.

## 18.3 Sponsored merchant placements

Merchants can pay for visibility, but sponsored ranking must be separate from organic price ranking.

Layout:

BEST PRICE
Organic #1

SPONSORED OFFER
Clearly labeled

## 18.4 Merchant lead fees

For cars/high-ticket categories:

- Qualified lead fee
- Appointment fee
- Completed sale commission

## 18.5 Merchant SaaS later

Merchant dashboard:

- Demand heatmaps
- Lost-price analysis
- Competitor price deltas
- Bid opportunities
- Conversion metrics

## 18.6 Premium consumer tier later

Possible LOWEST+:

- Ad-free
- Longer price history
- More alerts
- Family watchlists
- Advanced buy/wait forecasting
- Priority concierge for high-ticket buys

Do not require subscription for core comparison.

---

# 19. Advertising Product Rules

Trust beats ad yield.

Rules:

1. Never show an interstitial before the user sees their first result
2. Never hide the actual cheapest result behind an ad
3. Never rank sponsored merchants above cheaper organic merchants without clear separation
4. Never auto-play loud audio
5. Cap interstitial frequency
6. Prefer native ads matching visual system but carrying explicit Sponsored label
7. Disable personalized advertising until appropriate consent is obtained
8. Provide ad privacy settings where required
9. Make paid partner disclosure permanent and readable

Suggested V1 ad units:

- Home discovery feed native ad: max 1 per 8 organic cards
- Search results: 1 sponsored card after the organic winner section
- Watchlist: banner only after enough content
- No ads on camera, onboarding, permission prompts, checkout handoff, privacy screens

---

# 20. App Store / Play Store Architecture

LOWEST sells/routs users to physical goods. Do not implement digital-goods purchases through external payment flows in ways that conflict with platform rules.

The app should:

- Use merchant deep links or browser handoff for physical-goods checkout where appropriate
- Clearly state when checkout is completed with a third-party merchant
- Provide Privacy Policy and Terms links
- Provide account deletion if accounts are created
- Properly declare collected data in store privacy disclosures
- Request camera/location/notification permissions only at the moment of need
- Avoid dark patterns in ATT or ad consent
- Keep tracking SDKs auditable and minimal

Android builds must target the then-current Google Play required API level at submission time. Re-check immediately before release because deadlines move.

iOS builds must use the currently accepted Xcode/iOS SDK at submission time. Re-check immediately before release.

---

# 21. Recommended Tech Stack

Primary recommendation for vibe-code speed:

## Mobile

React Native + Expo + TypeScript

Reasons:

- One codebase
- Fast camera integrations
- OTA updates for eligible JS changes
- Strong ecosystem
- Easy AI-assisted development
- iOS + Android

## Backend

Supabase initially:

- PostgreSQL
- Auth
- Row-level security
- Edge Functions
- Storage
- Realtime where needed

Alternative if scale/complexity later requires it:

- Postgres
- Redis
- Node/NestJS or Fastify
- Queue workers
- Object storage
- ClickHouse/BigQuery for analytics

## Search

Start with Postgres trigram/full-text + vector extension.

Move to dedicated search infrastructure only after need is proven.

## Vision/AI

Provider abstraction:

VisionProvider

- identifyProduct(image)
- extractText(image)
- generateEmbedding(image/text)

Do not hardcode a single AI provider throughout the app.

## Analytics

Product analytics abstraction supporting a provider such as PostHog/Amplitude/Firebase Analytics.

## Crash/error monitoring

Sentry or equivalent.

## Ads

AdMob/Google Mobile Ads or another store-compliant network behind an AdProvider abstraction.

## Push notifications

Expo notifications initially, or FCM/APNs with provider abstraction.

---

# 22. Suggested Monorepo Structure

/apps
  /mobile
  /admin
  /merchant-dashboard   # future
/packages
  /ui
  /types
  /config
  /analytics
  /merchant-adapters
  /product-matching
  /pricing
  /api-client
/supabase
  /migrations
  /functions
/docs

If using a single repo for MVP, keep boundaries even if deployment is simple.

---

# 23. Database Schema — MVP

## users

- id uuid PK
- email nullable
- phone nullable
- auth_provider
- display_name nullable
- home_pincode nullable
- currency default INR
- ads_consent_status
- analytics_consent_status
- created_at
- updated_at

## brands

- id
- name
- normalized_name
- logo_url

## categories

- id
- parent_id nullable
- name
- slug

## products

- id uuid
- brand_id
- category_id
- canonical_name
- normalized_name
- variant
- size_value
- size_unit
- quantity
- model_number
- gtin
- ean
- upc
- mpn
- canonical_image_url
- attributes jsonb
- status
- created_at
- updated_at

Indexes:

- normalized_name
- gtin
- ean
- upc
- model_number
- brand_id/category_id

## product_aliases

- id
- product_id
- alias
- normalized_alias
- source

## merchants

- id
- name
- slug
- logo_url
- source_type
- affiliate_enabled
- sponsored_enabled
- deep_link_template
- status

## merchant_products

- id
- merchant_id
- product_id nullable until matched
- merchant_product_id
- merchant_title
- merchant_url
- merchant_image_url
- raw_attributes jsonb
- match_confidence
- match_method
- last_seen_at

## offers

- id
- merchant_product_id
- pincode_bucket
- item_price
- mrp nullable
- delivery_fee nullable
- platform_fee nullable
- mandatory_fee nullable
- public_discount nullable
- estimated_true_price
- currency
- availability
- eta_min_minutes nullable
- eta_max_minutes nullable
- source_timestamp
- expires_at nullable
- raw_payload jsonb

## price_snapshots

- id
- offer_id
- product_id
- merchant_id
- pincode_bucket
- item_price
- true_price
- availability
- observed_at

## searches

- id
- user_id nullable
- input_type
- query_text nullable
- image_path nullable
- barcode nullable
- location_bucket
- resolved_product_id nullable
- confidence nullable
- latency_ms
- created_at

## outbound_clicks

- id
- user_id nullable
- product_id
- merchant_id
- offer_id
- click_id
- source_screen
- affiliate_program nullable
- created_at

## watchlists

- id
- user_id
- product_id
- target_price nullable
- enabled
- created_at

## savings_events

- id
- user_id
- product_id
- selected_offer_id
- baseline_offer_id nullable
- baseline_price
- selected_true_price
- estimated_saving
- methodology
- created_at

## ad_events

- id
- user_id nullable
- placement
- network
- ad_unit
- event_type
- revenue_micros nullable
- created_at

## sponsored_campaigns

- id
- merchant_id
- product_id nullable
- category_id nullable
- placement
- bid_model
- budget
- start_at
- end_at
- status

---

# 24. API Contract — MVP

POST /v1/identify/image

Input:

- image
- pincode

Output:

- candidates[]
- confidence

POST /v1/identify/barcode

GET /v1/products/:id

GET /v1/products/:id/offers?pincode=

POST /v1/search

POST /v1/outbound-click

POST /v1/watchlist

PATCH /v1/watchlist/:id

GET /v1/watchlist

GET /v1/product/:id/history

GET /v1/savings

GET /v1/config

Config endpoint should include remote feature flags.

---

# 25. Offer Ranking

Organic default ranking:

1. Exact product match required
2. Available inventory
3. Lowest TRUE PRICE
4. Higher confidence
5. Fresher source data
6. Faster ETA only as tiebreaker unless user selects Fastest

Allow user sorting:

- Cheapest
- Fastest
- Best value

Sponsored results must be separate.

---

# 26. Home Screen

Minimal home:

Header:
LOWEST

Main headline:
WHAT DO YOU WANT TO BUY?

Primary giant control:
[ TAKE A PHOTO ]

Secondary controls:
[ Scan barcode ]
[ Paste link ]
[ Type product ]

Below:

YOU SAVED ₹1,842 THIS MONTH

WATCHING
3 price alerts

TRENDING DEALS
Optional content feed

Ad inventory should appear only below the primary task area.

---

# 27. Camera UX

Camera view must be extremely fast.

Overlay copy:

POINT AT THE PRODUCT

Hints:

- Get the label in frame
- Barcode works best for packaged products

Controls:

- Shutter
- Gallery
- Barcode mode
- Flash

After capture:

ANALYSING...

Progress animation should not fake exact percentages.

If match confidence is low:

WHICH ONE IS IT?

Show candidate cards.

---

# 28. Result Screen UX

Hierarchy:

1. Canonical product
2. Best verified price
3. Savings statement
4. BUY button
5. TRUE PRICE breakdown
6. Alternatives
7. Price history
8. Buy/Wait signal
9. Set alert
10. Similar products
11. Clearly labeled sponsored content

---

# 29. Onboarding

Maximum 3 pages.

Page 1:
NEVER OVERPAY AGAIN.

Page 2:
SNAP ANY PRODUCT.
WE COMPARE SUPPORTED SELLERS.

Page 3:
YOU CHOOSE WHERE TO BUY.

CTA:
START SAVING

Do not force account creation before first search.

Ask account creation when user wants:

- alerts
- savings history
- sync

---

# 30. Authentication

Support guest mode.

Optional login:

- Apple
- Google
- Phone/email magic link if desired

For iOS, if offering third-party/social login, ensure Apple sign-in requirements are respected where applicable.

---

# 31. Privacy

Principles:

- Collect minimum necessary data
- Do not sell personally identifiable user data
- Do not expose exact user location
- Do not upload the entire photo library
- Process only selected images
- Provide image retention policy
- Allow deletion
- Encrypt sensitive data in transit and at rest
- Separate analytics identifiers from user profile where feasible

Camera images may contain personal information in the background. Prefer deleting raw search images after product extraction unless retention is explicitly needed and disclosed.

---

# 32. Admin Console

Build a simple web admin app.

Functions:

- Search products
- Merge duplicate products
- Correct product mapping
- Disable merchant connector
- View connector health
- View stale offer rate
- Manage sponsored campaigns
- View flagged misleading prices
- Review AI identification failures
- Manage categories
- Push feature flags
- View ad configuration

---

# 33. Merchant Health System

Each source gets:

- success rate
- median latency
- stale rate
- match accuracy
- price confirmation rate
- deep-link failure rate
- last successful fetch

If a connector becomes unreliable, degrade or disable it automatically.

---

# 34. Caching

Do not query every merchant from scratch for every user.

Cache offers by:

canonical_product_id + location_bucket

TTL depends on source/category.

Quick commerce:
short TTL

Electronics:
longer TTL

Always show last verified timestamp when stale risk is material.

---

# 35. Search Orchestration

Request flow:

1. Resolve product
2. Check fresh cache
3. Return immediate cached offers if valid
4. In parallel refresh connectors
5. Stream/update newer offers
6. Recalculate TRUE PRICE
7. Persist snapshots

Target perceived result:

First useful result < 2 seconds where cached.

Full refresh ideally < 5 seconds.

---

# 36. AI Cost Control

Do not run expensive vision calls when a barcode is available.

Decision tree:

Barcode found?
YES → identifier lookup
NO → OCR + lightweight classification
Need stronger resolution?
YES → vision model

Cache image hashes to avoid duplicate processing.

Track AI cost per successful product resolution.

---

# 37. Fraud & Abuse

Threats:

- Fake merchant offers
- Affiliate click spam
- Bot searches
- Ad fraud
- Coupon poisoning
- Merchant price baiting
- Malicious image uploads

Controls:

- Rate limits
- Signed click IDs
- Merchant verification
- Offer freshness requirements
- Abuse scoring
- Server-side attribution
- Image type/size validation
- Malware-safe storage handling
- Suspicious traffic filtering

---

# 38. Analytics Events

Core:

app_open
onboarding_started
onboarding_completed
camera_opened
photo_captured
barcode_scanned
link_pasted
text_search_submitted
product_identification_started
product_identified
product_identification_failed
candidate_selected
offers_requested
offers_loaded
best_offer_viewed
price_breakdown_opened
buy_clicked
merchant_handoff
alert_created
price_history_viewed
buy_wait_viewed
share_clicked
ad_impression
ad_clicked
sponsored_offer_impression
sponsored_offer_clicked
account_created
return_visit

Funnel:

Open → Search → Product resolved → Offer shown → Buy click

North-star metric:

Weekly users who receive at least one valid cheaper alternative or verified best-price result.

Commercial metrics:

- Revenue per search
- Revenue per active user
- Affiliate conversion rate
- Ad ARPDAU
- Merchant revenue
- Cost per resolved search

---

# 39. Ad Metrics

Monitor:

- Fill rate
- eCPM
- Impression/user/day
- CTR
- Revenue/session
- Retention vs ad exposure
- Search completion rate before/after ad rollout

Never maximize eCPM at the expense of product trust.

---

# 40. Growth Loops

## Share savings

Card:

I SAVED ₹342 WITH LOWEST

[product]

Found ₹X cheaper.

NEVER OVERPAY AGAIN.

## Referral

Give users a referral code/link.

Do not promise cash referral rewards until economics and fraud controls are proven.

## Price-drop sharing

"This iPhone just hit its 90-day low."

## SEO web layer

Create public product pages for indexable price comparison where sources permit.

This can become a major acquisition engine.

---

# 41. App Store Listing Draft

Name placeholder:
LOWEST — Price Finder

Subtitle:
Snap it. Find it cheaper.

Description opening:

Never overpay again.

Take a photo, scan a barcode, paste a product link or type what you want. LOWEST identifies the item, compares supported sellers, and shows the best available verified buying options in one place.

Key features:

- Camera product search
- Barcode scanning
- True delivered price comparison
- Price history
- Price-drop alerts
- Buy/Wait guidance where available
- One-tap handoff to sellers
- Savings tracker

Required disclosure:

LOWEST is a comparison and discovery service. Purchases are completed with third-party merchants. Prices and availability can change between comparison and checkout.

---

# 42. Play Store Listing Draft

Short description:

Snap any product and find the best supported price.

Long description should emphasize transparency and merchant handoff, avoid guaranteed savings claims.

---

# 43. App Icon Direction

Do not use shopping-cart cliché.

Concept:

A black square with a minimal white camera/viewfinder corner and one sharp downward arrow.

Alternate:

A bold L constructed from a camera focus bracket and price-down arrow.

The icon must remain readable at small sizes.

---

# 44. Design System

Palette:

- Near black
- Warm white
- One electric accent, ideally acid/lime or signal green
- Neutral grays

Typography:

- Strong grotesk/sans
- Large numeric pricing
- Tight information hierarchy

Components:

- PriceCard
- MerchantRow
- TruePriceBadge
- ConfidenceBadge
- SavingsPill
- SponsoredBadge
- PriceChart
- CameraShutter
- SearchInput
- AlertButton

---

# 45. Accessibility

- Screen reader labels
- Dynamic type
- Contrast compliance
- Large touch targets
- Do not communicate best price by color alone
- Haptics optional
- Reduced motion
- Camera flow accessible with barcode/text alternatives

---

# 46. Feature Flags

Examples:

camera_search_enabled
barcode_enabled
merchant_amazon_enabled
merchant_ondc_enabled
merchant_x_enabled
price_history_enabled
buy_wait_enabled
native_ads_enabled
interstitial_ads_enabled
sponsored_results_enabled
reverse_bidding_enabled
group_buy_enabled

Remote config must allow instant kill-switches.

---

# 47. Testing Matrix

Unit tests:

- Price normalization
- TRUE PRICE calculation
- Product deduplication
- Offer ranking
- Confidence scoring
- Savings calculation

Integration tests:

- Connector response normalization
- Product match to merchant listing
- Deep links
- Auth
- Alerts

E2E:

- Guest scans barcode
- Guest photographs product
- User confirms candidate
- Offers load
- User clicks merchant
- User sets price alert
- User signs in

Store-release QA:

- Permission copy
- Privacy links
- Account deletion
- ATT/consent if applicable
- Ad labeling
- Offline handling
- Slow network
- Empty results
- Unavailable product
- Wrong product correction

---

# 48. Error States

NO MATCH

"We couldn't identify this confidently. Try the barcode, front label, or type the product name."

NO OFFERS

"We found the product, but no supported sellers are available for your location yet."

STALE PRICE

"This price was last verified X minutes/hours ago. Confirm at checkout."

MERCHANT ERROR

"This seller isn't responding right now. Other verified options are below."

---

# 49. Legal / Trust Copy

Comparison disclaimer:

"Prices, availability, fees and delivery estimates can change. LOWEST ranks organic offers using available product and pricing data. Always confirm the final payable amount on the merchant's checkout screen."

Affiliate disclosure:

"LOWEST may earn a commission when you buy through certain links. This does not determine the organic cheapest-price ranking."

Sponsored disclosure:

"Sponsored placements are paid promotions and are clearly labeled."

---

# 50. Development Phases

## Phase 0 — Repository bootstrap

- Expo/React Native project
- TypeScript strict mode
- Supabase project
- Environment configuration
- CI
- Lint/format/test
- Sentry
- Analytics abstraction
- Feature flags

## Phase 1 — Camera MVP

- Camera
- Gallery
- Barcode
- Product identification
- Candidate confirmation
- Canonical product detail page

## Phase 2 — Offer engine

- Merchant adapter interface
- 2–3 legal/approved demo/production-capable sources
- Offer normalization
- TRUE PRICE
- Ranking
- Deep links

## Phase 3 — Retention

- Guest/account upgrade
- Watchlist
- Alerts
- Savings history
- Price snapshots

## Phase 4 — Monetization

- Affiliate attribution
- Native ad placements
- Sponsored campaign model
- Revenue analytics

## Phase 5 — Store launch

- Privacy policy
- Terms
- Account deletion
- Store screenshots
- App icon
- Data safety/privacy disclosure
- TestFlight
- Internal Play testing
- Production releases

## Phase 6 — Post-launch

- More connectors
- Better product graph
- Buy/Wait model
- SEO pages
- Merchant portal
- Reverse bidding pilot

---

# 51. V1 Launch Criteria

Do not launch merely because the app compiles.

Minimum quality gates:

- Camera to result works reliably
- Barcode flow works
- Product candidate correction exists
- At least meaningful supported offer coverage exists for chosen launch categories/locations
- Deep links work
- Price disclaimer is visible
- Ads are labeled
- Crash-free sessions are acceptable
- Search latency measured
- Analytics functioning
- Privacy policy live
- Account deletion live if accounts exist
- No prohibited scraping dependency

---

# 52. Initial Geographic Rollout

Start with one or a few metros where merchant data coverage is strongest.

Suggested pilot candidates:

- Delhi NCR
- Bengaluru
- Mumbai

Choose based on actual connector coverage, not branding preference.

---

# 53. Cold Start Strategy

The hardest problem is not mobile code. It is data coverage.

Mitigation:

1. Barcode database/API for initial product identity
2. Approved affiliate/product feeds
3. ONDC connectivity/partner path
4. Direct feeds from smaller ecommerce sellers
5. Admin-assisted product matching
6. User corrections
7. Cache popular SKU offers

Launch category by category rather than pretending every object in India is immediately comparable.

---

# 54. Sponsored Marketplace Model

Potential advertiser types:

- FMCG brands
- D2C brands
- Retailers
- Banks/card issuers
- Consumer electronics brands

Ad products:

- Sponsored alternative
- Sponsored category card
- Brand takeover of discovery feed, clearly labeled
- Bank offer module
- Merchant bid placement

Never allow paid promotion to masquerade as best price.

---

# 55. Merchant Bidding Data Model — Future

## buy_requests

- id
- user_id
- product_id
- location_bucket
- quantity
- max_price nullable
- purchase_window
- attributes jsonb
- status
- expires_at

## merchant_bids

- id
- buy_request_id
- merchant_id
- total_price
- conditions jsonb
- valid_until
- status

## bid_events

- id
- bid_id
- event_type
- created_at

---

# 56. AI Agent Architecture — Future

A shopping agent can orchestrate:

1. Identify intent
2. Resolve product
3. Gather offers
4. Check constraints
5. Calculate landed cost
6. Explain tradeoffs
7. Ask user only when necessary
8. Route checkout

Example:

User: "I want this shampoo but I need it tonight and don't want to pay more than ₹550."

Agent:

- Exact product found
- Cheapest overall: ₹519 tomorrow
- Cheapest tonight: ₹536 in 18 minutes

Recommended:

BUY ₹536 — arrives tonight

---

# 57. Do Not Build List

Do not waste V1 time on:

- Social feed
- Chat between buyers
- Crypto rewards
- Complex loyalty points
- Own checkout for every merchant
- Warehousing
- Delivery fleet
- Full car marketplace
- Full fashion visual search
- Every-city launch
- Fake AI recommendation narratives
- Scraping systems designed to bypass merchant defenses

---

# 58. Monetization Rollout Order

1. Affiliate links
2. Native ads after engagement is validated
3. Sponsored merchant cards
4. Merchant lead generation
5. Merchant analytics SaaS
6. Reverse bidding revenue
7. Optional premium plan

Ads should not be the only business model. The most attractive long-term economics come from commerce intent and merchant competition.

---

# 59. Example Revenue Model

Illustrative only, not forecast:

Assume 100,000 MAU.

If 30,000 users perform 4 searches/month = 120,000 monetizable searches.

Revenue components might include:

- Ad impressions from result/discovery screens
- Affiliate purchase commissions
- Sponsored campaigns

Do not hardcode economics until actual eCPM, CTR, conversion, AOV and commission data are known.

Track contribution margin per resolved search.

---

# 60. KPI Dashboard

Product:

- DAU/MAU
- Searches/user
- Product resolution rate
- Exact-match rate
- Offer coverage rate
- Median offers per product
- Median result latency
- Buy click-through
- Alert creation rate
- D1/D7/D30 retention

Commerce:

- Outbound clicks
- Conversion where known
- GMV referred
- Affiliate revenue
- Revenue per active user

Ads:

- Ad impressions
- eCPM
- Revenue
- Retention delta

Data quality:

- Stale offers
- Wrong matches
- User corrections
- Connector uptime

---

# 61. Security Checklist

- RLS enabled on user-owned tables
- Service secrets never bundled in client
- Signed server operations for merchant API calls
- Rate limit identify/search endpoints
- Validate image MIME and size
- Strip image metadata where appropriate
- Redact sensitive logs
- Rotate keys
- Separate dev/staging/prod
- Sentry PII controls
- Dependency scanning
- Secret scanning

---

# 62. CI/CD

GitHub Actions should run:

- install
- typecheck
- lint
- unit tests
- build checks

Protected main branch recommended.

Deployment environments:

- development
- staging
- production

Mobile:

- EAS Build or equivalent
- TestFlight
- Google Play Internal Testing

---

# 63. Environment Variables

Example:

EXPO_PUBLIC_API_URL
EXPO_PUBLIC_SUPABASE_URL
EXPO_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY server only
VISION_PROVIDER_API_KEY server only
BARCODE_PROVIDER_API_KEY server only
MERCHANT_* server only
AFFILIATE_* server only
SENTRY_DSN
ANALYTICS_KEY
ADMOB_IOS_APP_ID
ADMOB_ANDROID_APP_ID

Never expose server keys through EXPO_PUBLIC_ variables.

---

# 64. Definition of Done for Every Feature

A feature is not done until:

- UX states implemented
- Loading/error/empty states implemented
- Analytics events added
- Accessibility checked
- Unit/integration test where practical
- Feature flag added for risky integrations
- Privacy impact considered
- Documentation updated

---

# 65. Claude Code / Codex Master Instruction

Use the following directive when building the repository:

> You are the principal engineer, product designer, security engineer, QA lead, growth engineer and release manager for LOWEST. Work against the existing repository. Do not return isolated snippets when you can implement the feature directly. Inspect the codebase before modifying it. Preserve working code. Follow existing conventions unless there is a strong reason to improve them. Build a production-capable camera-first shopping comparison app for iOS and Android using the product specification in docs/LOWEST_MASTER_PRODUCT_SPEC.md as the source of truth.
>
> Prioritize a shippable V1 over theoretical completeness. Build the architecture so merchant sources are adapters and can be legally enabled/disabled independently. Never create systems designed to bypass anti-bot protections or violate merchant terms. Use APIs, feeds, affiliate programs, ONDC-compatible integrations, direct merchant data, and other permitted sources.
>
> The first successful flow must be: open app → photograph or scan a product → identify it → show exact-product offer comparisons → calculate TRUE PRICE → highlight organic cheapest verified option → deep-link to merchant → record click → allow alert/save history.
>
> Guest mode must work. Login must not block first value. Ads must never obscure the camera or organic winner. Sponsored offers must always be labeled and separated from organic ranking.
>
> Keep TypeScript strict, secrets server-side, migrations reversible, user data protected, analytics batched, and UI responsive. Add loading, empty, stale-price, uncertain-match, offline and merchant-failure states. Add tests for pricing, matching and offer sorting. Add remote feature flags around merchant connectors, ads, sponsored cards and experimental features.
>
> At the end of every implementation batch provide: files modified, migrations, tests run, unresolved risks, manual configuration required, store-review implications, and next highest-value task.

---

# 66. First Ten Engineering Tickets

1. Bootstrap Expo TypeScript mobile app and Supabase environment
2. Build LOWEST design system and home screen
3. Implement camera/gallery/barcode capture
4. Implement product identification provider interface
5. Create canonical product schema and migrations
6. Create merchant adapter interface and first data source
7. Build offer normalization + TRUE PRICE engine
8. Build result screen + ranking + merchant handoff
9. Add analytics/error monitoring/feature flags
10. Add watchlist + alerts + savings history

---

# 67. Launch Message

Hero:

NEVER OVERPAY AGAIN.

Body:

Take a photo of what you want. LOWEST identifies it, compares supported sellers, and shows the best verified way to buy it.

CTA:

SNAP SOMETHING

---

# 68. Strategic End State

LOWEST starts as a camera-first comparison app.

Then it becomes:

Product recognition
→ Product identity graph
→ Price intelligence
→ Purchase timing
→ Demand aggregation
→ Merchant bidding
→ Commerce routing

The ultimate strategic position is:

> Consumers tell LOWEST what they want. Sellers compete to fulfill it.

That is a substantially stronger company than a simple price-comparison scraper.
