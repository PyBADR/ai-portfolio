# MongoDB + Streamlit Dashboard Setup Guide

## Overview
This guide explains how to set up and run the Streamlit dashboard with live MongoDB data integration for the AI Portfolio project.

## Prerequisites
- Python 3.8 or higher
- MongoDB installed and running locally (or access to a MongoDB instance)
- Git installed

## Architecture
The setup connects three main components:
1. **MongoDB**: Database storing live AI portfolio data
2. **Streamlit Dashboard**: Interactive web application for data visualization
3. **GitHub**: Version control and code repository

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/PyBADR/ai-portfolio.git
cd ai-portfolio
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages include:
- `streamlit>=1.28.0` - Web application framework
- `pymongo>=4.6.0` - MongoDB Python driver
- `pandas>=2.0.0` - Data manipulation
- `plotly>=5.17.0` - Interactive visualizations

### 4. MongoDB Setup

#### Start MongoDB
```bash
# On macOS with Homebrew
brew services start mongodb-community

# Or manually
mongod --config /usr/local/etc/mongod.conf
```

#### Verify MongoDB Connection
```bash
# Connect to MongoDB shell
mongosh

# Check databases
show dbs

# Use the ai_portfolio database
use ai_portfolio

# Check collections
show collections
```

#### MongoDB Configuration
The dashboard connects to MongoDB using:
- **Host**: `localhost` (127.0.0.1)
- **Port**: `27017` (default)
- **Database**: `ai_portfolio`
- **Collections**: fraud_events, chats, users, artifacts, classifier_samples, motivating_quotes

### 5. Run the Streamlit Dashboard

#### Default Port (8501)
```bash
streamlit run streamlit_dashboard.py
```

#### Custom Port
```bash
streamlit run streamlit_dashboard.py --server.port 8505
```

The dashboard will automatically open in your browser at:
- Default: http://localhost:8501
- Custom: http://localhost:8505

### 6. Dashboard Features

#### Live Data Monitoring
- **Auto Refresh**: Automatically updates data every 30 seconds (configurable)
- **Collection Selector**: Switch between different MongoDB collections
- **Key Metrics**: Total collections, document counts, database name
- **Data Table**: Interactive table showing live data from selected collection
- **Statistics**: Data shape, memory usage, null values, column information
- **Raw Document Viewer**: Expandable section to view raw MongoDB documents

#### Supported Collections
1. **fraud_events**: Fraud detection events with confidence scores
2. **chats**: Conversation history and chat data
3. **users**: User information and profiles
4. **artifacts**: Generated artifacts and outputs
5. **classifier_samples**: Classification training samples
6. **motivating_quotes**: Inspirational quotes database

## File Structure
```
ai-portfolio/
├── streamlit_dashboard.py    # Main dashboard application
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
└── MONGODB_DASHBOARD_SETUP.md # This file
```

## Troubleshooting

### MongoDB Connection Issues
```python
# Error: Connection refused
# Solution: Ensure MongoDB is running
brew services start mongodb-community

# Error: Database not found
# Solution: Create the database and collections
mongosh
use ai_portfolio
db.createCollection("fraud_events")
```

### Port Already in Use
```bash
# Error: Port 8501 is already in use
# Solution: Use a different port
streamlit run streamlit_dashboard.py --server.port 8505

# Or kill the existing process
lsof -ti:8501 | xargs kill -9
```

### Missing Dependencies
```bash
# Error: ModuleNotFoundError
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Configuration

### MongoDB Connection String
Edit `streamlit_dashboard.py` to customize the MongoDB connection:
```python
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "ai_portfolio"
```

### Dashboard Settings
Customize refresh interval and other settings in the sidebar:
- **Auto Refresh**: Toggle automatic data updates
- **Refresh Interval**: Set update frequency (seconds)
- **Collection**: Select which MongoDB collection to display

## GitHub Integration

### Push Updates to GitHub
```bash
# Add changes
git add .

# Commit with message
git commit -m "Update dashboard features"

# Push to GitHub
git push origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

## Production Deployment

### Environment Variables
For production, use environment variables for sensitive data:
```bash
export MONGO_URI="mongodb://username:password@host:port"
export DATABASE_NAME="ai_portfolio"
```

### Streamlit Cloud Deployment
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud dashboard
5. Deploy!

## Additional Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)

## Support
For issues or questions:
- GitHub Issues: https://github.com/PyBADR/ai-portfolio/issues
- Email: support@example.com

## License
This project is part of the AI Portfolio workspace.

---
**Last Updated**: December 11, 2025
**Version**: 1.0.0
