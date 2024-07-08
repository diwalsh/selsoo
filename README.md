# selsoo
#### Video Demo:  [selsoo on youtube](https://www.youtube.com/watch?v%253D-FOJuNiV3Lk)
#### Description:
selsoo is a web application i designed and made for the final project of CS50x.

it is a flask application that uses python, html, css and javascript, as well as SQLite3 and API connections.
when a user goes to selsoo -- they are immediately prompted to log in. a user cannot do anything without logging in first.

once a user is logged in, they are able to access a new session, or an archive of their previous soothing sessions. if they don't have any history of sessions, the archive will say it is empty and prompt the user to start their first session.

when a session begins, the user is prompted with 8 emojis to choose from. the emojis later direct the user through an emoji tree of selection to narrow down what negative emotion or feeling they are experiencing. the first 8 emojis to choose from are quite general, and include sad, angry, tired, apathetic, shocked, anxious, ill and uncomfortable.

once a user selects one of those eight, they are prompted with four emojis related to that feeling, to try to narrow it down further. once one of those next 4 emojis are selected, lastly, the user is faced with 6 specific emojis to even further narrow down their experience. each of these 6 emojis features a hover text so the user can see in english which of the emojis stands for which specific emotion.

once the user selects an emoji on the third screen, the name of the emotion in the hover box of that emoji is sent back to the flask app. there, i wrote a script to connect to openAI's API which prompts the chat function to generate a soothing meditation story using the emotion name sent back to the flask app. i wrote the template for this prompt into python, and it is personalized for whatever emotion is selected. from there the chat is sent its story back again, and is tasked with describing an illustration to go along with the story. that prompt is decorated with visual specifics i wrote and then sent back to openAI to generate an illustration to my specifications. lastly, the chat bot is tasked with titling the story based on the description of the illustration.

all of this data is then populated into a subsequent webpage that shows the short meditation story, along with the illustration and title. this information is also stored into a database for that user. any story generated in that user's session is compiled in the database. the archive pulls from that database in order to populate little preview cards of past stories for later use. the card includes the title, image and a preview of the story, as well as the emotion and the date and time it was generated. when a user clicks on a card in the archive, that story is populated in its own page the same way it was when it was first generated.

i had a lot of fun with this project and can easily see room for it to grow -- incorporating social media aspects, and further complicating the prompt and what is collected and sent to the chat bot in order to even further personalize the story. such as... say, collecting information on what is causing the negative emotion, and not just the negative emotion itself.

thanks for everything!