#!/usr/bin/env python3
from flask import Flask, request, session, redirect, url_for
import hashlib
import time

app = Flask(__name__)
app.secret_key = "insecure_secret_key_12345"  # WEAK (intentionally)

# In‑memory user store
users = {
    'admin': 'admin123',
    'alice': 'password',
    'bob': '123456'
}

# In‑memory session store (vulnerable – exposes session data)
sessions = {}

@app.route('/')
def home():
    if 'username' in session:
        return f'''
        <h1>Welcome, {session['username']}!</h1>
        <p>Your session ID: <code>{session.get('session_id', 'N/A')}</code></p>
        <p><a href="/profile">View Profile</a></p>
        <p><a href="/logout">Logout</a></p>
        <hr>
        <h3>Vulnerability Demo</h3>
        <p>Session ID is exposed in URL: 
        <a href="/profile?session_id={session.get('session_id', '')}">Profile with session in URL</a></p>
        '''
    return '''
    <h1>Session Hijacking Simulator</h1>
    <h2>Vulnerable Session Management</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
    <p>Test credentials: admin/admin123, alice/password, bob/123456</p>
    <hr>
    <h3>Vulnerabilities:</h3>
    <ul>
        <li>Session ID in URL (predictable)</li>
        <li>Session fixation possible</li>
        <li>No session expiration</li>
        <li>No secure/HttpOnly flags on cookies</li>
    </ul>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in users and users[username] == password:
        # Generate a weak session ID (MD5 of username + timestamp)
        session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()[:16]
        session['username'] = username
        session['session_id'] = session_id
        sessions[session_id] = username
        return redirect(url_for('home'))
    return 'Invalid credentials. <a href="/">Try again</a>'

@app.route('/profile')
def profile():
    # Vulnerability: session can be passed in URL
    session_id = request.args.get('session_id')
    if session_id and session_id in sessions:
        username = sessions[session_id]
        return f'''
        <h1>User Profile</h1>
        <p>Username: {username}</p>
        <p>Session ID: {session_id}</p>
        <p><a href="/">Home</a></p>
        <hr>
        <h3>[!] Vulnerability: Session hijacking possible!</h3>
        <p>You can access any user's session by changing the session_id parameter.</p>
        '''
    elif 'username' in session:
        return f'<h1>Profile of {session["username"]}</h1><p><a href="/">Home</a></p>'
    return 'Please login first. <a href="/">Login</a>'

@app.route('/logout')
def logout():
    session.clear()
    return 'Logged out. <a href="/">Home</a>'

@app.route('/hijack/<session_id>')
def hijack(session_id):
    """Demonstrate session hijacking"""
    if session_id in sessions:
        username = sessions[session_id]
        # Set the hijacked session
        session['username'] = username
        session['session_id'] = session_id
        return f'''
        <h1>[!] SESSION HIJACKED!</h1>
        <p>You have successfully hijacked the session of: {username}</p>
        <p>Session ID: {session_id}</p>
        <p><a href="/">Go to home</a></p>
        <hr>
        <h3>How this works:</h3>
        <p>1. The victim's session ID was exposed in the URL</p>
        <p>2. The attacker captured the session ID</p>
        <p>3. The attacker uses the session ID to access the victim's account</p>
        '''
    return 'Invalid session ID'

@app.route('/fixation')
def fixation():
    """Demonstrate session fixation"""
    session_id = request.args.get('session_id', 'attacker_controlled')
    session['username'] = 'attacker'
    session['session_id'] = session_id
    sessions[session_id] = 'attacker'
    return f'''
    <h1>Session Fixation Demo</h1>
    <p>Session ID set to: {session_id}</p>
    <p>Now visit: <a href="/fixation_login?session_id={session_id}">Fixation Login</a></p>
    '''

@app.route('/fixation_login')
def fixation_login():
    session_id = request.args.get('session_id')
    if session_id:
        session['session_id'] = session_id
        return f'''
        <h1>[!] Session Fixation Successful!</h1>
        <p>The user is now using the attacker's session ID: {session_id}</p>
        <p>The attacker can now access this session.</p>
        '''
    return 'No session ID provided'

if __name__ == '__main__':
    print("=" * 60)
    print("  SESSION HIJACKING SIMULATOR")
    print("=" * 60)
    print("[*] Running on http://0.0.0.0:5000")
    print("\nVulnerabilities demonstrated:")
    print("  1. Session ID in URL")
    print("  2. Session fixation")
    print("  3. No session expiration")
    print("  4. Weak session IDs\n")
    print("[!] For educational purposes only")
    app.run(host='0.0.0.0', port=5000, debug=False)
