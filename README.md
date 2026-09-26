# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **PostgreSQL**: Hosted database via Supabase, accessed through SQLAlchemy

## 📁 Project Structure

```
notetaking-app/
├── src/
│   ├── models/
│   │   ├── user.py          # User model (template)
│   │   └── note.py          # Note model with database schema
│   ├── routes/
│   │   ├── user.py          # User API routes (template)
│   │   └── note.py          # Note API endpoints
│   ├── static/
│   │   ├── index.html       # Frontend application
│   │   └── favicon.ico      # Application icon
│   └── main.py              # Flask application entry point
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment configuration
└── README.md               # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

   Remark: On Windows, use `venv\Scripts\activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   Copy `.env.example` to `.env` and set `DATABASE_URL` to your Supabase PostgreSQL connection string. Keep the `.env` file private; do not commit it. The URL should include `sslmode=require` when required by your Supabase connection settings.

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5001`

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes
- `POST /api/notes/translate` - Translate a note title and content without changing the saved note

Translation request:
```json
{
  "title": "My Note Title",
  "content": "Note content here...",
  "target_language": "Chinese"
}
```

The response contains a `translation` object with string `title` and `content` fields, along with the selected `target_language`. Translation uses the DeepSeek `deepseek-chat` model through the OpenAI-compatible SDK; configure `OPENAI_API_KEY` in the environment or a root `.env` file. Translation prompts live in `prompts/translate_prompt.md`. The original note is not modified.

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-09-03T11:26:38.123456",
  "updated_at": "2025-09-03T11:27:30.654321"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Translate controls**: Select a target language and display the translated title and content without overwriting the note
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

Tables are created from the SQLAlchemy models at startup. The integer primary keys, text fields, and timestamps in those models are supported by PostgreSQL.

## 🚀 Deployment

The application is configured for easy deployment with:
- CORS enabled for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration
- Supabase PostgreSQL configured through the `DATABASE_URL` environment variable

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Required PostgreSQL connection URL for Supabase
- `OPENAI_API_KEY`: Optional API key used by the AI translation feature

The application loads variables from a root `.env` file for local development and reads them from the process environment in deployed environments. It has no local SQLite fallback.

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Note categories and tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities

---

**Built with ❤️ using Flask, PostgreSQL, and modern web technologies**
