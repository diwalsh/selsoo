# Selsoo

### Video Demo
[Selsoo on YouTube](https://www.youtube.com/watch?v%253D-FOJuNiV3Lk)

### Description
Selsoo is a web application I designed and developed as the final project for CS50x. It is my very first application! This Flask app leverages Python, HTML, CSS, JavaScript, SQLite3, and API connections.

### Features

#### User Authentication
- Users are required to log in to access the application.
- No actions can be performed without logging in.

#### Sessions and Archive
- Logged-in users can start a new session or view an archive of previous sessions.
- If there is no session history, the archive prompts the user to start their first session.

#### Emoji Selection Process
- **First Level:** Users choose from 8 general emojis: sad, angry, tired, apathetic, shocked, anxious, ill, and uncomfortable.
- **Second Level:** Each selected emoji leads to 4 related emojis to narrow down the feeling.
- **Third Level:** Finally, 6 specific emojis are presented, each with hover text explaining the emotion.

### Story Generation
- Once the user selects an emoji, the emotion is sent to the Flask app.
- A script connects to OpenAI's API to generate a soothing meditation story based on the selected emotion.
- The chatbot also creates an illustration description and a title for the story.

### Display and Storage
- The generated story, illustration, and title are displayed on a webpage.
- This data is stored in a database, allowing users to view a preview of past stories in the archive.
- Archive cards show the title, image, story preview, emotion, and date/time of creation.
- Clicking a card displays the full story as it was initially generated.

### Future Enhancements
- Potential growth includes adding social media features.
- Further customization of the story prompt by collecting additional user information about the cause of the negative emotion.

### Final Thoughts
I had a lot of fun with this project and see many opportunities for it to grow and improve. Thank you for everything! :)
