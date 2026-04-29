# 🎨 Design System & UX Philosophy - EIA

“Explain complex election processes in the simplest, most interactive way possible.”

## 🧭 Core Principles
*   **Clarity over complexity**: Distill bureaucratic jargon into actionable steps.
*   **Guided learning**: Focus on the next immediate step rather than information overload.
*   **Interactive > static**: Use conversational flows and dynamic timelines.
*   **Mobile-first experience**: Optimized for on-the-go voters.
*   **Minimal UI for performance**: Fast loading times for low-bandwidth scenarios.

## 👥 Target Users
*   First-time voters and students.
*   Citizens unfamiliar with election protocols.
*   Users seeking quick, reliable guidance on-the-go.

## 🧩 Core User Flows
1.  **Quick Question Flow (Chat-Based)**: User → Ask Question → AI + Knowledge Service → Structured Answer.
2.  **Guided Learning Flow**: Home → Select Topic (e.g., Eligibility) → Step-by-Step Guide → Completion.
3.  **Timeline Exploration Flow**: Home → View Timeline → Scroll/Interact with Phases.

## 🖥️ Core Screens
*   **Home Screen**: Simple search/input ("Ask about elections...") + Quick action buttons.
*   **Chat Assistant Screen**: Conversational bubbles with structured responses (Steps, Bullet points).
*   **Step-by-Step Guide**: Simplified procedural learning with progress indicators.
*   **Timeline Screen**: Visual vertical stepper showing phases (Registration → Voting → Results).

## 🎯 UX Features
*   🔍 **Smart Suggestions**: Auto-suggest common queries to reduce typing effort.
*   ✅ **Structured Responses**: Steps and bullet points instead of long paragraphs.
*   🧠 **Context Awareness**: Session-based memory to suggest the next logical step.
*   🌐 **Accessibility**: High contrast, simple language ("Explain like I'm 18"), and screen-reader optimized.

## 🎨 UI System
*   **Color Palette**: Trust-Blue (Primary), Success-Green (Accent), Light-Gray (Background).
*   **Typography**: Sans-serif (Inter/System) with clear hierarchy.
*   **Components**: Reusable buttons, cards for steps, and minimalist chat bubbles.

## ⚡ Performance Design
*   No heavy animation libraries; CSS-based transitions only.
*   Lazy load components/screens.
*   SVG icons only; zero heavy image assets.

## ✅ Summary
The design is optimized for speed, interactivity, and accessibility, ensuring it is easy to build, demo, and maintain under the 10MB limit.
