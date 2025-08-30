# Indian States Geography Quiz System with Machine Learning

An intelligent quiz system that personalizes questions about Indian states and union territories based on student performance using machine learning algorithms.

## 🇮🇳 Features

- **🗺️ Interactive Indian Map**: Click on any state to get geography questions
- **🏛️ State-Specific Questions**: Questions tailored to each state's geography, culture, history
- **🧠 Adaptive Difficulty**: Automatically adjusts question difficulty based on student performance
- **📊 Performance Tracking**: Monitors response time, accuracy, and attempts per state
- **🤖 ML-Powered**: Uses machine learning to predict student knowledge levels
- **📈 Real-time Adaptation**: Continuously learns and adapts to each student
- **🎯 Comprehensive Coverage**: All 28 states + 8 union territories
- **🖥️ Dual Interface**: Console-based and graphical map interface
- **🚀 Arduino/ESP32 Ready**: Designed to be lightweight for embedded hardware deployment

## 🎯 How It Works

1. **🗺️ State Selection**: Students click on any Indian state on the interactive map
2. **🧠 ML Assessment**: System analyzes performance metrics (response time, accuracy, attempts)
3. **🤖 Difficulty Prediction**: ML model predicts optimal question difficulty for that state
4. **❓ Dynamic Question Selection**: Automatically selects appropriate difficulty questions
5. **📊 Continuous Learning**: Model improves with more student interactions
6. **🏆 Progress Tracking**: Tracks performance across all states visited

## 🏛️ Question Categories

### **Geography & Location**
- State capitals, major cities
- Neighboring states, borders
- Rivers, mountains, climate
- Natural resources, agriculture

### **History & Culture**
- Historical events, monuments
- Traditional festivals, cuisine
- Famous personalities
- Art, music, dance forms

### **Economy & Development**
- Major industries, agriculture
- Tourist destinations
- Educational institutions
- Transportation networks

## 🗂️ Project Structure

```
├── ml_model/
│   ├── adaptive_quiz_model.py    # Core ML model for difficulty prediction
│   ├── question_bank.py          # Indian states question database
│   └── student_tracker.py        # Student performance tracking by state
├── api/
│   └── app.py                    # Flask API server with state-specific endpoints
├── data/
│   ├── questions.csv             # State-wise question database
│   └── students.csv              # Student performance data
├── tests/
│   └── test_model.py             # Unit tests
├── indian_map_interface.py       # Interactive graphical map interface
├── requirements.txt               # Python dependencies
├── main.py                       # Main console application
└── arduino_config.h              # Arduino/ESP32 configuration
```

## 🚀 Installation

1. **Install Python 3.8+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### **1. Console Interface**
```bash
python main.py
```
- Train ML model
- Manage students
- Take state geography quizzes
- View analytics
- Start API server

### **2. Interactive Map Interface**
```bash
python indian_map_interface.py
```
- Visual map of India
- Click on states to get questions
- Real-time performance tracking
- Graphical quiz interface

### **3. API Server**
```bash
python api/app.py
```
- RESTful API endpoints
- State-specific quiz management
- Student performance tracking
- ML model training

### **4. Run Tests**
```bash
python tests/test_model.py
```

## 🌐 API Endpoints

### **States & Questions**
- `GET /states/list` - Get all Indian states and union territories
- `GET /states/{state}/questions` - Get questions for specific state
- `POST /quiz/start` - Start quiz for specific state
- `POST /quiz/answer` - Submit answer and get feedback

### **Student Management**
- `POST /student/create` - Create new student profile
- `GET /student/progress` - Get student progress
- `GET /student/{id}/state/{state}/progress` - Get state-specific progress

### **ML Model**
- `POST /model/train` - Train ML model with performance data
- `GET /model/info` - Get model information

## 🗺️ Supported States & Union Territories

### **28 States**
Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal

### **8 Union Territories**
Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry

## 🧠 Machine Learning Features

- **Random Forest Algorithm**: Lightweight ML model for embedded systems
- **5 Key Features**: Response time, accuracy, attempts, difficulty, recent performance
- **Adaptive Learning**: Continuously improves with student interactions
- **Fallback Heuristics**: Works even without training data
- **Memory Optimized**: Designed for Arduino/ESP32 deployment

## 🔧 System Requirements

### **Development**
- Python 3.8+
- 4GB RAM
- 1GB storage

### **Production (Arduino/ESP32)**
- ESP32 Development Board
- 4MB Flash Memory
- 520KB SRAM
- MicroSD card (8GB+)
- Display (OLED/TFT/LCD)

## 🚀 Future Improvements

- **🗣️ Voice Interface**: Speech recognition for hands-free operation
- **📱 Mobile App**: Android/iOS companion app
- **☁️ Cloud Sync**: Multi-device synchronization
- **🎨 Advanced Graphics**: High-resolution state maps
- **🌍 Multi-language**: Support for regional languages
- **📊 Advanced Analytics**: Detailed learning insights
- **🤝 Multiplayer**: Competitive quiz modes

## 🏗️ Arduino/ESP32 Deployment

The system is specifically designed for embedded hardware:
- **Reduced ML complexity** (25 estimators instead of 50)
- **Memory-efficient data structures**
- **Binary storage optimization**
- **Power management features**
- **Complete deployment guide** included

See `ARDUINO_ESP32_DEPLOYMENT_GUIDE.md` for detailed instructions.

## 📚 Sample Questions

### **Maharashtra (Easy)**
**Q:** What is the capital of Maharashtra?
**Options:** Mumbai, Pune, Nagpur, Thane
**Answer:** Mumbai
**Explanation:** Mumbai is the capital and financial capital of India

### **Karnataka (Medium)**
**Q:** Which ancient empire had its capital in Karnataka?
**Options:** Maurya, Gupta, Vijayanagara, Chola
**Answer:** Vijayanagara
**Explanation:** Vijayanagara Empire had its capital in Hampi, Karnataka

### **Rajasthan (Medium)**
**Q:** Which fort is known as the Golden Fort?
**Options:** Amber Fort, Jaisalmer Fort, Chittorgarh Fort, Ranthambore Fort
**Answer:** Jaisalmer Fort
**Explanation:** Jaisalmer Fort is known as the Golden Fort due to its yellow sandstone

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add more state-specific questions
4. Improve ML algorithms
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Indian Geography**: Rich cultural and geographical diversity
- **Educational Technology**: Modern learning approaches
- **Machine Learning**: Adaptive learning algorithms
- **Open Source**: Community-driven development

---

**🇮🇳 Explore India, Learn Geography, Master Knowledge! 🇮🇳**
