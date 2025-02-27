# The Nutritionist

## Overview
The Nutritionist is a web-based application built using Streamlit that helps users analyze their meals using AI. Users can upload meal images, and the app provides a calorie breakdown, macronutrient analysis, and dietary recommendations. The results can be saved and retrieved later.

## Features
- **AI-Powered Meal Analysis**: Estimates calorie content, macronutrients, and provides health recommendations.
- **Image Upload & Processing**: Users can upload meal images for AI-driven analysis.
- **Database Storage**: Saves meal history for future reference.
- **PDF Report Generation**: Allows users to download meal analysis reports.
- **Email Report Delivery**: Sends the analysis report directly to users' emails.

## Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python, Google Generative AI (Gemini Pro)
- **APIs & Libraries**:
  - SQLite (for storing meal history)
  - PIL (for image processing)
  - ReportLab (for generating PDFs)
  - SMTP (for email notifications)
- **Environment Management**: dotenv (for API keys and configurations)

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/nutritionist-app.git
   cd nutritionist-app
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   pip install -r requirements.txt
   ```
3. Set up the `.env` file with the required API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   FROM_EMAIL=your_email@example.com
   FROM_PASSWORD=your_email_password
   ```
4. Run the application:
   ```bash
   streamlit run main.py
   ```

## Usage
- Open the application in the browser.
- Upload an image of your meal.
- Select the meal time and portion size.
- Click on "Analyze My Meal" to get AI-generated insights.
- View, download, or email the generated report.
- Check the history section for previous meal analyses.

## Contribution
Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

## License
This project is licensed under the MIT License.

