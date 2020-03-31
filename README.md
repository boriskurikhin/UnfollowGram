# UnfollowGram

Ever been really annoyed trying to figure out who unfollowed you, or who is not following you back on Instagram? I got a solution! UnfollowGram is a simple Python program which **currently** lists all instagram users (a.k.a. the 🐍s) who don't follow you back. 

#### Roadmap for this program
* Display of changes from the last time you ran the program
* A "follow threshold"; *certain # of followers, above which, those users will be ignored because they're likely famous (i.e [Drake](https://instagram.com/champagnepapi) is followed by millions, and obviosuly doesn't follow everyone back)*
* Adding a white-list *(ie. you want to keep following your dad's small business account)*
* Automatically unfollowing all the snakes
* Moving this code to a seperate server which will be up and running 24/7, unfollowing unfollowers!
* Maybe even a small API, who knows?

## Installation

I will make the installation & execution of this program "more consumer facing" soon...

1. Save `unfollow.py` 
2. Install Python 3 & [pip3](https://pip.pypa.io/en/stable/)
3. In your Terminal or Command Prompt, use `pip3` to install `requests`
```bash
pip3 install requests
```
4. Create a `login.json` file in the same directory as `unfollow.py`
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

## Usage

Once you've followed the installation instructions above, navigate to the program's directory, open up Terminal or Command Prompt, and type in the following:

```bash
python3 unfollow.py
```

After it's done, open a file called `snakes.txt`

## License
[MIT](https://choosealicense.com/licenses/mit/)
