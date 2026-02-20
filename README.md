This is an excellent pivot. Shifting to a serverless, API-driven architecture using Vercel, Firebase, and Groq makes the setup incredibly lightweight, fast, and cost-effective to deploy.

Here is the comprehensive project plan tailored to your updated tech stack, followed by the "antigravity" prompt to instantly scaffold the project using an AI coding assistant.

1. Updated Technology Architecture
Frontend & Hosting: Vanilla HTML, CSS, and JavaScript (or a static site generator), deployed seamlessly via Vercel.

Authentication & Database: Google Firebase (Firebase Auth for secure logins, Firestore for storing user profiles, health metrics, and coaching history).

AI Engine & "Backend" Logic: Groq API (Leveraging ultra-fast LLMs like LLaMA 3 on Groq to process user data and generate real-time adaptive fitness, nutrition, and mental wellness plans).

Integrations: Wearable device REST APIs (e.g., Apple HealthKit, Google Fit, Oura) handled via client-side or serverless functions on Vercel.

2. Project Plan (4–6 Months Timeline)
Phase 1: Foundation & UI Scaffolding (Weeks 1–4)

Set up the GitHub repository and link it to Vercel for continuous deployment.

Design the responsive HTML/CSS/JS frontend UI (Login, Dashboard, Chat/Coaching Interface).

Integrate Firebase Authentication (Email/Password & Google Sign-in).

Set up the Firestore database schema (Users, Logs, Goals).

Phase 2: Core AI Integration (Weeks 5–8)

Integrate the Groq API into Vercel Serverless Functions to securely handle AI requests without exposing your API keys on the frontend.

Develop the core prompt logic so Groq acts as the "Aromi AI Agent" (analyzing mood, energy, and sleep to output adaptive daily plans).

Build the interactive coaching interface where users chat or log daily metrics.

Phase 3: Module Development (Weeks 9–14)

Physical Health & Nutrition: Build tracking forms and display Groq's generated meal/workout plans.

Mental Wellness: Implement mood tracking and energy-level sliders.

Wearable Integration: Connect third-party APIs (like Google Fit) to automatically pull step counts and sleep data into Firestore to feed into the Groq AI context.

Phase 4: Admin Dashboard & Refinement (Weeks 15–18)

Create a separate secure HTML page for the Admin Dashboard to view aggregated user insights and system health.

Refine the continuous learning loop: Ensure Groq's API calls reference the user's past 7 days of data from Firestore to make truly dynamic adjustments.

Phase 5: Testing & Launch (Weeks 19–24)

End-to-end testing of the web app on mobile and desktop browsers.

Finalize Vercel production deployment.

Onboard beta users for the initial launch.

3. The "Antigravity" Prompt for Groq AI
Use this prompt in a tool like Cursor, Bolt.new, v0.dev, or directly into an AI coding assistant powered by Groq to instantly generate the foundational code for your project.

Copy and paste the text below:

System Role: Act as an expert Full-Stack Developer architecting a serverless web application called "Aromi AI Agent".

Project Context: Aromi AI is a holistic, adaptive coaching app that dynamically alters fitness, nutrition, and mental wellness plans based on real-time user mood, energy, and daily performance.

Tech Stack Constraint: > * Frontend: Pure HTML, CSS (Tailwind CSS via CDN for styling), and Vanilla JavaScript. Ready for Vercel deployment.

Authentication & DB: Google Firebase (Auth and Firestore V9 modular SDK).

AI/Backend Logic: Groq API (using Llama-3-70b-versatile or similar) to generate coaching plans.

Instructions for Code Generation: Please generate the core scaffolding for this project. I need the following files fully coded and ready to run:

index.html: The landing and login page featuring Firebase Authentication (Email/Password and Google Login UI).

dashboard.html: The main user interface containing:

A "Daily Check-in" form (Mood slider, Energy slider, Sleep hours input).

A dynamic display area for "Today's Adaptive Plan" (Fitness, Nutrition, Mindfulness).

A chat interface to converse directly with the Aromi AI Agent.

firebase-config.js: The initialization script for Firebase Auth and Firestore. Include placeholder API keys.

app.js: The main logic file that:

Handles user state changes (logging in/out).

Saves the "Daily Check-in" data to Firestore.

Contains an async function getAromiCoachingPlan(mood, energy, sleep) that makes a fetch request to the Groq API. Write the specific system prompt inside this function telling the Groq LLM to act as the Aromi AI coach and return a JSON object containing workout, meal_plan, and mental_focus based on the user's inputs.

Focus heavily on a clean, modern, and mobile-responsive UI using Tailwind CSS, and ensure the Groq API integration handles JSON parsing correctly.




