# SceneX_V2
SceneX_V2



cd src/ai/backend
source venv/bin/activate
uvicorn app.main:app --reload --log-level debug





cd src/ai/frontend
npm run dev




sudo apt update
sudo apt install python3 python3-venv

cd ~/.config/blender/4.3/scripts/addons/SceneX/src/ai/backend
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt 





Next steps:
1. cd ~/Documents/src/AISceneGen/backend
2. python -m venv venv
3. source venv/bin/activate  # or .\venv\Scripts\activate on Windows
4. pip install -r requirements.txt

5. cd ../frontend
6. npm install
7. Update .env with your settings

8. Start Redis server
9. Start backend: uvicorn app.main:app --reload
10. Start frontend: npm run dev