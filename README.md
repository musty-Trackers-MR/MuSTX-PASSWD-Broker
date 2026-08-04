# MuSTX-PASSWD-Broker

git clone https://github.com/<your-username>/musty-cracker.git


cd musty-cracker

pip install -r requirements.txt


python3 musty.py -H <hash> -a md5 -w wordlist.txt




cat > README.md << 'EOF'
# MUSTY - Educational Password Cracker

Dictionary-based hash cracker for learning cybersecurity concepts.

## ⚠️ Disclaimer
Only use on hashes you own or have explicit permission to test
(your own accounts, CTF challenges, authorized labs like TryHackMe/HackTheBox).
Unauthorized use against systems you don't own is illegal.

## Usage
python3 musty.py -H <hash> -a md5 -w wordlist.txt
EOF

git add README.md
git commit -m "Add README with usage and disclaimer"
git push


git remote add origin https://github.com/<your-username>/musty-cracker.git
git branch -M main
git push -u origin main
