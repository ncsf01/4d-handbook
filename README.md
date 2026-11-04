# 4D Handbook — Flask version

Promotional website (in Portuguese) for **The Beginner's 4D Handbook: A Roleplay Style Primer**, by Mike Melnick and James Bacon, a guide to the 4D roleplaying style, which focuses on getting into character and staying there as long as possible.

> This is the `flask` branch. The `main` branch holds the static Bootstrap version, published at https://ncsf01.github.io/4d-handbook/

## About

Built as a web development assignment at Fatec (Software Development, 1st semester), Activity 3: deploying a Flask web server on an AWS EC2 instance.

This is the third version of the project:

1. [4d-handbook-v1](https://github.com/ncsf01/4d-handbook-v1): plain HTML and CSS
2. [4d-handbook](https://github.com/ncsf01/4d-handbook) (`main`): rewritten with Bootstrap
3. `flask` branch (this one): the Bootstrap site served by Flask, using template inheritance

## Pages

- **Home** (`/`): introduction to the 4D style, a quote carousel and its three core ideas
- **About** (`/sobre`): the origin of the style, the 5 practical pillars of the 4D player and the handbook's goals
- **Contact** (`/contato`): community links (Discord and YouTube channels) and a contact form (visual only, not functional)

## Project structure

```
4d-handbook/
├── app.py              # Flask app and routes
├── requirements.txt    # dependencies with versions
├── templates/
│   ├── base.html       # shared layout: navbar, content block and footer
│   ├── index.html      # pages that extend base.html
│   ├── about.html
│   └── contato.html
└── static/
    ├── css/style.css
    └── img/capa.webp
```

## Running locally

```bash
git clone -b flask https://github.com/ncsf01/4d-handbook.git
cd 4d-handbook
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

The app listens on `0.0.0.0:5000`, so it also accepts external connections.

## Built with

- HTML
- CSS
- Bootstrap
- Python + Flask (Jinja templates)
- AWS EC2 (Ubuntu Server)

## Credits

The 4D style and *The Beginner's 4D Handbook* belong to their authors. The book is available on [DriveThruRPG](https://www.drivethrurpg.com/en/product/549599/the-beginner-s-4d-handbook).
