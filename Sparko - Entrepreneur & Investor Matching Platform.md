# Sparko - Entrepreneur & Investor Matching Platform

## Project Overview
Sparko is a Tinder-inspired web application that connects entrepreneurs with investors through an intuitive swipe-based interface. The platform facilitates meaningful business partnerships by allowing users to discover, match, and communicate with potential collaborators.

## Core Features

### User Roles
- **Entrepreneurs**: Seeking funding, partnerships, or business guidance
- **Investors**: Looking for investment opportunities and promising startups
- **Flexible Role Switching**: Users can change their role and profile anytime

### Card-Based Matching System
**Sparko Card Content (13 fields):**
1. Name/Nickname (e.g., Tiffany / Chih-Jung)
2. Title/Role (e.g., "Founder", "Product Manager", "Developer", "Investor")
3. Company/Project Name (optional)
4. Location/Timezone
5. Tagline (e.g., "AI-driven SaaS startup in progress")
6. Skills/Expertise (2-3 tags: React, UI/UX, PE Funding)
7. Looking For (investors, tech partners, co-founders, beta users)
8. Bio (50-80 words)
9. Collaboration Needs (e.g., "Seeking full-stack engineer for MVP development")
10. Photo/Logo
11. Social Links (LinkedIn/Website/GitHub - revealed after successful match)
12. Super Spark 🔥 Button (limited uses)
13. Like/Skip Buttons

### Interaction Mechanics
- **Left Swipe**: Reject/Skip
- **Right Swipe**: Like/Interest
- **Super Spark**: Special interest with visual effects (sparkle animation)
- **Mutual Match**: Opens chat functionality immediately
- **Super Spark Effect**: Makes cards appear with sparkle effects to increase match probability

### Smart Matching Algorithm
- **Industry-based filtering**: Matches complementary roles (entrepreneurs ↔ investors)
- **Intelligent recommendations**: Based on skills, location, and collaboration needs
- **Preference learning**: Adapts to user behavior over time

### Premium Features
- **Super Spark Limits**: 3 free per week, additional purchases available
- **Premium Unlocks**:
  - View feedback from other users
  - Early access to contact information (email/LinkedIn)
  - Legal document templates
  - Advanced analytics and insights

### Multi-language Support
- **Primary Language**: English
- **Language Selector**: Dropdown in header/settings
- **Supported Languages**: English, Traditional Chinese (expandable)
- **Localization**: All UI text, error messages, and notifications

## Technical Architecture

### Frontend Stack
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS + Custom CSS for animations
- **State Management**: React Context + useReducer
- **Routing**: React Router v6
- **Animations**: Framer Motion for swipe gestures and transitions
- **Internationalization**: react-i18next

### Backend Stack
- **Framework**: Flask (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **File Storage**: Local storage (expandable to cloud)
- **Payment Integration**: Stripe (for premium features)
- **API Design**: RESTful APIs

### Database Schema
```sql
-- Users table
users (id, email, password_hash, role, created_at, updated_at)

-- Profiles table
profiles (id, user_id, name, title, company, location, tagline, skills, looking_for, bio, needs, photo_url, social_links)

-- Swipes table
swipes (id, swiper_id, swiped_id, action, created_at) -- action: like, skip, super_spark

-- Matches table
matches (id, user1_id, user2_id, created_at, chat_unlocked)

-- Messages table
messages (id, match_id, sender_id, content, created_at)

-- Premium features
super_sparks (id, user_id, count, expires_at)
purchases (id, user_id, product_type, amount, created_at)
```

## Design System

### Color Palette
- **Primary**: #FF4458 (Sparko Red)
- **Secondary**: #6C5CE7 (Purple)
- **Accent**: #FFD93D (Gold for Super Spark)
- **Background**: #FFFFFF (White)
- **Text**: #2D3436 (Dark Gray)
- **Success**: #00B894 (Green)
- **Warning**: #FDCB6E (Orange)

### Typography
- **Primary Font**: Inter (modern, clean)
- **Headings**: 32px, 24px, 20px
- **Body Text**: 16px, 14px
- **Small Text**: 12px

### UI Components
- **Cards**: Rounded corners (16px), subtle shadows
- **Buttons**: Rounded (8px), hover effects
- **Icons**: Feather icons for consistency
- **Animations**: Smooth transitions (300ms ease-in-out)

## User Experience Flow

### Onboarding
1. Landing page with value proposition
2. Sign up/Login
3. Role selection (Entrepreneur/Investor)
4. Profile creation wizard
5. Tutorial for swipe mechanics

### Main App Flow
1. Dashboard with card stack
2. Swipe through potential matches
3. View matches and start conversations
4. Profile management
5. Premium features access

### Responsive Design
- **Desktop**: Full card view with side navigation
- **Tablet**: Optimized card size and touch interactions
- **Mobile**: Native-like experience with gesture support

## Development Phases

### Phase 1: Core MVP
- User authentication and profiles
- Basic swipe functionality
- Simple matching algorithm
- Chat system

### Phase 2: Enhanced Features
- Super Spark implementation
- Smart filtering
- Premium features
- Payment integration

### Phase 3: Polish & Scale
- Advanced animations
- Performance optimization
- Multi-language support
- Analytics dashboard

## Success Metrics
- User registration and retention rates
- Match success rates
- Premium feature conversion
- User engagement (daily active users)
- Revenue from premium features

