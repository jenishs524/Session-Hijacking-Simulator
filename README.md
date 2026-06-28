# Session-Hijacking-Simulator

🎯 Objective

To demonstrate—in a controlled, educational environment—how session hijacking and fixation attacks are executed against a vulnerable web application. The simulator exposes multiple insecure session management practices, including:

    Session ID in URL: Exposes the session identifier as a query parameter, making it visible in browser history, referer headers, and server logs.

    Predictable Session IDs: Generates weak session IDs (e.g., MD5 of username + timestamp), enabling attackers to guess or brute‑force valid session tokens.

    Missing HttpOnly and Secure Flags: Sets session cookies without the HttpOnly flag (allowing client‑side scripts to read them via XSS) and without the Secure flag (allowing transmission over unencrypted HTTP connections).

    No Session Expiration: Tokens remain valid indefinitely, allowing attackers to use stolen tokens long after the user has logged out.

    Session Fixation: Allows an attacker to set a user's session identifier before they authenticate, then use that same identifier to access the authenticated session.

By observing these vulnerabilities in action, security teams and developers can better understand the importance of implementing secure session management practices, such as using strong, random session IDs, setting proper cookie flags, and enforcing session expiration.
🧠 How It Works – Technical Overview

The Session Hijacking Simulator is a Flask‑based web application with intentionally weakened security controls. It exposes multiple attack vectors:
1. Session ID in URL (Exposure)

    Mechanism: When a user logs in, the application generates a session ID and passes it as a URL parameter (e.g., http://example.com/profile?session_id=abc123).

    Attack Vector: An attacker can capture this session ID from:

        Browser history (if the user shares the link).

        HTTP Referer headers (when the user clicks on an external link).

        Network traffic (if the connection is not encrypted).

    Demonstration: Once the attacker obtains the session ID, they can simply paste it into their browser URL and access the victim's account without credentials.

2. Predictable Session IDs (Guessability)

    Mechanism: Session IDs are generated using weak algorithms—for example, MD5 hashing of username + timestamp or simple sequential numbers.

    Attack Vector: An attacker can enumerate possible session IDs by guessing timestamps or usernames, or by predicting the pattern of ID generation.

    Demonstration: The tool highlights how a simple brute‑force attack can guess a valid session ID, leading to unauthorised access.

3. Missing HttpOnly & Secure Flags

    Mechanism: The session cookie is set without HttpOnly (so JavaScript can read it) and without Secure (so it can be transmitted over HTTP).

    Attack Vector:

        XSS Exploitation: A cross‑site scripting vulnerability in the application can read the cookie and exfiltrate it to the attacker.

        Man‑in‑the‑Middle (MITM): If the application is accessed over HTTP, the session cookie can be intercepted in plaintext.

    Demonstration: The tool displays the raw cookie to the user, showing its insecure attributes. An attacker can simulate an XSS attack to extract the cookie and replay it.

4. No Session Expiration

    Mechanism: The session never expires, even after logout (or the session ID remains valid for an excessive duration).

    Attack Vector: A stolen session ID can be reused indefinitely, even if the victim logs out.

    Demonstration: The tool allows the attacker to reuse a session ID long after the victim has closed their browser.

5. Session Fixation

    Mechanism: The application accepts a user‑supplied session ID via a URL parameter (?session_id=attacker_controlled) before authentication. After login, the same session ID is used for the authenticated session.

    Attack Vector:

        Attacker visits the application and generates a session ID (or creates one manually).

        Attacker sends a link to the victim: http://example.com/login?session_id=attacker_controlled.

        Victim clicks the link and logs in (their credentials are stored against the attacker's session ID).

        Attacker uses the same session ID to access the victim's account.

    Demonstration: The tool provides a step‑by‑step walkthrough of this attack, showing how the attacker's session ID becomes the victim's authenticated session.

✨ Advanced Features (Real‑World Upgrade)
Feature	Implementation
Interactive Attack Demonstrations	Each vulnerability is presented as a separate route or screen, allowing users to "hack" the application with a single click, clearly visualising the attack chain.
Session ID Predictability Visualiser	Displays a sample of generated session IDs to show the pattern, highlighting how easy they are to guess.
Cookie Inspector	Shows the exact cookie attributes (HttpOnly, Secure, SameSite, Path) and flags insecure configurations.
Step‑by‑Step Session Fixation Walkthrough	A guided tutorial that leads the user through the fixation attack, from generating the session ID to hijacking the victim's session.
Exploit Simulation	Users can enter any session ID into a hijack endpoint (/hijack/<session_id>) and immediately see the associated account, demonstrating how trivial session hijacking becomes when IDs are exposed.
Logging & Audit Trail	Logs all session‑related actions (logins, page accesses, hijack attempts) to a JSON file for forensic review and attack validation.
Security Enhancement Guide	Provides a side‑by‑side comparison of the vulnerable implementation vs. a secure implementation, explaining how to fix each issue (e.g., using secrets.token_urlsafe(), setting HttpOnly and Secure flags).
🛠️ Tools & Technologies

    Python 3 – core application logic.

    Flask – web framework for building the vulnerable application.

    hashlib – for generating weak (predictable) session IDs.

    secrets – (contrast) for showing how to generate strong IDs.

    datetime – for session expiration (or absence thereof).

    JavaScript (optional) – for demonstrating client‑side cookie access when HttpOnly is missing.

🔬 Testing & Use Case

Scenario:
A security awareness trainer wants to demonstrate session hijacking risks to a group of junior developers. They deploy the Session Hijacking Simulator in a lab environment and walk through a complete attack chain.

Process – Session Hijacking via URL Exposure:

    Victim (Alice) logs in as alice:

        URL after login: http://localhost:5000/profile?session_id=5f4dcc3b5aa765d61d8327deb882cf99

    Attacker (Bob) intercepts this URL from network logs or browser history.

    Bob opens a new browser (or incognito mode) and visits the same URL directly.

    Result: Bob is now logged in as Alice without any credentials, with full access to her profile.

Process – Session Fixation:

    Bob visits http://localhost:5000/fixation?session_id=bob123.

    The application sets session_id=bob123 for the session.

    Bob sends a phishing link to Alice: http://localhost:5000/fixation_login?session_id=bob123

    Alice clicks the link and logs in with her credentials.

    Bob now visits /hijack/bob123 and is immediately granted Alice's session.

    Result: Bob has successfully fixed Alice's session, bypassing authentication entirely.

Outcome:

    The developers see first‑hand how easy session hijacking can be when security controls are missing.

    They receive a clear checklist of fixes (e.g., Secure flag, HttpOnly flag, strong session IDs, expiration) to prevent these attacks in their own applications.

    The trainer uses the logged data (session_log.json) to demonstrate how auditing can reveal attack patterns.

📁 Output Example (Session Log)

A typical log entry contains:

    Timestamp – Date and time of the event.

    Action – e.g., login, page_access, hijack_attempt.

    Username – The authenticated user (if any).

    Session ID – The session identifier used.

    IP Address – Source IP of the request.

    Event Details – e.g., Session ID exposed in URL, Session fixation attempt.

📝 Conclusion

The Session Hijacking Simulator is an invaluable tool for security awareness training and secure coding education. It transforms abstract concepts into tangible, visual demonstrations, allowing developers and security professionals to witness firsthand how insecure session management can lead to account compromise. By covering a wide range of vulnerabilities—from session ID exposure in URLs to fixation and predictable token generation—it provides a comprehensive understanding of session security. During testing, the simulator successfully demonstrated all attack vectors, reinforcing the importance of implementing secure defaults: using cryptographically strong random session IDs, setting HttpOnly and Secure flags, enforcing session expiration, and never exposing session IDs in URLs. This tool serves as both an effective training aid and a cautionary blueprint for building secure authentication systems.
