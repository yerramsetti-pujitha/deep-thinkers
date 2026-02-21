import { auth, db, googleProvider } from "./firebase-config.js";
import { signInWithPopup, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// --- Auth Handling ---
const googleBtn = document.getElementById('googleLoginBtn');
if(googleBtn) googleBtn.onclick = () => signInWithPopup(auth, googleProvider);

const logoutBtn = document.getElementById('logoutBtn');
if(logoutBtn) logoutBtn.onclick = () => signOut(auth);

onAuthStateChanged(auth, (user) => {
    if (user && window.location.pathname.includes('index.html')) window.location.href = 'dashboard.html';
    if (!user && window.location.pathname.includes('dashboard.html')) window.location.href = 'index.html';
});

// --- Groq Integration ---
async function getAromiCoachingPlan(mood, energy, sleep) {
    const GROQ_API_KEY = "YOUR_GROQ_API_KEY"; // Placeholder
    const prompt = `You are Aromi, a health coach. User stats: Mood ${mood}/10, Energy ${energy}/10, Sleep ${sleep}hrs. 
    Provide a personalized workout, meal plan, and mental focus.
    Return ONLY JSON: {"workout": "...", "meal_plan": "...", "mental_focus": "..."}`;

    try {
        const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: { "Authorization": `Bearer ${GROQ_API_KEY}`, "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "llama3-70b-8192",
                messages: [{ role: "system", content: prompt }],
                response_format: { type: "json_object" }
            })
        });
        const data = await res.json();
        return JSON.parse(data.choices[0].message.content);
    } catch (err) {
        console.error("Groq Error:", err);
        return null;
    }
}

// --- Dashboard Actions ---
const syncBtn = document.getElementById('syncBtn');
if(syncBtn) {
    syncBtn.onclick = async () => {
        const mood = document.getElementById('mood').value;
        const energy = document.getElementById('energy').value;
        const sleep = document.getElementById('sleep').value;
        
        document.getElementById('loading').classList.remove('hidden');

        // Save to Firebase
        await addDoc(collection(db, "users", auth.currentUser.uid, "logs"), {
            mood, energy, sleep, timestamp: serverTimestamp()
        });

        // Get AI Plan
        const plan = await getAromiCoachingPlan(mood, energy, sleep);
        if(plan) {
            document.getElementById('workout').innerText = plan.workout;
            document.getElementById('meal').innerText = plan.meal_plan;
            document.getElementById('mental').innerText = plan.mental_focus;
        }
        document.getElementById('loading').classList.add('hidden');
    };
}