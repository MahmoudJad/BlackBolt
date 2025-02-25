# BlackBolt 🎵  
**Powering the sound of the band!**  

## Description  
BlackBolt is a Flask-based microservice responsible for managing the music section of the band's web app. It provides APIs for uploading, storing, and retrieving songs, ensuring smooth audio streaming and metadata handling.  

## Features  
- Upload and store songs with metadata (title, artist, duration).  
- Fetch and stream songs efficiently.  
- Secure API endpoints for managing song content.  
- Scalable and optimized for performance.  

## Installation  
```bash
git clone https://github.com/yourusername/BlackBolt.git
cd BlackBolt
pip install -r requirements.txt
python app.py

## API Endpoints 

| Method | Endpoint       | Description               |
|--------|--------------|---------------------------|
| GET    | `/health`    | Check the service health   |
| GET    | `/count` | Retrieve the songs count |
| GET   | `/songs`    | Retrieve all songs from DB  |
| GET | `/song/<int:id>` | Search for specific song with ID |
| POST | `/song` | Create new songs |
| PUT | `/song/<int:id> | Update song with ID |
| DELETE | `/song/<int:id>` | Delete song with ID | 


## Technologies Used
- Flask
- PostgreSQL / SQLite
- Cloud Storage Integration