# Marketing Strategy Decision Tool

A comprehensive marketing strategy tool built with Streamlit that helps businesses make data-driven decisions using proven marketing frameworks.

## Features

- **Product Analysis**: Configure product type and lifecycle stage
- **Market Strategy**: Apply Ansoff Matrix for strategic planning
- **Customer Segmentation**: Select relevant targeting criteria
- **Competitive Analysis**: Assess Porter's 5 Forces
- **Distribution Strategy**: Get channel recommendations based on product and market characteristics
- **WhatsApp Integration**: Direct booking capability for channel setup
- **Complete Recommendations**: Get comprehensive marketing strategy recommendations

## Marketing Frameworks Used

1. **Consumer Behavior Model** (Engel, Blackwell, Miniard & Harcourt 2001)
2. **Porter's 5 Forces Framework**
3. **Ansoff Matrix**
4. **Product Lifecycle (PLC) Model**
5. **Distribution Channel Strategy Framework**

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/marketing-decision-tool.git
cd marketing-decision-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as your main file
5. Click "Deploy"

### Deploy to Heroku

1. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Usage

### Step-by-Step Guide

1. **Product Information**
   - Select your product type (FMCG, Luxury, Electronics, Service)
   - Choose lifecycle stage (Introduction, Growth, Maturity, Decline)

2. **Market Strategy**
   - Select market-product combination using Ansoff Matrix
   - Get strategic direction (Penetration, Development, Diversification)

3. **Customer Segmentation**
   - Choose relevant segmentation criteria
   - Options include: User Status, Usage Rate, Loyalty, Attitude, Demographics, Psychographics

4. **Competitive Forces**
   - Assess all 5 forces in your market
   - Rate each force as Low, Medium, or High

5. **Distribution Channel**
   - Configure customization level (High/Low)
   - Select market concentration (Concentrated/Fragmented)
   - Get channel recommendation with pros/cons
   - Book channel setup via WhatsApp

6. **View Recommendations**
   - Get complete marketing strategy
   - Includes: Core strategy, Promotion, Pricing, Distribution, Messaging

## Distribution Channel Framework

The tool recommends distribution channels based on two dimensions:

| Customization | Market Type | Recommended Channel |
|---------------|-------------|---------------------|
| High | Concentrated | Direct Distribution (VMS) |
| High | Fragmented | Franchise Operations |
| Low | Concentrated | Distribution + Personal Selling |
| Low | Fragmented | Third-Party Intensive Distribution |

## Project Structure

```
marketing-decision-tool/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore file
└── config.toml           # Streamlit configuration (optional)
```

## Technologies Used

- **Python 3.8+**
- **Streamlit**: Web application framework
- **urllib**: URL encoding for WhatsApp integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Marketing frameworks based on established academic research
- Inspired by practical marketing strategy needs
- Built with Streamlit for ease of use and deployment

## Contact

For questions or support, please open an issue on GitHub.

## Screenshots

*(Add screenshots of your application here)*

---

**Note**: This tool provides strategic recommendations based on established marketing frameworks. Always validate recommendations with market research and adapt to your specific business context.
