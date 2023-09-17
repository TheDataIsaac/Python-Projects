This is a Python class that extracts data from a YouTube channel using the YouTube Data API. The extracted data includes video ID, title, upload date, view count, like count, and comment count, and it is saved in a pandas dataframe.

### Prerequisites:
This code requires the following Python packages:
requests
pandas

### Usage:
To use the YouTubeDataExtractor class, follow these steps:

- Obtain a Google API key with access to the YouTube Data API.
- Import the YouTubeDataExtractor class and create an instance of the class, passing in the channel ID and API key as parameters.
- from YouTubeDataExtractor import YouTubeDataExtractor
- channel_id = 'YOUR_CHANNEL_ID'
- api_key = 'YOUR_API_KEY'
- youtube_data = YouTubeDataExtractor(channel_id, api_key)
- Call the extract_data() method of the instance to extract the data from the YouTube channel. This will return a pandas dataframe containing the extracted data.
- data = youtube_data.extract_data()

### License:
This code is licensed under the MIT License. See the LICENSE file for details.
