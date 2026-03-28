#!/usr/bin/env python3
"""
Extract all translatable strings from JackPoker HTML pages into en.json.
This creates a structured locale file with keys organized by page and section.
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser
from collections import OrderedDict

# We'll manually curate the English strings since auto-extraction from complex HTML
# with inline SVGs, scripts, etc. is error-prone. This gives us clean, well-organized keys.

locale = OrderedDict()

# ============================================================
# GLOBAL / SHARED STRINGS (nav, footer, CTAs used across pages)
# ============================================================
locale["nav"] = {
    "home": "Home",
    "games": "Games",
    "bonuses": "Bonuses",
    "tournaments": "Tournaments",
    "news": "News",
    "promo_code": "Promo Code",
    "play_now": "Play Now",
    "theme_toggle_label": "Toggle theme"
}

locale["footer"] = {
    "description": "JackPoker is a modern online poker platform offering Texas Hold'em, PLO, Spin&Win, and tournament action. Licensed and certified by iTech Labs, BMM TestLabs, and GLI. Play responsibly.",
    "platform": "Platform",
    "resources": "Resources",
    "payments": "Payments",
    "faq": "FAQ",
    "terms": "Terms of Service",
    "privacy": "Privacy Policy",
    "copyright": "&copy; 2026 JackPoker. Operated by Jack La International Limitada. Licensed in Anjouan, Union of Comoros. Play responsibly. 18+",
    "certified_by": "Certified by iTech Labs &bull; BMM TestLabs &bull; GLI"
}

locale["cta"] = {
    "play_now": "Play Now",
    "play_now_at": "Play Now at JackPoker",
    "play_now_icon": "♠ Play Now",
    "claim_bonus": "Claim Bonus Now ♠",
    "explore_games": "Explore Games",
    "learn_bonuses": "Learn About Bonuses",
    "join_action": "Join the Action ♠",
    "view_schedule": "View Schedule",
    "copy_code": "Copy Code",
    "copy_clipboard": "Copy to Clipboard",
    "read_more": "Read More",
    "view_all_news": "View All News"
}

locale["promo"] = {
    "code": "WELCOME",
    "code_label": "Promo Code",
    "official_label": "OFFICIAL JACKPOKER PROMO CODE"
}

locale["responsible"] = {
    "disclaimer": "18+ only. New players only. Wagering requirements apply. Play responsibly. Licensed in Anjouan, Union of Comoros. Certified by iTech Labs, BMM TestLabs & GLI."
}

# ============================================================
# HOMEPAGE (index.html)
# ============================================================
locale["home"] = {
    "meta_title": "JackPoker \u2013 The Future of Online Poker | 300% Welcome Bonus",
    "meta_description": "Join JackPoker for world-class online poker. Texas Hold'em, PLO, Spin & Win tournaments, and a 300% welcome bonus up to $2,000. Play in your browser \u2014 no download required.",

    "badge": "OFFICIAL JACKPOKER PLATFORM \u2014 EST. 2021",
    "players_online": "players online now",
    "hero_title_1": "The Future of",
    "hero_title_2": "Online Poker",
    "hero_subtitle": "World-class poker action straight to your browser. Unbeatable bonuses, 50,000+ active players, and no downloads required.",

    "stats_prizes": "MONTHLY PRIZES",
    "stats_players": "ACTIVE PLAYERS",
    "stats_availability": "GAME AVAILABILITY",
    "stats_bonus": "WELCOME BONUS",

    "why_section_label": "WHY JACKPOKER",
    "why_title_1": "Everything You Need in One",
    "why_title_2": "Poker Platform",
    "why_subtitle": "Since launching in 2021, we've built JackPoker from the ground up with one goal: to give every poker player the best possible experience. Here's what sets us apart from every other platform on the market.",

    "feature_games_title": "Massive Game Selection",
    "feature_games_desc": "We offer the widest variety of poker formats in the industry. Choose from No-Limit Texas Hold'em at stakes ranging from NL10 to NL2000, Pot-Limit Omaha, PLO5, PLO6, the legendary Spin&Win with jackpots up to $1 million, and our unique Push-Fold format for lightning-fast action. Whether you prefer deep-stack cash games, sit-and-gos, or massive multi-table tournaments, you'll never run out of action at JackPoker. Our game lobby updates in real time so you always know where the softest tables are.",

    "feature_bonus_title": "Biggest Welcome Bonus",
    "feature_bonus_desc": "New players at JackPoker receive one of the most generous welcome packages in online poker: a 300% match bonus up to $2,000, a 20% instant cash component credited immediately, access to the Lootbox system offering rewards up to 1,000%, and a structured Welcome Quests path through Silver, Gold, and Supernova tiers. Use promo code WELCOME at registration and start your journey with a massive bankroll boost. The more you deposit, the more you unlock \u2014 our tiered quest system ensures rewards at every stage of your progression.",

    "feature_crypto_title": "Crypto-Friendly Platform",
    "feature_crypto_desc": "JackPoker is built for the modern player who values speed, privacy, and financial freedom. We accept Bitcoin, Ethereum, USDT, TRX, Litecoin, DOGE, and BNB alongside traditional payment methods. Crypto deposits are processed instantly, and withdrawals typically clear within minutes \u2014 no lengthy bank transfer waits. Our platform is fully compatible with hardware wallets and major software wallets. For players in regions with restricted banking, crypto gives you full, unrestricted access to everything JackPoker has to offer.",

    "feature_freerolls_title": "Daily Freerolls",
    "feature_freerolls_desc": "We run 8 freeroll tournaments every single day, giving you constant opportunities to build your bankroll without risking a cent. Our monthly freeroll prize pool exceeds $200,000, and seasonal series can push that figure even higher. Freerolls are open to all registered players \u2014 no deposit required. It's our way of ensuring that everyone, from first-time players to seasoned grinders, has a fair shot at winning real money every day.",

    "feature_vip_title": "VIP Rakeback Program",
    "feature_vip_desc": "Our VIP program gives you something that most platforms don't: lifetime rakeback. From the moment you start playing, a percentage of every pot you contribute to is returned to your account. The more you play, the higher your rakeback tier climbs. Top-tier players enjoy up to 60% effective rakeback through our leaderboard bonuses, monthly cashback, and exclusive VIP rewards. There are no resets \u2014 your progress is permanent.",

    "feature_browser_title": "Browser-Based Play",
    "feature_browser_desc": "Forget downloads, installations, and system requirements. JackPoker runs directly in your web browser on any device \u2014 Windows, macOS, Linux, Chromebook, iPad, or Android tablet. Our HTML5 engine delivers smooth performance with responsive design that adapts to your screen. Start a session on your laptop at home, continue on your phone during commute, and finish on your tablet in bed. Your session, your balance, and your table position carry over seamlessly.",

    "bonus_section_label": "EXCLUSIVE WELCOME PACKAGE",
    "bonus_title_1": "300% First Deposit",
    "bonus_title_2": "Bonus",
    "bonus_title_3": "Up to $2,000",
    "bonus_description": "JackPoker's welcome package is designed to give every new player a serious advantage right from the start. When you register and make your first deposit using promo code",
    "bonus_description_2": ", you unlock one of the most comprehensive bonus structures in online poker. Our package isn't a single offer \u2014 it's a multi-layered system that rewards you across your first weeks of play.",
    "bonus_match_intro": "The headline offer is a 300% match on your first deposit, up to a maximum of $2,000 in bonus funds. Deposit $100 and get $300 in bonus money. Deposit $666 and unlock the full $2,000. That's real money added to your account to play with, giving you the bankroll to take shots at bigger games without risking your own funds.",

    "bonus_instant_title": "20% Instant Cash",
    "bonus_instant_desc": "Deposited immediately to your real money balance \u2014 no wagering required. Available to withdraw at any time.",
    "bonus_instant_badge": "Instant",
    "bonus_match_title": "300% Match Bonus",
    "bonus_match_desc": "Triple your deposit up to $2,000 in bonus funds, released progressively as you play cash games and tournaments.",
    "bonus_match_badge": "300%",
    "bonus_lootbox_title": "Lootbox Rewards",
    "bonus_lootbox_desc": "Random multiplier rewards up to 1,000% on selected deposits. Every deposit is a chance to hit big.",
    "bonus_lootbox_badge": "1,000\u00d7",
    "bonus_quests_title": "Welcome Quests",
    "bonus_quests_desc": "Progress through Silver, Gold, and Supernova tiers to unlock additional bonuses, free tournament entries, and exclusive rakeback boosts.",
    "bonus_quests_badge": "3 Tiers",

    "trust_section_label": "TRUSTED WORLDWIDE",
    "trust_title_1": "Built on",
    "trust_title_2": "Trust & Security",
    "trust_description": "JackPoker operates under strict regulatory oversight with independent certification from three of the most respected testing laboratories in online gaming. Every hand is verifiably random, every transaction is encrypted, and every player's funds are held in segregated accounts.",
    "trust_rng_title": "Certified RNG",
    "trust_rng_desc": "Every card dealt on JackPoker is generated by a cryptographically secure random number generator that has been independently tested and certified by iTech Labs, BMM TestLabs, and GLI. Our RNG passes all standard statistical tests for randomness and is re-audited on a regular cycle.",
    "trust_encryption_title": "Bank-Grade Encryption",
    "trust_encryption_desc": "All data transmitted between your device and our servers is protected by 256-bit TLS encryption \u2014 the same standard used by major banks and financial institutions. Your personal information, financial details, and gameplay data are never exposed.",
    "trust_license_title": "Licensed & Regulated",
    "trust_license_desc": "JackPoker is operated by Jack La International Limitada, licensed in Anjouan, Union of Comoros. We comply with all applicable gaming regulations and maintain transparent operations with regular compliance reporting.",
    "trust_support_title": "24/7 Support",
    "trust_support_desc": "Our customer support team is available around the clock via live chat, email, and Telegram. Average response time is under 3 minutes during peak hours. We support English, Russian, Portuguese, and Spanish.",

    "numbers_prizes_label": "MONTHLY PRIZE DISTRIBUTION",
    "numbers_freerolls_label": "DAILY FREEROLL TOURNAMENTS",
    "numbers_bonus_label": "WELCOME BONUS MATCH",
    "numbers_rakeback_label": "LIFETIME RAKEBACK",

    "final_cta_label": "JOIN TODAY",
    "final_cta_title_1": "Ready to Play?",
    "final_cta_title_2": "Start Winning Now.",
    "final_cta_desc": "Join over 50,000 players already competing at JackPoker. Create your free account in under two minutes, make your first deposit with promo code WELCOME, and claim your 300% bonus up to $2,000. The tables are packed and the action never stops.",

    "faq_title": "Frequently Asked Questions",
    "faq_q1": "What is JackPoker and how does it work?",
    "faq_a1": "JackPoker is an online poker platform where you can play Texas Hold'em, Omaha (PLO/PLO5/PLO6), Spin & Win jackpot tournaments, and Push-Fold games. The platform runs directly in your web browser \u2014 no software download is needed. Simply register, deposit, and join a table. Games run 24/7 with thousands of active players at all times.",
    "faq_q2": "What is the JackPoker welcome bonus and how does it work?",
    "faq_a2": "New players receive a 300% match bonus on their first deposit, up to $2,000 in bonus funds. On top of that, you get 20% instant cash (no wagering required), Lootbox random multiplier rewards, and access to Welcome Quests with three tiers of additional bonuses. Use promo code WELCOME during registration to activate the full package.",
    "faq_q3": "What poker games are available at JackPoker?",
    "faq_a3": "JackPoker offers No-Limit Texas Hold'em (NL10 to NL2000), Pot-Limit Omaha in PLO4, PLO5, and PLO6 variants, Spin & Win jackpot sit-and-gos with prizes up to $1,000,000, Push-Fold short-stack games, multi-table tournaments with daily guarantees, and sit-and-go tournaments at all stake levels.",
    "faq_q4": "Is JackPoker safe and licensed?",
    "faq_a4": "Yes. JackPoker is operated by Jack La International Limitada, licensed in Anjouan, Union of Comoros. The platform's random number generator is independently certified by iTech Labs, BMM TestLabs, and GLI. All transactions use 256-bit TLS encryption, and player funds are held in segregated accounts.",
    "faq_q5": "How do I make a deposit at JackPoker?",
    "faq_a5": "JackPoker supports a wide range of payment methods including Visa, Mastercard, Skrill, Neteller, and major cryptocurrencies (Bitcoin, Ethereum, USDT, TRX, Litecoin, DOGE, BNB). Crypto deposits are instant. Traditional methods typically process within minutes. There are no deposit fees.",
    "faq_q6": "What is the JackPoker promo code and where do I enter it?",
    "faq_a6": "The current JackPoker promo code is WELCOME. Enter it during account registration in the 'Promo Code' or 'Bonus Code' field. It activates the full welcome package: 300% match bonus up to $2,000, 20% instant cash, Lootbox rewards, and Welcome Quest progression."
}

# ============================================================
# GAMES PAGE (games.html)
# ============================================================
locale["games"] = {
    "meta_title": "JackPoker Games \u2014 Texas Hold'em, PLO, Spin & Win, Push-Fold & More",
    "meta_description": "Explore all poker games at JackPoker. Texas Hold'em NL10-NL2000, PLO4/PLO5/PLO6, Spin & Win jackpots up to $1M, Push-Fold, tournaments, and integrated casino.",

    "breadcrumb": "Games",
    "page_label": "GAME LOBBY",
    "page_title_1": "Our",
    "page_title_2": "Games",
    "page_intro": "From beginner micro-stakes to high-roller NL2000 action, JackPoker hosts a complete suite of poker formats and casino titles built for players of every skill level. Explore everything we have on offer.",

    "tab_holdem": "Texas Hold'em",
    "tab_omaha": "Omaha",
    "tab_spin": "Spin & Win",
    "tab_pushfold": "Push-Fold",
    "tab_casino": "Casino",
    "tab_platform": "Platform",
    "tab_stakes": "Stakes Table",
    "tab_software": "Software",
    "tab_payments": "Payments",

    "section_label": "THE FULL LINEUP",
    "section_title_1": "Every Game,",
    "section_title_2": "Every Format",
    "section_subtitle": "JackPoker brings together the most played poker variants, a fast-action jackpot format, and a fully integrated casino \u2014 all on a single platform with one unified wallet.",

    "holdem_title": "Texas Hold'em",
    "holdem_desc": "The king of poker formats. Our No-Limit Hold'em tables run from micro-stakes NL10 all the way to high-roller NL2000. Dynamic table selection means you always find action at your preferred stake. Features include run-it-twice, anonymous tables, and customisable table themes.",

    "omaha_title": "Pot-Limit Omaha",
    "omaha_desc": "The action game. JackPoker offers PLO4 (traditional four-card), PLO5 (five-card), and PLO6 (six-card) at stakes from micro to high. Omaha tables on JackPoker consistently run softer than most platforms, especially at PLO5 and PLO6 where the player pool is growing rapidly.",

    "spin_title": "Spin & Win",
    "spin_desc": "Our flagship jackpot format. Three players, hyper-turbo blind structure, and a random prize multiplier up to $1,000,000. Games last 3\u20137 minutes on average. The multiplier is determined at the start \u2014 you could be playing for 2\u00d7 your buy-in or a life-changing jackpot on any given game.",

    "pushfold_title": "Push-Fold",
    "pushfold_desc": "A JackPoker original. You start with a short stack and every decision is all-in or fold. No post-flop play, no complex bet sizing \u2014 just pure preflop strategy. Games are ultra-fast and perfect for players who want high-volume, high-variance action in short sessions.",

    "mtt_title": "Multi-Table Tournaments",
    "mtt_desc": "Our daily tournament schedule features over $3.5 million in monthly guaranteed prize pools. From $1 buy-in micro events to high-stakes showdowns, there's a tournament starting every few minutes. Highlight events include the Big Bang Sunday ($45,000 GTD), daily grind series, and seasonal championship events with massive overlays.",

    "sng_title": "Sit & Go Tournaments",
    "sng_desc": "On-demand tournament action. Our Sit & Go lobby covers 6-max, 9-max, and heads-up formats at all stake levels. Buy in, wait for the table to fill, and play. Average wait time is under 30 seconds during peak hours.",

    "stakes_title": "Stakes & Limits",
    "stakes_subtitle": "Full breakdown of available stakes across all game types.",
    "stakes_game": "Game",
    "stakes_min": "Min Stake",
    "stakes_max": "Max Stake",
    "stakes_tables": "Tables",

    "software_label": "THE ENGINE",
    "software_title_1": "Purpose-Built",
    "software_title_2": "Poker Software",
    "software_desc": "JackPoker's proprietary HTML5 engine was built from the ground up for browser-based poker. No downloads, no plugins, no Java \u2014 just open your browser and play.",
    "software_feature_1_title": "Browser-Based",
    "software_feature_1_desc": "Works on Chrome, Firefox, Safari, and Edge. No download required. Full functionality on Windows, macOS, Linux, and Chromebook.",
    "software_feature_2_title": "Multi-Table Support",
    "software_feature_2_desc": "Play up to 20 tables simultaneously with our tiled layout system. Resize, arrange, and snap tables to fit your screen.",
    "software_feature_3_title": "Mobile Optimised",
    "software_feature_3_desc": "Responsive design adapts to any screen size. Full touch support on iOS and Android devices. Portrait and landscape modes.",
    "software_feature_4_title": "Custom Themes",
    "software_feature_4_desc": "Choose from multiple table felt colours, card designs, and background themes. Adjust bet slider sensitivity and action buttons to your preference.",

    "payments_label": "DEPOSITS & WITHDRAWALS",
    "payments_title_1": "Payment",
    "payments_title_2": "Methods",
    "payments_subtitle": "JackPoker supports a wide range of payment options to make deposits and withdrawals fast, secure, and convenient.",
    "payments_method": "Method",
    "payments_deposit": "Deposit",
    "payments_withdrawal": "Withdrawal",
    "payments_min_dep": "Min Deposit",
    "payments_instant": "Instant",
    "payments_minutes": "minutes",
    "payments_hours": "hours",
    "payments_business_days": "business days"
}

# ============================================================
# TOURNAMENTS PAGE (tournaments.html)
# ============================================================
locale["tournaments"] = {
    "meta_title": "JackPoker Tournaments \u2014 $3.5M+ Monthly GTD | Freerolls, Sunday Major & More",
    "meta_description": "Join JackPoker tournaments with over $3.5 million in monthly guarantees. Daily freerolls, the Big Bang Sunday, seasonal series, and satellite qualifiers for major events.",

    "breadcrumb": "Tournaments",
    "badge": "LIVE NOW \u2014 CASH CARNIVAL 2026",
    "hero_title_1": "Tournaments at",
    "hero_title_2": "JackPoker",
    "hero_intro": "We run one of the most action-packed tournament schedules in online poker. With over <strong>$3.5 million</strong> in monthly guaranteed prize pools, <strong>eight daily freerolls</strong>, a headline weekly event carrying a $45,000 guarantee, and blockbuster seasonal series, there is always a tournament starting in minutes \u2014 no matter your buy-in level or skill set. From pure freerolls that require no deposit whatsoever, all the way up to high-roller satellites and multi-flight main events, our calendar delivers non-stop tournament poker 24 hours a day, 365 days a year.",

    "stats_guarantees_label": "MONTHLY GUARANTEES",
    "stats_freerolls_label": "DAILY FREEROLLS",
    "stats_sunday_label": "BIG BANG SUNDAY GTD",
    "stats_freeroll_prizes_label": "MONTHLY FREEROLL PRIZES",

    "carnival_label": "CURRENT EVENT",
    "carnival_title_1": "Cash Carnival \u2014",
    "carnival_title_2": "$500,000 in Cash Prizes",
    "carnival_desc": "The Cash Carnival is JackPoker's flagship seasonal promotion, running across multiple weeks with half a million dollars in total prizes. The format combines cash game leaderboards, tournament series, and special challenges into one massive festival of poker.",
    "carnival_feature_1": "Weekly cash game leaderboards with $50,000+ in prizes per week across NL, PLO, and Spin&Win",
    "carnival_feature_2": "Dedicated tournament series with buy-ins from $1 to $500 and guaranteed prize pools reaching $100,000 on flagship events",
    "carnival_feature_3": "Daily challenges awarding instant cash prizes, free tournament entries, and Lootbox multipliers up to 500\u00d7",
    "carnival_feature_4": "Grand Finale main event with a $200,000 guaranteed prize pool and satellites starting from $0 (freeroll qualifiers)",

    "schedule_label": "DAILY SCHEDULE",
    "schedule_title_1": "Tournament",
    "schedule_title_2": "Calendar",
    "schedule_subtitle": "Our daily schedule features dozens of events from micro buy-ins to high-stakes showdowns. Here are the headline events that anchor each day's action.",
    "schedule_event": "Event",
    "schedule_buyin": "Buy-In",
    "schedule_guarantee": "Guarantee",
    "schedule_time": "Time (UTC)",
    "schedule_frequency": "Frequency",

    "types_label": "FORMAT GUIDE",
    "types_title_1": "Tournament",
    "types_title_2": "Types",
    "types_subtitle": "JackPoker offers a wide range of tournament formats to suit every playing style and bankroll. Here's a breakdown of what's available.",

    "freeroll_label": "PLAY FOR FREE",
    "freeroll_title_1": "Freeroll",
    "freeroll_title_2": "Tournaments",
    "freeroll_desc": "We believe every player should have access to real-money prize pools without risking a single dollar. That's why JackPoker runs eight dedicated freeroll tournaments every single day \u2014 more than any other platform in the industry.",

    "seasonal_label": "SEASONAL EVENTS",
    "seasonal_title_1": "Major",
    "seasonal_title_2": "Series & Events",
    "seasonal_desc": "Throughout the year, JackPoker hosts several blockbuster tournament series with prize pools that dwarf our regular daily schedule.",

    "cta_label": "START PLAYING",
    "cta_title_1": "Your Tournament",
    "cta_title_2": "Career Starts Here.",
    "cta_desc": "Register at JackPoker, enter promo code WELCOME to claim your 300% welcome bonus, and jump into your first tournament. With freerolls running all day, you don't even need to deposit to start winning."
}

# ============================================================
# BONUSES PAGE (bonuses.html)
# ============================================================
locale["bonuses"] = {
    "meta_title": "JackPoker Bonuses & Promotions \u2014 300% up to $2,000 + Freerolls & Rakeback",
    "meta_description": "Explore all JackPoker bonuses: 300% welcome match, 20% instant cash, Lootbox rewards, Welcome Quests, daily freerolls, and lifetime VIP rakeback.",

    "breadcrumb": "Bonuses & Promotions",
    "page_label": "OFFICIAL JACKPOKER PROMOTIONS",
    "page_title_1": "Bonuses &",
    "page_title_2": "Promotions",
    "page_intro": "We believe that every player deserves an extraordinary start. Our bonus program is one of the most generous in online poker \u2014 a 300% welcome match, instant cash credits, randomised Lootbox multipliers up to 1,000%, tiered Welcome Quests, lifetime rakeback up to 20%, and weekly promotions with hundreds of thousands of dollars in guaranteed prizes. Everything you need to know about claiming, wagering, and maximising your rewards is right here.",

    "highlight_match": "Welcome Match",
    "highlight_match_val": "300% up to $2,000",
    "highlight_cash": "Instant Cash",
    "highlight_cash_val": "20% Credit",
    "highlight_lootbox": "Lootbox Max",
    "highlight_lootbox_val": "1,000% Multiplier",
    "highlight_code": "Promo Code",
    "highlight_code_val": "WELCOME",

    "stats_match_label": "MAX WELCOME MATCH",
    "stats_rakeback_label": "LIFETIME RAKEBACK",
    "stats_freerolls_label": "MONTHLY FREEROLLS",
    "stats_carnival_label": "CASH CARNIVAL PRIZE POOL",

    "welcome_label": "THE FULL WELCOME PACKAGE",
    "welcome_title_1": "Everything You Get with",
    "welcome_title_2": "Promo Code WELCOME",
    "welcome_subtitle": "When you register at JackPoker and enter promo code WELCOME, you unlock a multi-layered welcome package that goes far beyond a simple deposit match.",

    "rakeback_label": "LIFETIME REWARDS",
    "rakeback_title_1": "VIP Rakeback",
    "rakeback_title_2": "Program",

    "weekly_label": "RECURRING PROMOTIONS",
    "weekly_title_1": "Weekly",
    "weekly_title_2": "Promotions",

    "terms_label": "FINE PRINT",
    "terms_title_1": "Bonus",
    "terms_title_2": "Terms & Conditions",

    "cta_label": "CLAIM YOUR BONUS",
    "cta_title_1": "Start Playing with",
    "cta_title_2": "a 300% Boost.",
    "cta_desc": "Register at JackPoker, enter promo code WELCOME on the deposit screen, and your bonus activates instantly. Minimum deposit: $10. Maximum bonus: $2,000. Your poker journey starts now."
}

# ============================================================
# PROMO CODE PAGE (promo-code.html)
# ============================================================
locale["promo_code"] = {
    "meta_title": "JackPoker Promo Code: WELCOME \u2014 300% Bonus up to $2,000 (March 2026)",
    "meta_description": "Use JackPoker promo code WELCOME to unlock a 300% deposit bonus up to $2,000, 20% instant cash, Lootbox rewards, and exclusive Welcome Quests. Verified March 2026.",

    "breadcrumb": "Promo Code",
    "hero_title_1": "Promo Code:",
    "hero_title_2": "WELCOME",
    "hero_desc": "Unlock your 300% welcome bonus up to $2,000 \u2014 plus instant cash, a Lootbox, and exclusive Welcome Quests. Enter the code during registration and your entire welcome package activates automatically.",

    "section_label": "YOUR EXCLUSIVE CODE",
    "section_title_1": "One Code.",
    "section_title_2": "The Full Package.",
    "section_desc_1": "When you join JackPoker using promo code",
    "section_desc_2": ", you don't just get a bonus \u2014 you unlock the complete JackPoker welcome experience. That means a 300% match on your first deposit, a slice of immediate cash in your pocket, a Lootbox with a mystery multiplier up to 1,000%, and entry into our tiered Welcome Quest program where you earn even more as you play.",
    "section_desc_3": "The code is completely free to use. There's no subscription, no catch, and no complicated qualification process. Simply register, enter",
    "section_desc_4": "in the promo code field, and make your first deposit. Everything activates automatically.",

    "how_label": "STEP BY STEP",
    "how_title_1": "How to Use",
    "how_title_2": "the Promo Code",
    "how_step1_title": "Create Your Account",
    "how_step1_desc": "Visit JackPoker and click 'Register'. Fill in your details \u2014 the process takes under 2 minutes.",
    "how_step2_title": "Enter Promo Code",
    "how_step2_desc": "In the registration form, find the 'Promo Code' or 'Bonus Code' field and type WELCOME.",
    "how_step3_title": "Make Your First Deposit",
    "how_step3_desc": "Choose your preferred payment method and deposit any amount from $10 upwards.",
    "how_step4_title": "Play & Earn",
    "how_step4_desc": "Your 300% match bonus is credited immediately. Start playing and work through Welcome Quests for even more rewards.",

    "unlocks_label": "WHAT YOU UNLOCK",
    "unlocks_title_1": "Full Bonus",
    "unlocks_title_2": "Breakdown",

    "compare_label": "CODE COMPARISON",
    "compare_title_1": "WELCOME vs",
    "compare_title_2": "Other Codes",

    "faq_title": "Promo Code FAQ",

    "cta_label": "USE YOUR CODE NOW",
    "cta_title_1": "Don't Miss",
    "cta_title_2": "Your Bonus.",
    "cta_desc": "Promo code WELCOME is available to all new players. Register now, enter the code, make your first deposit, and start playing with up to 300% extra in your account. No complicated steps, no hidden requirements."
}

# ============================================================
# NEWS PAGE (news.html)
# ============================================================
locale["news"] = {
    "meta_title": "JackPoker News \u2014 Latest Updates, Events & Platform Announcements",
    "meta_description": "Stay up to date with JackPoker news. Platform updates, tournament announcements, promotional events, and community highlights.",

    "breadcrumb": "News",
    "page_label": "LATEST UPDATES",
    "page_title_1": "JackPoker",
    "page_title_2": "News",
    "page_intro": "The latest announcements, event coverage, platform updates, and community stories from JackPoker. Stay informed about everything happening on the platform.",

    "article_read_more": "Read Full Article \u2192",
    "article_date_prefix": "",

    "news_1_title": "Cash Carnival 2026 Launches with $500,000 in Prizes",
    "news_1_date": "March 15, 2026",
    "news_1_tag": "Events",
    "news_1_excerpt": "JackPoker's biggest seasonal promotion is back. The Cash Carnival 2026 runs for six weeks with half a million dollars distributed across cash game leaderboards, tournament series, daily challenges, and a $200,000 Grand Finale main event.",

    "news_2_title": "New PLO6 Tables Now Live",
    "news_2_date": "March 10, 2026",
    "news_2_tag": "Platform",
    "news_2_excerpt": "Six-card Pot-Limit Omaha has arrived at JackPoker. PLO6 tables are now running at stakes from $0.10/$0.25 to $5/$10, joining our existing PLO4 and PLO5 offerings.",

    "news_3_title": "February Freeroll Series Awards Over $250,000",
    "news_3_date": "March 3, 2026",
    "news_3_tag": "Promotions",
    "news_3_excerpt": "Last month's expanded freeroll schedule delivered over $250,000 in prizes to JackPoker players. The February Freeroll Festival featured boosted guarantees, special themed events, and a $10,000 freeroll finale.",

    "news_4_title": "Mobile App Update: Multi-Table Support",
    "news_4_date": "February 24, 2026",
    "news_4_tag": "Platform",
    "news_4_excerpt": "JackPoker's mobile experience just got a major upgrade. Players can now run up to 4 tables simultaneously on iOS and Android devices, with a new tiled layout system optimised for smaller screens.",

    "news_5_title": "JackPoker Partners with iTech Labs for Enhanced RNG Certification",
    "news_5_date": "February 15, 2026",
    "news_5_tag": "Security",
    "news_5_excerpt": "In our ongoing commitment to fair play, JackPoker has expanded its RNG certification partnership with iTech Labs. The new agreement includes quarterly audits and real-time monitoring.",

    "news_6_title": "Spin & Win Jackpot Hit: Player Wins $287,000",
    "news_6_date": "February 8, 2026",
    "news_6_tag": "Community",
    "news_6_excerpt": "A JackPoker player hit a massive Spin & Win jackpot this week, turning a $100 buy-in into $287,000 in under five minutes. The lucky winner, playing from Brazil, triggered the 2,870\u00d7 multiplier."
}

# ============================================================
# LANGUAGE METADATA
# ============================================================
locale["_meta"] = {
    "lang_code": "en",
    "lang_name": "English",
    "lang_flag": "US",
    "dir": "ltr",
    "currency_symbol": "$",
    "locale_code": "en-US"
}

# Write output
out_dir = Path("/home/user/workspace/jackpoker-fan-site/i18n/locales")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "en.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(locale, f, indent=2, ensure_ascii=False)

# Count keys
total = 0
for section in locale.values():
    if isinstance(section, dict):
        total += len(section)

print(f"Extracted {total} translatable strings across {len(locale)} sections")
print(f"Written to {out_file}")
