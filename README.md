**Description**: A Python application that uses Tkinter and Selenium to analyze Instagram follower relationships from a given data zip file. Users can see mutual followers, followers who are not following back, and the users they are following but not being followed by. The script also includes an unfollow feature for selected users and a follower unfollow automation using PyAutoGUI.

**README**:

# Instagram Follower Analyzer
Instagram Follower Analyzer is a Python project that allows users to analyze their Instagram follower relationships. This application provides an interface to upload a zip file containing Instagram follower data, and displays mutual followers, followers who are not following back, and those you are following but not being followed by. The application also includes an option to unfollow selected users.

## Features 
- Upload and process Instagram data zip file
- View mutual followers
- View followers not following back
- View following who are not followed back
- Unfollow selected users
- Unfollow automation using PyAutoGUI 

## Dependencies
- Python
- Tkinter
- Selenium
- PyAutoGUI

## Setup
1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the script using `python main.py`

## Usage
- Click on "Upload ZIP File" to select and process your Instagram data zip file.
- View your mutual followers, followers that are not following back, and the users you are following but not being followed by.
- In the "Following Not Followed Back" tab, select the users you wish to unfollow and click "Unfollow Selected".
- The application will then use Selenium to log into Instagram and unfollow the selected users.

**NOTE:** Your Instagram username and password need to be hard-coded into the script. Please ensure to keep your credentials secure.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)